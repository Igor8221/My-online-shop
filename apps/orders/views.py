from django.shortcuts import render, get_object_or_404, redirect
from apps.orders.models import Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CheckoutForm, OrderStatusForm



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.user and not request.user.is_staff:
        messages.error(request, "Вы не можете просматривать этот заказ.")
        return redirect('order_list')

    if request.method == 'POST' and request.user.is_staff:
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус заказа успешно обновлен.")
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderStatusForm(instance=order) if request.user.is_staff else None

    return render(request, 'order_detail.html', {'order': order, 'form': form})


@staff_member_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


@login_required
def checkout(request):
    cart = request.user.cart.first()

    if not cart or cart.items.count() == 0:
        messages.error(request, "Ваша корзина пуста!")
        return redirect('cart_view')

    if request.method == 'POST':
        form = CheckoutForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  

            order = Order.objects.create(user=request.user)

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart.items.all().delete()

            messages.success(request, "Заказ успешно оформлен!")
            return redirect('order_detail', order_id=order.id)
    else:
        form = CheckoutForm(instance=request.user)

    return render(request, 'checkout.html', {'form': form, 'cart': cart})
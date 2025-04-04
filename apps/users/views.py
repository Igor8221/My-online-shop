from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from apps.products.models import Product, Category, Review
from apps.users.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from apps.users.forms import UserRegisterForm, CustomPasswordChangeForm, ChangePhoneForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)  # Получаем корзину пользователя или создаем её, если нет

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)  # Получаем товар в корзине или создаем новый

    if not created:
        cart_item.quantity += 1  # Если товар уже есть в корзине, увеличиваем его количество.
        cart_item.save()    # Сохраняем изменения в корзине.

    return redirect('cart')  


def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)  # Получаем объект CartItem для данного товара в корзине.
    cart_item.delete()

    return redirect('cart')  


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart_view.html', {'cart': cart})


@login_required
def profile(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    categories = Category.objects.all() if request.user.is_staff else None  # Если пользователь администратор, показываем все категории.
    return render(request, 'profile.html', {'cart': cart, 'categories': categories})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш пароль был успешно изменен!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)   # Если форма не отправлена, создаем пустую форму.
    return render(request, 'change_password.html', {'form': form})

@login_required
def change_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')   # Получаем новый email
        request.user.email = email  # Изменяем email пользователя
        request.user.save()
        messages.success(request, 'Ваша почта была успешно изменена!')
        return redirect('profile')
    return render(request, 'change_email.html')


def login_view(request):
    if request.method == 'POST':
        username_or_email_or_phone = request.POST.get('username_or_email_or_phone')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email_or_phone, password=password)  # Проверяем пользователя

        if user is not None:
            login(request, user)   # Авторизуем пользователя
            return redirect('profile')
        else:
            messages.error(request, 'Неверный логин или пароль.')

    form = AuthenticationForm() # Создаем форму для логина
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # Получаем данные из формы регистрации
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Пожалуйста, войдите.')
            return redirect('login')
    else:
        form = UserRegisterForm() # Если форма не отправлена, показываем пустую форму
    return render(request, 'register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def delete_category(request, category_id):
    if not request.user.is_staff:
        messages.error(request, "У вас нет прав на выполнение этого действия.")
        return redirect('profile')

    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Категория успешно удалена.")
    return redirect('profile')



@login_required
def change_name(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        messages.success(request, 'Ваши данные были успешно обновлены!')
        return redirect('profile') 

    return redirect('profile')


@login_required
def leave_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        review = Review(product=product, user=request.user, text=text, rating=rating)  # Создаем отзыв.
        review.save()
        return redirect('product_detail', product_id=product.id)  # Перенаправляем на страницу товара.
    return render(request, 'leave_review.html', {'product': product})


@login_required
def change_phone_view(request):
    if request.method == 'POST':
        form = ChangePhoneForm(request.POST, instance=request.user) # Получаем форму для изменения номера телефона.
        if form.is_valid():
            form.save()
            messages.success(request, "Номер телефона успешно обновлен.")
            return redirect('profile')
        else:
            messages.error(request, "Ошибка! Проверьте корректность номера.")
    else:
        form = ChangePhoneForm(instance=request.user)  # Создаем форму с текущим номером телефона.

    return render(request, 'change_phone.html', {'form': form})
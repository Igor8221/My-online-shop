from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.admin.views.decorators import staff_member_required
from apps.products.models import *
from django.views.generic.detail import DetailView
from django.contrib import messages
# Create your views here.

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('category_list')  # Ссылка на список категорий
    return render(request, 'add_category.html')


@staff_member_required
def product_list(request):
    # Получаем все продукты из базы данных
    products = Product.objects.all()

    return render(request, 'product_list.html', {'products': products})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        main_image = request.FILES.get('main_image')
        additional_images = request.FILES.getlist('additional_images')

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Категория не найдена.')

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category
        )

        # Создаём главное изображение и сохраняем его в product.main_image
        if main_image:
            main_img_obj = ProductImage.objects.create(
                product=product,
                image=main_image,
                is_main=True
            )
            product.main_image = main_img_obj  # Обновляем поле main_image
            product.save(update_fields=['main_image'])  # Сохраняем продукт еще раз

        # Добавляем дополнительные изображения
        for img in additional_images:
            ProductImage.objects.create(
                product=product,
                image=img,
                is_main=False
            )

        # Добавляем характеристики
        names = request.POST.getlist('characteristics_name[]')
        values = request.POST.getlist('characteristics_value[]')

        for name, value in zip(names, values):
            if name and value:
                ProductCharacteristic.objects.create(
                    product=product,
                    name=name,
                    value=value
                )

        return redirect('product_list')

    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    return render(request, 'product_detail.html', {'product': product})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})


@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        category_id = request.POST.get('category')

        try:
            category = Category.objects.get(id=category_id)
            product.category = category
        except Category.DoesNotExist:
            raise ValidationError('Категория не найдена.')

        product.save()

        main_image = request.FILES.get('main_image')
        if main_image:
            ProductImage.objects.filter(product=product, is_main=True).delete()
            ProductImage.objects.create(
                product=product,
                image=main_image,
                is_main=True
            )

        additional_images = request.FILES.getlist('additional_images')
        for img in additional_images:
            ProductImage.objects.create(
                product=product,
                image=img,
                is_main=False
            )

        ProductCharacteristic.objects.filter(product=product).delete()
        names = request.POST.getlist('characteristics_name[]')
        values = request.POST.getlist('characteristics_value[]')
        for name, value in zip(names, values):
            if name and value:
                ProductCharacteristic.objects.create(
                    product=product,
                    name=name,
                    value=value
                )

        return redirect('product_detail', product_id=product.id)

    characteristics = ProductCharacteristic.objects.filter(product=product)
    characteristics_data = [{'name': ch.name, 'value': ch.value} for ch in characteristics]

    return render(request, 'edit_product.html', {
        'product': product,
        'categories': categories,
        'characteristics': characteristics_data
    })

@staff_member_required
def delete_product(request, product_id):
    # Получаем товар по его ID
    product = get_object_or_404(Product, id=product_id)

    # Удаляем сам товар
    product.delete()

    # Отправляем сообщение об успешном удалении
    messages.success(request, 'Карточка товара была успешно удалена.')

    # Перенаправляем на страницу со списком товаров
    return redirect('product_list')
import requests
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CategorySerializer, NewsSerializer, ProductSerializer

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import News
from apps.products.models import Category, Product
from .forms import NewsForm
from apps.users.models import Cart
import random

""" Формирование URL API """
def index_page(request):
    api_url = "http://127.0.0.1:8000/api/categories-news/"

    try:
        """ Запрос к API """
        response = requests.get(api_url)  
        response.raise_for_status()  
        
        """ Превращает JSON-ответ в словарь Python """
        data = response.json()  
    except requests.RequestException as e:
        print(f"Ошибка при запросе API: {e}")
        
        """ При ошибке кладутся пустые списки чтоб шаблон не ломался """
        data = {'categories': [], 'latest_news': []}
    
    """ Подготовка контекста для шаблона """
    context = {
        'categories': data.get('categories', []),
        'latest_news': data.get('latest_news', [])
    }
    return render(request, 'index.html', context)

def about_store(request):
    return render(request, 'about-store.html')

def contacts(request):
    return render(request, 'contacts.html')

def news_list(request):
    news_items = News.objects.all().order_by('-published_at')
    return render(request, 'news_list.html', {'news_items': news_items})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news_detail.html', {'news': news})

@login_required
def news_create(request):
    if not request.user.is_staff:
        return redirect('news_list')
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm()
    
    return render(request, 'news_form.html', {'form': form})

def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user.is_staff:
        news.delete()
        messages.success(request, "Новость успешно удалена.")
    return redirect('news_list')

def warranty(request):
    return render(request, 'warranty.html')

def spocoby_pokupki(request):
    return render(request, 'spocoby_pokupki.html')


def trade_in(request):
    return render(request, 'trade_in.html')


class CategoryNewsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        
        """ получение категорий """
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)

        """ получение новостей """
        latest_news = News.objects.order_by('-published_at')[:2]
        news_serializer = NewsSerializer(latest_news, many=True)

        """ получение популярных продуктов """
        popular_products = Product.objects.filter(rating__gt=0).order_by('-rating')[:3]
        if not popular_products:
            products = list(Product.objects.all())
            if len(products) >= 3:
                popular_products = random.sample(products, 3)
            else:
                popular_products = products

        product_serializer = ProductSerializer(popular_products, many=True)
        
        """ Проверка наличия товаров в корзине """
        cart_has_items = False
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            if cart and cart.items.exists():
                cart_has_items = True
        
        """ Ответ в формате JSON """
        return Response({
            'categories': category_serializer.data,
            'latest_news': news_serializer.data,
            'popular_products': product_serializer.data,
            'cart_has_items': cart_has_items
        })
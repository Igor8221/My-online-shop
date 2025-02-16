import requests

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


def index_page(request):
    api_url = "http://127.0.0.1:8000/api/categories-news/"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        data = response.json()  
    except requests.RequestException as e:
        print(f"Ошибка при запросе API: {e}")
        data = {'categories': [], 'latest_news': []}

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

def warranty(request):
    return render(request, 'warranty.html')

def spocoby_pokupki(request):
    return render(request, 'spocoby_pokupki.html')


def trade_in(request):
    return render(request, 'trade_in.html')


class CategoryNewsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)

        latest_news = News.objects.order_by('-published_at')[:2]
        news_serializer = NewsSerializer(latest_news, many=True)

        popular_products = Product.objects.filter(rating__gt=0).order_by('-rating')[:3]
        if not popular_products:
            products = list(Product.objects.all())
            if len(products) >= 3:
                popular_products = random.sample(products, 3)
            else:
                popular_products = products

        product_serializer = ProductSerializer(popular_products, many=True)

        cart_has_items = False
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            if cart and cart.items.exists():
                cart_has_items = True

        return Response({
            'categories': category_serializer.data,
            'latest_news': news_serializer.data,
            'popular_products': product_serializer.data,
            'cart_has_items': cart_has_items
        })
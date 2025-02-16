from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.main import views


urlpatterns = [
    path('', views.index_page, name='index'),
    path('about-the-store', views.about_store, name='about-store'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('news/create/', views.news_create, name='news_create'),
    path('contacts/', views.contacts, name='contacts'),
    path('warranty/', views.warranty, name='warranty'),
    path('spocoby-pokupki/', views.spocoby_pokupki, name='spocoby-pokupki'),
    path('trade-in', views.trade_in, name='trade-in'),
    path('api/categories-news/', views.CategoryNewsAPIView.as_view(), name='categories-news'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



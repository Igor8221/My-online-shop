from django.urls import path
from apps.products import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('administrator/add-category/', views.add_category, name='add_category'),
    path('administrator/add-product/', views.add_product, name='add_product'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('products/', views.product_list, name='product_list'), 
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


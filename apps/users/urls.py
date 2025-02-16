from apps.users import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-email/', views.change_email, name='change_email'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('change-phone/', views.change_phone_view, name='change_phone'),
    path('logout/', views.logout_view, name='logout'),
    path('change_name/', views.change_name, name='change_name'),
    path('leave-review/<int:product_id>/', views.leave_review, name='leave_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

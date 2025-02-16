from django.urls import path
from apps.orders import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('administrator/orders/', views.order_list, name='order_list'),
    path('checkout/', views.checkout, name='checkout'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


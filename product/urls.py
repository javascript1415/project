from product import views
from django.urls import path
urlpatterns = [
    path('add_product',views.add_product,name = 'add_product'),
    path('delete/<int:product_id>/', views.del_pro, name='delete_product'),
    path('edit/<int:product_id>/', views.edit_pro, name='edit_product'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart_detail, name='cart_detail'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order'),
    path('sellorder/', views.sellorder, name='sellorder'),
    path('sellorder/<int:id>', views.status_update, name='status_update'),
    path('add_address/', views.add_address, name='add_address'),

]

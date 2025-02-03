
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('account.urls')),
    path('customer/',include('customer.urls')),
    path('seller/',include('seller.urls')),
    path('product/',include('product.urls')),
    path('orders/', include('order.urls')), 
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

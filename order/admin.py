from django.contrib import admin
from order.models import Order , Addres
# Register your models here.
class orderAdmin(admin.ModelAdmin):

    list_display = ['id','seller','user','ordered_at','updated_at',"status","total_amount"]

admin.site.register(Order ,orderAdmin)


class AddresAdmin(admin.ModelAdmin):

    list_display = ['id','user','phone','muncipality',"city",'tol']

admin.site.register(Addres ,AddresAdmin)
from django.contrib import admin
from .models import Product , CartItem

class ProductModelAdmin(admin.ModelAdmin):
    # Specify the fields you want to display in the list view
    list_display = ['id','name', 'description', 'price', 'created_at', 'updated_at']

    # Optional: Customize ordering in the list view
    ordering = ['name']  # Order by product name, or any other field of Product model

    # Optional: If you want to add filters, ensure the fields exist in the Product model
    list_filter = ['created_at', 'price']  # You can filter by fields available in Product model

    # Optional: Search functionality for fields you want to make searchable
    search_fields = ['name', 'description']  # Search by product name or description

    # Optional: Fields for filtering relationships, if any (e.g., ForeignKey or ManyToMany fields)
    filter_horizontal = []  # Remove this if there are no many-to-many relationships to filter

admin.site.register(Product, ProductModelAdmin)


class CartModelAdmin(admin.ModelAdmin):
    # Specify the fields you want to display in the list view
    list_display = ['id','user', 'product', 'quantity']

    # Optional: Customize ordering in the list view
    ordering = ['user']  # Order by product name, or any other field of Product model


    # Optional: Search functionality for fields you want to make searchable
    search_fields = ['user', 'product']  # Search by product name or description

    # Optional: Fields for filtering relationships, if any (e.g., ForeignKey or ManyToMany fields)
    filter_horizontal = []  # Remove this if there are no many-to-many relationships to filter

admin.site.register(CartItem, CartModelAdmin)
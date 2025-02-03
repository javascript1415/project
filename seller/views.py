from django.shortcuts import render
from core.decorators import login_and_role_required
from product.models import Product
from order.models import Order

@login_and_role_required("seller")
def seller_dashboard_view(request):
    products = Product.objects.filter(seller = request.user).order_by('id')
    orders = Order.objects.filter(seller = request.user)
    total = 0
    for p in orders:
        if p.status == "Delivered":
            total += p.total_amount
    return render(request,'seller/dashboard.html',{"products":products,'orders':orders,'total':total})
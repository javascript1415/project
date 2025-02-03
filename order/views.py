from django.shortcuts import render , redirect ,get_object_or_404
from . models import Order , Addres
from product.models import CartItem
from .forms import addressForm 
from core.decorators import login_and_role_required

# Create your views here.


@login_and_role_required("customer")
def order_list(request):
    selected_items = Order.objects.filter(user=request.user)
    ad = Addres.objects.filter(user=request.user).first()
    
    return render(request,'order/orders.html',{'selected_items':selected_items,'ad':ad})


@login_and_role_required("customer")
def add_address(request):
    instance = Addres.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = addressForm(request.POST, instance=instance)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            item = Order.objects.filter(user = request.user)
            if not item:
                return redirect('cart_detail')
            return redirect('order')
    else:
        form = addressForm(instance=instance)
    
    return render(request, 'order/add_address.html', {'form': form})

@login_and_role_required("seller")
def sellorder(request):
    orders = Order.objects.filter(seller=request.user).order_by('ordered_at')

    addresses = Addres.objects.filter(user__in=[order.user for order in orders])
    address_dict = {address.user: address for address in addresses}

    for order in orders:
        order.buyer_address = address_dict.get(order.user, None)

    return render(request, 'order/sellorder.html', {
        'orders': orders,
    })


@login_and_role_required("seller")
def status_update(request, id):
    
    if request.method == "POST":
            order = get_object_or_404(Order, id=id, seller=request.user)
            order.status = request.POST.get('status')
            order.save()
            
            return redirect('sellorder')

    return render(request, 'order/status_update.html', { 'order': order})

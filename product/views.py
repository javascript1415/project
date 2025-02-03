from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Product , CartItem
from .forms import ProductForm
from core.decorators import login_and_role_required
from order.models import Order
from django.db import transaction
from decimal import Decimal
from order.models import  Addres 
from django.http import Http404

# Create your views here.


@login_and_role_required("seller")
def add_product(request):   
    user = request.user
    print(user.id)
    print(user)
    if request.method == 'POST':
        print("Request FILES:", request.FILES)  
        form = ProductForm(request.POST,request.FILES)
        # print(form)
        if form.is_valid():
            product = form.save(commit=False)
            product_name = form.cleaned_data['name']
            if Product.objects.filter(name=product_name, seller=user).exists():
                messages.error(request, 'A product with this name already exists. Please choose a different name.')
                return redirect('add_product')  # Redirect to the same page to try again

            product.seller = user
            print(product.image)
            # print(request.user)
            print(f"Product image: {product.image}")
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    # print(form)
    return render(request,'addpro.html',{'fo':form})

@login_and_role_required("seller")
def del_pro(request,product_id):
    product = get_object_or_404(Product,id=product_id,seller=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('seller_dashboard')  # Redirect to seller dashboard after deletion

    # Optional: You can show a confirmation page here before actually deleting
    return render(request,'del.html',{'product': product})

@login_and_role_required("seller")
def edit_pro(request,product_id):
    product = get_object_or_404(Product,id = product_id,seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('seller_dashboard')  # Redirect to seller dashboard or another appropriate page
    else:
        form = ProductForm(instance=product)
    return render(request,'edit.html',{"form":form})

@login_and_role_required("customer")
def add_to_cart(request, product_id):
    if not request.user.is_authenticated :
        messages.error(request, "You need to log in first to add items to the cart.")
        return redirect('login')  # Replace 'login' with the name of your login URL pattern if different
    if request.user.is_seller:
        messages.error(request,'login as customer to add rpoducts to the cart')
        return redirect('home')
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product,sell =product.seller)
    
    if created:
        messages.success(request, "Successfully added to the cart")
    else:  
        cart_item.quantity += 1 
        if cart_item.quantity > 5:
            cart_item.quantity = 5
            messages.error(request,"maximun product qualtity reached")
            return redirect('home')
        cart_item.save()  
        messages.success(request, "Added 1 more item")
    
    return redirect('home')  # Assuming 'ho' was meant to be 'home'




@login_and_role_required("customer")
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        if 'orderform' in request.POST:
            selected_items = request.POST.getlist('orderyes')
            print("Selected items:", selected_items)

            if not selected_items:
                messages.warning(request, 'Please select at least one item to order')
                return redirect('cart_detail')

            selected_objects = CartItem.objects.filter(id__in=selected_items)
            try:
                address = get_object_or_404(Addres, user=request.user)
            except Http404:
                return redirect('add_address')  # Redirect to the 'add_address' view if address is not found

            if not address:
                return redirect('add_address')
            try:
                with transaction.atomic():
                    for item in selected_objects:
                        ord = Order(
                            user=request.user,
                            seller=item.sell,
                            items= item.product , # Links the CartItem to the Order
                            total_amount=Decimal(item.total_price),
                            quantity = item.quantity
                        ) 
                        print(ord)
                        ord.save()
                        item.product.quantity = item.product.quantity - item.quantity
                        item.product.save()
                        print(f"Order saved: {ord}")
                        item.delete()  # Deletes the CartItem after the order is created
                        print(f"Deleted cart item: {item}")
                        print(Order.objects.filter(user = request.user))

                messages.success(request, 'Order placed successfully!')
                    
            except Exception as e:
                print(f"Transaction failed: {e}")
                messages.error(request, "There was an issue processing your order.")
                return redirect('cart_detail')

            return redirect('add_address')
        
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_and_role_required("customer")
def remove_from_cart(request,item_id):
    product = get_object_or_404(CartItem,id=item_id,user=request.user)
    product.delete()
    return redirect('cart_detail') 



@login_and_role_required("customer")
def update_cart(request, item_id):
    if request.method == 'POST':
        try:
            # Get the CartItem directly
            cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
            
            # Get and validate quantity
            quantity = request.POST.get('quantity')
            if not quantity or not quantity.isdigit():
                messages.error(request, "Please enter a valid quantity")
                return redirect('cart_detail')
            
            # Convert to integer and validate range
            quantity = int(quantity)
            if quantity > 5:
                quantity = 5
                messages.warning(request, "Maximum quantity is 5")
            elif quantity < 1:
                quantity = 1
                messages.warning(request, "Minimum quantity is 1")
            
            # Update the cart item
            cart_item.quantity = quantity
            cart_item.save()
            
            messages.success(request, "Cart updated successfully!")
            
        except CartItem.DoesNotExist:
            messages.error(request, "Cart item not found")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            
    return redirect('cart_detail')
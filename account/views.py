from django.shortcuts import render , redirect
from account.forms import RegistrationForm ,PasswordResetForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from abhi import settings
from account.utils import send_activation_email , send_reset_password_email
from account.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import SetPasswordForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site 
from product.models import Product
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage

# Create your views here.
def home(request):
    products_list = Product.objects.all().order_by('?')  # Random order
    paginator = Paginator(products_list, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)  # Get the requested page

    return render(request, 'account/home.html', {"products": products})
@csrf_protect
def register_view(request):
  if request.user.is_authenticated:
      return redirect('home')
  else:
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            role = request.POST.get('role')

            if role == 'seller':
                user.is_seller = True
                user.is_customer = False
            elif role == 'customer':
                user.is_customer = True
                user.is_seller = False
            
            user.save()
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate',kwargs={"uidb64":uidb64,"token":token})
            activation_url = f"{settings.SITE_DOMAIN}{activation_link}"
            send_activation_email(user.email, activation_url)
            messages.success(request,"ur form is  been saved sucessfully kindly check ur email to verifiey ur account")
            return redirect('login')
        
    else:
        form = RegistrationForm()

    return render(request,'account/register.html',{'form':form})

def activate_account(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
        if user.is_active:
            messages.warning(request,"the user is already active")
            return redirect('login')
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request,"ur account has ben sucessfully activated  log in now")
            return redirect('login')
        
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        messages.error(request,"activation process failed try again :)")
        return redirect('register')
       


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
                    return redirect('customer_dashboard')
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            print(email,password)
            messages.error(request,"email and the pw are nessary")
            return redirect('login')
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            messages.error(request,"gmail or pw invalid")
            return redirect('login')  

        if not user.is_active:
            messages.warning(request,"1st of all verify ur email and activate it")
            return redirect('login')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            if request.user.is_seller:
                return redirect('seller_dashboard')
            elif request.user.is_customer:
                return redirect('customer_dashboard')
            else:
                print(user.is_seller,user.is_customer)
                messages.error(request,"u dont have permission inside here")
                return redirect('home')
        else:
            messages.error(request,"gmail or pw invalid")
            return redirect('login')  
       
        
    return render(request,'account/login.html')





def password_reset_view(request):
    if request.method=="POST":
        form= PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
               token = default_token_generator.make_token(user)
               uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
               reset_link = reverse('password_reset_confirm', 
                    kwargs={'uidb64': uidb64, 'token': token})
               current_site = get_current_site(request)
               absolute_url = f"http://{current_site.domain}{reset_link}"
               print(reset_link)
               print(absolute_url)
               
               # Send email
               send_reset_password_email(user.email, absolute_url)
               messages.success(request, "Password reset link has been sent to your email.")
               return redirect('login')
            else:
             messages.error(request, "No account found with this email address.")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('password_reset')
    else:
        form = PasswordResetForm()
    return render(request,'account/password_reset.html',{'form':form})

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            messages.error(
                request, "Invalid or expired password reset token. Please try again."
            )
            return redirect('password_reset')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "An error occurred. Please try again later.")
        return redirect('password_reset')

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been successfully reset.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors: 
                    messages.error(request, error)
    else:
        form = SetPasswordForm(user)

    return render(request, 'account/password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})


def product_view(request , product_id):
    product = Product.objects.get(id = product_id)
    return render(request,'account/product.html',{'product':product})


from django.db.models import Case, When, IntegerField, Value, Q
from django.db.models.functions import Lower

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Convert query to lowercase for case-insensitive comparison
        query_lower = query.lower()
        
        results = Product.objects.annotate(
            # Convert name to lowercase for comparison
            name_lower=Lower('name'),
            # Calculate search priority
            priority=Case(
                # Highest priority: Name starts with query (case-insensitive)
                When(name_lower__startswith=query_lower, then=Value(1)),
                # Second priority: Name contains query exactly
                When(name__icontains=query, then=Value(2)),
                # Third priority: Description contains query
                When(description__icontains=query, then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        ).filter(
            # Filter for either name or description matches
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        ).order_by('priority', 'name')  # Sort by priority first, then alphabetically
    
    # Pagination logic
    paginator = Paginator(results, 12)
    page_number = request.GET.get('page')
    
    try:
        paginated_results = paginator.get_page(page_number)
    except PageNotAnInteger:
        paginated_results = paginator.get_page(1)
    except EmptyPage:
        paginated_results = paginator.get_page(paginator.num_pages)
    
    context = {
        'query': query,
        'results': paginated_results
    }
    return render(request, 'account/search_results.html', context)
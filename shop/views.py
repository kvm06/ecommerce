from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Product, Category, Cart, CartItem
from django.contrib.auth.models import Group, User
from django import forms
from .forms import SignUpForm, FilterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
# Create your views here.

def home(request):
    form = FilterForm(request.POST)
    products=Product.objects.all()
    resolutions = dict(form.data).get("resolution_field")
    corpuses = dict(form.data).get("corpus_field")
    brands = dict(form.data).get("brand_field")
    if resolutions is not None:
        products = products.filter(resolution__in = resolutions)
    
    if corpuses is not None:
        products = products.filter(corpus__in = corpuses)

    if brands is not None:
            products = products.filter(brand__in = brands)

    return render(request, 'shop/home.html', {'form': form, 'products':products})

# def home(request, category_slug=None):
#     category_page=None
#     products=None

#     if request.method == "POST":
#         # products = Product.objects.filter(resolution="4mp")
#         print(list(request.POST.items()))

#     else:
#         if category_slug != None:
#             category_page = get_object_or_404(Category, slug=category_slug)
#             products = Product.objects.filter(category=category_page, available=True)
#         else:
#             products = Product.objects.all().filter(available=True)

#     return render(request, "shop/home.html", {'category':category_page, 'products': products})

def product(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, "shop/product.html", {'product': product})

def _cart_id(request):
    cart_session = request.session.session_key
    if not cart_session:
        cart_session = request.session.create()

    return cart_session

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect('cart_detail')

def minus_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def delete_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        print(cart_items.values())
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'shop/cart.html', dict(cart_items=cart_items, total=total, counter=counter))

def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='User')
            user_group.user_set.add(signup_user)
    else:
        form = SignUpForm()
    return render(request, 'shop/signup.html', {'form':form})

def log_in_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form':form})

def log_out_view(request):
    logout(request)
    return redirect('home')
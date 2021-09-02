from django import http
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls.base import is_valid_path
from django.utils.translation import check_for_language
from .models import Product, Category, Cart, CartItem, CheckboxChoices
from django.contrib.auth.models import Group, User
from django import forms
from .forms import SignUpForm, FilterForm, ContactForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
# Create your views here.

def home(request, category_slug=None):

    contact_form = ContactForm()
    filter_form = FilterForm(request.POST)
    products=Product.objects.all()
    category_page=None

    if request.method == 'POST':
        if filter_form.is_valid():
            for form_field in filter_form.fields.keys():
                filter_request = form_field + "__in"
                search_list = filter_form.cleaned_data[form_field]
                if search_list:
                    products = products.filter(**{filter_request: search_list})
        else:
            filter_form = FilterForm() 
    else: 
        if category_slug != None:
            category_page = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=category_page, available=True)

    current_counts = {}
    total_counts = {}
    for field in filter_form.fields:
        num = 0
        for choice in filter_form.fields[field].choices:
            current_count = products.filter(**{field:choice[0]}).count()
            total_count = Product.objects.all().filter(**{field:choice[0]}).count()
            key = '{0}_{1}_{2}'.format("id", field, num)
            current_counts[key] = current_count
            total_counts[key] = total_count
            num += 1

    for choices in filter_form.fields["resolution"].choices:
        print(choices)        
    return render(request, 'shop/home.html', {'products':products, 'filter_form': filter_form, 'contact_form':contact_form, 'category':category_page, 'current_counts':current_counts, 'total_counts':total_counts})
    
def contact_me(request):
    contact_form = ContactForm(request.POST)

    # if contact_form.is_valid():
    #     subject = contact_form.cleaned_data['subject']
    #     message = contact_form.cleaned_data['message']
    #     sender = contact_form.cleaned_data['sender']
    #     cc_myself = contact_form.cleaned_data['cc_myself']

    #     recipients = ['koloev_vis@mail.ru']

    #     if cc_myself:
    #         recipients.append(sender)
    #     send_mail(subject, message, sender, recipients)
    #     return HttpResponseRedirect('thanks')
    # else:
    #     print('form is no valid')
    return redirect('home')

def thanks(request):
    return render(request, "shop/thanks.html")

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

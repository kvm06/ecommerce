from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('category/<slug:category_slug>', views.home, name="product_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product, name="product_detail"),
    path('cart', views.cart_detail, name="cart_detail"),
    path('cart/add/<int:product_id>', views.add_to_cart, name="add_to_cart"),
    path('cart/minus/<int:product_id>', views.minus_from_cart, name="minus_from_cart"),
    path('cart/delete/<int:product_id>', views.delete_from_cart, name="delete_from_cart"),
    path('account/create/', views.sign_up_view, name="sign_up_view"),
    path('account/login/', views.log_in_view, name="log_in_view"),
    path('account/logout/', views.log_out_view, name="log_out_view"),
] 
 
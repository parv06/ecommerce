from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from products.models import Product, CartItem


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('/')


@login_required()
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart/cart.html', {'cart_items': cart_items})


# @login_required
# def remove_from_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     cart_item = CartItem.objects.get(user=request.user, product=product)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('cart')  #


@login_required
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(user=request.user, product__id=product_id)
            cart_item.delete()
            return redirect('cart')
        except CartItem.DoesNotExist:
            pass
    return redirect('cart')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

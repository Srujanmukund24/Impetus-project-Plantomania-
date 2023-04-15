from django.shortcuts import render,redirect
from .models import Product,CartItem,Category
from django.contrib import messages

def store(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)

def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    # Check if the product is already in the cart
    cart_item = CartItem.objects.filter(product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'{product.name} added to cart')
    else:
        CartItem.objects.create(product=product)
        messages.success(request, f'{product.name} added to cart')
    products = Product.objects.all()
    context = {
        'products': products
    }

    return render(request, 'store/store.html', context)
def cart(request):

    cart_items = CartItem.objects.filter(user=request.user)
    # cart_items = CartItem.objects.all()


    total_price = sum([item.product.price * item.quantity for item in cart_items])

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'store/cart.html', context)
from django.shortcuts import redirect

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        cart_item = CartItem.objects.get(product_id=product_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart')

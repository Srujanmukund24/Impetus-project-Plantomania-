from django.shortcuts import render,redirect
from .models import Product,CartItem,Category
from django.contrib import messages
import stripe
from django.conf import settings
from .forms import BillingForm
from django.http import JsonResponse
import stripe
from django.conf import settings
import razorpay
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt

def store(request):
    # categoryy = request.POST.get('plant_options')
    products = Product.objects.filter(category__name=request.POST.get('plant_options'))
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
def plantop(request):
    return render(request, 'store/plantop.html')

def checkout(request):

    cart_items = CartItem.objects.filter(user=request.user)

    total_price = sum([item.product.price * item.quantity for item in cart_items])

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():

            customer = stripe.Customer.create(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                address={
                    'line1': form.cleaned_data['address_line1'],
                    'line2': form.cleaned_data['address_line2'],
                    'city': form.cleaned_data['city'],
                    'state': form.cleaned_data['state'],
                    'postal_code': form.cleaned_data['postal_code'],
                    'country': form.cleaned_data['country'],
                }
            )

            charge = stripe.Charge.create(
                customer=customer.id,
                amount=int(total_price * 100),
                currency='usd',
                description='Example charge',
            )

            # Clear the user's cart
            CartItem.objects.filter(user=request.user).delete()

            return redirect('land')

    else:
        form = BillingForm()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_price1': total_price * 100,
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, 'store/checkout.html', context)





def create_payment(request):
    if request.method=='POST':

        # cart_items = CartItem.objects.filter(user=request.user)
        #
        # total_price = sum([item.product.price * item.quantity for item in cart_items])
        amount=100;
        order_currency='INR'
        client=razorpay.Client(
            auth=('rzp_test_xdK2Xh5HZzMR5n','wopMADxA79HLhSSkWsNu0w6L')

        )
        payment = client.order.create({'amount': amount, 'currency': "INR", 'payment_capture': '1'})
        return render(request, 'store/checkout.html')
@csrf_exempt
def sucess(request):
    return render(request, 'store/sucess.html')


from django.shortcuts import render, get_object_or_404
from .models import Product


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/product_detail.html', {'product': product})








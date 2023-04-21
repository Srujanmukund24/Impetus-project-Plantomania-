from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login,authenticate, logout
# Create your views here.
from store.models import Product

def home(request):
    products = Product.objects.filter(category__name='top')
    context = {
        'products': products
    }


    return render(request, 'users/home.html',context)

def login(request):
    return render(request,'users/login.html')
def register(request):

        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your Account has been created! You are now able to Login.')
                return redirect('login')
        else:
            form = UserRegisterForm

        return render(request, 'users/register.html', {'form': form})

def team(request):
    return render(request, 'users/team.html')
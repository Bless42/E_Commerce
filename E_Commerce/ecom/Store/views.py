from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import SignUpForm,  UpdateUserForm, ChangePasswordForm
from django import forms


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #did there feel out the form 
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Your password has been updated..."))
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
        messages.success(request, ("You Must Be Logged In TO VIEW THAT PAGE!"))
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ("User Has Been Updated. "))
            return redirect('home')
        return render(request, "update_user.html", {"user_form":user_form})
    else:
         messages.success(request, ("You Must Be Logged In To Access That Page!!"))
         return redirect('home')



def category_summary(request):
    categories = Category.objects.all()
    return render(request, "category_summary.html", {"categories":categories})



def category(request,foo):
    #replace hyphens with spaces 
    foo = foo.replace('-', ' ') 
    #grab category from url
    try:
        #look up the category
        category = Category.objects.get(name=foo)
        print('category ===>', category)
        products = Product.objects.filter(Category=category)
        print('cat ', products)
        return render(request, 'category.html', {'products':products, 'category': category})

    except:
        messages.success(request, ("That category those not exist. "))
        return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products':products, 'categories': categories})


def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!. "))
            return redirect('home')
        else:
            messages.success(request, ("there was and error, please try again . "))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out... thanks for stoping by. "))
    return redirect('home')

def register_user(request):
    form = SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered succesfully!! welcome!"))
            return redirect('home')
        else:
            messages.success(request, ("whoops!! there was a problem Registering please try again"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})




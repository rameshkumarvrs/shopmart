from django.shortcuts import render, redirect
from django.contrib import messages
from shop.form import CustomUserForm
from . models import *
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json


# Create your views here.

def home(request):
    products = Product.objects.filter(trending=1)
    return render(request, "shop/index.html", {"products": products})


def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, "shop/fav.html", {'fav': fav})
    else:
        return redirect("/") 

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout user succesfully")
    return redirect("/")

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {'cart': cart})
    else:
        return redirect("/")   


def remove_cart(request, cid):
    cart_items = Cart.objects.get(id=cid)
    cart_items.delete()
    return redirect("/cart")


def remove_fav(request, fid):
    fav_items = Favourite.objects.get(id=fid)
    fav_items.delete()
    return redirect("/favviewpage")

def fav_page(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            
            print(data['pid'])
           
            pid=data['pid']
           
            Favourite.objects.create(user=request.user, products_id=pid)
            return JsonResponse({'status': 'Product added to faverites'}, status=200)
        else:
            return JsonResponse({'status': 'Login to addFaverite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid access'}, status=200)



def add_to_cart(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            print(data['product_qty'])
            print(data['pid'])
            product_qty=data['product_qty']
            pid=data['pid']

            # print(request.user.id)
            product_status = Product.objects.get(id=pid)
            
            if product_status:
                if Cart.objects.filter(user=request.user.id, products_id=pid):
                    return JsonResponse({'status': 'Product already in Cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user, products_id=pid, product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock not available'}, status=200)
            else:
                return JsonResponse({'status': 'Added to cart', 'pid': pid, 'qty': product_qty}, status=200)
        else:
            return JsonResponse({'status': 'Login to addCart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid access'}, status=200)

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get("username")
            pwd = request.POST.get("password")
            user = authenticate(request, username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request, "User Succesfully logged in")
                return redirect("/")
            else:
                messages.error(request, "Inavalid username and Password")
                return redirect('/login')
        return render(request, "shop/login.html")

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successfull")
            return redirect('/login')
    return render(request, "shop/register.html", {'form': form})


def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, "shop/collections.html", {"category": category})

def collectionsview(request,name):
    print("fhbdhjfbhdsbfbsdfbjdsfbbsdf", name)
    if (Category.objects.filter(name=name, status=0)):
        products = Product.objects.filter(category__name=name)
        return render(request, "shop/products/index.html", {"products": products, "category_name": name })
    else:
        messages.warning(request, "No such categories Found")
        return redirect('collections')
    

def product_details(request, cname, pname):
    if (Category.objects.filter(name=cname, status=0)):
        category = Category.objects.filter(name=cname, status=0)
        if (Product.objects.filter(name=pname, status=0)):
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/product_details.html", {"products": products} )

        else:
            messages.error(request, "No such products found")
            return redirect('collections')    
    
    else:
        messages.error(request, "No such categories found")
        return redirect('collections')

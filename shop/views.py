from django.shortcuts import render, redirect
from django.contrib import messages

from . models import *

# Create your views here.

def home(request):
    return render(request, "shop/index.html")

def register(request):
    return render(request, "shop/register.html")


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

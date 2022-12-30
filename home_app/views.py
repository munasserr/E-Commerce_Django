from django.shortcuts import render
from .models import *
from shopping_app.models import *

def home(request) :
    user = request.user
    if user.is_authenticated :
        carti = CartItem.objects.filter(user=request.user , ordered = False)
        contxt = {
            'prod' : Product.objects.all(),
            'prdu' : carti 
        }
    else:
        # carti = CartItem.objects.filter(user=request.user , ordered = False)
        contxt = {
        'prod' : Product.objects.all(),
        # 'prdu' : carti 
    }

    return render(request , 'home.html',contxt)


def about(request) :
    return render(request , 'about.html')

def service(request) :
    return render(request , 'ourservice.html')

def contact(request) :
    return render(request , 'contact.html')


from django.shortcuts import HttpResponse, redirect, render , get_object_or_404
from home_app.models import *
from shopping_app.models import *
from django import template
from .forms import * 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def shop(request):

    price_from =request.GET.get('price_from',0)
    price_to =request.GET.get('price_to',10000)
    sorting = request.GET.get('sorting' , '-data_added')
    product =Product.objects.filter(price__gte = price_from).filter(price__lte = price_to)
    carti = CartItem.objects.filter(user=request.user , ordered=False)
    contxt = {
        'prod' : product.order_by(sorting),
        'price_from' :price_from,
        'price_to' :price_to,
        'sorting' : sorting ,
        'prdu' : carti,
    }

    if request.method == 'POST' :
        name = request.POST['name']
        products = Product.objects.filter(name__icontains = name )
        ctxt = {
            'prod' : products
        } 
        
        return render(request , 'shop.html' ,ctxt)

    return render(request , 'shop.html' ,contxt)

def shopdet(request , id):
    prd = Product.objects.all()
    product_id =Product.objects.get(id=id)
    carti = CartItem.objects.filter(user=request.user , ordered=False)
    ctxt = {
            'prod' : product_id,
            'prd' : prd,
            'prdu' : carti
        } 
    return render(request , 'shopdetails.html' , ctxt)

def checkout(request):
        form=CheckoutForm()

        cart = CartItem.objects.filter(user=request.user , ordered=False)
        cart_items = Cart.objects.get(user = request.user, ordered = False)
        carti = CartItem.objects.filter(user=request.user , ordered = False) #for the sidebar
        context = {
            'tot' : cart_items,
            'prd' : cart,
            'form' : form,
            'prdu' : carti 
        }
        # Order.objects.update(user=request.user,cart=Cart.objects.get(user = request.user, ordered = False))
        if request.method == 'POST':
            form = CheckoutForm(request.POST ,request.FILES)
            if form.is_valid():
                    Order.objects.create(user=request.user ,cart=Cart.objects.get(user = request.user, ordered = False))
                    main_order = Order.objects.get(user = request.user, ordered = False)
                    field = form.cleaned_data

                    main_order.fname = field['fname']
                    main_order.lname = field['lname']
                    main_order.user_name = field['user_name']
                    main_order.email = field['email']
                    main_order.address = field['address']
                    main_order.country = field['country']
                    main_order.zip = field['zip']
                    main_order.payment_option = field['payment_option']
                    main_order.credit_card_number = field['credit_card_number']
                    main_order.exp_date = field['exp_date']
                    main_order.cvv = field['cvv']
                    # main_order.cart = Cart.objects.get(user = request.user, ordered = False)
                    main_order.ordered = True
                    c_cart = main_order.cart
                    c_cart.ordered = True

                    cart_items = main_order.cart.items.all()
                    cart_items.update(ordered=True)
                    for item in cart_items:
                        item.save()
                    main_order.save()
                    c_cart.save()
                    messages.success(request,"Your Order Has Been Placed Successfully")
                    return redirect('/shop')
            else:
                messages.warning(request,"Failed Placing Your Order")
                return redirect('/shop/checkout')

        return render(request , 'checkout.html',context)

@login_required
def add_to_cart(request , id) :
    item = get_object_or_404(Product , id = id)
    order_item ,created = CartItem.objects.get_or_create(item = item ,user = request.user , ordered = False)
    order_qs = Cart.objects.filter(user = request.user , ordered = False )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is on the order
        if order.items.filter(item__id = item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("/shop/" , id = id)
        
        else :
            ordered_date = timezone.now()
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
    
    else:
        ordered_date = timezone.now()
        order = Cart.objects.create(user=request.user, orderd_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect("/shop/" , id = id)


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Product , id = id)
    order_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = CartItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("/shop/cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("/shop/",id = id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("/shop/t", id = id)



@login_required
def cart(request):

    carti = CartItem.objects.filter(user=request.user , ordered=False)
    cart = CartItem.objects.filter(user=request.user , ordered=False)
    cart_items = Cart.objects.get(user = request.user, ordered = False)

    ctxt = {
            'tot' : cart_items,
            'prd' : cart,
            'prdu' : carti,
            'couponform' : CouponForm(),
        } 

    return render(request , 'cart.html' , ctxt)

def get_coupon(request , code):
    try :

        coupon = Coupon.objects.get(code=code)
        return coupon

    except ObjectDoesNotExist :
        messages.info(request , 'This Coupon Is Invalid Or Doesn\'t Exist')
        return redirect('/shop/cart')



def add_coupon(request):
    if request.method=='POST':
        form = CouponForm(request.POST)

        if form.is_valid():
            try :
                code=form.cleaned_data['code']
                order = Cart.objects.get(user=request.user , ordered = False)
                order.coupon = get_coupon(request,code)
                order.save()
                messages.success(request , 'Successfully Added This Coupon')
                return redirect('/shop/cart')
                

            except ObjectDoesNotExist :
                messages.info(request , 'You Don\'t Have An Active Order')
                return redirect('/shop/cart')

    return redirect('/shop/cart')


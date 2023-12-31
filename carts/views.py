from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Carts,Cart_item
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
def add_cart(request,product_id):
    current_url = request.META.get('HTTP_REFERER')
    current_user=request.user
    product=Product.objects.get(id=product_id)
    #if the user is authenticate
    if current_user.is_authenticated:
        try:
            cart = Carts.objects.get(cart_id=_cart_id(request)) 
        except Carts.DoesNotExist:
            cart = Carts.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()  
        is_cart_item_exists = Cart_item.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = Cart_item.objects.filter(product=product, user=current_user)
            for item in cart_item:
                
                item.quantity += 1
                item.save()

           

        else:
            cart_item = Cart_item.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
                cart =cart,

            )
            cart_item.save()
            messages.success(request,'Item Added to Cart')

       
      
        
    

        return redirect(current_url)   
   

    else:
        
        try:
            cart = Carts.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Carts.DoesNotExist:
            cart = Carts.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()     
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart.save()
        is_cart_item_exists = Cart_item.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = Cart_item.objects.filter(product=product, cart=cart)
            # cart_item.save()
            for item in cart_item:
                    
                item.quantity += 1
                item.save()
        else:
            cart_item = Cart_item.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )

            cart_item.save()
       

            messages.success(request,'Item Added to Cart')
        
    
        return redirect(current_url)

def Cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=Cart_item.objects.filter(user=request.user,is_active=True)
        else:
            cart=Carts.objects.get(cart_id=_cart_id(request))
            cart_items=Cart_item.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.new_price * cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total + tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }


    return render(request,'store/cart.html',context)
def remove_cart(request,product_id,cart_item_id):
    
    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=Cart_item.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart=Carts.objects.get(cart_id=_cart_id(request))
            cart_item=Cart_item.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
def remove_cart_item(request,product_id,cart_item_id):
    
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item=Cart_item.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart=Carts.objects.get(cart_id=_cart_id(request))
        cart_item=Cart_item.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=Cart_item.objects.filter(user=request.user,is_active=True)
        else:
            cart=Carts.objects.get(cart_id=_cart_id(request))
            cart_items=Cart_item.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.new_price * cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total + tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'store\checkout.html',context)
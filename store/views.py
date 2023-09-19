from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from django.http import HttpResponse
from .models import Product,ReviewRating,ProductGalery,UserProfile
from django.db.models import Q
from category.models import Category
from carts.models import Cart_item,Carts
from carts.views import _cart_id
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderedProduct,Order
# Create your views here.


def store(request,category_slug=None):
    categories=None
    products=None
    if category_slug != None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        paginator=Paginator(products,6)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,6)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    
    
    context={
        'products':paged_products,
        'product_count':product_count,
        
        
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=Cart_item.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct=OrderedProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderedProduct.DoesNotExist:
            orderproduct=None
    else:
        orderproduct=None
    #get the reviews 

    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)
    
    #get th eproduct gallery


    product_gallery=ProductGalery.objects.filter(product_id=single_product.id)

    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallery':product_gallery,
       
        
    }
    return render (request,'store/product-detail.html',context)
def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
    }
    return render(request,'store/store.html',context)

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


def mobile(request,data=None):
 
  if data==None:
     mobiles=Product.objects.filter(category__category_name='Mobile')
     paginator=Paginator(mobiles,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=mobiles.count()
  elif data in ['redmi','samsung','realme','iphone','asus','poco','nokia','lg','vivo','oppo']:
     mobiles=Product.objects.filter(category__category_name='Mobile').filter(brand=data)
     paginator=Paginator(mobiles,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=mobiles.count()
   
  elif data=='below':
    mobiles=Product.objects.filter(category__category_name='Mobile').filter(new_price__lt=10000)
    paginator=Paginator(mobiles,6)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    product_count=mobiles.count()
   
  elif data=='above':
    mobiles=Product.objects.filter(category__category_name='Mobile').filter(new_price__gt=10000)
    paginator=Paginator(mobiles,6)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    product_count=mobiles.count()

  
  context={
   
   'mobiles':paged_products,
   
   'mobiles_count':product_count
    
   
  }
  return render(request, 'mobile.html',context)

def laptop(request,data=None):
    if data==None:
     laptop=Product.objects.filter(category__category_name='laptop')
     paginator=Paginator(laptop,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=laptop.count()
    elif data in ['dell','hp','asus','lenovo','mac']:
     laptop=Product.objects.filter(category__category_name='laptop').filter(brand=data)
     paginator=Paginator(laptop,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=laptop.count()
   
    elif data=='below':
     
     laptop=Product.objects.filter(category__category_name='laptop').filter(new_price__lt=10000)
     paginator=Paginator(laptop,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=laptop.count()
   
    elif data=='above':
     laptop=Product.objects.filter(category__category_name='laptop').filter(new_price__gt=10000)
     paginator=Paginator(laptop,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=laptop.count()

    context={
       'laptop':paged_products,
       'laptop_count':product_count,
    }
    return render(request, 'laptop.html',context)

def tv(request,data=None):
    if data==None:
     tv=Product.objects.filter(category__category_name='T.V')
     paginator=Paginator(tv,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=tv.count()
    elif data in ['oneplus','samsung','kodak','mi','lg','redmi','vw','sansui']:
     tv=Product.objects.filter(category__category_name='T.V').filter(brand=data)
     paginator=Paginator(tv,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=tv.count()
   
    elif data=='below':
     
     tv=Product.objects.filter(category__category_name='T.V').filter(new_price__lt=15000)
     paginator=Paginator(tv,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=tv.count()
   
    elif data=='above':
     tv=Product.objects.filter(category__category_name='T.V').filter(new_price__gt=15000)
     paginator=Paginator(tv,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=tv.count()

    context={
       'tv':paged_products,
       'tv_count':product_count,
    }
    return render(request, 'tv.html',context)

def mens(request,data=None):
    if data==None:
     mens=Product.objects.filter(category__category_name='mens')
     paginator=Paginator(mens,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=mens.count()
    elif data in ['casualshirt','formalshirt','jeans','cottonpant','formalshoes','casualshoes','innerwear','tshirt']:
     mens=Product.objects.filter(category__category_name='men').filter(dress_type=data)
     paginator=Paginator(mens,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=mens.count()
   
    elif data=='below':
     
     mens=Product.objects.filter(category__category_name='mens').filter(new_price__lt=1000)
     paginator=Paginator(mens,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=mens.count()
   
    elif data=='above':
     mens=Product.objects.filter(category__category_name='mens').filter(new_price__gt=1000)
     paginator=Paginator(mens,6)
     page=request.GET.get('page')
     paged_products=paginator.get_page(page)
     product_count=mens.count()

    context={
       'mens':paged_products,
       'mens_count':product_count,
    }
    return render(request, 'mens.html',context)
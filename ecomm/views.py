from django.shortcuts import render,get_object_or_404
from store.models import Product,ReviewRating
from category.models import Category

def home(request):   
    mobile=Product.objects.filter(category__category_name='Mobile').filter(is_available=True,trending=1).order_by('-created_date')[:8]
    laptop=Product.objects.filter(category__category_name='laptop').filter(is_available=True,trending=1).order_by('-created_date')[:8]
    tv=Product.objects.filter(category__category_name='T.V').filter(is_available=True,trending=1).order_by('-created_date')[:8]
    product=Product.objects.filter(is_available=True,trending=1).order_by('-created_date')
    if product != None:
        for i in product:
            reviews=ReviewRating.objects.filter(product_id=i.id,status=True)
    context={
        'product':product,
        'reviews':reviews,
        'mobile':mobile,
        "laptop":laptop,
        'tv':tv,

    }
    return render(request,'store/home.html',context)

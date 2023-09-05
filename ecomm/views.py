from django.shortcuts import render,get_object_or_404
from store.models import Product

def home(request):
    product=Product.objects.all().filter(is_available=True)
    context={
        'product':product
    }
    return render(request,'store/home.html',context)
from django.shortcuts import get_object_or_404, render,redirect
from .forms import Registrationform,UserForm,UserProfileForm
from . models import Account,UserProfile
from orders.models import Order,OrderedProduct
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required 
from carts.models import Cart_item,Carts
from carts.views import _cart_id
#verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests
# Create your views here.


def register(request):
   
    if request.method == 'POST':
        form=Registrationform(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            
            current_site=get_current_site(request)
            mail_subject='Please activate your account'
            message=render_to_string('accounts/account_verifiation_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # messages.success(request,'Thank you registering with us. we have sent you an verification email to youe email address.Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+ email)
           
    else:
        form=Registrationform()

    context={
        'form':form
    }
    return render (request,'accounts/register.html',context)


def login(request):
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                
                cart=Carts.objects.get(cart_id = _cart_id (request))
                is_cart_item_exists=Cart_item.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    cart_item=Cart_item.objects.filter(cart=cart)
                   #getting the product variation by cart id
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variation.all()
                        product_variation.append(list(variation))
                    #get the cart item to access from the user to access its product variation
                    cart_item=Cart_item.objects.filter(user=user)
                    ex_var_list=[]
                    id=[]
                    for item in cart_item:
                        existing_variation=item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id=id[index]
                            item=Cart_item.objects.get(id=item_id)
                            item.quantity += 1
                            item.user=user
                            item.save()
                        else:
                            cart_item=Cart_item.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
            except:
                
                pass
            auth.login(request,user)
            messages.success(request,'Login successfull')
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
               
                params=dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
                
            except:
               return redirect('dashboard')
        else:
            messages.error(request,'invalid login credentials')
    return render (request,'accounts/signin.html')
@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulation! Your account is activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')

@login_required(login_url="login")
def dashboard(request):
    order=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    order_count=order.count()
    context={
        'order_count':order_count
    }
    return render(request,'store\dashboard.html',context)

def forgotPassword(request):
    if request.method == "POST":
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__iexact=email)
            #reset password
            current_site=get_current_site(request)
            mail_subject='reset your password'
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request,'Account does not exist!')
            return redirect('forgotPassword')
    return render(request,'accounts/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None


    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')


def resetPassword(request):
    if request.method == "POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfully!')
            return redirect('login')
        else:
            messages.error(request,'Password does not match')
    else:
        return render(request,'accounts/resetPassword.html')
    
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders
    }
    return render (request,'accounts/my_orders.html',context)

def edit_profile(request):
    user_profile=get_object_or_404(UserProfile,user=request.user)
    if request.method == "POST":
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=user_profile)
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        "user_profile":user_profile
    }

    return render(request,'accounts\edit_profile.html',context)
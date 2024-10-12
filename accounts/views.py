from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from blog import views

# Create your views here.

def register(request):
     if request.method =='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:   
               # if username is first then redirect to auth/register
               if User.objects.filter(username=username).first():
                    messages.success(request,"username is taken")
                    return redirect("/auth/register")
               else:
                    messages.error(request,"username or email has already exist")

               #  if email is also  first then redirect to auth/register
               if User.objects.filter(email=email).first():
                    messages.success(request,"email is taken")
                    return redirect("/auth/register")
               else:
                    messages.error(request,"username or email has already exist")

               user_obj=User.objects.create(username=username,email=email)    
               user_obj.set_password(password)
               user_obj.save()
               # function to generate token
               auth_token=str(uuid.uuid4())

               # auth_token and user is name of the field of profime model
               profile_obj=Profile.objects.create(user=user_obj,auth_token=auth_token)
               profile_obj.save()

               # function which will send mail to email varification
               send_mail_after_registration(email,auth_token)
               return redirect('/auth/token')
        except Exception as e:
             print(e)


     return render(request,'accounts/register.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.warning(request, "username or  password is wrong")
            return redirect('/auth/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        
        if not profile_obj.is_varified:
            messages.warning(request, "Profile is not verified, check your mail")
            return redirect("/auth/login")
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.warning(request, "username or  password is wrong")
            return redirect('/auth/login')
        if user is not None:
             request.session['user_id'] = user.id
             messages.info(request,"login successfully")
             print("session created")
             auth_login(request, user)
              #then dashboard of blog app
             return redirect('/dashboard')
        else:
             messages.info(request,"invalid credentials")
    
    return render(request, 'accounts/login.html')
  
        

def success(request):
     return render(request,'accounts/success.html')

def token_send(request):
     return render(request,'accounts/token_send.html')



# when user will click on the link given by mail
def verify(request,auth_token):
     try:
          progile_obj=Profile.objects.filter(auth_token=auth_token).first()
          if progile_obj:
               # is_varified is name of model field
               # if is_Varified = False (first time)
               if progile_obj.is_varified:
                    messages.success(request,"your account has  already verified")
                    return redirect('/auth/login')
               # if is_Varified=False then make True
               progile_obj.is_varified=True
               progile_obj.save()
               messages.success(request,"your account has been verified")
               return redirect('/auth/login')
          else:
               return redirect('/auth/error')     
     except Exception as e:
          print(e)         
          return redirect('/') 

# this is a simple function to send the mail with token link
def send_mail_after_registration(email,token):
     subject = "Your accounts nees to be verified"
     message = f"Hi paste the link to varify your  account http://127.0.0.1:8000/auth/verify/{token}"
     email_from = settings.EMAIL_HOST_USER
     recipient_list = [email]
     send_mail(subject,message,email_from,recipient_list)
     

def error_page(request):
     return render(request,'accounts/error_page.html')





def logout_View(request):
     if 'user_id' in request.session:
         del request.session['user_id']
         print("session del")
         if 'username' in request.session:
            print("session deleted",request.session['username'])
         else:
              print("keys is not there")   
     logout(request)
     messages.success(request,"logged out successfully.")
     return redirect('home')




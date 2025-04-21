from django.shortcuts import render ,redirect
from .models import *
from .models import Receipe
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login , logout 
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="/login/")
def receipes(request):
    if request.method=="POST":
         data=request.POST
         receipe_image=request.FILES.get('receipe_image')
         receipe_name = data.get('receipe_name')
         receipe_description = data.get('receipe_description')

         Receipe.objects.create(
            receipe_image=receipe_image,
            receipe_name= receipe_name,
            receipe_description=receipe_description,
            )

         return redirect('/receipes/')
    
    queryset=Receipe.objects.all()
    context={'receipes':queryset}

    return render (request,'receipes.html',context)

@login_required(login_url="/login/")
def update_receipe(request,id):
      queryset=Receipe.objects.get(id=id)
      if request.method == "POST":
         data=request.POST

         receipe_image=request.FILES.get('receipe_image')
         receipe_name = data.get('receipe_name')
         receipe_description = data.get('receipe_description')

         queryset.receipe_name=receipe_name
         queryset.receipe_description=receipe_description

         if receipe_image:
              queryset.receipe_image=receipe_image
         
         queryset.save()
         
         return redirect('/receipes/')
      

      context={'receipes':queryset}
      return render (request,'update_receipes.html',context)

@login_required(login_url="/login/")
def delete_receipe(request,id):
     queryset=Receipe.objects.get(id=id)
     queryset.delete()
     return redirect('/receipes/')


def login_page(request):
     if request.method == "POST":
          username=request.POST.get('username')
          password=request.POST.get('password')
           
           #username check 
          if not User.objects.filter(username = username).exists():
               messages.error(request,'Invalid Username')
               return redirect('/login/')
          print(f"username: {username}, password: {password}")
          user = authenticate(username = username , password = password)
          print(f"user: {user}")
          if user is None:
               messages.error(request,'Invalid Password')
               return redirect('/login/')
          else:
               login(request,user) 
               return redirect('/receipes/')

     return render(request,'login.html')

def logout_page(request):
     logout(request)
     return redirect('/login/')

def  register(request):
     if request.method == "POST":
          #data ko le liya gaya gaya hai post method se
          first_name=request.POST.get('first_name')
          last_name=request.POST.get('last_name')
          username=request.POST.get('username')
          password=request.POST.get('password')

          #username duplicate na ho eske liye
          if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exists')
                return redirect('/register/')

          # ab sare data ko user model me dalenge 
          user =User.objects.create_user(
               
               username=username,
               password=password,
               first_name=first_name,
               last_name=last_name,
          )

          messages.success(request,'Acount Created succesfully')

          return redirect('/login/')
     

     return render(request,'register.html')
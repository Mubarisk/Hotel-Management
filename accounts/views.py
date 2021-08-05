from django.core.exceptions import ObjectDoesNotExist
from django.forms import forms
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from customers.models import MyUser
from customers.forms import MyUserForm,HotelForm
from django.contrib.auth.hashers import make_password
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password']:
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user:
                login(request, user)
                if user.position == 'admin':
                    return redirect('/admin/')
                elif user.position == 'customer':
                    return redirect('/')
                elif user.position == 'owner':
                    return redirect('/hotel/')

        return render(request, 'login.html')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
         form = MyUserForm(request.POST,request.FILES)
         if form.is_valid():
             form.save()
             email = form.cleaned_data.get('email')
             raw_password = form.cleaned_data.get('password1')
             user = authenticate(username=email, password=raw_password)
             login(request, user)
            
             return redirect('/')
         else:
              
              form=MyUserForm()
              return render(request,'register.html',{'form':form,'err':'err occure'})
    else:  
        
        form=MyUserForm()
        return render(request,'register.html',{'form':form})
    




def forgot(request):
    if request.method=='POST':
        try:
            verify_user=MyUser.objects.get(email=request.POST['email'])
            if verify_user.position=='customer':
                print('hy')
                return render(request,'password-form.html',{'mail':request.POST['email']})
            else:
                return render(request,'email-confirmation.html',{'err':'you are not user , contact administrator'})
        except ObjectDoesNotExist:
                return render(request,'email-confirmation.html',{'err':'no email found'})
      

    return render(request,'email-confirmation.html')

def reset(request,mail):
    verify_user=MyUser.objects.get(email=mail)
    if verify_user.position=='customer':
        if request.POST['pass1']==request.POST['pass2']:
            verify_user.set_password(request.POST['pass1'])
            verify_user.save()
            return redirect('/')
    else:
        return render(request,'email-confirmation.html',{'err':'you are not user , contact administrator'})

from django.shortcuts import render,redirect
from django.contrib.auth. models import User,auth
from django.contrib.auth import login as auth_login,authenticate
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.
@never_cache
def login(request):
    if request.session.session_key:
        if request.user.is_staff:
            return redirect('admin')
        else:
            return redirect('home')
    if request.POST:
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = user_name,password = password)
        if user:
            if user.is_superuser:
                auth_login(request,user)
                return redirect('admin')
            else:
                auth_login(request,user)
                return redirect('home')
        else:
            messages.error(request,'invalid user')
            return redirect('login')
    return render(request,'login.html')

@never_cache
def signup(request):
    if request.session.session_key:
        if request.user.is_staff:
            return redirect('admin')
        else:
            return redirect('home')
    if request.POST:
        f_name = request.POST.get('firstName')
        l_name = request.POST.get('lastName')
        user = request.POST.get('username')
        email = request.POST.get('emailAddress')
        password = request.POST.get('password')
        password2 = request.POST.get('confirmPassword')
        username_obj = User.objects.filter(username = user)
        print(user)
        if username_obj:
            messages.error(request,'user already exist')
            return redirect('signup')
        else:
            if password == password2:
                newUser = User.objects.create_user(username=user,email=email,password=password2,first_name=f_name,last_name=l_name)
                newUser.save()
                messages.success(request,'successfuly created')
                return redirect('login')
            else:
                messages.error(request,'password not match')
                return redirect('signup')
    return render(request,'signup.html')

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth. models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
@login_required(login_url='/')
def adminHome(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.POST:
        search = request.POST.get('search')
        user_obj= User.objects.filter(username = search, is_superuser= False)
        if user_obj:
            return render(request,'adminHome.html',{'user':user_obj})
        else:
            messages.error(request,'invalid user')
            return redirect('admin')
    else:
        users_obj= User.objects.filter(is_superuser=False)
        return render(request,'adminHome.html',{'user':users_obj})
    

@login_required(login_url='/')
def deleteUser(request,id):
    print(id,'clicked')
    if not request.user.is_superuser:
        return redirect('home')
    instance = User.objects.get(id=id)
    instance.delete()
    messages.success(request,'user deleted')
    return redirect('admin')

@never_cache
@login_required(login_url='/')
def editUser(request,id):
    user = get_object_or_404(User, id=id)
    if request.POST:
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        user.first_name = firstName
        user.last_name = lastName
        user.username = username
        user.email = email
        user.save()
        messages.success(request,'successfuly saved')
        return redirect('admin')
    user_details = {
        'id' : user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
    }
    context = {
        'user_details': [user_details]
    }
    return render(request,'edit.html',context)

@never_cache
@login_required(login_url='/')
def createUser(request):
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
            return redirect('createUser')
        else:
            if password == password2:
                newUser = User.objects.create_user(username=user,email=email,password=password2,first_name=f_name,last_name=l_name)
                newUser.save()
                messages.success(request,'successfuly created')
                return redirect('admin')
            else:
                messages.error(request,'password not match')
                return redirect('createUser')
    return render(request,'createUser.html')

@never_cache
@login_required(login_url='/')
def userHome(request):
    if request.session.session_key:
        if request.user.is_staff:
            return redirect('admin')
    return render(request,'userHome.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
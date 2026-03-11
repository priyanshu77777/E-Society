from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from core.models import User

def resident_signup(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(
            email=email,
            password=password,
            role=role
        )

        login(request, user)

        if role == "resident":
            return redirect('resident_dashboard')

        elif role == "society_admin":
            return redirect('society_admin_dashboard')

        else:
            return redirect('super_admin_dashboard')

    return render(request, 'auth/signup.html')

def login_view(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:

            login(request, user)

            if user.role == "resident":
                return redirect('resident_dashboard')

            elif user.role == "society_admin":
                return redirect('society_admin_dashboard')

            else:
                return redirect('super_admin_dashboard')

        else:
            return render(request,'auth/login.html',{'error':'Invalid username or password'})

    return render(request,'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
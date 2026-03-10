from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import User, Society


# ==========================
# LOGIN VIEW
# ==========================
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # Role-based redirect
            if user.role == "SUPER_ADMIN":
                return redirect("super_admin_dashboard")

            elif user.role == "SOCIETY_ADMIN":
                return redirect("society_admin_dashboard")

            elif user.role == "RESIDENT":
                return redirect("resident_dashboard")

        else:
            messages.error(request, "Invalid email or password")

    return render(request, "auth/login.html")


# ==========================
# LOGOUT VIEW
# ==========================
def logout_view(request):
    logout(request)
    return redirect("login")


# ==========================
# RESIDENT SIGNUP (Society Code Verification)
# ==========================
def resident_signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        society_code = request.POST.get("society_code")

        # Verify society code
        try:
            society = Society.objects.get(society_code=society_code)
        except Society.DoesNotExist:
            messages.error(request, "Invalid Society Code")
            return redirect("resident_signup")

        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            role="RESIDENT",
            society=society
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "auth/signup.html")
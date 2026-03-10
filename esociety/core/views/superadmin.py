from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Society
from django.contrib.auth import get_user_model
from functools import wraps

User = get_user_model()


# 🔐 Superadmin access check decorator
def super_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.role != "SUPER_ADMIN":
            return redirect("login")  # safer redirect

        return view_func(request, *args, **kwargs)
    return wrapper


# 📊 Dashboard
@login_required
@super_admin_required
def super_admin_dashboard(request):
    total_societies = Society.objects.count()
    total_admins = User.objects.filter(role="SOCIETY_ADMIN").count()

    context = {
        "total_societies": total_societies,
        "total_admins": total_admins,
    }
    return render(request, "superadmin/dashboard.html", context)


# 📋 Society List
@login_required
@super_admin_required
def society_list(request):
    societies = Society.objects.all()
    return render(request, "superadmin/society_list.html", {"societies": societies})


# ➕ Add Society
@login_required
@super_admin_required
def add_society(request):
    if request.method == "POST":
        name = request.POST.get("name")
        city = request.POST.get("city")
        address = request.POST.get("address")

        Society.objects.create(
            name=name,
            city=city,
            address=address
        )

        messages.success(request, "Society added successfully")
        return redirect("society_list")

    return render(request, "superadmin/add_society.html")


# ✏ Edit Society
@login_required
@super_admin_required
def edit_society(request, pk):
    society = get_object_or_404(Society, pk=pk)

    if request.method == "POST":
        society.name = request.POST.get("name")
        society.city = request.POST.get("city")
        society.address = request.POST.get("address")
        society.save()

        messages.success(request, "Society updated successfully")
        return redirect("society_list")

    return render(request, "superadmin/edit_society.html", {"society": society})


# ❌ Delete Society
@login_required
@super_admin_required
def delete_society(request, pk):
    society = get_object_or_404(Society, pk=pk)
    society.delete()
    messages.success(request, "Society deleted successfully")
    return redirect("society_list")


# 🔎 Society Detail
@login_required
@super_admin_required
def society_detail(request, pk):
    society = get_object_or_404(Society, pk=pk)
    return render(request, "superadmin/society_detail.html", {"society": society})
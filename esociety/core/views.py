from django.shortcuts import render, redirect, get_object_or_404
from .models import Member,Complaint,Society,Flat,Maintenance,Notice
from .forms import ComplaintForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


# SIGNUP
def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if Member.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        Member.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=make_password(password),
            role=role
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "core/signup.html")


# LOGIN
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            member = Member.objects.get(email=email)

            if check_password(password, member.password):
                request.session["member_id"] = member.id
                request.session["member_name"] = member.name
                request.session["role"] = member.role

                return redirect("dashboard")

            else:
                messages.error(request, "Invalid password")

        except Member.DoesNotExist:
            messages.error(request, "Email not found")

    return render(request, "core/login.html")


# DASHBOARD (temporary)
def dashboard(request):
    if not request.session.get("member_id"):
        return redirect("login")

    context={
        "total_members":Member.objects.count(),
        "total_complaints":Complaint.objects.count(),
        "pending_maintenance":Maintenance.objects.filter(status=False).count(),
        "total_notices":Notice.objects.count(),
    }
    return render(request,"core/dashboard.html",context)

def society_list(request):
    return render(request,"core/society_list.html")

def member_list(request):
    return render(request,"core/member_list.html")

def flat_list(request):
    return render(request,"core/flat_list.html")

def maintenance_list(request):
    return render(request,"core/maintenance_list.html")

def complaint_list(request):
    return render(request,"core/complaint_list.html")

def notice_list(request):
    return render(request,"core/notice_list.html")

def logout(request):
    request.session.flush()
    return redirect("login")

# LIST
def complaint_list(request):
    if not request.session.get("member_id"):
        return redirect("login")

    complaints = Complaint.objects.filter(member_id=request.session["member_id"])
    return render(request,"core/complaint_list.html",{"complaints":complaints})


# CREATE
def complaint_create(request):
    form = ComplaintForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.member_id = request.session["member_id"]
        obj.save()
        return redirect("complaint_list")

    return render(request,"core/complaint_form.html",{"form":form})


# DELETE
def complaint_delete(request,id):
    Complaint.objects.get(id=id).delete()
    return redirect("complaint_list")

def is_admin(request):
    return request.session.get("role") == "Admin"

def society_list(request):
    societies = Society.objects.all()
    return render(request,"core/society_list.html",{"societies":societies})

def society_create(request):
    if request.method=="POST":
        Society.objects.create(
            society_name=request.POST.get("name"),
            address=request.POST.get("address")
        )
        return redirect("society_list")

    return render(request,"core/society_form.html")

def flat_list(request):
    flats = Flat.objects.select_related("society")
    return render(request,"core/flat_list.html",{"flats":flats})

def maintenance_list(request):
    data = Maintenance.objects.select_related("flat")
    return render(request,"core/maintenance_list.html",{"data":data})

def maintenance_mark_paid(request,id):
    obj = Maintenance.objects.get(id=id)
    obj.status=True
    obj.save()
    return redirect("maintenance_list")

def notice_list(request):
    notices = Notice.objects.all()
    return render(request,"core/notice_list.html",{"notices":notices})

def notice_create(request):
    if request.method=="POST":
        Notice.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            publish_date=request.POST.get("date")
        )
        return redirect("notice_list")

    return render(request,"core/notice_form.html")

def complaint_update_status(request,id):
    obj = Complaint.objects.get(id=id)
    obj.status="Resolved"
    obj.save()
    return redirect("complaint_list")

def maintenance_mark_paid(request,id):
    obj = Maintenance.objects.get(id=id)
    obj.status=True
    obj.save()
    return redirect("maintenance_list")
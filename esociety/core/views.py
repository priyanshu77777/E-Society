from email.mime import image
from time import timezone
from turtle import title
from urllib import request
from unicodedata import category

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from httpx import request
from django.contrib.auth.decorators import login_required
from .models import Complaint, Flat, Notice, Payment, Society, Maintenance
import json
from openai import OpenAI           
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.http import JsonResponse
from .models import Payment

User = get_user_model()

# =========================
# SIGNUP
# =========================
def signup_view(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        society_id = request.POST.get("society_id")  # ✅ NEW

        # FORCE ROLE
        if role == "admin":
            role = "SOCIETY_ADMIN"
        elif role == "super_admin":
            role = "SUPER_ADMIN"
        else:
            role = "RESIDENT"

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        # ✅ CREATE USER
        user = User.objects.create_user(
            email=email,
            password=password,
            role=role
        )

        # ✅ ASSIGN SOCIETY ONLY IF RESIDENT
        if role == "RESIDENT" and society_id:
            user.society_id = society_id
            user.save()

        return redirect("login")

    # ✅ SEND societies to HTML
    societies = Society.objects.all()

    return render(request, "auth/signup.html", {
        "societies": societies
    })

# =========================
# LOGIN
# =========================
def login_view(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            print("USER ROLE:", user.role)  # DEBUG

            if user.role == "SUPER_ADMIN":
                return redirect("super_admin_dashboard")
            elif user.role == "SOCIETY_ADMIN":
                return redirect("admin_dashboard")
            else:
                return redirect("resident_dashboard")

        else:
            messages.error(request, "Invalid credentials")

    return render(request, "auth/login.html")

# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect("home")

# =========================
# RESIDENT DASHBOARD
# =========================
@login_required
def resident_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)

    pending_count = complaints.filter(status="Pending").count()
    resolved_count = complaints.filter(status="Resolved").count()

    notices = Notice.objects.filter(
        society=request.user.society   # ✅ ONLY THEIR SOCIETY
    ).order_by('-created_at')

    context = {
        'complaints': complaints,
        'pending_count': pending_count,
        'resolved_count': resolved_count,
        'total_count': complaints.count(),
        'notices': notices
    }

    return render(request, 'resident/dashboard.html', {
        'complaints': complaints,
        'notices': notices
    })

# =========================
# ADMIN DASHBOARD
# =========================
@login_required
def admin_dashboard(request):

    print("ADMIN DASHBOARD OPENED")  # DEBUG

    if request.user.role != "SOCIETY_ADMIN":
        return redirect("resident_dashboard")

    status = request.GET.get("status")

    if status:
        complaints = Complaint.objects.filter(status=status)
    else:
        complaints = Complaint.objects.all()

    total = complaints.count()
    pending = complaints.filter(status="Pending").count()
    resolved = complaints.filter(status="Resolved").count()

    notices = Notice.objects.all()

    return render(request, "admin/dashboard.html", {
        "complaints": complaints,
        "notices": notices,
        "total": total,
        "pending": pending,
        "resolved": resolved
    })

@login_required
def update_status(request, complaint_id):

    complaint = Complaint.objects.get(id=complaint_id)

    complaint.status = "Resolved"
    complaint.save()

    return redirect("admin_dashboard")


# =========================
# CREATE COMPLAINT
# =========================
@login_required
def add_complaint(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        image = request.FILES.get("image", None)

        Complaint.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            image=image  # this will work even if no file uploaded
)

        return redirect("resident_dashboard")

    return render(request, "resident/add_complaint.html")


# 🤖 REAL AI IMPROVE
@csrf_exempt
def improve_complaint(request):
    if request.method == "POST":
        text = request.POST.get("text", "").lower()

        complaints = [
            (["water", "leak", "pipeline"], 
             "There is a water leakage/supply issue in my flat which needs immediate attention."),

            (["electric", "power", "light"], 
             "Frequent power cuts and electrical issues are affecting daily activities."),

            (["lift", "elevator"], 
             "The lift is not functioning properly and requires urgent maintenance."),

            (["security", "guard", "unsafe"], 
             "There is a security concern regarding unauthorized access in the society."),

            (["clean", "garbage", "dirty"], 
             "The cleanliness of common areas is not being maintained properly."),

            (["parking", "vehicle"], 
             "There is an issue regarding parking space management causing inconvenience."),

            (["noise", "loud"], 
             "There is excessive noise disturbance affecting peaceful living."),

            (["internet", "wifi"], 
             "Internet connectivity in the society is unstable and needs improvement."),

            (["drainage", "sewage"], 
             "There is a drainage/sewage blockage issue that requires urgent attention."),

            (["maintenance", "repair"], 
             "General maintenance work is pending and needs to be addressed."),

            (["dog", "animal"], 
             "There is an issue related to stray animals causing disturbance in the society."),

            (["lighting", "dark"], 
             "Street lights/common area lights are not working properly.")
        ]

        result = "There is an issue that needs attention. Kindly resolve it as soon as possible."

        for keywords, response in complaints:
            if any(word in text for word in keywords):
                result = response
                break

        return JsonResponse({"result": result}) 


# =========================
# ADD NOTICE (ADMIN)
# =========================
def add_notice(request):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")

        Notice.objects.create(
            title=title,
            message=message,
            society=request.user.society   # 🔥 IMPORTANT
        )

        return redirect("admin_dashboard")

    return render(request, "add_notice.html")


@login_required
def profile(request):
    return render(request, "resident/profile.html", {
        "user": request.user
    })

# =========================
# FLAT
# =========================
@login_required
def create_flat(request):
    if request.user.role != "SOCIETY_ADMIN":
        return redirect("resident_dashboard")

    if request.method == "POST":
        flat_number = request.POST.get("flat_number")
        block_name = request.POST.get("block_name")

        Flat.objects.create(
            flat_number=flat_number,   # ✅ correct field
            block_name=block_name,     # ✅ required field
            society=request.user.society,
            status="VACANT"
        )

        return redirect("create_flat")

    flats = Flat.objects.filter(society=request.user.society)

    return render(request, "admin/create_flat.html", {
        "flats": flats
    })

@login_required
def assign_flat(request):

    if request.user.role != "SOCIETY_ADMIN":
        return redirect("resident_dashboard")

    users = User.objects.filter(
        role="RESIDENT",
        society=request.user.society
    )

    flats = Flat.objects.filter(
        society=request.user.society,
        status="VACANT"
    )

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        flat_id = request.POST.get("flat_id")

        user = User.objects.get(id=user_id)
        flat = Flat.objects.get(id=flat_id)

        # ✅ ASSIGN
        flat.resident = user
        flat.status = "OCCUPIED"
        flat.save()

        return redirect("assign_flat")

    return render(request, "admin/assign_flat.html", {
        "users": users,
        "flats": flats
    })

# =========================
# PAYMENTS PAGE
# =========================
@login_required
def payments(request):
    # get user's flat payments
    payments = Payment.objects.filter(flat__resident=request.user)

    return render(request, "resident/payment.html", {
        "payments": payments
    })


# =========================
# CREATE RAZORPAY ORDER
# =========================
@login_required
def create_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id, flat__resident=request.user)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    amount = int(payment.maintenance.amount * 100)  # convert ₹ to paise

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    # save order id
    payment.razorpay_order_id = order['id']
    payment.save()

    return JsonResponse({
        "order_id": order['id'],
        "key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "payment_id": payment.id
    })


# =========================
# VERIFY PAYMENT
# =========================
@csrf_exempt
def verify_payment(request):
    data = json.loads(request.body)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        })

        payment = Payment.objects.get(razorpay_order_id=data['razorpay_order_id'])

        payment.razorpay_payment_id = data['razorpay_payment_id']
        payment.razorpay_signature = data['razorpay_signature']
        payment.status = "PAID"
        payment.payment_mode = "Razorpay"
        payment.paid_date = timezone.now()
        payment.save()

        return JsonResponse({"status": "success"})

    except Exception as e:
        return JsonResponse({"status": "failed"})
    
# =========================
# MANAGE PAYMENTS (ADMIN)
# =========================
@login_required
def manage_payments(request):

    if request.user.role != "SOCIETY_ADMIN":
        return redirect("resident_dashboard")

    payments = Payment.objects.filter(
        flat__society=request.user.society
    ).select_related("flat", "maintenance")

    return render(request, "admin/manage_payments.html", {
        "payments": payments
    })

# =========================
# Create Maintenance
# =========================
@login_required
def create_maintenance(request):

    if request.user.role != "SOCIETY_ADMIN":
        return redirect("resident_dashboard")

    if request.method == "POST":
        month = request.POST.get("month")
        amount = request.POST.get("amount")
        due_date = request.POST.get("due_date")

        maintenance = Maintenance.objects.create(
            society=request.user.society,
            month=month,
            amount=amount,
            due_date=due_date
        )

        # ✅ CREATE PAYMENTS FOR ALL FLATS
        flats = Flat.objects.filter(society=request.user.society)

        for flat in flats:
            Payment.objects.create(
                maintenance=maintenance,
                flat=flat
            )

        return redirect("manage_payments")

    return render(request, "admin/create_maintenance.html")
    
def home(request):
    resident_count = User.objects.filter(role="RESIDENT").count()
    complaint_count = Complaint.objects.count()
    society_count = Society.objects.count()

    context = {
        'resident_count': resident_count,
        'complaint_count': complaint_count,
        'society_count': society_count
    }

    return render(request, 'home.html', context)

def ai_improve(request):
    data = json.loads(request.body)
    text = data.get("text")

    # ✅ REMOVE repeated prefix
    clean_text = text.replace("Detailed Complaint:", "").strip()

    improved = "Detailed Complaint: " + clean_text

    # Category + AI logic
    if "water" in clean_text.lower():
        category = "Plumbing"
        solution = "Check pipeline or contact plumber"
        priority = "High"
    elif "light" in clean_text.lower():
        category = "Electrical"
        solution = "Check wiring or switchboard"
        priority = "Medium"
    else:
        category = "General"
        solution = "Maintenance team will inspect"
        priority = "Low"

    return JsonResponse({
        "improved": improved,
        "category": category,
        "priority": priority,
        "solution": solution
    })

def ai_assistant(request):
    data = json.loads(request.body)
    msg = data.get("message").lower()

    if "complaint" in msg:
        reply = "Go to Add Complaint section to raise an issue."
    elif "payment" in msg:
        reply = "Check your payments section for due or paid bills."
    elif "status" in msg:
        reply = "You can track complaint status in dashboard."
    else:
        reply = "I am here to help with society services!"

    return JsonResponse({"reply": reply})

# =========================
# SUPER ADMIN DASHBOARD
# =========================
@login_required
def super_admin_dashboard(request):
    if request.user.role != "SUPER_ADMIN":
        return redirect("home")

    total_societies = Society.objects.count()
    total_users = User.objects.count()
    total_admins = User.objects.filter(role="SOCIETY_ADMIN").count()
    recent_societies = Society.objects.order_by('-id')[:5]
    recent_admins = User.objects.filter(role="SOCIETY_ADMIN").order_by('-id')[:5]

    return render(request, "super_admin/dashboard.html", {
        "total_societies": total_societies,
        "total_users": total_users,
        "total_admins": total_admins,
        "recent_societies": recent_societies,
        "recent_admins": recent_admins,
    })


# =========================
# CREATE SOCIETY PAGE (SUPER ADMIN)
# =========================
@login_required
def create_society(request):

    if request.user.role != "SUPER_ADMIN":
        return redirect("home")

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        city = request.POST.get("city")

        if name:
            Society.objects.create(
                name=name,
                address=address,
                city=city
            )

        return redirect("super_admin_dashboard")

    # 👇 THIS LINE IS IMPORTANT
    return render(request, "super_admin/create_society.html")


# =========================
# CREATE ADMIN PAGE (SUPER ADMIN)
# =========================
@login_required
def create_admin(request):
    if request.user.role != "SUPER_ADMIN":
        return redirect("home")

    societies = Society.objects.all()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        society_id = request.POST.get("society")

        if email and password and society_id:
            society = Society.objects.get(id=society_id)

            User.objects.create_user(
                email=email,
                password=password,
                role="SOCIETY_ADMIN",
                society=society
            )

        return redirect("admin_list")

    return render(request, "super_admin/create_admin.html", {
        "societies": societies
    })


# =========================
# SOCIETY LIST (SUPER ADMIN)
# =========================
@login_required
def society_list(request):
    if request.user.role != "SUPER_ADMIN":
        return redirect("home")

    societies = Society.objects.all()

    return render(request, "super_admin/society_list.html", {
        "societies": societies
    })


# =========================
# ADMIN LIST (SUPER ADMIN)
# =========================
@login_required
def admin_list(request):
    if request.user.role != "SUPER_ADMIN":
        return redirect("home")

    admins = User.objects.filter(role="SOCIETY_ADMIN")

    return render(request, "super_admin/admin_list.html", {
        "admins": admins,
        "societies": Society.objects.all()
    })


# =========================
# DELETE SOCIETY (SUPER ADMIN)
# =========================
@login_required
def delete_society(request, id):
    if request.user.role != "SUPER_ADMIN":
        return redirect("home")

    Society.objects.get(id=id).delete()
    return redirect("society_list")

# =========================
# EDIT ADMIN (SUPER ADMIN)
# =========================
@login_required
def edit_admin(request, id):

    if request.user.role != "SUPER_ADMIN":
        return redirect("home")

    admin = User.objects.get(id=id)
    societies = Society.objects.all()

    if request.method == "POST":
        society_id = request.POST.get("society")

        admin.society_id = society_id
        admin.save()

        return redirect("view_admins")

    return render(request, "super_admin/edit_admin.html", {
        "admin": admin,
        "societies": societies
    })
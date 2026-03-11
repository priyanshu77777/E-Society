from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from core.decorators import resident_required, society_admin_required
from core.models import Complaint, Flat


# =====================================================
# 👤 RESIDENT SIDE
# =====================================================

@login_required
@resident_required
def complaint_create(request):

    # Get resident's flat
    flat = Flat.objects.filter(resident=request.user).first()

    if not flat:
        return redirect("resident_dashboard")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Complaint.objects.create(
            title=title,
            description=description,
            society=request.user.society,
            flat=flat
        )

        return redirect("my_complaints")

    return render(request, "complaints/create.html")


@login_required
@resident_required
def my_complaints(request):

    flat = Flat.objects.filter(resident=request.user).first()

    complaints = Complaint.objects.filter(
        flat=flat
    ).order_by("-created_at")

    paginator = Paginator(complaints, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "complaints/my_complaints.html", {
        "page_obj": page_obj
    })


# =====================================================
# 🏢 SOCIETY ADMIN SIDE
# =====================================================

@login_required
@society_admin_required
def complaint_list(request):

    complaints = Complaint.objects.filter(
        society=request.user.society
    ).order_by("-created_at")

    # 🔍 Search
    search_query = request.GET.get("search")
    if search_query:
        complaints = complaints.filter(
            Q(title__icontains=search_query)
        )

    # 📌 Status filter
    status_filter = request.GET.get("status")
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    paginator = Paginator(complaints, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "complaints/list.html", {
        "page_obj": page_obj
    })


@login_required
@society_admin_required
def complaint_update(request, complaint_id):

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        society=request.user.society
    )

    if request.method == "POST":
        complaint.status = request.POST.get("status")
        complaint.admin_remarks = request.POST.get("admin_remarks")
        complaint.assigned_to = request.POST.get("assigned_to")
        complaint.save()

        return redirect("complaint_list")

    return render(request, "complaints/update.html", {
        "complaint": complaint
    })
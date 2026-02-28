from django.shortcuts import render, redirect
from core.models import Complaint
from core.decorators import role_required


@role_required(["RESIDENT"])
def add_complaint(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Complaint.objects.create(
            user=request.user,
            title=title,
            description=description
        )

        return redirect("resident_dashboard")

    return render(request, "complaints/add_complaint.html")


@role_required(["SOCIETY_ADMIN"])
def complaint_list(request):
    complaints = Complaint.objects.filter(
        user__society=request.user.society
    )
    return render(request, "complaints/complaint_list.html", {"complaints": complaints})
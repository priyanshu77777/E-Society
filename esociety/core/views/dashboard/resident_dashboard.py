from django.shortcuts import render
from django.utils import timezone
from core.models import Maintenance, Complaint, Notice, Member
from core.decorators import resident_required
from django.contrib.auth.decorators import login_required


@login_required
@resident_required
def resident_dashboard(request):

    society = request.user.society

    # Get primary member linked to user (if needed later)
    member = Member.objects.filter(
        society=society,
        phone__isnull=False
    ).first()

    pending_maintenance = Maintenance.objects.filter(
        society=society,
        status="PENDING"
    ).count()

    my_complaints = Complaint.objects.filter(
        society=society
    ).order_by("-created_at")[:5]

    today = timezone.now().date()

    active_notices = Notice.objects.filter(
        society=society,
        expiry_date__gte=today
    ).order_by("-created_at")[:5]

    context = {
        "pending_maintenance": pending_maintenance,
        "my_complaints": my_complaints,
        "active_notices": active_notices,
    }

    return render(request, "dashboard/resident_dashboard.html", context)
from django.shortcuts import render
from django.utils import timezone
from core.models import Flat, Member, Complaint, Maintenance, Notice
from core.decorators import society_admin_required
from django.contrib.auth.decorators import login_required


@login_required
@society_admin_required
def society_admin_dashboard(request):

    society = request.user.society

    total_flats = Flat.objects.filter(society=society).count()
    total_members = Member.objects.filter(society=society).count()

    pending_complaints = Complaint.objects.filter(
        society=society,
        status="PENDING"
    ).count()

    maintenance_due = Maintenance.objects.filter(
        society=society,
        status="PENDING"
    ).count()

    today = timezone.now().date()

    recent_notices = Notice.objects.filter(
        society=society,
        expiry_date__gte=today
    ).order_by("-created_at")[:5]

    context = {
        "total_flats": total_flats,
        "total_members": total_members,
        "pending_complaints": pending_complaints,
        "maintenance_due": maintenance_due,
        "recent_notices": recent_notices,
    }

    return render(request, "dashboard/society_admin_dashboard.html", context)
from django.shortcuts import render
from django.contrib.auth import get_user_model
from core.models import Society, Flat, Member
from core.decorators import superadmin_required
from django.contrib.auth.decorators import login_required

User = get_user_model()


@login_required
@superadmin_required
def super_admin_dashboard(request):

    total_societies = Society.objects.count()
    total_admins = User.objects.filter(role="SOCIETY_ADMIN").count()
    total_residents = User.objects.filter(role="RESIDENT").count()
    total_flats = Flat.objects.count()
    total_members = Member.objects.count()

    context = {
        "total_societies": total_societies,
        "total_admins": total_admins,
        "total_residents": total_residents,
        "total_flats": total_flats,
        "total_members": total_members,
    }

    return render(request, "dashboard/super_admin_dashboard.html", context)
from django.shortcuts import render, redirect
from core.models import Maintenance
from core.decorators import role_required


@role_required(["SOCIETY_ADMIN"])
def maintenance_list(request):
    records = Maintenance.objects.filter(
        society=request.user.society
    )
    return render(request, "maintenance/list.html", {"records": records})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Maintenance
from core.forms import MaintenanceForm


@login_required
def maintenance_list(request):
    society = request.user.society
    maintenance = Maintenance.objects.filter(society=society)

    return render(request, "maintenance/list.html", {
        "maintenance": maintenance
    })


@login_required
def maintenance_create(request):
    society = request.user.society

    if request.method == "POST":
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.society = society
            bill.status = "Pending"
            bill.save()
            return redirect("maintenance_list")
    else:
        form = MaintenanceForm()

    return render(request, "maintenance/create.html", {"form": form})


@login_required
def mark_paid(request, pk):
    society = request.user.society
    bill = get_object_or_404(Maintenance, pk=pk, society=society)

    bill.status = "Paid"
    bill.save()

    return redirect("maintenance_list")
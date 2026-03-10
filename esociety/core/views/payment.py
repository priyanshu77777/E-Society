from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Payment
from core.forms import MaintenanceForm


@login_required
def payment_list(request):
    society = request.user.society
    payments = Payment.objects.filter(society=society)

    return render(request, "payment/list.html", {
        "payments": payments
    })


@login_required
def payment_history(request):
    society = request.user.society
    payments = Payment.objects.filter(
        society=society,
        status="Paid"
    ).order_by("-paid_at")

    return render(request, "payment/history.html", {
        "payments": payments
    })


@login_required
def mark_payment_paid(request, pk):
    society = request.user.society
    payment = get_object_or_404(Payment, pk=pk, society=society)

    payment.status = "Paid"
    payment.save()

    return redirect("payment_list")
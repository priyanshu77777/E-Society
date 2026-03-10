from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Society
from core.forms import SocietyForm


@login_required
def society_detail(request):
    society = request.user.society
    return render(request, "society/detail.html", {"society": society})


@login_required
def society_edit(request):
    society = request.user.society

    if request.method == "POST":
        form = SocietyForm(request.POST, instance=society)
        if form.is_valid():
            form.save()
            return redirect("society_detail")
    else:
        form = SocietyForm(instance=society)

    return render(request, "society/edit.html", {"form": form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Flat, Member
from core.forms import FlatForm


@login_required
def flat_list(request):
    society = request.user.society
    flats = Flat.objects.filter(society=society)

    return render(request, "flats/list.html", {"flats": flats})


@login_required
def flat_create(request):
    society = request.user.society

    if request.method == "POST":
        form = FlatForm(request.POST)
        if form.is_valid():
            flat = form.save(commit=False)
            flat.society = society
            flat.save()
            return redirect("flat_list")
    else:
        form = FlatForm()

    return render(request, "flats/create.html", {"form": form})


@login_required
def flat_update(request, pk):
    society = request.user.society
    flat = get_object_or_404(Flat, pk=pk, society=society)

    if request.method == "POST":
        form = FlatForm(request.POST, instance=flat)
        if form.is_valid():
            form.save()
            return redirect("flat_list")
    else:
        form = FlatForm(instance=flat)

    return render(request, "flats/update.html", {"form": form})


@login_required
def assign_member(request, pk):
    society = request.user.society
    flat = get_object_or_404(Flat, pk=pk, society=society)

    members = Member.objects.filter(society=society)

    if request.method == "POST":
        member_id = request.POST.get("member")
        member = Member.objects.get(id=member_id)
        flat.member = member
        flat.status = "Occupied"
        flat.save()
        return redirect("flat_list")

    return render(request, "flats/assign.html", {
        "flat": flat,
        "members": members
    })
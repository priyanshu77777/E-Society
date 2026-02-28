from django.shortcuts import render, redirect
from core.models import Flat
from core.decorators import role_required


@role_required(["SOCIETY_ADMIN"])
def flat_list(request):
    flats = Flat.objects.filter(society=request.user.society)
    return render(request, "flats/flat_list.html", {"flats": flats})


@role_required(["SOCIETY_ADMIN"])
def add_flat(request):
    if request.method == "POST":
        number = request.POST.get("number")

        Flat.objects.create(
            number=number,
            society=request.user.society
        )

        return redirect("flat_list")

    return render(request, "flats/add_flat.html")
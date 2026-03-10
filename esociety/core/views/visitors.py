from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Visitor
from core.forms import VisitorForm


@login_required
def visitor_list(request):
    society = request.user.society
    visitors = Visitor.objects.filter(society=society).order_by("-visit_date")

    return render(request, "visitors/list.html", {
        "visitors": visitors
    })


@login_required
def visitor_create(request):
    society = request.user.society

    if request.method == "POST":
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.society = society
            visitor.save()
            return redirect("visitor_list")
    else:
        form = VisitorForm()

    return render(request, "visitors/create.html", {
        "form": form
    })


@login_required
def visitor_delete(request, pk):
    society = request.user.society
    visitor = get_object_or_404(Visitor, pk=pk, society=society)

    visitor.delete()
    return redirect("visitor_list")
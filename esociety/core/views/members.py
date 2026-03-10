from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from core.models import Member
from core.forms import MemberForm


@login_required
def member_list(request):
    society = request.user.society
    query = request.GET.get("q")

    members = Member.objects.filter(society=society)

    if query:
        members = members.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    context = {
        "members": members,
        "query": query
    }
    return render(request, "members/list.html", context)


@login_required
def member_create(request):
    society = request.user.society

    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.society = society
            member.save()
            return redirect("member_list")
    else:
        form = MemberForm()

    return render(request, "members/create.html", {"form": form})


@login_required
def member_update(request, pk):
    society = request.user.society
    member = get_object_or_404(Member, pk=pk, society=society)

    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect("member_list")
    else:
        form = MemberForm(instance=member)

    return render(request, "members/update.html", {"form": form})


@login_required
def member_delete(request, pk):
    society = request.user.society
    member = get_object_or_404(Member, pk=pk, society=society)

    if request.method == "POST":
        member.delete()
        return redirect("member_list")

    return render(request, "members/delete.html", {"member": member})
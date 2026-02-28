from django.shortcuts import render, redirect
from core.models import Notice
from core.decorators import role_required


@role_required(["SOCIETY_ADMIN"])
def add_notice(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        Notice.objects.create(
            society=request.user.society,
            title=title,
            content=content
        )

        return redirect("society_admin_dashboard")

    return render(request, "notices/add_notice.html")


@role_required(["RESIDENT"])
def notice_list(request):
    notices = Notice.objects.filter(
        society=request.user.society
    )
    return render(request, "notices/list.html", {"notices": notices})
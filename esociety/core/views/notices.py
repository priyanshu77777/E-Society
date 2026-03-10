from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Notice
from core.forms import NoticeForm


@login_required
def notice_list(request):
    society = request.user.society
    notices = Notice.objects.filter(society=society).order_by("-created_at")

    return render(request, "notices/list.html", {"notices": notices})


@login_required
def notice_create(request):
    society = request.user.society

    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.society = society
            notice.save()
            return redirect("notice_list")
    else:
        form = NoticeForm()

    return render(request, "notices/create.html", {"form": form})


@login_required
def notice_delete(request, pk):
    society = request.user.society
    notice = get_object_or_404(Notice, pk=pk, society=society)

    notice.delete()
    return redirect("notice_list")
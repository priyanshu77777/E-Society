from django.shortcuts import render
from core.models import User
from core.decorators import role_required


@role_required(["SOCIETY_ADMIN"])
def member_list(request):
    members = User.objects.filter(
        society=request.user.society,
        role="RESIDENT"
    )
    return render(request, "members/member_list.html", {"members": members})
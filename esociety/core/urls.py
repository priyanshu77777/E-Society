from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("society/",views.society_list,name="society_list"),
    path("members/",views.member_list,name="member_list"),
    path("flats/",views.flat_list,name="flat_list"),
    path("maintenance/",views.maintenance_list,name="maintenance_list"),
    path("complaints/",views.complaint_list,name="complaint_list"),
    path("notices/",views.notice_list,name="notice_list"),
    path("logout/",views.logout,name="logout"),
    path("complaints/add/",views.complaint_create,name="complaint_create"),
    path("complaints/delete/<int:id>/",views.complaint_delete,name="complaint_delete"),
    path("complaints/resolve/<int:id>/",views.complaint_update_status,name="complaint_resolve"),
]
from django.urls import path

# DASHBOARD
from .views.superadmin import super_admin_dashboard
from .views.society import society_admin_dashboard
from .views.members import resident_dashboard

# MODULES
from .views.members import *
from .views.flats import *
from .views.complaints import *
from .views.maintenance import *
from .views.notices import *
from .views.visitors import *
from .views.payment import *
from .views.society import society_detail, society_edit
from .views.auth import login_view, logout_view, resident_signup
urlpatterns = [

    # AUTH
    path('signup/', resident_signup, name='resident_signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # DASHBOARD
    path('resident/dashboard/', resident_dashboard, name='resident_dashboard'),
    path('society-admin/dashboard/', society_admin_dashboard, name='society_admin_dashboard'),
    path('super-admin/dashboard/', super_admin_dashboard, name='super_admin_dashboard'),

    # FLATS
    path('flats/', flat_list, name='flat_list'),
    path('flats/create/', flat_create, name='flat_create'),
    path('flats/update/<int:id>/', flat_update, name='flat_update'),

    # MEMBERS
    path('members/', member_list, name='member_list'),
    path('members/create/', member_create, name='member_create'),
    path('members/update/<int:id>/', member_update, name='member_update'),

    # COMPLAINTS
    path('complaints/', complaint_list, name='complaint_list'),
    path('complaints/create/', complaint_create, name='complaint_create'),
    path('complaints/update/<int:id>/', complaint_update, name='complaint_update'),
    path('complaints/my/', my_complaints, name='my_complaints'),

    # MAINTENANCE
    path('maintenance/', maintenance_list, name='maintenance_list'),
    path('maintenance/create/', maintenance_create, name='maintenance_create'),
    path('maintenance/list/', maintenance_list, name='maintenance_list'),

    # NOTICES
    path('notices/', notice_list, name='notice_list'),
    path('notices/create/', notice_create, name='notice_create'),
    path('notices/delete/<int:id>/', notice_delete, name='notice_delete'),

    # VISITORS
    path('visitors/', visitor_list, name='visitor_list'),
    path('visitors/create/', visitor_create, name='visitor_create'),

    # PAYMENTS
    path('payments/', payment_list, name='payment_list'),
    path('payments/history/', payment_history, name='payment_history'),

    # SOCIETY
    path('society/detail/', society_detail, name='society_detail'),
    path('society/edit/', society_edit, name='society_edit'),

]
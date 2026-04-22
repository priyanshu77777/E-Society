from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),

    # Auth
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    # Dashboards
    path('resident/dashboard/', views.resident_dashboard, name="resident_dashboard"),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # Complaints
    path('complaint/create/', views.add_complaint, name="add_complaint"),
    path('complaint/resolve/<int:complaint_id>/', views.update_status, name='update_status'),

    # Admin Features
    path("create-flat/", views.create_flat, name="create_flat"),
    path("assign-flat/", views.assign_flat, name="assign_flat"),
    path('add-notice/', views.add_notice, name='add_notice'),
    path('manage-payments/', views.manage_payments, name='manage_payments'),

    # Payments
    path('payments/', views.payments, name='payments'),
    path('create-maintenance/', views.create_maintenance, name='create_maintenance'),
    path('create-payment/<int:payment_id>/', views.create_payment, name='create_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),

    # AI
    path('ai-improve/', views.ai_improve, name='ai_improve'),
    path('improve-ai/', views.improve_complaint, name='improve_ai'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # SUPER ADMIN
    path("super-admin/", views.super_admin_dashboard, name="super_admin_dashboard"),
    path("create-society/", views.create_society, name="create_society"),
    path("create-admin/", views.create_admin, name="create_admin"),
    path("societies/", views.society_list, name="society_list"),
    path("admins/", views.admin_list, name="admin_list"),
    path("delete-society/<int:id>/", views.delete_society, name="delete_society"),
    path("edit-admin/<int:id>/", views.edit_admin, name="edit_admin"),

]
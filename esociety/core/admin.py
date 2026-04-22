from django.contrib import admin
from .models import User, Society, Flat, Member, Maintenance, Payment, Complaint, Notice, Visitor

admin.site.register(User)
admin.site.register(Society)
admin.site.register(Flat)
admin.site.register(Member)
admin.site.register(Maintenance)
admin.site.register(Payment)
admin.site.register(Complaint)
admin.site.register(Notice)
admin.site.register(Visitor)
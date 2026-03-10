from django import forms
from core.models import (Member,Flat,Complaint,Maintenance,Notice,Society,Visitor,Payment)
from django.contrib.auth.models import User


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ["society"]


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        exclude = ["society"]


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ["society", "created_by"]


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        exclude = ["society"]


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        exclude = ["society"]


class SocietyForm(forms.ModelForm):
    class Meta:
        model = Society
        fields = "__all__"

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        exclude = ["society"]

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ["society"]


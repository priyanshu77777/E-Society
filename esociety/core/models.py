from django.db import models


class Society(models.Model):
    society_name = models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Member(models.Model):
    ROLE_CHOICES = (
        ('Admin','Admin'),
        ('Resident','Resident'),
    )

    society = models.ForeignKey(Society, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Flat(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    flat_number = models.CharField(max_length=10)
    block_name = models.CharField(max_length=50)


class Maintenance(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    due_date = models.DateField()
    status = models.BooleanField(default=False)


class Complaint(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=50, default="Open")
    created_at = models.DateTimeField(auto_now_add=True)


class Notice(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    publish_date = models.DateField()
    status = models.BooleanField(default=True)
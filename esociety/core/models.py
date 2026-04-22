import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


# =========================
# Custom User Model
# =========================
class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('SOCIETY_ADMIN', 'Society Admin'),
        ('RESIDENT', 'Resident'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='RESIDENT')
    society = models.ForeignKey('Society', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# =========================
# Society
# =========================
class Society(models.Model):
    name = models.CharField(max_length=150)

    society_code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True
    )

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.society_code:
            self.society_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================
# Flat
# =========================
class Flat(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    resident = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="flats")
    flat_number = models.CharField(max_length=20)
    flat = models.CharField(max_length=50, null=True, blank=True)
    block_name = models.CharField(max_length=50)

    STATUS_CHOICES = (
        ('VACANT', 'Vacant'),
        ('OCCUPIED', 'Occupied'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='VACANT')

    def __str__(self):
        return f"{self.block_name}-{self.flat_number}"


# =========================
# Member
# =========================
class Member(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    is_primary = models.BooleanField(default=False)  # main resident

    def __str__(self):
        return self.name


# =========================
# Maintenance (GLOBAL)
# =========================
class Maintenance(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.month} - {self.society.name}"


# =========================
# Payment (PER FLAT + Razorpay)
# =========================
class Payment(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, related_name="payments")
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, null=True, blank=True)

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    paid_date = models.DateTimeField(null=True, blank=True)

    # Razorpay fields
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    payment_mode = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('maintenance', 'flat')

    def __str__(self):
        return f"{self.flat} - {self.maintenance.month} - {self.status}"

# =========================
# Complaint
# =========================
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    CATEGORY_CHOICES = [
        ('Water', 'Water'),
        ('Electricity', 'Electricity'),
        ('Lift', 'Lift'),
        ('Security', 'Security'),
        ('Cleanliness', 'Cleanliness'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='complaints/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
# =========================
# Notice
# =========================
class Notice(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# Visitor
# =========================
class Visitor(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    purpose = models.CharField(max_length=200)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name 


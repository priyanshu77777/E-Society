from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================
# Custom User Model
# =========================
class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('SOCIETY_ADMIN', 'Society Admin'),
        ('RESIDENT', 'Resident'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='RESIDENT')
    society = models.ForeignKey('Society', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# =========================
# Society
# =========================
class Society(models.Model):
    name = models.CharField(max_length=150)
    society_code = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# Flat
# =========================
class Flat(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)

    resident = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="flats")

    flat_number = models.CharField(max_length=20)
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
# Maintenance
# =========================
class Maintenance(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=20)

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.flat} - {self.month}"


# =========================
# Payment
# =========================
class Payment(models.Model):
    maintenance = models.OneToOneField(Maintenance, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return self.transaction_id


# =========================
# Complaint
# =========================
class Complaint(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    )

    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"


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
    

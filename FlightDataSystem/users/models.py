from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('foi_fod', 'FOI/FOD'),
        ('ccd', 'CCD'),
        ('oep', 'OEP'),
        ('of', 'OF'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    division = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

class Division(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Flight(models.Model):
    date = models.DateField()
    flight_number = models.CharField(max_length=50)
    aircraft_registration = models.CharField(max_length=50)
    flight_crew = models.TextField()
    sn_crew = models.TextField()
    cabin_crew = models.TextField(blank=True, null=True)
    afl_number = models.CharField(max_length=50, blank=True, null=True)
    from_location = models.CharField(max_length=100, blank=True, null=True)
    to_location = models.CharField(max_length=100, blank=True, null=True)
    air_time_hrs = models.IntegerField(blank=True, null=True)
    air_time_mins = models.IntegerField(blank=True, null=True)
    block_time_hrs = models.IntegerField(blank=True, null=True)
    block_time_mins = models.IntegerField(blank=True, null=True)
    fuel_uplift_liters = models.FloatField(blank=True, null=True)
    sp_gravity = models.FloatField(blank=True, null=True)
    temp_c = models.FloatField(blank=True, null=True)
    fuel_added_kg = models.FloatField(blank=True, null=True)
    total_fuel_tons = models.FloatField(blank=True, null=True)
    fuel_burnt_tons = models.FloatField(blank=True, null=True)
    remaining_fuel_tons = models.FloatField(blank=True, null=True)
    mail_kg = models.FloatField(blank=True, null=True)
    cargo_kg = models.FloatField(blank=True, null=True)
    pax = models.IntegerField(blank=True, null=True)
    weight_kg = models.FloatField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)  # Add this line
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now=True)  # Add this line

    def __str__(self):
        return f"{self.flight_number} - {self.date}"

    def is_editable(self):
        from django.utils import timezone
        return (timezone.now() - self.created_at).total_seconds() < 3600  # 1 hour

class Log(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('edit', 'Edit'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

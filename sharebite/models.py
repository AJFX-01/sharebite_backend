""" models.py """

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# user model
class User(AbstractUser):
    """ Base user types """
    is_donor = models.BooleanField(default=False)
    is_receiver = models.BooleanField(default=False)

# Donations Model
class Donation(models.Model):
    """ Base donation models """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Successful', 'Successful'),
    ]
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    is_reserved = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reserved_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name='reserved_donations'
    )
    status = models.CharField(max_length=15, \
                              choices=STATUS_CHOICES, default='Pending')  # Default status

    def cancel_reservation(self):
        """ Pick up of donation cancelled """
        self.is_delivered = False
        self.reserved_by = None
        self.save()

    def __str__(self):
        return f"{self.title} - Donor: {self.donor.username}"

# Proof Model
class Proof(models.Model):
    """ Basic Proofs """
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='proof')
    proof_image = models.ImageField(upload_to='proofs/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Proof for Donation ID: {self.donation.id}"


# Admin Drop- Off Sites
class DropOffsite(models.Model):
    """ Drop off sites """
    location = models.CharField(max_length=255)
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='added_sites')
    created_at = models.DateTimeField(auto_now_add=True)

# Reciepts
class Receipt(models.Model):
    """ Receipt Models """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receipts')
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='receipts')
    proof_image = models.ImageField(upload_to='receipts/')
    pickup_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt for {self.donation.title} by {self.user.username}"

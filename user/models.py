from django.db import models

# Create your models here.
class Usermodel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class HouseBiddingmodel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100)
    Title = models.CharField(max_length=100)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    sqft_total = models.IntegerField()
    floors = models.IntegerField()
    house_type = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default='India')
    Budget = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user
    
class UserBidAcceptedRejectedmodel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100)
    property_id = models.IntegerField()
    contractor_bid_id = models.IntegerField()
    status = models.CharField(max_length=10, choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
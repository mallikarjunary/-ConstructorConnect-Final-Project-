from django.db import models

# Create your models here.
class Contractormodel(models.Model):
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
    
class ContractorBidmodel(models.Model):
    id = models.AutoField(primary_key=True)
    contractor = models.CharField(max_length=100)
    property_id = models.IntegerField()
    bid_amount = models.IntegerField()

    def __str__(self):
        return self.contractor
    
class ContractorWeeklyUpdateActionModel(models.Model):
    id = models.AutoField(primary_key=True)
    from_date = models.DateField()
    to_date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    cost_utilized = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.IntegerField()
    property_id = models.IntegerField()
    contractor_id = models.IntegerField()

    def __str__(self):
        return self.title

class UpdateActionImage(models.Model):
    update_action = models.ForeignKey(ContractorWeeklyUpdateActionModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='contractor_images/')

    def __str__(self):
        return f"{self.update_action.title} - Image"
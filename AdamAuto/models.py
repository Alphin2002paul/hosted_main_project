from django.db import models
from django.contrib.auth.models import User

class Brand(models.Model):
    company_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.company_name

class ModelName(models.Model):
    model_name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.model_name

class CertifiedCar(models.Model):
    manufacturer = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model_name = models.ForeignKey(ModelName, on_delete=models.CASCADE)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    car_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.manufacturer} {self.model_name} ({self.year})"

class CertifiedCarImage(models.Model):
    car = models.ForeignKey(CertifiedCar, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='certified_cars/')
    
    def __str__(self):
        return f"Image for {self.car}" 
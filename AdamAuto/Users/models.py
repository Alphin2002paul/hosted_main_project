from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('dealer', 'Dealer'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    Phone_number = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=255, null=True,default=1)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    description = models.TextField(null=True)


    def __str__(self):
        return self.username

class Tbl_Company(models.Model):
    company_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.company_name

class Tbl_Color(models.Model):
    color_name = models.CharField(max_length=20, default='Unknown Color')

    def __str__(self):
        return self.color_name

class Tbl_Model(models.Model):
    model_name = models.CharField(max_length=20)

    def __str__(self):
        return self.model_name
class VehicleType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class UserCarDetails(models.Model):
    manufacturer = models.ForeignKey(Tbl_Company, on_delete=models.CASCADE)
    model_name = models.ForeignKey(Tbl_Model, on_delete=models.CASCADE)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.ForeignKey(Tbl_Color, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=100)
    kilometers = models.IntegerField()
    transmission = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=100)
    insurance_validity = models.DateField()
    pollution_validity = models.DateField()
    tax_validity = models.DateField()
    car_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    owner_status = models.CharField(max_length=100)
    car_status = models.CharField(max_length=100)
    car_cc = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.manufacturer} {self.model_name} ({self.year})"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LikedCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_cars')
    car = models.ForeignKey('UserCarDetails', on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

class CarImage(models.Model):
    car = models.ForeignKey(UserCarDetails, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"Image for {self.car}"

from django.conf import settings

class Service(models.Model):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    transmission = models.CharField(max_length=50)
    fuel = models.CharField(max_length=50)
    year = models.IntegerField()
    problem = models.TextField()
    service_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slot_allocated = models.CharField(max_length=20, default='Pending')
    status = models.CharField(max_length=20, default='Pending')  # New status field


    def __str__(self):
        return f"{self.manufacturer} {self.model} - {self.user.username}"
    
    
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SellCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=20)
    kilometers = models.IntegerField()
    transmission = models.CharField(max_length=20)
    condition = models.TextField()
    reg_number = models.CharField(max_length=20)
    insurance_validity = models.DateField()
    pollution_validity = models.DateField()
    tax_validity = models.DateField()
    car_type = models.CharField(max_length=50)
    owner_status = models.IntegerField()
    car_cc = models.IntegerField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.manufacturer} {self.model} - {self.user.username}"

class SellCarImage(models.Model):
    sell_car = models.ForeignKey(SellCar, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sell_car_images/')

    def __str__(self):
        return f"Image for {self.sell_car}"
    
    from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)        
    car = models.ForeignKey(UserCarDetails, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    manufacturer_name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    year = models.IntegerField(validators=[MinValueValidator(2011), MaxValueValidator(2024)])

    # Rating fields
    comfort_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    performance_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    fuel_efficiency_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    safety_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    technology_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    description = models.TextField(null=True, blank=True)   
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.manufacturer_name} {self.model_name} ({self.year}) - Feedback by {self.user.username}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        


from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class TestDriveBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey('UserCarDetails', on_delete=models.CASCADE)  # Use string reference if UserCarDetails is defined later
    date = models.DateField()
    time = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ['car', 'date', 'time'],
            ['user', 'car', 'date']
        ]
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.car.manufacturer} {self.car.model_name} - {self.date}"



from django.db import models
from django.conf import settings

class CarPurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(UserCarDetails, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_option = models.CharField(max_length=20, default='showroom')
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='completed')
    # New fields
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    payment_mode = models.CharField(max_length=20, blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)  # New field


    def __str__(self):
        return f"{self.user.username} - {self.car.manufacturer} {self.car.model_name} - {self.purchase_date}"


from django.db import models
from django.conf import settings

class CarEnquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    model_year = models.IntegerField()
    color = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.manufacturer} {self.model_name} - {self.user.username}"

from django.db import models
from django.utils import timezone
from datetime import timedelta

class Subscription(models.Model):
    SUBSCRIPTION_TYPES = (
        ('free', 'Free'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired')  # Added expired status
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    transaction_id = models.CharField(max_length=100, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='free')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_mode = models.CharField(max_length=20, default='Online')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Set end_date based on subscription_type
        if not self.end_date and self.subscription_type != 'free':
            if self.subscription_type == 'standard':
                self.end_date = self.start_date + timedelta(days=30)
            elif self.subscription_type == 'premium':
                self.end_date = self.start_date + timedelta(days=90)
        super().save(*args, **kwargs)

    def is_active(self):
        if self.status not in ['completed', 'pending']:
            return False
        if not self.end_date:
            return True
        return timezone.now() <= self.end_date

    @classmethod
    def delete_expired_subscriptions(cls):
        """
        Delete all expired subscriptions that are past their end date
        """
        now = timezone.now()
        expired_subscriptions = cls.objects.filter(
            end_date__lt=now,
            status='completed'
        )
        
        # Update status to expired before deletion
        expired_subscriptions.update(status='expired')
        
        # Delete the expired subscriptions
        expired_subscriptions.delete()
        
        return len(expired_subscriptions)

    def __str__(self):
        return f"{self.user.username}'s {self.subscription_type} subscription"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

class CertifiedCar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=20)
    kilometers = models.IntegerField()
    transmission = models.CharField(max_length=20)
    condition = models.TextField()
    reg_number = models.CharField(max_length=20, unique=True)
    insurance_validity = models.DateField()
    pollution_validity = models.DateField()
    tax_validity = models.DateField()
    car_type = models.CharField(max_length=50)
    owner_status = models.IntegerField()
    car_cc = models.IntegerField()
    car_status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.manufacturer} {self.model_name} - {self.user.username}"

    class Meta:
        unique_together = ['user', 'reg_number']

class CertifiedCarImage(models.Model):
    certified_car = models.ForeignKey(CertifiedCar, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='certified_car_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.certified_car} - {self.created_at}"
    
    
class ChatMessage(models.Model):
    car = models.ForeignKey('CertifiedCar', on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Chat between {self.sender.username} and {self.receiver.username} for {self.car}"
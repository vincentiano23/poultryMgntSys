from django.db import models
from django.contrib.auth.models import User

# Poultry Inventory

class Chicken(models.Model):
    CATEGORY_CHOICES = [
        ('Broiler', 'Broiler'),
        ('Layer', 'Layer'),
        ('Kienyeji', 'Kienyeji'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.quantity}"

# Egg Inventory
class Egg(models.Model):
    quantity = models.PositiveIntegerField()
    collected_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} eggs on {self.collected_date}"  

# Feed Inventory
class Feed(models.Model):
    name = models.CharField(max_length=100)
    quantity_kg = models.FloatField()
    date_purchased = models.DateField()
    
    def __str__(self):
        return f"{self.name} - {self.quantity_kg}kg"  

# Health Monitoring
class HealthRecord(models.Model):
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100, blank=True, null=True)
    medication = models.CharField(max_length=200, blank=True, null=True)
    date_treated = models.DateField()
    
    def __str__(self):
        return f"{self.chicken.category} - {self.disease} treated on {self.date_treated}"  

# Sales
class Sale(models.Model):
    customer_name = models.CharField(max_length=100)
    item = models.CharField(max_length=50, choices=[('Chicken', 'Chicken'), ('Egg', 'Egg')])
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    date_sold = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer_name} - {self.quantity} {self.item}(s)"  

# Expenses
class Expense(models.Model):
    description = models.CharField(max_length=200)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.description} - KES {self.amount}"  

# User Roles
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Worker', 'Worker')])
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

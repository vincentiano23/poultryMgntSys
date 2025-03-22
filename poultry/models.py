from django.db import models
from django.contrib.auth.models import User

# Poultry Inventory

class Chicken(models.Model):
    CATEGORY_CHOICES = [
        ('Broiler', 'Broiler'),
        ('Layer', 'Layer'),
        ('Kienyeji', 'Kienyeji'),
    ]
    BUY_FROM_CHOICES = [
        ('Local Hatch', 'Local Hatch'),
        ('Kukuchic', 'Kukuchic'),
        ('Kenchic', 'Kenchic'),
        ('Others', 'Others'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField()
    age_in_weeks = models.PositiveIntegerField()
    weight_kg = models.FloatField(null=True, blank=True)
    buy_from = models.CharField(max_length=50, choices=BUY_FROM_CHOICES)
    other_source = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.quantity} - {self.age_in_weeks} weeks"
    

# Immunization Records
class ImmunizationRecord(models.Model):
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=100)
    date_administered = models.DateField()

    def __str__(self):
        return f"{self.chicken.category} - {self.vaccine_name} on {self.date_administered}"

# Egg Incubation Schedule
class IncubationSchedule(models.Model):
    breed = models.CharField(max_length=50)
    incubation_date = models.DateField()
    label = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.breed} - Incubated on {self.incubation_date}"  
    
# Egg Inventory
class Egg(models.Model):
    VARIETY_CHOICES = [
        ('white', 'White'),
        ('brown', 'Brown'),
        ('organic', 'Organic'),
        ('free_range', 'Free Range'),
    ]

    variety = models.CharField(max_length=20, choices=VARIETY_CHOICES,null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price_per_egg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    collected_date = models.DateField(auto_now_add=True)
 

    def __str__(self):
        return f"{self.quantity} {self.variety} eggs on {self.collected_date}"
    
# Feed Inventory
class Feed(models.Model):
    FEED_CHOICES = [
        ('Starter Mash', 'Starter Mash'),
        ('Grower Mash', 'Grower Mash'),
        ('Layer Mash', 'Layer Mash'),
        ('Finisher Mash', 'Finisher Mash'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, choices=FEED_CHOICES, default='Other')
    custom_name = models.CharField(max_length=255, default="")
    quantity_kg = models.FloatField()
    remaining_kg = models.FloatField(default=0)
    date_purchased = models.DateField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.remaining_kg:
            self.remaining_kg = self.quantity_kg
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name if self.name != 'Other' else self.custom_name} - {self.remaining_kg}/{self.quantity_kg}kg"

# Mortality Records
class MortalityRecord(models.Model):
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE)
    age_at_death = models.PositiveIntegerField()
    cause_of_death = models.CharField(max_length=200)
    comment = models.TextField(null=True, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.chicken.category} - Died at {self.age_at_death} weeks due to {self.cause_of_death}"


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
    chicken = models.ForeignKey(Chicken, null=True, blank=True, on_delete=models.CASCADE)
    eggs = models.ForeignKey(Egg, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_sold = models.DateTimeField(auto_now_add=True)
    chicken_variety = models.CharField(max_length=50, null=True, blank=True)  
    egg_variety = models.CharField(max_length=20, null=True, blank=True)
    related_sale = models.ForeignKey('Sale', null=True, blank=True, on_delete=models.CASCADE) 
   
    def __str__(self):
        return f"{self.customer_name} - {self.quantity} sold"


# Expenses
class Expense(models.Model):
    description = models.CharField(max_length=200)
    amount = models.FloatField()
    related_sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - KES {self.amount}"

# User Roles
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Worker', 'Worker')])
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Salary(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="salaries")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.worker.username} - {self.amount} Ksh - {self.status}"
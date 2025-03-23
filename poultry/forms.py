from django import forms
from .models import Chicken, Egg, Sale, Feed, Expense, HealthRecord, MortalityRecord, IncubationSchedule, Salary, Profile


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'role']  

    def clean_role(self):
        role = self.cleaned_data.get('role')
        user = self.instance.user  
        if role == "admin" and not user.is_superuser:
            raise forms.ValidationError("Only superusers can create admins.")
        
        return role
    
class BulkChickenForm(forms.Form):
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
    
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="Select Chicken Type")
    quantity = forms.IntegerField(min_value=1, label="Enter Quantity")
    age_in_weeks = forms.IntegerField(min_value=0, label="Enter Age (weeks)", required=False)
    buy_from = forms.ChoiceField(choices=BUY_FROM_CHOICES, label="Buy From")
    other_source = forms.CharField(max_length=100, required=False, label="If Other, specify")
    weight_kg = forms.FloatField(required=False, label="Weight (kg)")

class EggCollectionForm(forms.ModelForm):
    class Meta:
        model = Egg
        fields = ['quantity']
        labels = {
            'quantity': 'Number of Eggs Collected'
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'chicken', 'eggs', 'quantity', 'price']
        labels = {
            'customer_name': 'Customer Name',
            'quantity': 'Quantity Sold',
            'price': 'Price per Unit'
        }

class FeedForm(forms.ModelForm):
    FEED_CHOICES = [
        ('Starter', 'Starter'),
        ('Grower', 'Grower'),
        ('Finisher', 'Finisher'),
        ('Layer Mash', 'Layer Mash'),
        ('Kienyeji Mash', 'Kienyeji Mash'),
    ]
    name = forms.ChoiceField(choices=FEED_CHOICES, label="Select Feed Type")
    
    class Meta:
        model = Feed
        fields = ['name', 'quantity_kg']
        labels = {
            'quantity_kg': 'Quantity (kg)'
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount']
        labels = {
            'description': 'Expense Description',
            'amount': 'Amount (KES)'
        }

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['chicken', 'disease', 'medication']
        labels = {
            'disease': 'Disease (if any)',
            'medication': 'Medication Administered'
        }

class DeadChickenForm(forms.ModelForm):
    class Meta:
        model = MortalityRecord
        fields = ['age_at_death', 'cause_of_death', 'comment']
        labels = {
            'age_at_death': 'Age at Death (weeks)',
            'cause_of_death': 'Cause of Death',
            'comment': 'Additional Comments (if any)'
        }

class IncubationScheduleForm(forms.ModelForm):
    class Meta:
        model = IncubationSchedule
        fields = ['breed', 'incubation_date', 'label']
        labels = {
            'breed': 'Breed',
            'incubation_date': 'Incubation Date',
            'label': 'Label (for identification)'
        }

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['worker', 'amount', 'status']
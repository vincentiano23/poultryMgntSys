from django import forms
from .models import Chicken, Egg, Sale, Feed, Expense, HealthRecord 

class BulkChickenForm(forms.Form):
    CATEGORY_CHOICES = [
        ('Broiler', 'Broiler'),
        ('Layer', 'Layer'),
        ('Kienyeji', 'Kienyeji'),
    ]
    
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="Select Chicken Type")
    quantity = forms.IntegerField(min_value=1, label="Enter Quantity")

class EggCollectionForm(forms.ModelForm):
    class Meta:
        model = Egg
        fields = ['quantity']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name','item', 'quantity', 'price']

class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['name','quantity_kg']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount']

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['chicken', 'disease', 'medication']
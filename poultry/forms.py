from django import forms
from .models import Chicken, Egg

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
from django.contrib import admin
from .models import Chicken, Egg, Feed, HealthRecord, Sale, Expense, Profile

@admin.register(Chicken)
class ChickenAdmin(admin.ModelAdmin):
    list_display = ('category', 'quantity', 'date_added')
    list_filter = ('category', 'date_added')
    search_fields = ('category',)

@admin.register(Egg)
class EggAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'collected_date')
    list_filter = ('collected_date',)
    search_fields = ('collected_date',)

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity_kg', 'date_purchased')
    list_filter = ('date_purchased',)
    search_fields = ('name',)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('chicken', 'disease', 'medication', 'date_treated')
    list_filter = ('date_treated', 'disease')
    search_fields = ('chicken__category', 'disease')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'item', 'quantity', 'price', 'date_sold')
    list_filter = ('date_sold', 'item')
    search_fields = ('customer_name', 'item')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('description',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)


from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from .models import Chicken, Egg, Feed, HealthRecord, Sale, Expense, Profile

@admin.register(Chicken)
class ChickenAdmin(admin.ModelAdmin):
    list_display = ('category', 'quantity', 'age_in_weeks', 'weight_kg', 'date_added')
    list_filter = ('category', 'date_added')
    search_fields = ('category',)

@admin.register(Egg)
class EggAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'collected_date')
    list_filter = ('collected_date',)
    search_fields = ('collected_date',)

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity_kg', 'remaining_kg', 'date_purchased')
    list_filter = ('date_purchased',)
    search_fields = ('name',)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('chicken', 'disease', 'medication', 'date_treated')
    list_filter = ('date_treated', 'disease')
    search_fields = ('chicken__category', 'disease')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'get_item', 'quantity', 'price', 'date_sold')
    list_filter = ('date_sold', 'chicken', 'eggs')  # Proper filtering
    search_fields = ('customer_name', 'chicken__category', 'eggs__collected_date')

    def get_item(self, obj):
        if obj.chicken:
            return f"Chicken ({obj.chicken.category})"
        elif obj.eggs:
            return "Eggs"
        return "Unknown"

    get_item.short_description = "Item"  # Display name in admin panel

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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['role'].disabled = True
        return form

# Optional: Add a custom admin view for better management
class CustomAdminSite(admin.AdminSite):
    site_header = "Poultry Management Admin"
    site_title = "Poultry Management Admin Portal"
    index_title = "Welcome to the Poultry Management Admin Portal"

admin_site = CustomAdminSite(name='custom_admin')
admin_site.register(Chicken, ChickenAdmin)
admin_site.register(Egg, EggAdmin)
admin_site.register(Feed, FeedAdmin)
admin_site.register(HealthRecord, HealthRecordAdmin)
admin_site.register(Sale, SaleAdmin)
admin_site.register(Expense, ExpenseAdmin)
admin_site.register(Profile, ProfileAdmin)

def superuser_required(view_func):
    """Restrict admin actions to superusers only."""
    return user_passes_test(lambda u: u.is_superuser)(view_func)

# Restrict admin login to superusers only
admin.site.login = superuser_required(admin.site.login)
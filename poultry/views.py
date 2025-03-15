from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages  
from django.db import models
from .forms import EggCollectionForm, BulkChickenForm
from .models import Chicken, Egg, Feed, HealthRecord, Sale, Expense


# User Authentication Views

def user_login(request):
    """Handles user login"""
    if request.method == 'POST':
        username, password = request.POST.get('username'), request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! You have successfully logged in.")
            return redirect('admin_dashboard' if user.is_staff else 'dashboard')
        messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'poultry/login.html')

@login_required
def user_logout(request):
    """Handles user logout"""
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

def register(request):
    """Handles user registration"""
    if request.method == 'POST':
        username, password = request.POST.get('username'), request.POST.get('password')
        role = request.POST.get('role', 'worker')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose a different one.")
            return redirect('register')
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, is_staff=(role == 'admin'))
        login(request, user)
        messages.success(request, "Account successfully created! Welcome to the system.")
        return redirect('admin_dashboard' if user.is_staff else 'dashboard')
    
    return render(request, 'poultry/register.html')

# Dashboard Views

@login_required
def dashboard(request):
    chickens = Chicken.objects.values('category').annotate(total=models.Sum('quantity'))
    
    context = {
        'total_chickens': sum(chicken['total'] for chicken in chickens),
        'chicken_types': chickens,  # This will hold total counts per category
        'total_eggs': Egg.objects.aggregate(total=models.Sum('quantity'))['total'] or 0,
    }
    return render(request, 'poultry/dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    if not request.user.is_staff:
        messages.error(request, "Access Denied: You are not authorized to view this page.")
        return redirect('dashboard')
    
    context = {
        'username': request.user.username,
        'chickens': Chicken.objects.all(),
        'eggs': Egg.objects.all(),
        'feeds': Feed.objects.all(),
        'sales': Sale.objects.all(),
        'expenses': Expense.objects.all(),
        'health_records': HealthRecord.objects.all(),
    }
    return render(request, 'poultry/admin_dashboard.html', context)

# Chicken Management Views

def add_chicken(request):
    if request.method == "POST":
        form = BulkChickenForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get('category')  # Ensure the form has this field
            quantity = form.cleaned_data.get('quantity', 0) or 0

            if quantity > 0:
                Chicken.objects.create(category=category, quantity=quantity)
                messages.success(request, f"{quantity} {category} chickens added successfully!")
                return redirect('view_chickens')  # Redirect to the view chickens page
        
    else:
        form = BulkChickenForm()

    return render(request, 'poultry/add_chicken.html', {'form': form})

def view_chickens(request):
    """Displays list of all chickens"""
    return render(request, 'poultry/view_chickens.html', {'chickens': Chicken.objects.all()})

# Egg Management Views

def add_eggs(request):
    """Handles egg collection"""
    if request.method == "POST":
        form = EggCollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_eggs')
    else:
        form = EggCollectionForm()
    return render(request, 'poultry/add_eggs.html', {'form': form})

def view_eggs(request):
    """Displays collected eggs sorted by collection date"""
    return render(request, 'poultry/view_eggs.html', {'eggs': Egg.objects.all().order_by('collected_date')})

# Worker Management Views

@login_required
def manage_workers(request):
    """Allows admin to manage workers"""
    if not request.user.is_staff:
        messages.error(request, "Access Denied!")
        return redirect('dashboard')
    
    if request.method == "POST":
        username, password = request.POST.get("username"), request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, f"Worker {username} added successfully!")
    
    return render(request, "poultry/manage_workers.html", {"workers": User.objects.filter(is_staff=False)})

@login_required
def delete_worker(request, worker_id):
    """Allows admin to remove a worker"""
    if not request.user.is_staff:
        messages.error(request, "Access Denied!")
        return redirect('dashboard')
    
    User.objects.get(id=worker_id).delete()
    messages.success(request, "Worker removed successfully!")
    return redirect('manage_workers')

# Sales Management Views

@login_required
def manage_sales(request):
    """Displays sales records"""
    if not request.user.is_staff:
        messages.error(request, "Access Denied!")
        return redirect('dashboard')
    
    return render(request, 'poultry/manage_sales.html', {"sales": Sale.objects.all()})

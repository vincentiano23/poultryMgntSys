from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages  
from django.db.models import Sum, F
from .forms import EggCollectionForm, BulkChickenForm, IncubationScheduleForm, DeadChickenForm
from .models import Chicken, Egg, Feed, HealthRecord, Sale, Expense, IncubationSchedule, MortalityRecord

def user_login(request):
    """Handles user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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
        username = request.POST.get('username')
        password = request.POST.get('password')
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

@login_required
def dashboard(request):
    """Worker dashboard"""
    chickens = Chicken.objects.values('category').annotate(total=Sum('quantity'))
    total_sales = Sale.objects.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
    total_feeds = Feed.objects.aggregate(total=Sum('quantity_kg'))['total'] or 0
    context = {
        'total_chickens': sum(chicken['total'] for chicken in chickens),
        'chicken_types': chickens,
        'total_eggs': Egg.objects.aggregate(total=Sum('quantity'))['total'] or 0,
        'total_feeds': total_feeds,
        'total_sales': total_sales,
    }
    return render(request, 'poultry/dashboard.html', context)

@login_required
def admin_dashboard(request):
    """Admin dashboard"""
    if not request.user.is_staff:
        messages.error(request, "Access Denied: You are not authorized to view this page.")
        return redirect('dashboard')

    chickens = Chicken.objects.values('category').annotate(total=Sum('quantity'))
    total_sales = Sale.objects.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
    context = {
        'total_chickens': sum(chicken['total'] for chicken in chickens),
        'chicken_types': chickens,
        'total_eggs': Egg.objects.aggregate(total=Sum('quantity'))['total'] or 0,
        'total_sales': total_sales,
        'chickens': Chicken.objects.all(),
        'eggs': Egg.objects.all(),
        'feeds': Feed.objects.all(),
        'sales': Sale.objects.all(),
        'expenses': Expense.objects.all(),
        'health_records': HealthRecord.objects.all(),
    }
    return render(request, 'poultry/admin_dashboard.html', context)

@login_required
def add_chicken(request):
    """Add new chickens to the inventory"""
    if request.method == "POST":
        form = BulkChickenForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            quantity = form.cleaned_data.get('quantity', 0)
            age_in_weeks = form.cleaned_data.get('age_in_weeks')
            buy_from = form.cleaned_data.get('buy_from')
            weight_kg = form.cleaned_data.get('weight_kg')

            if quantity > 0:
                Chicken.objects.create(
                    category=category,
                    quantity=quantity,
                    age_in_weeks=age_in_weeks,
                    buy_from=buy_from,
                    weight_kg=weight_kg
                )
                messages.success(request, f"{quantity} {category} chickens added successfully!")
                return redirect('dashboard')
    else:
        form = BulkChickenForm()
    return render(request, 'poultry/add_chicken.html', {'form': form})

@login_required
def view_chickens(request):
    """View all chickens with metadata"""
    return render(request, 'poultry/view_chickens.html', {'chickens': Chicken.objects.all()})

@login_required
def add_eggs(request):
    """Record egg collection"""
    if request.method == "POST":
        form = EggCollectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Egg collection recorded successfully!")
            return redirect('view_eggs')
    else:
        form = EggCollectionForm()
    return render(request, 'poultry/add_eggs.html', {'form': form})

@login_required
def view_eggs(request):
    """View collected eggs"""
    return render(request, 'poultry/view_eggs.html', {'eggs': Egg.objects.all().order_by('-collected_date')})

@login_required
def log_feed(request):
    """Log feed records"""
    if request.method == "POST":
        name = request.POST.get('name')
        quantity_kg = request.POST.get('quantity_kg')

        Feed.objects.create(
            name=name,
            quantity_kg=quantity_kg,
        )

        messages.success(request, "Feed record added successfully!")
        return redirect('log_feed')

    return render(request, 'poultry/log_feed.html')

@login_required
def manage_workers(request):
    """Manage workers"""
    if not request.user.is_staff:
        messages.error(request, "Access Denied!")
        return redirect('dashboard')
    return render(request, "poultry/manage_workers.html", {"workers": User.objects.filter(is_staff=False)})

@login_required
def delete_worker(request, worker_id):
    """Delete worker account"""
    if not request.user.is_staff:
        messages.error(request, "Access Denied!")
        return redirect('dashboard')
    worker = get_object_or_404(User, id=worker_id)
    worker.delete()
    messages.success(request, "Worker removed successfully!")
    return redirect('manage_workers')

@login_required
def manage_sales(request):
    """View and manage sales"""
    if not request.user.is_staff:
        messages.error(request, "Access Denied!")
        return redirect('dashboard')
    return render(request, 'poultry/manage_sales.html', {"sales": Sale.objects.all()})

@login_required
def record_poultry_sale(request):
    """Record a new poultry sale"""
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        quantity = int(request.POST.get("quantity", 0))
        price = float(request.POST.get("price", 0))
        poultry_type = request.POST.get("sale_type")  # Updated to match the form field name

        # Validate input
        if quantity <= 0 or price <= 0:
            messages.error(request, "Quantity and price must be greater than zero.")
            return redirect("record_poultry_sale")

        if poultry_type == "chicken":
            chicken_id = request.POST.get("chicken_id")
            chicken = Chicken.objects.get(id=chicken_id) if chicken_id else None
            if not chicken:
                messages.error(request, "Invalid chicken selection!")
                return redirect("record_poultry_sale")
            if chicken.quantity < quantity:
                messages.error(request, "Insufficient quantity of chickens to sell!")
                return redirect("record_poultry_sale")
            chicken.quantity -= quantity
            chicken.save()
            sale = Sale.objects.create(
                customer_name=customer_name,
                chicken=chicken,
                quantity=quantity,
                price=price * quantity  # Calculate total price
            )
        elif poultry_type == "egg":
            egg_id = request.POST.get("egg_id")
            egg = Egg.objects.get(id=egg_id) if egg_id else None
            if not egg:
                messages.error(request, "Invalid egg selection!")
                return redirect("record_poultry_sale")
            if egg.quantity < quantity:
                messages.error(request, "Insufficient quantity of eggs to sell!")
                return redirect("record_poultry_sale")
            egg.quantity -= quantity
            egg.save()
            sale = Sale.objects.create(
                customer_name=customer_name,
                eggs=egg,
                quantity=quantity,
                price=price * quantity  # Calculate total price
            )
        else:
            messages.error(request, "Invalid poultry type selected!")
            return redirect("record_poultry_sale")

        messages.success(request, f"Sale recorded successfully! Total price: Ksh {sale.price:.2f}")
        return redirect("record_poultry_sale")

    return render(request, "poultry/record_sale.html", {
        "sales": Sale.objects.all(),
        "chickens": Chicken.objects.all(),
        "eggs": Egg.objects.all(),
    })

@login_required
def record_incubation(request):
    """Record egg incubation schedule"""
    if request.method == "POST":
        form = IncubationScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Incubation schedule recorded successfully!")
            return redirect('view_incubation_schedules')
    else:
        form = IncubationScheduleForm()
    return render(request, 'poultry/record_incubation.html', {'form': form})

@login_required
def view_incubation_schedules(request):
    """View all incubation schedules"""
    return render(request, 'poultry/view_incubation.html', {'incubations': IncubationSchedule.objects.all()})

@login_required
def log_dead_chicken(request):
    """Log dead chickens"""
    if request.method == "POST":
        form = DeadChickenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dead chicken recorded successfully!")
            return redirect('dashboard')
    else:
        form = DeadChickenForm()
    return render(request, 'poultry/log_dead_chicken.html', {'form': form})

@login_required
def view_dead_chickens(request):
    """View all dead chickens"""
    return render(request, 'poultry/view_dead_chickens.html', {'dead_chickens': MortalityRecord.objects.all()})
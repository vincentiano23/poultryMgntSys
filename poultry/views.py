from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages  
from django.db.models import Sum, F
from decimal import Decimal
from django.utils import timezone
from .forms import EggCollectionForm, BulkChickenForm, IncubationScheduleForm, DeadChickenForm, ExpenseForm, SalaryForm
from .models import Chicken, Egg, Feed, HealthRecord, Sale, Expense, IncubationSchedule, MortalityRecord, Salary

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
    egg_counts = Egg.objects.values('variety').annotate(total=Sum('quantity'))
    total_sales = Sale.objects.aggregate(total=Sum(F('price') * F('quantity')))['total'] or Decimal('0.0')
    total_expenses = Expense.objects.aggregate(total=Sum("amount"))["total"] or Decimal('0.0')
    total_expenses = Decimal(str(total_expenses)) 
    net_profit = total_sales - total_expenses
    total_feeds = Feed.objects.aggregate(total_used=Sum('quantity_kg'))['total_used'] or 0
    feed_types = Feed.objects.values('name').annotate(total=Sum('quantity_kg'))
    context = {
        'username': request.user.username,
        'total_chickens': sum(chicken['total'] for chicken in chickens),
        'chicken_types': chickens,
        'egg_counts': egg_counts,
        'total_eggs': Egg.objects.aggregate(total=Sum('quantity'))['total'] or 0,
        'total_feeds': total_feeds,
        'feed_types': feed_types,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_profit': net_profit,

    }
    return render(request, 'poultry/dashboard.html', context)

@login_required
def admin_dashboard(request):
    """Admin dashboard with enhanced data aggregation"""
    
    if not request.user.is_staff:
        messages.error(request, "Access Denied: You are not authorized to view this page.")
        return redirect('dashboard')
    chickens = Chicken.objects.values('category').annotate(total=Sum('quantity'))
    egg_counts = Egg.objects.values('variety').annotate(total=Sum('quantity'))
    total_chickens = sum(chicken['total'] for chicken in chickens)
    broiler_count = next((ch['total'] for ch in chickens if ch['category'] == 'Broiler'), 0)
    layers_count = next((ch['total'] for ch in chickens if ch['category'] == 'Layer'), 0)
    kienyeji_count = next((ch['total'] for ch in chickens if ch['category'] == 'Kienyeji'), 0)
    total_sales = Sale.objects.aggregate(total=Sum(F('price') * F('quantity')))['total'] or Decimal('0.0')
    total_feeds = Feed.objects.aggregate(total_used=Sum('quantity_kg'))['total_used'] or Decimal('0.0')
    feed_types = Feed.objects.values('name').annotate(total=Sum('quantity_kg'))
    total_expenses = Expense.objects.aggregate(total=Sum("amount"))["total"] or Decimal('0.0')
    total_expenses = Decimal(str(total_expenses)) 
    net_profit = total_sales - total_expenses

    context = {
        'username': request.user.username,
        'total_chickens': total_chickens,
        'chicken_types': chickens,
        'egg_counts': egg_counts,
        'broiler_count': broiler_count,
        'layers_count': layers_count,
        'kienyeji_count': kienyeji_count,
        'total_eggs': Egg.objects.aggregate(total=Sum('quantity'))['total'] or 0,
        'total_sales': total_sales,
        'total_feeds': total_feeds,
        'feed_types': feed_types,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
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
    if request.method == "POST":
        variety = request.POST.get("egg_variety")
        quantity = int(request.POST.get("quantity", 0))
        price_per_egg = float(request.POST.get("price_per_egg", 0))
        if quantity <= 0 or price_per_egg <= 0:
            messages.error(request, "Quantity and price must be greater than zero.")
            return redirect("add_eggs")
        egg = Egg(variety=variety, quantity=quantity, price_per_egg=price_per_egg)
        egg.save()
        messages.success(request, f"{quantity} eggs added successfully!")
        return redirect("add_eggs") 
    return render(request, "poultry/add_eggs.html", {
        "eggs": Egg.objects.all(),  
    })

@login_required
def view_eggs(request):
    """View collected eggs"""
    return render(request, 'poultry/view_eggs.html', {'eggs': Egg.objects.all().order_by('-collected_date')})

@login_required
def log_feed(request):
    """Log feed records"""
    if request.method == "POST":
        name = request.POST.get('name')
        custom_name = request.POST.get('custom_name', '').strip()
        quantity_kg = request.POST.get('quantity_kg')
        date_purchased = request.POST.get('date_purchased')
        # Validate inputs
        if not name or not quantity_kg or not date_purchased:
            messages.error(request, "All fields are required.")
            return redirect('log_feed')
        try:
            quantity_kg = float(quantity_kg)
            if quantity_kg <= 0:
                messages.error(request, "Quantity must be a positive number.")
                return redirect('log_feed')
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
            return redirect('log_feed')

        # Save feed entry
        feed = Feed.objects.create(
            name=name,
            custom_name=custom_name if name == "Other" else "",
            quantity_kg=quantity_kg,
            remaining_kg=quantity_kg,
            date_purchased=date_purchased
        )
        messages.success(request, f"Feed '{feed.name}' recorded successfully!")
        return redirect('log_feed')
    return render(request, 'poultry/log_feed.html')

@login_required
def manage_workers(request):
    """Manage workers"""
    if not request.user.is_staff:
        messages.error(request, "Access Denied!")
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            worker = User.objects.create_user(username=username, password=password)
            messages.success(request, "Worker added successfully!")

    workers = User.objects.filter(is_staff=False)
    return render(request, "poultry/manage_workers.html", {"workers": workers})


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
    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        sale_type = request.POST.get('sale_type')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        chicken = None
        egg = None

        if sale_type == "chicken":
            chicken_id = request.POST.get('chicken_id')
            chicken = Chicken.objects.get(id=chicken_id)
            if chicken.quantity < quantity:
                messages.error(request, "Not enough chickens available.")
                return redirect('manage_sales')
            chicken.quantity -= quantity  
            chicken.save() 

        elif sale_type == "egg":
            egg_id = request.POST.get('egg_id')
            egg = Egg.objects.get(id=egg_id)
            if egg.quantity < quantity:
                messages.error(request, "Not enough eggs available.")
                return redirect('manage_sales')
            egg.quantity -= quantity  
            egg.save()  

        sale = Sale(
            customer_name=customer_name,
            sale_type=sale_type,
            quantity=quantity,
            price=price,
            date_sold=timezone.now(),
            chicken=chicken,
            egg=egg,
        )
        sale.save()  

        messages.success(request, "Sale recorded successfully!")
        return redirect('manage_sales')

    sales = Sale.objects.all()
    chickens = Chicken.objects.all()  
    eggs = Egg.objects.all()  

    context = {
        'sales': sales,
        'chickens': chickens,
        'eggs': eggs,
    }
    return render(request, 'poultry/manage_sales.html', context)

@login_required
def manage_salaries(request):
    """Admin function to manage workers' salaries."""
    salaries = Salary.objects.select_related('worker').order_by('-payment_date')
    if request.method == "POST":
        form = SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_salaries")
    else:
        form = SalaryForm()

    context = {
        "salaries": salaries,
        "form": form
    }
    return render(request, "poultry/manage_salaries.html", context)

@login_required
def record_poultry_sale(request):
    """Record a new poultry sale"""
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        quantity = int(request.POST.get("quantity", 0))
        price = float(request.POST.get("price", 0))
        poultry_type = request.POST.get("sale_type") 

      
        if quantity <= 0 or price <= 0:
            messages.error(request, "Quantity and price must be greater than zero.")
            return redirect("record_poultry_sale")

        if poultry_type == "chicken":
            chicken_id = request.POST.get("chicken_id")
            chicken = Chicken.objects.get(id=chicken_id) if chicken_id else None
            chicken_variety = request.POST.get("chicken_variety")  # Get the chicken variety
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
                price=price * quantity,
                chicken_variety=chicken_variety  
            )
        elif poultry_type == "egg":
            egg_id = request.POST.get("egg_id")
            egg_variety = request.POST.get("egg_variety")  
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
                price=price * quantity, 
                egg_variety=egg_variety  
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

@login_required
def expenses_list(request):
    expenses = Expense.objects.all()  
    total_expenses = sum(exp.amount for exp in expenses) 

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense added successfully!")
            return redirect("expenses_list")  
    else:
        form = ExpenseForm()

    context = {
        "expenses": expenses,
        "total_expenses": total_expenses,
        "form": form
    }
    return render(request, "poultry/expenses.html", context)
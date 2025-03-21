from django.urls import path
from . import views
from .views import dashboard, admin_dashboard, user_login, user_logout, register, manage_workers, delete_worker, manage_sales, add_chicken, add_eggs, view_eggs, view_chickens,view_incubation_schedules, expenses_list

urlpatterns = [
    path('', user_login, name='login'), 
    path('dashboard/', dashboard, name='dashboard'), 
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'), 
    path('logout/', user_logout, name='logout'),
    path('manage_workers/', manage_workers, name='manage_workers'),
    path('delete_worker/<int:worker_id>/', delete_worker, name='delete_worker'),
    path('manage_sales/', manage_sales, name='manage_sales'),
    path('add-chicken/', add_chicken, name='add_chicken'),
    path('view-chickens/', view_chickens, name='view_chickens'),
    path('add_eggs/', add_eggs, name='add_eggs'),
    path('view_eggs/', view_eggs, name='view_eggs'),
    path('register/', register, name='register'),
    path('log-feed/', views.log_feed, name='log_feed'),
    path('log-dead-chicken/', views.log_dead_chicken, name='log_dead_chicken'),
    path('record-sale/', views.record_poultry_sale, name='record_poultry_sale'),
    path('record-incubation/', views.record_incubation, name='record_incubation'),
    path('view-incubation/', views.view_incubation_schedules, name='view_incubation'),
    path("expenses/", expenses_list, name="expenses_list"),
]

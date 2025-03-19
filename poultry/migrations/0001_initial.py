# Generated by Django 5.1.7 on 2025-03-19 19:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chicken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Broiler', 'Broiler'), ('Layer', 'Layer'), ('Kienyeji', 'Kienyeji')], max_length=20)),
                ('quantity', models.PositiveIntegerField()),
                ('age_in_weeks', models.PositiveIntegerField()),
                ('weight_kg', models.FloatField(blank=True, null=True)),
                ('buy_from', models.CharField(choices=[('Local Hatch', 'Local Hatch'), ('Kukuchic', 'Kukuchic'), ('Kenchic', 'Kenchic'), ('Others', 'Others')], max_length=50)),
                ('other_source', models.CharField(blank=True, max_length=100, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Egg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('collected_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Starter Mash', 'Starter Mash'), ('Grower Mash', 'Grower Mash'), ('Layer Mash', 'Layer Mash'), ('Finisher Mash', 'Finisher Mash'), ('Other', 'Other')], default='Other', max_length=100)),
                ('custom_name', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity_kg', models.FloatField()),
                ('remaining_kg', models.FloatField(default=0)),
                ('date_purchased', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncubationSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed', models.CharField(max_length=50)),
                ('incubation_date', models.DateField()),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.CharField(blank=True, max_length=100, null=True)),
                ('medication', models.CharField(blank=True, max_length=200, null=True)),
                ('date_treated', models.DateField()),
                ('chicken', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poultry.chicken')),
            ],
        ),
        migrations.CreateModel(
            name='ImmunizationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(max_length=100)),
                ('date_administered', models.DateField()),
                ('chicken', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poultry.chicken')),
            ],
        ),
        migrations.CreateModel(
            name='MortalityRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_at_death', models.PositiveIntegerField()),
                ('cause_of_death', models.CharField(max_length=200)),
                ('comment', models.TextField(blank=True, null=True)),
                ('date_recorded', models.DateField(auto_now_add=True)),
                ('chicken', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poultry.chicken')),
                ('recorded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Worker', 'Worker')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('date_sold', models.DateField(auto_now_add=True)),
                ('chicken', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='poultry.chicken')),
                ('eggs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='poultry.egg')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('amount', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('related_sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='poultry.sale')),
            ],
        ),
    ]

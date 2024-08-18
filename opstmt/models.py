from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Additional fields for your custom user model
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change the related_name to avoid clashes
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change the related_name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USER_TYPE_CHOICES = (
        ('college', 'College'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class College(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='college_profile')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='students',  null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Company(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.student.user.username} with {self.num_companies} companies in {self.year}"


class Year(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='years')
    year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Year {self.year} fir {self.company.name}"

class Opstmt(models.Model):
    year = models.OneToOneField(Year, related_name='opstmt', on_delete=models.CASCADE)
    net_sales = models.FloatField(default=0)
    sales_domestic = models.FloatField(default=0)
    sales_exports = models.FloatField(default=0)
    others = models.FloatField(default=0)
    total_sales = models.FloatField(default=0)
    opening_stock_finished_goods = models.FloatField(default=0)
    opening_stock_wip = models.FloatField(default=0)  # WIP: Work In Process
    opening_stock_rm = models.FloatField(default=0)  # RM: Raw Material
    purchase_rm = models.FloatField(default=0)
    power_fuel = models.FloatField(default=0)
    direct_labour = models.FloatField(default=0)
    repairs_maintenance = models.FloatField(default=0)
    mfg_direct_expenses = models.FloatField(default=0)
    depreciation = models.FloatField(default=0)
    closing_stock_finished_goods = models.FloatField(default=0)
    closing_stock_wip = models.FloatField(default=0)
    closing_stock_rm = models.FloatField(default=0)
    cost_of_sales = models.FloatField(default=0)
    cost_of_production = models.FloatField(default=0)
    gross_profit_loss = models.FloatField(default=0)
    selling_adm_expenses = models.FloatField(default=0)
    interest_fin_charges = models.FloatField(default=0)
    operating_profit_loss = models.FloatField(default=0)
    other_income_expenses = models.FloatField(default=0)
    add_other_income = models.FloatField(default=0)
    less_other_expenses = models.FloatField(default=0)
    profit_before_tax = models.FloatField(default=0)
    provision_for_taxes = models.FloatField(default=0)
    net_profit_after_tax_loss = models.FloatField(default=0)
    pbd_it = models.FloatField(default=0)
    cash_accruals = models.FloatField(default=0)
    dividend_drawings = models.FloatField(default=0)
    retained_profit = models.FloatField(default=0)
    net_cash_accrual = models.FloatField(default=0)

    def __str__(self):
        return f"{self.year.year} - Opstmt"

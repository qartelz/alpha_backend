from django.contrib import admin
from .models import Student, College, Company
# Register your models here.
admin.site.register(Student)
admin.site.register(Company)

admin.site.register(College)
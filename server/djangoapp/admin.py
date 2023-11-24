from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    '''CarModelInline class'''
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    '''CarModelAdmin class'''
    list_display = ('name',)

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    '''CarMakeAdmin class with CarModelInline'''
    inlines = [CarModelInline]
    list_display = ('name',)

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm

# Register your models here.
admin.site.register(subplans)
admin.site.register(contact)
admin.site.register(live)
admin.site.register(employeecontrol)
admin.site.register(bills)
admin.site.register(food)
admin.site.register(foodplan)
admin.site.register(grocerylist)
admin.site.register(logs)
admin.site.register(dietplan)

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['username', 'mobno', 'gender','height','weight','target',]
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ( 'mobno', 'gender','height','weight','target','diets','playlist','bill','foodplans','lives','log','age')}),
    ) #this will allow to change these fields in admin module


admin.site.register(MyUser, MyUserAdmin)
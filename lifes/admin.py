from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm

# Register your models here.
class subplansAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('plan','price',)

admin.site.register(subplans,subplansAdmin)

class contactAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('email','bookcall','bookapp',)
    search_fields = ('email','mobno',)
    list_filter =('bookapp','bookcall',)

admin.site.register(contact,contactAdmin)

class liveAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('name','slottime','date',)
    search_fields = ('slottime','date',)

admin.site.register(live,liveAdmin)

class empAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('name','mobno','employeetype',)
    search_fields = ('mobno',)
    list_filter =('employeetype','gender',)

admin.site.register(employeecontrol,empAdmin)

class billadmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('name','price',)
    search_fields = ('name',)

admin.site.register(bills,billadmin)

class foodadmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('name','calories',)
    search_fields = ('name','calories',)

admin.site.register(food, foodadmin)

class foodplanadmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(foodplan,foodplanadmin)

class groadmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('name','address',)
    search_fields = ('address',)

admin.site.register(grocerylist,groadmin)

class logadmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(logs,logadmin)

class dietplanadmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(dietplan)

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['username', 'mobno', 'gender','height','weight','target',]
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ( 'mobno', 'gender','height','weight','target','diets','playlist','bill','foodplans','lives','log','age','allot')}),
    ) #this will allow to change these fields in admin module


admin.site.register(MyUser, MyUserAdmin)

class BmiAdmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(bmi, BmiAdmin)

class BmrAdmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(bmr, BmrAdmin)
from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm
from import_export.admin import ImportExportModelAdmin
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
    list_display = ('name',)

admin.site.register(grocerylist,groadmin)

class logadmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(logs,logadmin)

class dietplanadmin(admin.ModelAdmin):
    list_display = ('day',)
    list_per_page = 15

admin.site.register(dietplan,dietplanadmin)

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['username', 'mobno', 'gender','height','weight','target',]
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobno', 'gender','height','weight','target','diets','bill','lives','age','allotnutri','allotdieti','allottrain','sub','bio','location','address','pic','fitness','streaks','steps','fordiet','fornut','forfit')}),
    ) #this will allow to change these fields in admin module


admin.site.register(MyUser, MyUserAdmin)

class BmiAdmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(bmi, BmiAdmin)

class BmrAdmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(bmr, BmrAdmin)

class complaintAdmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(complaint,complaintAdmin)

class requestAdmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(requestchange,requestAdmin)


class equipmentadmin(ImportExportModelAdmin):
    list_per_page = 15

admin.site.register(equipment,equipmentadmin)

class exerciseadmin(ImportExportModelAdmin):
    list_per_page = 15


admin.site.register(exercise,exerciseadmin)

class otpadmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(otpstore,otpadmin)

class quantadmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(quantuser,quantadmin)

class quantyrepssetsadmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(quantyrepssets,quantyrepssetsadmin)


class exerciseplanadmin(admin.ModelAdmin):
    list_display = ['day',]
    list_per_page = 15

admin.site.register(exerciseplan,exerciseplanadmin)

class exlogadmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(exlogs,exlogadmin)

class stepadmim(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(step,stepadmim)

class streakadmin(admin.ModelAdmin):
    list_per_page = 15

admin.site.register(streak,streakadmin)
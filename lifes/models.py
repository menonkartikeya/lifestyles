from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

targets = (
    ('Gain Weight','Gain Weight'),
    ('Stay Fit','Stay Fit'),
    ('Loose Weight','Loose Weight'),
)
types = (
    ('Free Plan','Free Plan'),
    ('Basic Plan','Basic Plan'),
    ('Premium Plan','Premium Plan'),
)
emptype = (
    ('Nutritionist','Nutritionist'),
    ('Dietician','Dietician'),
    ('employee','employee'),
    ('trainee','trainee'),
    ('finance','finance'),
)
gen = (
    ('Male','Male'),
    ('Female','Female'),
    ('Prefer not to say','Prefer not to say'),
)

class food(models.Model):
    pic = models.ImageField()
    name = models.CharField(max_length=100)
    stuff = models.CharField(max_length=10000)
    calories = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    fiber = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manage Food Items!"


class foodplan(models.Model):
    video = models.URLField()
    textrecipe = models.CharField(max_length=10000)
    fooditem = models.OneToOneField(food,on_delete=models.CASCADE,primary_key=True)

    def __str__(self):
        obj = food.objects.get(id=self.fooditem.id)
        return obj.name

    class Meta:
        verbose_name_plural = "Manage Food Plans!"

class dietplan(models.Model):
    breakfast = models.ForeignKey(foodplan,on_delete=models.CASCADE,related_name="Breakfast")
    lunch = models.ForeignKey(foodplan,on_delete=models.CASCADE,related_name="Lunch")
    snacks = models.ForeignKey(foodplan,on_delete=models.CASCADE,related_name="Snacks")
    dinner = models.ForeignKey(foodplan,on_delete=models.CASCADE,related_name="Dinner")
    remarks = models.CharField(max_length=1000,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Manage Diet Plans Issued!"


class bills(models.Model):
    invoicepdf = models.FileField(null=True,blank=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manage Bills!"


class live(models.Model):
    slottime = models.TimeField()
    date = models.DateField()

    def name(self):
        obj = MyUser.objects.get(lives=self.id)
        return obj.username

    class Meta:
        verbose_name_plural = "Check Live Meetings!"

class logs(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Log Questions!"

class MyUser(AbstractUser):
    gender = models.CharField(choices=gen,max_length=50,blank=True,null=True)
    mobno = models.IntegerField(default=0)
    height = models.FloatField(default=0.0,blank=True)
    weight = models.FloatField(default=0.0,blank=True)
    target = models.CharField(choices=targets,max_length=60,blank=True,null=True)
    diets = models.ForeignKey(dietplan, on_delete=models.CASCADE,blank=True,null=True)
    playlist = models.URLField(blank=True,null=True)
    bill = models.ManyToManyField(bills,blank=True)
    foodplans = models.ManyToManyField(foodplan,blank=True)
    lives = models.ManyToManyField(live,blank=True)
    log = models.ManyToManyField(logs,blank=True)
    age = models.IntegerField(blank=True,null=True)
    allot = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "User Details!"

class contact(models.Model):
    email = models.EmailField()
    mobno = models.IntegerField(default=0)
    bookcall = models.BooleanField(null=True,blank=True)
    bookapp = models.BooleanField(null=True,blank=True)
    message = models.CharField(max_length=500)
    check = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Check Contact Entries!"

class employeecontrol(models.Model):
    id = models.OneToOneField(MyUser, on_delete = models.CASCADE,primary_key=True)
    alloted = models.ManyToManyField(MyUser, blank=True, related_name="Alloted_Users")
    mobno = models.IntegerField()
    employeetype = models.CharField(choices=emptype,max_length=100)
    certificate = models.URLField()
    resume = models.URLField()
    gender = models.CharField(choices=gen,max_length=50)

    def name(self):
        obj = MyUser.objects.get(id=self.id.id)
        return obj.username

    class Meta:
        verbose_name_plural = "Check Employees!"

class grocerylist(models.Model):
    id = models.OneToOneField(MyUser,on_delete=models.CASCADE,primary_key=True)
    items = models.CharField(max_length=1000)
    address = models.CharField(max_length=500)
    billitem = models.OneToOneField(bills,on_delete=models.CASCADE,null=True,blank=True)

    def name(self):
        obj = MyUser.objects.get(id=self.id.id)
        return obj.username

    class Meta:
        verbose_name_plural = "Current Grocery Lists!"

class subplans(models.Model):
    allot = models.ManyToManyField(MyUser, blank=True, related_name="Alloted_Subs")
    plan = models.CharField(choices=types,max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.plan
    
    class Meta:
        verbose_name_plural = "Subscription Plans!"


class bmi(models.Model):
    us = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    bmi = models.FloatField(default=0.0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        obj = MyUser.objects.get(id=self.us.id)
        obj1 = "Username - "+obj.username+" Date: "+str(self.date)
        return obj1

    class Meta:
        verbose_name_plural = "BMI INDEX"

class bmr(models.Model):
    us = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    bmr = models.FloatField(default=0.0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        obj = MyUser.objects.get(id=self.us.id)
        obj1 = "Username - "+obj.username+" Date: "+str(self.date)
        return obj1

    class Meta:
        verbose_name_plural = "BMR INDEX"

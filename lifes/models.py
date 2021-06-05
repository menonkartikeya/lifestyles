from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
# Create your models here.

targets = (
    ('Gain Weight','Gain Weight'),
    ('Stay Fit','Stay Fit'),
    ('Loose Weight','Loose Weight'),
)
types = (
    ('Free Plan','Free Plan'),
    ('Basic Plan','Basic Plan'),
    ('Semi-Premium Plan','Semi-Premium Plan'),
    ('Premium Plan','Premium Plan'),
)
emptype = (
    ('Nutritionist','Nutritionist'),
    ('Dietician','Dietician'),
    ('employee','employee'),
    ('Fitness Trainer','Fitness Trainer'),
    ('finance','finance'),
)
gen = (
    ('Male','Male'),
    ('Female','Female'),
    ('Prefer not to say','Prefer not to say'),
)
sizes = (
    ("piece","piece"),
    ("slice","slice"),
    ("Katori","Katori"),
    ("g","g"),
    ("oz","oz"),
    ("cup","cup"),
    ("serving","serving"),
    ("mg","mg"),
)
day = (
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday'),
    ('Sunday','Sunday'),
)
billtypes = (
    ('subscriptions','subscriptions'),
    ('grocery','grocery'),
    ('products','products'),
    ('Other','Other'),
)
meal = (
    ('preworkout','preworkout'),
    ('postworkout','postworkout'),
    ('lunch','lunch'),
    ('snacks','snacks'),
    ('dinner','dinner'),
)
cuisine = (
    ('italian','italian'),
    ('chinese','chinese'),
    ('japanese','japanese'),
    ('indian','indian'),
    ('french','french'),
    ('american','american'),
    ('greek','greek'),
    ('spanish','spanish'),
    ('mediterranean','mediterranean'),
    ('lebanese','lebanese'),
    ('moroccan','moroccan'),
    ('turkish','turkish'),
    ('Thai','Thai'),
    ('Cajun','Cajun'),
    ('mexican','mexican'),
    ('caribbean','caribbean'),
    ('german','german'),
    ('russian','russian'),
    ('hungarian','hungarian'),
)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class food(models.Model):
    pic = models.URLField()
    name = models.CharField(max_length=100)
    stuff = models.CharField(max_length=10000)
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fiber = models.FloatField(default=0)
    unit = models.CharField(choices=sizes,max_length=100)
    tag = models.CharField(max_length=50,choices=cuisine,default="indian")
    time_taken = models.CharField(max_length=10,default="10")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manage Food Items!"


class foodplan(models.Model):
    textrecipe = models.CharField(max_length=10000)
    fooditem = models.OneToOneField(food,on_delete=models.CASCADE,primary_key=True)

    def __str__(self):
        obj = food.objects.get(id=self.fooditem.id)
        return obj.name

    class Meta:
        verbose_name_plural = "Manage Food Plans!"

class equipment(models.Model):
    name = models.CharField(max_length=200)
    image_path = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manage Equipment!"


class exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    muscle_group = models.CharField(max_length=100)
    muscle_worked = models.CharField(max_length=100)
    equipments = models.ManyToManyField(equipment,blank=True)
    video_path = models.URLField(null=True, blank=True)
    image_path = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manage Exercises!"


class exerciseplan(models.Model):
    day = models.CharField(choices=day,max_length=50,default='Monday')
    exercisename = models.ManyToManyField(exercise,related_name="Exercise")
    remarks = models.CharField(max_length=1000,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Manage Excercise PLans Issued!"

class dietplan(models.Model):
    day = models.CharField(choices=day,max_length=50,default='Monday')
    preworkout = models.ManyToManyField(foodplan,related_name="Pre_Workout")
    postworkout = models.ManyToManyField(foodplan,related_name="Post_Workout")
    lunch = models.ManyToManyField(foodplan,related_name="Lunch")
    snacks = models.ManyToManyField(foodplan,related_name="Snacks")
    dinner = models.ManyToManyField(foodplan,related_name="Dinner")
    remarks = models.CharField(max_length=1000,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Manage Diet Plans Issued!"


class bills(models.Model):
    invoicepdf = models.FileField(null=True,blank=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    billtype = models.CharField(choices=billtypes,max_length=1000,default="Other")
    expiry = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manage Bills!"


class subplans(models.Model):
    plan = models.CharField(choices=types,max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.plan
    
    class Meta:
        verbose_name_plural = "Subscription Plans!"

class streak(models.Model):
    points = models.IntegerField(default=0)
    days = models.IntegerField(default=0)

    def __str__(self):
        return self.days
    
    class Meta:
        verbose_name_plural = "Streaks!"


class live(models.Model):
    slottime = models.TimeField()
    date = models.DateField()

    
    def name(self):
        obj = MyUser.objects.get(lives=self.id)
        return obj.username

    class Meta:
        verbose_name_plural = "Check Live Meetings!"

class MyUser(AbstractUser):
    pic = models.ImageField(default='defaultpic.jpg')
    gender = models.CharField(choices=gen,max_length=50,blank=True,null=True)
    mobno = models.BigIntegerField(unique=True)
    height = models.FloatField(default=0.0,blank=True)
    weight = models.FloatField(default=0.0,blank=True)
    target = models.CharField(choices=targets,max_length=60,blank=True,null=True)
    diets = models.ManyToManyField(dietplan,blank=True)
    bill = models.ManyToManyField(bills,blank=True)
    lives = models.ManyToManyField(live,blank=True)
    age = models.IntegerField(blank=True,null=True)
    allotnutri = models.BooleanField(default=False)
    allotdieti = models.BooleanField(default=False)
    allottrain = models.BooleanField(default=False)
    sub = models.ForeignKey(subplans,on_delete=models.CASCADE,blank=True,null=True)
    streaks = models.ForeignKey(streak,on_delete=models.CASCADE,blank=True,null=True)
    bio = models.CharField(max_length=5000,blank=True,null=True)
    location = models.CharField(max_length=100,blank=True,null=True)
    address = models.CharField(max_length=1000,blank=True,null=True)
    fitness = models.ManyToManyField(exerciseplan,blank=True)

    #USERNAME_FIELD = 'mobno'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "User Details!"

class quantuser(models.Model):
    quantity = models.IntegerField(default=1)
    foodit = models.ForeignKey(food,on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    day = models.CharField(choices=day,max_length=50)
    meal = models.CharField(choices=meal,max_length=50)

    class Meta:
        verbose_name_plural = "Quantity Of Food!"

class logs(models.Model):
    preworkout = models.ManyToManyField(foodplan,blank=True,related_name="Pre_work")
    postworkout = models.ManyToManyField(foodplan,blank=True,related_name="Post_work")
    lunch = models.ManyToManyField(foodplan,blank=True,related_name="lunch")
    snacks = models.ManyToManyField(foodplan,blank=True,related_name="snack")
    dinner = models.ManyToManyField(foodplan,blank=True,related_name="dinner")
    date = models.DateField(auto_now_add=True)
    us = models.ForeignKey(MyUser,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Log Meals!"


class contact(models.Model):
    email = models.EmailField()
    mobno = models.BigIntegerField(default=0)
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
    mobno = models.BigIntegerField()
    employeetype = models.CharField(choices=emptype,max_length=100)
    certificate = models.URLField()
    resume = models.URLField()
    gender = models.CharField(choices=gen,max_length=50)

    def name(self):
        obj = MyUser.objects.get(id=self.id.id)
        return obj.username

    class Meta:
        verbose_name_plural = "Check Employees!"


class requestchange(models.Model):
    us = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True,null=True)
    emp = models.ForeignKey(employeecontrol,on_delete=models.CASCADE,blank=True,null=True)
    reason = models.CharField(max_length=10000)
    diet = models.ForeignKey(dietplan,on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name_plural = "User Requests"

class complaint(models.Model):
    us = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    emptype = models.ForeignKey(employeecontrol,on_delete=models.CASCADE)
    reason = models.CharField(max_length=10000)
    check = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "User Complaints"

class grocerylist(models.Model):
    groid = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    items = models.ManyToManyField(food,blank=True)
    billitem = models.OneToOneField(bills,on_delete=models.CASCADE,null=True,blank=True)

    def name(self):
        obj = MyUser.objects.get(id=self.groid.id)
        return obj.username

    class Meta:
        verbose_name_plural = "Current Grocery Lists!"


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
    maintcalo = models.IntegerField(default=0)

    def __str__(self):
        obj = MyUser.objects.get(id=self.us.id)
        obj1 = "Username - "+obj.username+" Date: "+str(self.date)
        return obj1

    class Meta:
        verbose_name_plural = "BMR INDEX"

class otpstore(models.Model):
    mobno = models.BigIntegerField()
    otp = models.BigIntegerField()
    username = models.CharField(max_length=100,blank=True,null=True)
    passw = models.CharField(max_length=100,blank=True,null=True)
    gender = models.CharField(choices=gen,max_length=50,blank=True,null=True)

    class Meta:
        verbose_name_plural = "OTP"

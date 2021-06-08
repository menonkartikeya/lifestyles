from __future__ import division
from typing_extensions import ParamSpecArgs
from django.shortcuts import render,redirect
from django.http import Http404, request
from .models import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import auth
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
import datetime
import _datetime
from django.contrib import messages
from django.db.models.query import EmptyQuerySet
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
import requests
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json
import math, random
from django.utils.datastructures import MultiValueDictKeyError
from itertools import chain
from twilio.rest import Client
from lifestyles.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from django.http import HttpResponse



def index(request): 
    headtitle = "Life Styles | Home"
    user = request.user
    #checks for employee or customer by is_Staff
    if user.is_staff == False:
        #checks for logged in
        if user.is_authenticated:
            usertype = "Customer"
        else:
            #prints None if user is not logged in
            usertype = None
    #check if user is employee and is active 
    elif user.is_active == True and user.is_staff == True:
        try:
            #try getting the employee object from employee table
            emp = employeecontrol.objects.get(id=user)
            #storing employee tye in usertype
            usertype = emp.employeetype
        except ObjectDoesNotExist:
            #if employee object does not exist
            usertype = None

    parms = {
        'title':headtitle,
        'usertype':usertype,
    }
    return render(request,'index.html',parms)

#BMI Calculation Function -- 
def bmicalc(weight,height):
    bmi = (weight/(height**2))
    if bmi < 16:
        state = "Severe Thinness"
    elif bmi > 16 and bmi < 17:
        state = "Moderate Thinness"
    elif bmi > 17 and bmi < 18:
        state = "Mild Thinness"
    elif bmi > 18 and bmi < 25:
        state = "Normal"
    elif bmi > 25 and bmi < 30:
        state = "Overweight"
    elif bmi > 30 and bmi < 35:
        state = "Obese Class I"
    elif bmi > 35 and bmi < 40:
        state = "Obese Class II"
    elif bmi > 40:
        state = "Obese Class III"
    context = [state,bmi]
    return context


#Customer Dashboard - shows customer previous BMI, find its alloted dietician, nutritionist and trainer according to plan
#shows grocery list of that user, meeting links of that user
#Required - streak feature
def dashboard(request):
    title = "Life Styles | Dashboard"
    parms = {
        'title':title,
    }
    user = request.user
    #checks for user logged in and user is not any kind of employee
    if user.is_authenticated and user.is_staff == False:
        #get all bmi object of that particular user and then get the latest bmi of that user
        bmii = bmi.objects.filter(us=user).order_by('-id')[0]
        bmrr = bmr.objects.filter(us=user).order_by('-id')[0]
        if user.allotdieti:
            #get user dietician if he is alloted one.
            finddieti = employeecontrol.objects.get(Q(employeetype="Dietician") & Q(alloted=user))
        else:
            #making that variable none in else part
            finddieti = None
        if user.allotnutri:
            #get user nutritionist if he is alloted one
            findnutri = employeecontrol.objects.get(Q(employeetype="Nutritionist") & Q(alloted=user))
        else:
            #else part making that var none
            findnutri = None
        if user.allottrain:
            #get user trainer if he is alloted one.
            findtrain = employeecontrol.objects.get(Q(employeetype="Fitness Trainer") & Q(alloted=user))
        else:
            #else making that var none
            findtrain = None
        #creating a list for storing grocery items
        grolist = []
        if user.sub.plan != "Free Plan":
            try:
                #trying to check for grocery list object
                grocery = grocerylist.objects.filter(groid=user.id).first()
            #if object does not exist then list will be none
            except ObjectDoesNotExist:
                grocery = None
            #if list is not none then get all the items from that object of grocery and store in list
            if grocery != None:
                grolist = grocery.items.all()
        #get all the meeting objects of that user
        meet = user.lives.all()
        live = []
        emps = []
        usem = []
        for per in meet:
            obj = MyUser.objects.filter(lives=per.id)
            for ob in obj:
                if ob.mobno != user.mobno:
                    emp = employeecontrol.objects.get(id=ob)
                    usem.append(ob)
                    live.append(per)
                    emps.append(emp)
        #make a flag variable for checking if meet object is empty or not
        flag = False
        #if meet count is 0 flag is true
        if meet.count() == 0:
            flag = True
        #if tmp list is empty then we pass these parameters basically bmi is passed as none
        #now code for diet plans.
        currday = datetime.datetime.today().weekday()
        currweek = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        curday = currweek[currday]
        try:
            dietplans = user.diets.get(day=curday)
        except ObjectDoesNotExist:
            dietplans = None
        i = dietplans.preworkout.all()
        premeal = []
        for item in i:
            premeal.append(item)
        j = dietplans.postworkout.all()
        postmeal = []
        for item in j:
            postmeal.append(item)
        lunch = []
        k = dietplans.lunch.all()
        for item in k:
            lunch.append(item)
        snacks = []
        l = dietplans.snacks.all()
        for item in l:
            snacks.append(item)
        m = dietplans.dinner.all()
        dinner = []
        for item in m:
            dinner.append(item)
        d = datetime.date.today()
        try:
            logg = logs.objects.get(Q(date=d) & Q(us=user))
        except ObjectDoesNotExist:
            logg = logs.objects.create(us=user,date=d)
        #lunch
        freelunch = []
        loglunch = logg.lunch.all()
        for i in lunch:
            if i not in loglunch:
                freelunch.append(i)
        #premeal
        freepre = []
        logpre = logg.preworkout.all()
        for i in premeal:
            if i not in logpre:
                freepre.append(i)
        #postmeal
        freepost = []
        logpost = logg.postworkout.all()
        for i in postmeal:
            if i not in logpost:
                freepost.append(i)
        #snacks
        freesnacks = []
        logsnacks = logg.snacks.all()
        for i in snacks:
            if i not in logsnacks:
                freesnacks.append(i)
        #dinner
        freedinner = []
        logdinner = logg.dinner.all()
        for i in dinner:
            if i not in logdinner:
                freedinner.append(i)
        #exercise
        try:
            exe = user.fitness.get(day=curday)
            exena = exe.exercisename.all()
            freeex = []
            try:
                exlog = exlogs.objects.get(Q(date=d) & Q(us=user))
            except exlogs.DoesNotExist:
                exlog = exlogs.objects.create(us=user,date=d)
            logex = exlog.exercisename.all()
            for i in exena:
                if i not in logex:
                    freeex.append(i)
        except ObjectDoesNotExist:
            exe = None
            freeex = []
            logex = []
        if request.method == "POST":
            if 'yess' in request.POST:
                tag = request.POST['tag']
                if tag == 'Lunch':
                    l = list(set(chain(freelunch,loglunch)))
                    for i in l:
                        try:
                            check = request.POST["l"+str(i.fooditem)]
                            if check == "on":
                                if i not in loglunch:
                                    logg.lunch.add(i)
                                    logg.save()
                                    messages.success(request,"Added to logs")
                        except MultiValueDictKeyError:
                            logg.lunch.remove(i)
                            logg.save()
                    return redirect("dashboard")
                if tag == "Pre workout meal":
                    l = list(set(chain(freepre,logpre)))
                    for i in l:
                        try:
                            check = request.POST["pr" + str(i.fooditem)]
                            if check == "on":
                                if i not in logpre:
                                    logg.preworkout.add(i)
                                    logg.save()
                                    messages.success(request,"Added to logs")
                        except MultiValueDictKeyError:
                            logg.preworkout.remove(i)
                            logg.save()
                    return redirect("dashboard")
                if tag == "Post workout meal":
                    l = list(set(chain(freepost,logpost)))
                    for i in l:
                        try:
                            check = request.POST["po" + str(i.fooditem)]
                            if check == "on":
                                if i not in logpost:
                                    logg.postworkout.add(i)
                                    logg.save()
                                    messages.success(request,"Added to logs")
                        except MultiValueDictKeyError:
                            logg.postworkout.remove(i)
                            logg.save()
                    return redirect("dashboard")
                if tag == "Snacks":
                    l = list(set(chain(freesnacks,logsnacks)))
                    for i in l:
                        try:
                            check = request.POST["s" + str(i.fooditem)]
                            if check == "on":
                                if i not in logsnacks:
                                    logg.snacks.add(i)
                                    logg.save()
                                    messages.success(request,"Added to logs")
                        except MultiValueDictKeyError:
                            logg.snacks.remove(i)
                            logg.save()
                    return redirect("dashboard")
                if tag == "Dinner":
                    l = list(set(chain(freedinner,logdinner)))
                    for i in l:
                        try:
                            check = request.POST["d" + str(i.fooditem)]
                            if check == "on":
                                if i not in logdinner:
                                    logg.dinner.add(i)
                                    logg.save()
                                    messages.success(request,"Added to logs")
                        except MultiValueDictKeyError:
                            logg.dinner.remove(i)
                            logg.save()
                    return redirect("dashboard")
            if 'exyes' in request.POST:
                l = list(set(chain(freeex,logex)))
                for i in l:
                    try:
                        check = request.POST[str(i.id)]
                        if check == "on":
                            if i not in logex:
                                exlog.exercisename.add(i)
                                exlog.save()
                                messages.success(request,"Added to Exercise logs")
                    except MultiValueDictKeyError:
                        exlog.exercisename.remove(i)
                        exlog.save()
                return redirect("dashboard")
        parms = {
            'title':"DASHBOARD | KOWI Lifestyles",
            'bmi':bmii,
            'bmr':bmrr,
            'grolist':grolist,
            'zip':zip(emps,live,usem),
            'flag':flag,
            'findnutri':findnutri,
            'finddieti':finddieti,
            'findtrain':findtrain,
            'curday':curday,
            'dietplans':dietplans,
            'premeal':freepre,
            'logpre':logpre,
            'postmeal':freepost,
            'logpost':logpost,
            'lunch':freelunch,
            'loglunch':loglunch,
            'snacks':freesnacks,
            'logsnacks':logsnacks,
            'dinner':freedinner,
            'logdinner':logdinner,
            'date':d,
            'exer':freeex,
            'logex':logex,
        }
        return render(request,'dashboard.html',parms)
    #if user is not logged in then it will redirect to login
    else:
        return redirect(login)
    
    return render(request,'dashboard.html',parms)

##Login / Signup ###
#logout function 
def logoutuser(request):
    logout(request)
    return redirect('login')

#activate email sending function!
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


#login function
def login(request):
    title = "Login | Lifestyles"
    if request.method == 'POST':
        #login with username and password
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        #checking for one more condition that is_staff is false or not to prevent employees to login as customer.
        if user is not None and user.is_staff == False:
            auth.login(request,user)
            messages.info(request,'Logged In Successfuly')
            #redirects to dashboard
            return redirect('dashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    return render(request,'login.html',{'title':title})

#login for any type of employee!
def elogin(request):
    title = "Employee Login | lifeStyles"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        #checking for is_staff and is_active for true to make sure its a active employee.
        if user is not None and user.is_staff == True and user.is_active == True:
            auth.login(request,user)
            messages.info(request,'Logged In')
            #after logging in redirect to edashboard
            return redirect('edashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('elogin')

    else:
        return render(request,'elogin.html',{'title':title})

#signup for customer only
def signup(request):
    title = "Register | LifeStyles"
    if request.method == 'POST':
        #signing up with all these fields
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        gender = request.POST['gender']
        height = request.POST['height']
        weight = request.POST['weight']
        subscription = request.POST['subscription']
        target = request.POST['target']
        mobno = request.POST['mobno']
        age = request.POST['age']
        if password1 == password2:
            if MyUser.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            elif MyUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            else:
                user = MyUser.objects.create_user(username=username,password=password1,email=email,gender=gender,height=height,weight=weight,target=target,mobno=mobno,age=age,sub=subscription).save()
                user = auth.authenticate(username=username,password=password1)
                auth.login(request,user)
                #sending verification mail!
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.info(request,'Check email and Verify your account')
                #after that return to index
                return redirect(index)
        else:
            messages.info(request,'Password not matched')
            return redirect('signup')
    return render(request,'signup.html',{'title':title})


#sign up for any kind of Employee
def esignup(request):
    title = "Register | LifeStyles"
    if request.method == 'POST':
        #sign up fields for any kind of employee
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        gender = request.POST['gender']
        mobno = request.POST['mobno']
        employeetype = request.POST['employeetype']
        resume = request.POST['resume']
        certificate = request.POST['certificate']
        if password1 == password2:
            if MyUser.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('esignup')
            elif MyUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('esignup')
            else:
                user = MyUser.objects.create_user(username=username,password=password1,email=email).save()
                user.is_active = False
                user.save()
                employee = employeecontrol.objects.create(id=user,gender=gender,certificate=certificate,resume=resume,employeetype=employeetype,mobno=mobno)
                #manual verification in case of employees
                messages.info(request,'We will Verify and mail You with the details!')
                return redirect(index)
        else:
            messages.info(request,'Password not matched')
            return redirect('esignup')
    return render(request,'esignup.html',{'title':title})

##########################################

#dashboard for Employee!
def edashboard(request):
    title = "Employee Dashboard | LifeStyles"
    user = request.user
    try:
        employee = employeecontrol.objects.get(id=user)
    except:
        messages.error(request,"Nope,You are not our Employee, Sorry!")
        return redirect(index)
    if user.is_authenticated and user.is_staff == True and user.is_active == True and employee.employeetype == 'employee':
        users = MyUser.objects.all()
        lives = user.lives.all()
        emptype = employee.employeetype
        unaln = []
        unald = []
        unalf = []
        for us in users:
            if us.is_staff == False:
                if us.allotnutri == False:
                    if us.sub == 'Basic Plan' or us.sub == 'Semi-Premium Plan' or us.sub == 'Premium Plan':
                        unaln.append(us)
                if us.allotdieti == False:
                    if us.sub == 'Premium Plan' or us.sub == 'Semi-Premium Plan':
                        unald.append(us)
                if us.sub == 'Basic Plan' or us.sub == 'Semi-Premium Plan' or us.sub == 'Premium Plan':
                    unalf.append(us)
        totpeeps = employeecontrol.objects.filter(Q(employeetype="Dietician") | Q(employeetype="Nutritionist") | Q(employeetype="Dietician"))[:5]
        freepeeps = []
        for peep in totpeeps:
            counter = peep.alloted.count()
            if counter <= 25:
                freepeeps.append(peep)
        contacted = contact.objects.filter(check=False)
        complaints = complaint.objects.filter(check=False)
        if request.method == "POST":
            check = request.POST['check']
            cid = request.POST['id']
            obj = complaint.objects.get(id=cid)
            if check=="on":
                obj.check = True
            else:
                obj.check = False
            obj.cid = cid
            obj.save()
            return redirect('edashboard')
        parms = {
            'title':title,
            'employee':employee,
            'emptype':emptype,
            'unaln':unaln,
            'unald':unald,
            'unalf':unalf,
            'freepeeps':freepeeps,
            'contacted':contacted[:5],
            'lives':lives,
            'complaint':complaints,
            }
        return render(request,'edashboard.html',parms)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    return render(request,'edashboard.html',{'title':title})

#profile for customer
def profile(request,id):
    title = "Profile | Lifestyles"
    user = request.user
    #check for user logged in
    if user.is_authenticated:
        #check user accessing the profile page is same user passsed in id or not
        if user.id == id:
            #check user is active or not
            if user.is_active == True:
                if request.method == 'POST':
                    if request.FILES['pic']:
                        myfile = request.FILES['pic']
                        fs = FileSystemStorage()
                        filename = fs.save(myfile.name, myfile)
                        user.pic = fs.url(filename)
                    if 'myprofile' in request.POST:
                        user.height = request.POST['height']
                        user.weight = request.POST['weight']
                        user.target = request.POST['target']
                        user.age = request.POST['age']
                        gender = request.POST['exampleRadios']
                        user.gender = gender
                        #checking user sub plans and then taking values ##from html if he wants to change or not!
                        if user.sub.plan == 'Basic Plan':
                            checknutri = request.POST['checknutri']
                            checkfitness = request.POST['checkfit']
                            if checknutri == "yes":
                                resnut = request.POST['resnut']
                                user.allotnutri = False
                                findnut = employeecontrol.objects.get(Q(employeetype="Nutritionist") & Q(alloted=user))
                                findnut.alloted.remove(user)
                                complaint.objects.create(us=user,emptype=findnut,reason=resnut)
                            if checkfitness == "yes":
                                resfit = request.POST['resfit']
                                user.allottrain = False
                                findfit = employeecontrol.objects.get(Q(employeetype="Fitness Trainer") & Q(alloted=user))
                                findfit.alloted.remove(user)
                                complaint.objects.create(us=user,emptype=findfit,reason=resfit)
                        if user.sub.plan == "Semi-Premium Plan" or user.sub.plan == "Premium Plan":
                            checkdieti = request.POST['checkdieti']
                            checknutri = request.POST['checknutri']
                            checkfitness = request.POST['checkfit']
                            if checknutri == "yes":
                                resnut = request.POST['resnut']
                                user.allotnutri = False
                                findnut = employeecontrol.objects.get(Q(employeetype="Nutritionist") & Q(alloted=user))
                                findnut.alloted.remove(user)
                                complaint.objects.create(us=user,emptype=findnut,reason=resnut)
                            if checkfitness == "yes":
                                resfit = request.POST['resfit']
                                user.allottrain = False
                                findfit = employeecontrol.objects.get(Q(employeetype="Fitness Trainer") & Q(alloted=user))
                                findfit.alloted.remove(user)
                                complaint.objects.create(us=user,emptype=findfit,reason=resfit)
                            if checkdieti == "yes":
                                resdiet = request.POST['resdiet']
                                user.allotdieti = False
                                finddieti = employeecontrol.objects.get(Q(employeetype="Dietician") & Q(alloted=user))
                                finddieti.alloted.remove(user)
                                complaint.objects.create(us=user,emptype=finddieti,reason=resdiet)
                    if 'personal' in request.POST:
                        user.first_name = request.POST['firstname']
                        user.last_name = request.POST['lastname']
                        user.mobno = request.POST['mobno']
                        user.email = request.POST['email']
                        user.bio = request.POST.get('bio')
                        user.address = request.POST['address']
                    user.save()
                    messages.success(request,"Changes Saved")
                    #return redirect('profile',user.id)
            else:
                messages.error(request,"Verify Account First")
                return redirect('dashboard')
    else:
        messages.error(request,"Login first")
        return redirect('login')
                    
    parms = {
        'title':title,
    }
    return render(request,'profile.html', parms)

#Employee profile! -- Right now it can be used by other employee types too!
def eprofile(request,id):
    title = "E-Profile | Lifestyles"
    user = request.user
    if user.is_authenticated and user.id == id and user.is_staff == True and user.is_active == True:
        findemp = employeecontrol.objects.get(id=user)
    parms = {
        'title':title,
        'emp':findemp,
    }
    return render(request,'eprofile.html', parms)

# @background(schedule=2629746)
# def unsubscribe_user(user_id,bill_id):
#     user = MyUser.objects.get(id=user_id)
#     bill = MyUser.bill.get(id=bill_id)
#     bill.expiry = True
#     user.email_user("Plan Expired","Your Subscription Plan Expired, Please Change Your Plan!")
#     bill.save()
    

#invoices function right now it just renders a html page!
def invoices(request,id):
    title = "Invoices | Lifestyles"
    user = request.user
    if user.is_authenticated and user.id == id and user.is_staff == False and user.is_active == True:
        lastthree = user.bill.filter(paid=True).order_by('-id')[:3][::-1]
        subbill = user.bill.filter(Q(paid=True) & Q(expiry=False) & Q(billtype="subscriptions"))
        duedate = []
        for bill in subbill:
            a = int(bill.date.strftime('%Y%m%d'))
            a_string = str(a)
            a_length = len(a_string)
            c = int(a_string[a_length - 2: a_length])
            b = _datetime.date.today()
            a_strings = str(b)
            a_lengths = len(a_strings)
            d = int(a_strings[a_lengths - 2: a_lengths])
            duedate.append((c+30)-d)
        grocery = grocerylist.objects.filter(groid=user.id)
        paid = []
        unpaid = []
        unpaidtot = 0
        unpaidprod = 0
        for gro in grocery:
            if gro.billitem.paid == True:
                paid.append(gro)
            else:
                unpaid.append(gro)
                unpaidtot+=gro.billitem.price
        unprodbill = user.bill.filter(Q(paid=False) & Q(expiry=False) & Q(billtype="products"))
        for i in unprodbill:
            unpaidprod+=i.price
        prodbill = user.bill.filter(Q(paid=True) & Q(expiry=True) & Q(billtype="products"))
    parms = {
        'title':title,
        'lastthree':lastthree,
        'duedate':duedate,
        'paid':paid,
        'unpaid':unpaid,
        'unpaidtot':unpaidtot,
        'unpaidprod':unpaidprod,
        'unprodbill':unprodbill,
        'prodbill':prodbill,
    }
    return render(request,'invoice.html',parms)


#Lives function -- right now it redirects to video chat application and if user is not logged in it will tell a 404 error
def lives(request):
    user = request.user
    if user.is_authenticated and user.is_active == True:
        return redirect('https://test-chat-web-android.web.app/')
    else:
        return render(request,'404.html')


#book function used by all employee types and customers too to book a slot time and date for user. 
#needs updating time feature to have slots!
def book(request):
    title = "Book Appointment | Lifestyles"
    user = request.user
    #checking user is logged in or not!
    if user.is_authenticated:
        #chcking for employee type
        if user.is_staff == True and user.is_active == True:
            #if its a employee then flag is set to true
            flag = True
            #get employee details
            findemp = employeecontrol.objects.get(id=user)
            #get employee alloted users
            allot = findemp.alloted.all()
            #checking if employee is any of the three types then only invoke the booking functionality
            if findemp.employeetype == "Nutritionist" or findemp.employeetype == "Dietician" or findemp.employeetype == "Fitness Trainer":
                if request.method == 'POST':
                    #for these three employees one more form field will be userid to send book appointment to that user.
                    userid = request.POST['userid']
                    slottime = request.POST['slottime']
                    date = request.POST['date']
                    #creating a live model object
                    obj = live.objects.create(id=userid,slottime=slottime,date=date)
                    conf = MyUser.objects.get(id=userid)
                    #adding that live object to that user
                    conf.lives.add(obj.id)
                    #adding that live object to our employee user too!
                    user.lives.add(obj.id)
                    #sending success message
                    messages.success(request,"Success")
                    return redirect(edashboard)
        #when user is customer
        elif user.is_staff == False:
            #user is customer so flag is set to false
            flag = False
            allot = None
            if user.sub.plan != "Free Plan":
                if request.method == "POST":
                    #booking for which type of user
                    bookfor = request.POST['bookfor']
                    slottime = request.POST['slottime']
                    date = request.POST['date']
                    #find that employee
                    findemp = employeecontrol.objects.get(Q(alloted=user) & Q(employeetype=bookfor))
                    allot = findemp.alloted.all()
                    #getting the user id of that employee
                    getus = MyUser.objects.get(username=findemp.id)
                    #creating live object
                    obj = live.objects.create(slottime=slottime,date=date)
                    #adding this live object to user
                    user.lives.add(obj.id)
                    #addling this live object to that employee user id
                    getus.lives.add(obj.id)
                    messages.success(request,"Success")
                    return redirect(dashboard)
            else:
                messages.error(request,"Change to a Paid Plan First!")
                return redirect('dashboard')
    else:
        return redirect(login)
    parms = {
        "title":title,
        'flag':flag,
        'allot':allot,
        'date':datetime.date.today(),
    }

    return render(request,'book.html',parms)

#bmi calculator -- 
def bmic(request):
    headtitle = "BMI | Lifestyles"
    bmii =0.0
    user = request.user
    state = ""
    if user.is_authenticated:
        bmii = bmi.objects.filter(us=user).order_by('-id')[0]
        bmiobjlist = bmi.objects.filter(us=user)
        bmilist = []
        bmidate = []
        bf = bmii.bodyfat
        for i in bmiobjlist:
            bmilist.append(i.bmi)
            bmidate.append(i.date)
        if bmii.bmi<=16.0:
            state = "Severe Thinness"
        elif bmii.bmi>16.0 and bmii.bmi<=17.0:
            state = "Moderate Thinness"
        elif bmii.bmi > 17.0 and bmii.bmi <= 18.0:
            state = "Mild Thinness"
        elif bmii.bmi > 18.0 and bmii.bmi <= 25.0:
            state = "Normal"
        elif bmii.bmi > 25.0 and bmii.bmi <= 30.0:
            state = "Overweight"
        elif bmii.bmi > 30.0 and bmii.bmi <= 35.0:
            state = "Obese Class I"
        elif bmii.bmi > 35.0 and bmii.bmi <= 40.0:
            state = "Obese Class II"
        elif bmii.bmi > 40.0:
            state = "Obese Class III"
        if request.method=="POST":
            weight_metric = request.POST.get("weight-metric")
            weight_imperial = request.POST.get("weight-imperial")

            if weight_metric:
                weight = float(request.POST.get("weight-metric"))
                height = float(request.POST.get("height-metric"))
            elif weight_imperial:
                weight = float(request.POST.get("weight-imperial"))/2.205
                height = (float(request.POST.get("feet"))*30.48 + float(request.POST.get("inches"))*2.54)/100
            cont = []
            cont = bmicalc(weight,height)
            bmii = cont[1]
            state = cont[0]
            user.weight = weight
            user.height = height
            if user.gender == "Female":
                bf = (1.20*bmii)+(0.23*user.age)-5.4
            elif user.gender == "Male":
                bf = (1.20*bmii)+(0.23*user.age)-16.2
            bmi.objects.create(us=user,bmi=round(bmii),bodyfat=bf,date=datetime.date.today())
            user.save()
            return redirect('bmic')
    parms = {
        'title':headtitle,
        'bmi':bmii,
        'bf':bf,
        'state':state,
        'bmilist':json.dumps(bmilist),
        'bmidate':json.dumps(bmidate,indent=4, sort_keys=True, default=str),
    }
    return render(request,'bmi.html',parms)



#subs plan -- will be added in future only rendering subs page right now
def subs(request):
    title = "Subs Plan | Lifestyles"
    parms = {
        'title':title,
    }
    return render(request,'sub.html',parms)

#growth page rendered only in this.
def growth(request,id):
    try:
        userr = MyUser.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request,'404.html')
    user = request.user
    if user.is_authenticated == True:
        if (user.id == id) or (user.is_staff == True and user.is_active == True):
            if user.is_staff:
                flag = True
            else:
                flag = False
            title = "Growth | Lifestyles"
            bmii = bmi.objects.filter(us=userr).order_by('-id')[0]
            bmrr = bmr.objects.filter(us=userr).order_by('-id')[0]
            bmiobjlist = bmi.objects.filter(us=userr)
            bmilist = []
            bmidate = []
            for i in bmiobjlist:
                bmilist.append(i.bmi)
                bmidate.append(i.date)
            bmrobjlist = bmr.objects.filter(us=userr)
            bmrlist = []
            bmrdate = []
            for i in bmrobjlist:
                bmrlist.append(i.bmr)
                bmrdate.append(i.date)
            parms = {
                'title':title,
                'bmi':bmii,
                'bmr':bmrr,
                'flag':flag,
                'bmilist':json.dumps(bmilist),
                'bmidate':json.dumps(bmidate,indent=4, sort_keys=True, default=str),
                'bmrlist':json.dumps(bmrlist),
                'bmrdate':json.dumps(bmrdate,indent=4, sort_keys=True, default=str),
            }
        else:
            messages.error(request,'Not authorized')
            return redirect('login')
    else:
        return redirect('login')
    return render(request,'growth.html',parms)

#grocery function according to user id!
def grocery(request,id):
    title = "Grocery | Lifestyles"
    user = request.user
    #confirming user is authenticated and only that particular user id is accessing its id.
    if user.is_authenticated and user.id == id:
        try:
            #getting that grocery object
            grocery = grocerylist.objects.filter(groid=user.id)
            paid = []
            unpaid = []
            unpaidtot = 0
            for gro in grocery:
                if gro.billitem.paid == True:
                    paid.append(gro)
                else:
                    unpaid.append(gro)
                    unpaidtot+=gro.billitem.price
        except ObjectDoesNotExist:
            return render(request,'404.html')
    parms = {
        'title':title,
        'grocery':grocery,
        'paid':paid,
        'unpaid':unpaid,
        'unpaidtot':unpaidtot,
    }
    return render(request,'grocery.html',parms)


#allocate function to allocate unallocated customers to free dieticians nutritionist and trainers.
def allocate(request,id):
    title = "Allocate | Lifestyles"
    user = request.user
    #getting the emp object
    try:
        emp = employeecontrol.objects.get(id=user)
    except ObjectDoesNotExist:
        return render(request,'404.html')
    #security checking for employee.
    if user.is_authenticated and user.is_staff == True and user.is_active == True and emp.employeetype == 'employee':
        #getting the target user to allocate
        target = MyUser.objects.get(id=id)
        #creating lists for storing free nutritionist dietician and trainers/
        freenutpeeps = []
        freefitpeeps = []
        freediepeeps = []
        #if conditions to check for user subscription plan.
        if target.sub.plan == 'Free Plan':
            messages.error(request,"User subbed to Free Plan, Not Applicable!")
            return redirect(edashboard)
        elif target.sub.plan == 'Basic Plan':
            #if fitness trainer is not alloted to that user
            if target.allottrain == False:
                totfitpeeps = employeecontrol.objects.filter(employeetype="Fitness Trainer")
                #get free fitness trainers in list
                for peep in totfitpeeps:
                    counter = peep.alloted.count()
                    if counter <= 100:
                        freefitpeeps.append(peep)
            #if nutritionist is not alloted to user
            if target.allotnutri == False:
                totnutpeeps = employeecontrol.objects.filter(employeetype="Nutritionist")
                for peep in totnutpeeps:
                    counter = peep.alloted.count()
                    if counter <= 50:
                        freenutpeeps.append(peep)
        #if he has dieitician too
        elif target.sub.plan == 'Semi-Premium Plan' or target.sub.plan == 'Premium Plan':
            if target.allottrain == False:
                totfitpeeps = employeecontrol.objects.filter(employeetype="Fitness Trainer")
                for peep in totfitpeeps:
                    counter = peep.alloted.count()
                    if counter <= 100:
                        freefitpeeps.append(peep)
            if target.allotnutri == False:
                totnutpeeps = employeecontrol.objects.filter(employeetype="Nutritionist")
                for peep in totnutpeeps:
                    counter = peep.alloted.count()
                    if counter <= 50:
                        freenutpeeps.append(peep)
            if target.allotdieti == False:
                totdiepeeps = employeecontrol.objects.filter(employeetype="Dietician")
                for peep in totdiepeeps:
                    counter = peep.alloted.count()
                    if counter <= 25:
                        freediepeeps.append(peep)     
        else:
            return render(request,'404.html')
        #form code to allocate the user!
        if request.method == 'POST':
            if target.sub.plan == 'Basic Plan':
                if target.allottrain == False:
                    fit = request.POST['fit']
                else:
                    fit = None
                if target.allotnutri == False:
                    nut = request.POST['nut']
                else:
                    nut = None
                if fit:
                    getus = MyUser.objects.get(username=fit)
                    getuser = employeecontrol.objects.get(id=getus.id)
                    getuser.alloted.add(id)
                    target.allottrain = True
                    target.save()
                    messages.success(request,'Fitness Trainer Added')
                if nut:
                    getus = MyUser.objects.get(username=nut)
                    getuser = employeecontrol.objects.get(id=getus.id)
                    getuser.alloted.add(id)
                    target.allotnutri = True
                    target.save()
                    messages.success(request,'Nutritionist Added')
            elif target.sub.plan == 'Semi-Premium Plan' or target.sub.plan == 'Premium Plan':
                if target.allotdieti == False:
                    diet = request.POST['diet']
                else:
                    diet = None
                if target.allottrain == False:
                    fit = request.POST['fit']
                else:
                    fit = None
                if target.allotnutri == False:
                    nut = request.POST['nut']
                else:
                    nut = None
                if fit:
                    getus = MyUser.objects.get(username=fit)
                    getuser = employeecontrol.objects.get(id=getus.id)
                    getuser.alloted.add(id)
                    target.allottrain = True
                    target.save()
                    messages.success(request,'Fitness Trainer Added')
                if nut:
                    getus = MyUser.objects.get(username=nut)
                    getuser = employeecontrol.objects.get(id=getus.id)
                    getuser.alloted.add(id)
                    target.allotnutri = True
                    target.save()
                    messages.success(request,'Nutritionist Added')
                if diet:
                    getus = MyUser.objects.get(username=diet)
                    getuser = employeecontrol.objects.get(id=getus.id)
                    getuser.alloted.add(id)
                    target.allotdieti = True
                    target.save()
                    messages.success(request,'Dietician Added')
            else:
                messages.error(request,'Error, User not Subscribed!')
        parms = {
                'title':title,
                'target':target,
                'freediepeeps':freediepeeps,
                'freenutpeeps':freenutpeeps,
                'freefitpeeps':freefitpeeps,
        } 
    else:
        messages.error(request,"Not Authorized!")
        return render(request,'404.html')
    return render(request, 'allocate.html',parms)

#contact us fucntion to render the html
def contactus(request):
    title = "Contact | Lifestyles"
    parms = {
        "title":title,
    }
    return render(request,'contact.html',parms)

#check contact entries for employee
def contactchecker(request):
    title = "Check Contact | Lifestyles"
    user = request.user
    if user.is_authenticated and user.is_staff == True and user.is_active == True:
        contacts = contact.objects.filter(check=False)
    else:
        messages.error(request,"Not Authorized")
    parms = {
        "title":title,
        'contacts':contacts,
    }
    return render(request,'contactchecker.html',parms)

#get the specific contact entry!
def contid(request,id):
    title = "Check Contact | Lifestyles"
    user = request.user
    if user.is_authenticated and user.is_staff == True and user.is_active == True:
        cont = contact.objects.get(id=id)
        if request.method == "POST":
            cont.check = True
            cont.save()
            messages.success(request,"Checked")
            return redirect(contactchecker)
    else:
        messages.error(request,"Not Authorized")
    parms = {
        "title":title,
        'cont':cont,
    }
    return render(request,'contid.html',parms)


#get unallocated users for employee and shows free diet, nut and fitness
def unalo(request,emptype):
    title = "Unallocated | KOWI"
    user = request.user
    try:
        emp = employeecontrol.objects.get(id=user)
    except ObjectDoesNotExist:
        return render(request,'404.html')
    
    if user.is_authenticated and user.is_staff == True and user.is_active == True and emp.employeetype == 'employee':
        users = MyUser.objects.all()
        unal = []
        for us in users:
            if emptype == 'Dietician':
                if us.is_staff == False and us.allotdieti == False:
                    if us.sub == 'Semi-Premium Plan' or us.sub == 'Premium Plan':
                        unal.append(us)
            elif emptype == 'Nutritionist':
                if us.is_staff == False and us.allotnutri == False:
                    unal.append(us)
            elif emptype == 'Fitness Trainer':
                if us.is_staff == False and us.allottrain == False:
                    unal.append(us)
        totpeeps = employeecontrol.objects.filter(employeetype=emptype)
        freepeeps = []
        for peep in totpeeps:
            counter = peep.alloted.count()
            if emptype == 'Dietician':
                if counter <= 25:
                    freepeeps.append(peep)
            elif emptype == 'Nutritionist':
                if counter <= 50:
                    freepeeps.append(peep)
            elif emptype == 'Fitness Trainer':
                if counter <= 100:
                    freepeeps.append(peep)
    parms = {
        "title":title,
        'unal':unal,
        'freepeeps':freepeeps,
        'emptype':emptype,
    }
    return render(request,'unalo.html',parms)

#bmr calculate
def bmrmain(weight,height,age,gender,status):
    heightincm=height*100
    if gender == 'male' or gender == 'Male':
        bmr=66.47+(13.75*weight)+(5.003*heightincm)-(6.755*age)
        if status == 'sedentary(little or no exercise':
            ans = bmr * 1.1
        elif status == 'lightly active (light exercise/sports 1-3 days/week)':
            ans = bmr * 1.275
        elif status == 'moderately active (moderate exercise/sports 3-5 days/week)':
            ans = bmr * 1.35
        elif status == 'very active (hard exercise/sports 6-7 days a week)':
            ans = bmr * 1.525
    elif gender == 'female' or gender == 'Female':
        bmr=655.1+(9.563*weight)+(1.85*heightincm)-(4.676*age)
        if status == 'sedentary (little or no exercise)':
            ans = bmr * 1.1
        elif status == 'lightly active (light exercise/sports 1-3 days/week)':
            ans = bmr * 1.275
        elif status == 'moderately active (moderate exercise/sports 3-5 days/week)':
            ans = bmr * 1.35
        elif status == 'very active (hard exercise/sports 6-7 days a week)':
            ans = bmr * 1.525
    return ans

#bmr calculater!
def bmrcal(request):
    headtitle = "Life Styles | Bmr"
    user = request.user
    bmrr =0.0
    if user.is_authenticated:
        bmrr = bmr.objects.filter(us=user).order_by('-id')[0]
        bmrobjlist = bmr.objects.filter(us=user)
        bmrlist = []
        bmrdate = []
        for i in bmrobjlist:
            bmrlist.append(i.bmr)
            bmrdate.append(i.date)
        if request.method=="POST":
            weight_metric = request.POST.get("weight-metric")
            weight_imperial = request.POST.get("weight-imperial")
            
            if weight_metric:
                weight = float(request.POST.get("weight-metric"))
                height = float(request.POST.get("height-metric"))
                age = int(request.POST.get("age-metric"))
                gender = str(request.POST.get("gender-metric"))
                status = str(request.POST.get("status-metric"))
            elif weight_imperial:
                weight = float(request.POST.get("weight-imperial"))/2.205
                height = (float(request.POST.get("feet"))*30.48 + float(request.POST.get("inches"))*2.54)/100
                age = int(request.POST.get("age-imperial"))
                gender = str(request.POST.get("gender-imperial")) 
                status = str(request.POST.get("status-imperial"))       
            cont = bmrmain(weight,height,age,gender,status)
            bmrr = cont
            user = request.user
            bmr.objects.create(us=user,bmr=round(bmrr),date=datetime.date.today())
            user.weight = weight
            user.height = height
            user.age = age
            user.gender = gender
            user.status = status
            user.save()
            return redirect('bmrcal')
    parms = {
        'title':headtitle,
        'bmr':bmrr,
        'bmrlist':json.dumps(bmrlist),
        'bmrdate':json.dumps(bmrdate,indent=4, sort_keys=True, default=str),
    }
    return render(request,'bmrmain.html',parms)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def foodapi(request):
    if request.method == 'GET':
        foods = food.objects.all()
        serializers = foodSerializer(foods,many=True)
        return Response(serializers.data)

# def callfoodapi(request):
#     resp = requests.get('http://127.0.0.1:8000/api/food/',headers={'Authorization':'Token deb22ecbedae623617daca421564a28e04186826'})
#     data = resp.json()
#     return JsonResponse(data,safe=False)


# @api_view(['POST',])
# @permission_classes([])
# def registration_view(request):
#     if request.method == "POST":
#         serializer = RegistrationSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = "Succesfully registered a new user"
#             data['mobno'] = user.mobno
#             token = Token.objects.get(user=user).key
#             data['token'] = token
#         else:
#             data = serializer.errors
        
#         return Response(data)
def sendsms(mobno,otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = "message=KOWI OTP-"+str(otp)+"&language=english&route=q&numbers="+str(mobno)
    headers = {
        'authorization': "ShUlFNBv1LRkpbq4yO8HJcma0W5jzAsYrgod6D9TVfneIZM723PerB2DK5iMEVsCuxX41AcOmvL36w7U",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    r = response.json()
    state = r['return']
    return state

def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
  
    return OTP

@api_view(['POST',])
@permission_classes([])
def reg_view(request):
    if request.method == 'POST':
        serializer = RegSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            username = serializer.validated_data['username']
            mobno = serializer.validated_data['mobno']
            password = serializer.validated_data['password']
            gender = serializer.validated_data['gender']
            otp = generateOTP()
            state = sendsms(mobno,otp)
            if state == True:
                otpstore.objects.create(mobno=mobno,username=username,passw=password,otp=otp,gender=gender)
                data['status'] = True
            else:
                data['status'] = False
        else:
            data = serializer.errors

        return Response(data)

@api_view(['POST',])
@permission_classes([])
def otp_verify(request):
    if request.method == "POST":
        serializer = otpSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            mobno = serializer.validated_data['mobno']
            otp = serializer.validated_data['otp']
            try:
                getobj = otpstore.objects.filter(mobno=mobno).order_by('-id')[0]
            except:
                data['response'] = 'Error'
            if otp == getobj.otp:
                user = MyUser(username=getobj.username,mobno=mobno,gender=getobj.gender)
                user.set_password(getobj.passw)
                user.save()
                data['response'] = "Successfully registered a new user"
                data['status'] = True
                token = Token.objects.get(user=user).key
                data['token'] = token
                obj = otpstore.objects.filter(mobno=mobno)
                for i in obj:
                    i.delete()
            else:
                data['response'] = "Incorrect Otp"
                data['status'] = False
        else:
            data = serializer.errors

        return Response(data)

@api_view(['POST',])
@permission_classes([])
def login_view(request):
    if request.method == "POST":
        serializer = loginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            mobno = serializer.validated_data['mobno']
            print(mobno)
            otp = generateOTP()
            state = sendsms(mobno,otp)
            if state == True:
                otpstore.objects.create(mobno=mobno,otp=otp)
                data['status'] = True
            else:
                data['status'] = False
        else:
            data = serializer.errors

        return Response(data)
    
@api_view(['POST',])
@permission_classes([])
def otp_loginverify(request):
    if request.method == "POST":
        serializer = otpSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            mobno = serializer.validated_data['mobno']
            otp = serializer.validated_data['otp']
            try:
                getobj = otpstore.objects.filter(mobno=mobno).order_by('-id')[0]
            except:
                data['response'] = 'Error'
            if otp == getobj.otp:
                user = MyUser.objects.get(mobno=mobno)
                data['response'] = "Successful Login"
                data['status'] = True
                token = Token.objects.get(user=user).key
                data['token'] = token
                obj = otpstore.objects.filter(mobno=mobno)
                for i in obj:
                    i.delete()
            else:
                data['response'] = "Incorrect Otp"
                data['status'] = False
        else:
            data = serializer.errors

        return Response(data)


@api_view(['POST','PUT','GET',])
@permission_classes((IsAuthenticated, ))
def profile_view(request):
    if request.method == "POST" or request.method == "PUT":
        serializer = ProfileSerializer(data=request.data,many=False)
        data = {}
        if serializer.is_valid():
            user = request.user
            user = serializer.update(user,serializer.validated_data)
            data['response'] = "Succesfully Updated!"            
        else:
            data = serializer.errors
        
        return Response(data)
    elif request.method == 'GET':
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def dietallapi(request):
    if request.method == "GET":
        user = request.user
        serializers = DietSerializer(user,many=False)
        data = {

        }
        data['response'] = "Successfull"
        dietplans = user.diets.all()
        for diet in dietplans:
            data[diet.day] = {}
            data[diet.day]["preworkout"]  = {}
            count=1
            for pre in diet.preworkout.all():
                data[diet.day]["preworkout"][count] =  pre.fooditem.name
                count+=1
            data[diet.day]["postworkout"] = {}
            count2=1
            for pos in diet.postworkout.all():
                data[diet.day]["postworkout"][count2] = pos.fooditem.name
                count2+=1
            data[diet.day]["lunch"]  = {}
            count3=1
            for lun in diet.lunch.all():
                data[diet.day]["lunch"][count3] = lun.fooditem.name    
                count3+=1
            data[diet.day]["snacks"] = {}
            count4=1
            for snc in diet.snacks.all():
                data[diet.day]["snacks"][count4] = snc.fooditem.name
                count4+=1
            data[diet.day]["dinner"]  = {}
            count5=1
            for din in diet.dinner.all():
                data[diet.day]["dinner"][count5] = din.fooditem.name
                count5+=1
            data[diet.day]["remarks"] = diet.remarks
        return Response(data)


def lookcustomer(request,id):
    try:
        userr = MyUser.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.error("No User Found")
        return redirect('elogin')
    user = request.user
    if user.is_authenticated and user.is_staff == True and user.is_active == True and user.id == id:
        emp = employeecontrol.objects.get(id=userr)
        emp_type = emp.employeetype
        alotted_users = emp.alloted.all()
        parms = {
            'title':"Lookup Customers | KOWI",
            'emp_type':emp_type,
            'alotted':alotted_users,
        }
        return render(request,'lookcustomer.html',parms)
    else:
        messages.error(request,"Login First")
        return redirect('elogin')


def exercised(request,date):
    title = "Exercise | Lifestyles"
    user = request.user
    if user.is_authenticated:
        if user.is_staff != True:
            count = 0
            df = datetime.datetime.strptime(date,'%Y-%m-%d')
            number_of_days = 7
            date_list = []
            unsliced = []
            week_list = []
            shortweek = ['MON','TUE','WED','THU','FRI','SAT','SUN']
            for day in range(number_of_days):
                a_date = (df + datetime.timedelta(days = day)).isoformat()
                unsliced.append(a_date[0:10])
                date_list.append(a_date[8:10])
            for day in range(number_of_days):
                tmp = date_list[day]
                tm = datetime.datetime.strptime(date_list[day],'%d')
                fm = tm.weekday()
                if fm == 6:
                    fm = 0
                else:
                    fm = fm+1
                week_list.append(shortweek[fm])
            currday = df.weekday()
            currweek = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            curday = currweek[currday]
            shortday = shortweek[currday]
            flag = False      
            try:
                exe = user.fitness.get(day=curday)
            except ObjectDoesNotExist:
                flag = True
            if flag == False:
                exena = exe.exercisename.all()
                exenaquant = []
                for i in exena:
                    try:
                        quant = quantyrepssets.objects.get(Q(user=user) & Q(exername=i) & Q(day=curday))
                        exenaquant.append(quant)
                    except ObjectDoesNotExist:
                        exenaquant.append("")
                try:
                    log = exlogs.objects.get(Q(date=df) & Q(us=user))
                except ObjectDoesNotExist:
                    log = exlogs.objects.create(us=user,date=df)
                free = []
                exlog = log.exercisename.all()
                for i in exena:
                    if i not in exlog:
                        free.append(i)
                logquant = []
                for i in exlog:
                    if i in exena:
                        count+=1
                    try:
                        quant = quantyrepssets.objects.get(Q(user=user) & Q(exername=i) & Q(day=curday))
                        logquant.append(quant)
                    except ObjectDoesNotExist:
                        logquant.append("")
                if count != 0:
                    if exena.count() != count:
                        count = int(100/(count+1))
                    else:
                        count = int(100)
                if request.method == "POST":
                    if 'cal' in request.POST:
                        inc = request.POST['incoming']
                        year = inc[-4:]
                        month = inc[0:2]
                        da = inc[3:5]
                        ur = year+"-"+month+"-"+da
                        return redirect('exercise',ur)
                    if 'work' in request.POST:
                        fo = request.POST['tags']
                        qu = request.POST['quan']
                        qua = request.POST['quans']
                        item = exercise.objects.get(id=fo)
                        if item not in exlog:
                            log.exercisename.add(item)
                            try:
                                quant = quantyrepssets.objects.get(Q(user=user) & Q(exername=item) & Q(day=curday))
                            except ObjectDoesNotExist:
                                quant = quantyrepssets.objects.create(user=user,exername=item,day=curday)
                            quant.quantsets += int(qu)
                            quant.quantreps += int(qua)
                            quant.save()
                            messages.success(request,"Exercise Log Updated")
                            return redirect('exercise',date)
                        else:
                            quant = quantyrepssets.objects.get(Q(user=user) & Q(exername=item) & Q(day=curday))
                            quant.quantsets += int(qu)
                            quant.quantreps += int(qua)
                            quant.save()
                            messages.success(request,"Quantity Updated")
                            return redirect('exercise',date)
                    if 'exsave' in request.POST:
                        l = list(set(chain(free,exlog)))
                        for meal in l:
                            try:
                                checker = request.POST[str(meal.id)]
                                if checker == "on":
                                    if meal not in exlog:
                                        log.exercisename.add(meal)
                                        messages.success(request,"Exercise Logs Updated")
                                        log.save()
                            except MultiValueDictKeyError:
                                if meal not in exena:
                                    quant = quantyrepssets.objects.get(Q(user=user) & Q(exername=meal) & Q(day=curday))
                                    quant.delete()
                                log.exercisename.remove(meal)
                                messages.success(request,"Exercise Logs Erased!")
                                log.save()
                        return redirect('exercise',date)
                parms = {
                        'title':title,
                        'day':curday,
                        'exercises':exercise.objects.all(),
                        'exercise':zip(exena,exenaquant),
                        'date':datetime.date.today(),
                        'free':zip(free,exenaquant),
                        'exlog':zip(exlog,logquant),
                        'count':count,
                        'week_list':zip(week_list,date_list,unsliced),
                    }
            else:
                if request.method == "POST":
                    if 'cal' in request.POST:
                        inc = request.POST['incoming']
                        year = inc[-4:]
                        month = inc[0:2]
                        da = inc[3:5]
                        ur = year+"-"+month+"-"+da
                        return redirect('foodplans',ur) 
                parms = {
                    'title':title,
                    'day':curday,
                    'date':datetime.date.today(),
                    'week_list':zip(week_list,date_list,unsliced),
                }
            return render(request,'Exercises.html',parms)
        else:
            return render(request,'404.html')
    else:
        return redirect('login')


def update(pre,log,part):
    free = []
    if part == 1:
        lor = log.preworkout.all()
    elif part == 2:
        lor = log.postworkout.all()
    elif part == 3:
        lor = log.lunch.all()
    elif part == 4:
        lor = log.snacks.all()
    else:
        lor = log.dinner.all()
    for i in pre:
        if i not in lor:
            free.append(i)
    return free

def foodquantityreturn(user,mealer,listt,curday):
    quantity = []
    for i in listt:
        try:
            quant = quantuser.objects.get(Q(user=user) & Q(foodit=i.fooditem) & Q(meal=mealer) & Q(day=curday))
            quantity.append(quant)
        except ObjectDoesNotExist:
            quantity.append("")
    return quantity




def rescale(values, new_min = 0, new_max = 100):
    output = []
    old_min, old_max = min(values), max(values)
    for v in values:
        new_v = (new_max - new_min) / (old_max - old_min) * (v - old_min) + new_min
        output.append(new_v)

    return output

def foodplans(request,date):
    title = "Food Plans | KOWI Lifestyles"
    user = request.user
    if user.is_authenticated:
        if user.is_staff != True:
            foog = food.objects.all()
            df = datetime.datetime.strptime(date,'%Y-%m-%d')
            number_of_days = 7
            date_list = []
            unsliced = []
            week_list = []
            shortweek = ['MON','TUE','WED','THU','FRI','SAT','SUN']
            for day in range(number_of_days):
                a_date = (df + datetime.timedelta(days = day)).isoformat()
                unsliced.append(a_date[0:10])
                date_list.append(a_date[8:10])
            for day in range(number_of_days):
                tmp = date_list[day]
                tm = datetime.datetime.strptime(date_list[day],'%d')
                fm = tm.weekday()
                if fm == 6:
                    fm = 0
                else:
                    fm = fm+1
                week_list.append(shortweek[fm])
            currday = df.weekday()
            currweek = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            curday = currweek[currday]
            shortday = shortweek[currday]
            flag = False
            try:
                diet = user.diets.get(day=curday)
            except ObjectDoesNotExist:
                flag = True
            pre = diet.preworkout.all()
            post = diet.postworkout.all()
            lunch = diet.lunch.all()
            snacks = diet.snacks.all()
            dinner = diet.dinner.all()
            try:
                logg = logs.objects.get(Q(date=df) & Q(us=user))
            except ObjectDoesNotExist:
                logg = logs.objects.create(us=user,date=df)
            free = update(pre,logg,1)
            log = logg.preworkout.all()
            prequant = foodquantityreturn(user,"preworkout",free,curday)
            logprequant = foodquantityreturn(user,"preworkout",log,curday)
            #now postworkout
            freepost = update(post,logg,2)
            logpost = logg.postworkout.all()
            postquant = foodquantityreturn(user,"postworkout",freepost,curday)
            logpostquant = foodquantityreturn(user,"postworkout",logpost,curday)
            #now lunch
            freelunch = update(lunch,logg,3)
            loglunch = logg.lunch.all()
            lunchquant = foodquantityreturn(user,"lunch",freelunch,curday)
            loglunchquant = foodquantityreturn(user,"lunch",loglunch,curday)
            #now snacks
            freesnacks = update(snacks,logg,4)
            logsnacks = logg.snacks.all()
            snacksquant = foodquantityreturn(user,"snacks",freesnacks,curday)
            logsnacksquant = foodquantityreturn(user,"snacks",logsnacks,curday)
            #now dinner
            freedinner = update(dinner,logg,5)
            logsdinner = logg.dinner.all()
            dinnerquant = foodquantityreturn(user,"dinner",freedinner,curday)
            logdinnerquant = foodquantityreturn(user,"dinner",logsdinner,curday)
            if request.method == "POST":
                if 'prework' in request.POST:
                    fo = request.POST['tags']
                    qu = request.POST['quan']
                    foo = food.objects.get(id=fo)
                    item = foodplan.objects.get(fooditem=foo)
                    if item not in logg.preworkout.all():
                        logg.preworkout.add(item)
                        try:
                            quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="preworkout") & Q(day=curday))
                        except ObjectDoesNotExist:
                            quant = quantuser.objects.create(user=user,foodit=foo,meal="preworkout",day=curday)
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"logs Updated")
                        return redirect('foodplans',date)
                    else:
                        quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="preworkout") & Q(day=curday))
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"Quantity Updated")
                        return redirect('foodplans',date)
                if 'prem' in request.POST:
                    l = list(set(chain(free,log)))
                    for meal in l:
                        try:
                            checker = request.POST[str(meal.fooditem.id)]
                            if checker == "on":
                                if meal not in log:
                                    logg.preworkout.add(meal)
                                    messages.success(request,"logs Updated")
                                    logg.save()
                        except MultiValueDictKeyError:
                            if meal not in pre:
                                quant = quantuser.objects.get(Q(user=user) & Q(foodit=meal.fooditem) & Q(meal="preworkout") & Q(day=curday))
                                quant.delete()
                            logg.preworkout.remove(meal)
                            messages.success(request,"This log is Erased!")
                            logg.save()
                    return redirect('foodplans',date)
                if 'postwork' in request.POST:
                    fo = request.POST['tags']
                    qu = request.POST['quan']
                    foo = food.objects.get(id=fo)
                    item = foodplan.objects.get(fooditem=foo)
                    if item not in logg.postworkout.all():
                        logg.postworkout.add(item)
                        try:
                            quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="postworkout") & Q(day=curday))
                        except ObjectDoesNotExist:
                            quant = quantuser.objects.create(user=user,foodit=foo,meal="postworkout",day=curday)
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"logs Updated")
                        return redirect('foodplans',date)
                    else:
                        quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="postworkout") & Q(day=curday))
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"Quantity Updated")
                        return redirect('foodplans',date)
                if 'posm' in request.POST:
                    l = list(set(chain(freepost,logpost)))
                    for meal in l:
                        try:
                            checker = request.POST[str(meal.fooditem.id)]
                            if checker == "on":
                                if meal not in log:
                                    logg.postworkout.add(meal)
                                    messages.success(request,"logs Updated")
                                    logg.save()
                        except MultiValueDictKeyError:
                            if meal not in post:
                                quant = quantuser.objects.get(Q(user=user) & Q(foodit=meal.fooditem) & Q(meal="postworkout") & Q(day=curday))
                                quant.delete()
                            logg.postworkout.remove(meal)
                            messages.success(request,"This log is Erased!")
                            logg.save()
                    return redirect('foodplans',date)
                if 'lunchwork' in request.POST:
                    fo = request.POST['tags']
                    qu = request.POST['quan']
                    foo = food.objects.get(id=fo)
                    item = foodplan.objects.get(fooditem=foo)
                    if item not in logg.lunch.all():
                        logg.lunch.add(item)
                        try:
                            quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="lunch") & Q(day=curday))
                        except ObjectDoesNotExist:
                            quant = quantuser.objects.create(user=user,foodit=foo,meal="lunch",day=curday)
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"logs Updated")
                        return redirect('foodplans',date)
                    else:
                        quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="lunch") & Q(day=curday))
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"Quantity Updated")
                        return redirect('foodplans',date)
                if 'lunchm' in request.POST:
                    l = list(set(chain(freelunch,loglunch)))
                    for meal in l:
                        try:
                            checker = request.POST[str(meal.fooditem.id)]
                            if checker == "on":
                                if meal not in log:
                                    logg.lunch.add(meal)
                                    messages.success(request,"logs Updated")
                                    logg.save()
                        except MultiValueDictKeyError:
                            if meal not in lunch:
                                quant = quantuser.objects.get(Q(user=user) & Q(foodit=meal.fooditem) & Q(meal="lunch") & Q(day=curday))
                                quant.delete()
                            logg.lunch.remove(meal)
                            messages.success(request,"This log is Erased!")
                            logg.save()
                    return redirect('foodplans',date)
                if 'snackwork' in request.POST:
                    fo = request.POST['tags']
                    qu = request.POST['quan']
                    foo = food.objects.get(id=fo)
                    item = foodplan.objects.get(fooditem=foo)
                    if item not in logg.snacks.all():
                        logg.snacks.add(item)
                        try:
                            quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="snacks") & Q(day=curday))
                        except ObjectDoesNotExist:
                            quant = quantuser.objects.create(user=user,foodit=foo,meal="snacks",day=curday)
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"logs Updated")
                        return redirect('foodplans',date)
                    else:
                        quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="snacks") & Q(day=curday))
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"Quantity Updated")
                        return redirect('foodplans',date)
                if 'snackm' in request.POST:
                    l = list(set(chain(freesnacks,logsnacks)))
                    for meal in l:
                        try:
                            checker = request.POST[str(meal.fooditem.id)]
                            if checker == "on":
                                if meal not in log:
                                    logg.snacks.add(meal)
                                    messages.success(request,"logs Updated")
                                    logg.save()
                        except MultiValueDictKeyError:
                            if meal not in snacks:
                                quant = quantuser.objects.get(Q(user=user) & Q(foodit=meal.fooditem) & Q(meal="snacks") & Q(day=curday))
                                quant.delete()
                            logg.snacks.remove(meal)
                            messages.success(request,"This log is Erased!")
                            logg.save()
                    return redirect('foodplans',date)
                if 'dinnerwork' in request.POST:
                    fo = request.POST['tags']
                    qu = request.POST['quan']
                    foo = food.objects.get(id=fo)
                    item = foodplan.objects.get(fooditem=foo)
                    if item not in logg.dinner.all():
                        logg.dinner.add(item)
                        try:
                            quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="dinner") & Q(day=curday))
                        except ObjectDoesNotExist:
                            quant = quantuser.objects.create(user=user,foodit=foo,meal="dinner",day=curday)
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"logs Updated")
                        return redirect('foodplans',date)
                    else:
                        quant = quantuser.objects.get(Q(user=user) & Q(foodit=foo) & Q(meal="dinner") & Q(day=curday))
                        quant.quantity += int(qu)
                        quant.save()
                        messages.success(request,"Quantity Updated")
                        return redirect('foodplans',date)
                if 'dinnerm' in request.POST:
                    l = list(set(chain(freedinner,logsdinner)))
                    for meal in l:
                        try:
                            checker = request.POST[str(meal.fooditem.id)]
                            if checker == "on":
                                if meal not in log:
                                    logg.dinner.add(meal)
                                    messages.success(request,"logs Updated")
                                    logg.save()
                        except MultiValueDictKeyError:
                            if meal not in dinner:
                                quant = quantuser.objects.get(Q(user=user) & Q(foodit=meal.fooditem) & Q(meal="dinner") & Q(day=curday))
                                quant.delete()
                            logg.dinner.remove(meal)
                            messages.success(request,"This log is Erased!")
                            logg.save()
                    return redirect('foodplans',date)
                if 'cal' in request.POST:
                    inc = request.POST['incoming']
                    year = inc[-4:]
                    month = inc[0:2]
                    da = inc[3:5]
                    ur = year+"-"+month+"-"+da
                    return redirect('foodplans',ur)
            intake = []
            cal,pro,fib,fat,car=0,0,0,0,0
            precount,postcount,lunchcount,snackscount,dinnercount=0,0,0,0,0
            for it,qu in zip(log,logprequant):
                if it in pre:
                    precount+=1
                if type(qu) == str:
                    cal = cal+(it.fooditem.calories)
                    pro = pro+(it.fooditem.protein)
                    fib = fib+(it.fooditem.fiber)
                    car = car+(it.fooditem.carbs)
                    fat = fat+(it.fooditem.fat)
                else:
                    cal = cal+(qu.quantity*it.fooditem.calories)
                    pro = pro+(qu.quantity*it.fooditem.protein)
                    fib = fib+(qu.quantity*it.fooditem.fiber)
                    car = car+(qu.quantity*it.fooditem.carbs)
                    fat = fat+(qu.quantity*it.fooditem.fat)
            for it,qu in zip(logpost,logpostquant):
                if it in post:
                    postcount+=1
                if type(qu) == str:
                    cal = cal+(it.fooditem.calories)
                    pro = pro+(it.fooditem.protein)
                    fib = fib+(it.fooditem.fiber)
                    car = car+(it.fooditem.carbs)
                    fat = fat+(it.fooditem.fat)
                else:
                    cal = cal+(qu.quantity*it.fooditem.calories)
                    pro = pro+(qu.quantity*it.fooditem.protein)
                    fib = fib+(qu.quantity*it.fooditem.fiber)
                    car = car+(qu.quantity*it.fooditem.carbs)
                    fat = fat+(qu.quantity*it.fooditem.fat)
            for it,qu in zip(loglunch,loglunchquant):
                if it in lunch:
                    lunchcount+=1
                if type(qu) == str:
                    cal = cal+(it.fooditem.calories)
                    pro = pro+(it.fooditem.protein)
                    fib = fib+(it.fooditem.fiber)
                    car = car+(it.fooditem.carbs)
                    fat = fat+(it.fooditem.fat)
                else:
                    cal = cal+(qu.quantity*it.fooditem.calories)
                    pro = pro+(qu.quantity*it.fooditem.protein)
                    fib = fib+(qu.quantity*it.fooditem.fiber)
                    car = car+(qu.quantity*it.fooditem.carbs)
                    fat = fat+(qu.quantity*it.fooditem.fat)
            for it,qu in zip(logsnacks,logsnacksquant):
                if it in snacks:
                    snackscount+=1
                if type(qu) == str:
                    cal = cal+(it.fooditem.calories)
                    pro = pro+(it.fooditem.protein)
                    fib = fib+(it.fooditem.fiber)
                    car = car+(it.fooditem.carbs)
                    fat = fat+(it.fooditem.fat)
                else:
                    cal = cal+(qu.quantity*it.fooditem.calories)
                    pro = pro+(qu.quantity*it.fooditem.protein)
                    fib = fib+(qu.quantity*it.fooditem.fiber)
                    car = car+(qu.quantity*it.fooditem.carbs)
                    fat = fat+(qu.quantity*it.fooditem.fat)
            
            for it,qu in zip(logsdinner,logdinnerquant):
                if it in dinner:
                    dinnercount+=1
                if type(qu) == str:
                    cal = cal+(it.fooditem.calories)
                    pro = pro+(it.fooditem.protein)
                    fib = fib+(it.fooditem.fiber)
                    car = car+(it.fooditem.carbs)
                    fat = fat+(it.fooditem.fat)
                else:
                    cal = cal+(qu.quantity*it.fooditem.calories)
                    pro = pro+(qu.quantity*it.fooditem.protein)
                    fib = fib+(qu.quantity*it.fooditem.fiber)
                    car = car+(qu.quantity*it.fooditem.carbs)
                    fat = fat+(qu.quantity*it.fooditem.fat)
            intake.append(cal)
            intake.append(pro)
            intake.append(fat)
            intake.append(car)
            intake.append(fib)

            if precount !=0:
                if pre.count() != precount:
                    precount = int(100/(precount+1))
                else:
                    precount = int(100)
            if postcount != 0:
                if post.count() != postcount:
                    postcount = int(100/(postcount+1))
                else:
                    postcount = int(100)
            if lunchcount !=0:
                if lunch.count() != lunchcount:
                    lunchcount = int(100/(lunchcount+1))
                else:
                    lunchcount = int(100)
            if snackscount != 0:
                if snacks.count() != snackscount:
                    snackscount = int(100/(snackscount+1))
                else:
                    snackscount = int(100)
            if dinnercount != 0:
                if dinner.count() != dinnercount:
                    dinnercount = int(100/(dinnercount+1))
                else:
                    dinnercount = int(100)
            parms = {
                'week_list':zip(week_list,date_list,unsliced),
                'freepre':zip(free,prequant),
                'post':zip(freepost,postquant),
                'logpost':zip(logpost,logpostquant),
                'lunch':zip(freelunch,lunchquant),
                'loglunch':zip(loglunch,loglunchquant),
                'snacks':zip(freesnacks,snacksquant),
                'logsnacks':zip(logsnacks,logsnacksquant),
                'freedinner':zip(freedinner,dinnerquant),
                'logsdinner':zip(logsdinner,logdinnerquant),
                'date':date,
                'title':title,
                'foods':foog,
                'varlog':precount,
                'varpostlog':postcount,
                'varlunchlog':lunchcount,
                'varsnackslog':snackscount,
                'vardinnerlog':dinnercount,
                'intake':json.dumps(intake),
                'logpre':zip(log,logprequant),
            }
            return render(request,'foodplans.html',parms)
        else:
            messages.error(request,'This Page isnt for you! Sorry! ')
            return render(request, '404.html')
    else:
        messages.error(request,'Login First!')
        return redirect('login')

def fooddetail(request,id):
    title = "Food Detail | Lifestyles"
    data={}
    foodvar = food.objects.get(id=id)
    try:
        foodp = foodplan.objects.get(fooditem=foodvar)
        data['recipe'] = foodp.textrecipe
    except ObjectDoesNotExist:
        data['recipe'] = "Food Recipe Doesn't Exist!"
    data['calorie'] = foodvar.calories
    data['image'] = foodvar.pic
    data['name'] = foodvar.name
    data['stuff'] = foodvar.stuff
    data['unit'] = foodvar.unit
    data['time'] = foodvar.time_taken
    data['tag'] = foodvar.tag
    nut = []
    nut.append(foodvar.fat)
    nut.append(foodvar.protein)
    nut.append(foodvar.carbs)
    nut.append(foodvar.fiber)
    data['nut'] = json.dumps(nut)
    return render(request,'fooddetail.html',data)

def setgrocery(request):
    title = "Set Grocery | Kowi"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            emp = employeecontrol.objects.get(id=user)
        except ObjectDoesNotExist:
            messages.error(request,"You Do Not Have a Employee Profile, Yet")
            return redirect("elogin")
        if emp.employeetype == "employee":
            customers = MyUser.objects.filter(Q(is_staff=False) & Q(sub.plan != "Free Plan"))
            foods = food.objects.all()

@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def exercise_view(request):
    if request.method == 'GET':
        user = request.user
        serializer = ExerciseSerializer(user,many=False)
        data = {

        }
        data['response'] = "Successfull"
        exe = user.fitness.all()
        for exena in exe:
            data[exena.day] = {}
            data[exena.day]["workout_day"] = exena.workoutday
            data[exena.day]["exercise"]  = {}
            count=1
            for ex in exena.exercisename.all():
                data[exena.day]["exercise"][count] = {}
                data[exena.day]["exercise"][count]["name"] =  ex.name
                data[exena.day]["exercise"][count]["description"] =  ex.description
                data[exena.day]["exercise"][count]["muscle_group"] =  ex.muscle_group
                data[exena.day]["exercise"][count]["muscle_worked"] =  ex.muscle_worked
                data[exena.day]["exercise"][count]["video_path"] =  ex.video_path
                data[exena.day]["exercise"][count]["image_path"] =  ex.image_path
                try:
                    quant = quantyrepssets.objects.get(Q(user=user) & Q(day=exena.day) & Q(exername=ex))
                except ObjectDoesNotExist:
                    quant = None
                if quant != None:
                    data[exena.day]["exercise"][count]["sets_quantity"] = quant.quantsets
                    data[exena.day]["exercise"][count]["reps_quantity"] = quant.quantreps
                else:
                    data[exena.day]["exercise"][count]["sets_quantity"] = "None"
                    data[exena.day]["exercise"][count]["reps_quantity"] = "None"
                count2=1
                data[exena.day]["exercise"][count]["equipments"] = {}
                for e in ex.equipments.all():
                    data[exena.day]["exercise"][count]["equipments"][count2] = {}
                    data[exena.day]["exercise"][count]["equipments"][count2]["name"] = e.name
                    data[exena.day]["exercise"][count]["equipments"][count2]["image_path"] = e.image_path
                    count2+=1
                count+=1
            data[exena.day]["remarks"] = exena.remarks
        return Response(data)

order_details = {
    'date': '4th May',
    'slot': '8pm',
}



def send_notification(request):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    

    message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Your appointment is coming up on {} at {}.'.format(
                order_details['date'], order_details['slot']),
            to='whatsapp:{}'.format(917887257977)
        )

    print(7887257977)
    print(message.sid)
    print('Great! Expect a message...')

    return HttpResponse("<h1>well done</h1>")

@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def streak_view(request):
    if request.method == 'GET':
        user = request.user
        serializer = StreakSerializer(user,many=False)
        data = {}
        data['response'] = "Successful"
        data['points'] = user.streaks.points
        data['no_of_days'] = user.streaks.days
        return Response(data)


@api_view(['POST',])
@permission_classes((IsAuthenticated, ))
def steps_view(request):
    if request.method == "POST":
        serializer = StepsSerializer(data=request.data,many=False)
        data = {}
        if serializer.is_valid():
            user = request.user
            user = serializer.update(user,serializer.validated_data)
            data['response'] = "Succesfully Updated!"            
        else:
            data = serializer.errors
        
        return Response(data)

@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def live_view(request):
    # if request.method == "POST":
    #     serializer = liveSerializer(data=request.data,many=False)
    #     data = {}
    #     if serializer.is_valid():
    #         user = request.user
    #         user = serializer.update(user,serializer.validated_data)
    #         data['response'] = "Succesfully Updated!"            
    #     else:
    #         data = serializer.errors
        
    #     return Response(data)
    if request.method == 'GET':
        user = request.user
        serializer = liveSerializer(user,many=False)
        liveobjs = user.lives.all()
        data = {}
        data["response"] = "Successful"
        count = 1
        for obj in liveobjs:
            data[count] = {}
            data[count]["time"] = obj.slottime
            data[count]["date"] = obj.date
            empobjs = MyUser.objects.filter(lives=obj.id)
            for ob in empobjs:
                if user.id != ob.id:
                    emp = employeecontrol.objects.get(id=ob)
                    data[count]["emp_name"] = ob.username
                    data[count]["emp_image"] = "/media/"+str(ob.pic)
                    if emp.employeetype == "Nutritionist":
                        data[count]["emp_type"] = emp.employeetype
                        data[count]["roomid"] = user.fornut
                    elif emp.employeetype == "Dietician":
                        data[count]["emp_type"] = emp.employeetype
                        data[count]["roomid"] = user.fordiet
                    elif emp.employeetype == "Fitness Trainer":
                        data[count]["emp_type"] = emp.employeetype
                        data[count]["roomid"] = user.forfit
                    else:
                        continue
                else:
                    continue
            count+=1
                    
        return Response(data)

# def streak_check_daily():
#     d = datetime.date.today()
#     users = MyUser.objects.filter(is_staff=False)
#     for user in users:
#         try:
#             logg = logs.objects.get(Q(date=d) & Q(us=user))
#             exlog = exlogs.objects.get(Q(date=d) & Q(us=user))
#             if (logg.preworkout.count() !=0 or logg.postworkout.count() !=0 or logg.lunch.count() != 0 or logg.snacks.count() != 0 or logg.dinner.count() != 0) and (exlog.exercisename.count() != 0):
#                 user.streaks.days+=1
#                 if user.sub.plan == "Free Plan":
#                     user.streaks.points+=10
#                 elif user.sub.plan == "Basic Plan":
#                     user.streaks.points+=20
#                 elif user.sub.plan == "Semi Premium Plan":
#                     user.streaks.points+=50
#                 elif user.sub.plan == "Premium Plan":
#                     user.streaks.points+=100
#             else:
#                 continue
#         except ObjectDoesNotExist:
#             continue


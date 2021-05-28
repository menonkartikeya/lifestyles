from typing_extensions import ParamSpecArgs
from django.shortcuts import render,redirect
from django.http import Http404
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
from background_task import background
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
# Create your views here.

#Home Page - currently renders which type of user is there and shows links according to that.
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
        bmii = bmi.objects.filter(us=user).order_by('-date').first()
        bmrr = bmr.objects.filter(us=user).order_by('-date').first()

            
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
        dietplans = user.diets.get(day=curday)
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
        parms = {
            'title':title,
            'bmi':bmii,
            'bmr':bmrr,
            'grolist':grolist,
            'meet':meet,
            'flag':flag,
            'findnutri':findnutri,
            'finddieti':finddieti,
            'findtrain':findtrain,
            'curday':curday,
            'dietplans':dietplans,
            'premeal':premeal,
            'postmeal':postmeal,
            'lunch':lunch,
            'snacks':snacks,
            'dinner':dinner,
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
                    user.mobno = request.POST['mobno']
                    user.target = request.POST['target']
                    user.age = request.POST['age']
                    #checking user sub plans and then taking values ##from html if he wants to change or not!#https://medium.com/django-rest/django-rest-framework-change-password-and-update-profile-1db0c144c0a3
                    if user.sub.plan == 'Basic Plan':
                        checknutri = request.POST['checknutri']
                        checkfitness = request.POST['checkfitness']
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
                        checkfitness = request.POST['checkfitness']
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
                    user.save()
                    messages.success(request,"Changes Saved")
                    return redirect('dashboard')
            else:
                messages.error(request,"Verify Account First")
                return redirect('dashboard')
                    
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

@background(schedule=2629746)
def unsubscribe_user(user_id,bill_id):
    user = MyUser.objects.get(id=user_id)
    bill = MyUser.bill.get(id=bill_id)
    bill.expiry = True
    user.email_user("Plan Expired","Your Subscription Plan Expired, Please Change Your Plan!")
    bill.save()
    

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
    }

    return render(request,'book.html',parms)

#bmi calculator -- 
def bmic(request):
    headtitle = "BMI | Lifestyles"
    bmii =0.0
    state = ""
    user = request.user
    if user.is_authenticated:
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
            save = request.POST.get("save")
            if save == "on":
                user = request.user
                bmi.objects.create(us=user,bmi=round(bmii),date=datetime.date.today())
                user.weight = weight
                user.height = height
                user.save()
    parms = {
        'title':headtitle,
        'bmi':bmii,
        'state':state,
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
def growth(request):
    title = "Growth | Lifestyles"
    parms = {
        'title':title,
    }
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
def bmrmain(weight,height,age,gender):
    heightincm=height*100
    if gender == 'male':
        bmr=66.47+(13.75*weight)+(5.003*heightincm)-(6.755*age)
    elif gender == 'female':
        bmr=655.1+(9.563*weight)+(1.85*heightincm)-(4.676*age)
    return bmr

#bmr calculater!
def bmrcal(request):
    headtitle = "Life Styles | Bmr"
    user = request.user
    usertype = None
    bmrr =0.0
    if user.is_authenticated:
        if request.method=="POST":
            weight_metric = request.POST.get("weight-metric")
            weight_imperial = request.POST.get("weight-imperial")

            if weight_metric:
                weight = float(request.POST.get("weight-metric"))
                height = float(request.POST.get("height-metric"))
                age = int(request.POST.get("age-metric"))
                gender = str(request.POST.get("gender-metric"))
            elif weight_imperial:
                weight = float(request.POST.get("weight-imperial"))/2.205
                height = (float(request.POST.get("feet"))*30.48 + float(request.POST.get("inches"))*2.54)/100
                age = int(request.POST.get("age-imperial"))
                gender = str(request.POST.get("gender-imperial"))        
            cont = bmrmain(weight,height,age,gender)
            bmrr = cont
            save = request.POST.get("save")
            if save == "on":
                user = request.user
                bmr.objects.create(us=user,bmr=round(bmrr),date=datetime.date.today())
                user.weight = weight
                user.height = height
                user.age = age
                user.gender = gender
                user.save()
    parms = {
        'title':headtitle,
        'usertype':usertype,
        'bmr':bmrr,
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

@api_view(['POST',])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Succesfully registered a new user"
            data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        
        return Response(data)
    
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = MyUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


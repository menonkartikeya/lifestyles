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
from django.contrib import messages
from math import pi
from django.db.models.query import EmptyQuerySet
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource
from django.db.models import Count
from django.http import JsonResponse
# Create your views here.


def index(request):
    headtitle = "Life Styles | Home"
    user = request.user
    if user.is_staff == False:
        if user.is_authenticated:
            usertype = "Customer"
        else:
            usertype = None
    elif user.is_active == True and user.is_staff == True:
        try:
            emp = employeecontrol.objects.get(id=user)
            usertype = emp.employeetype
        except ObjectDoesNotExist:
            usertype = None
    parms = {
        'title':headtitle,
        'usertype':usertype,
    }
    return render(request,'index.html',parms)

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

def dashboard(request):
    title = "Life Styles | Dashboard"
    parms = {
        'title':title,
    }
    user = request.user
    if user.is_authenticated and user.is_staff == False:
        bmii = bmi.objects.filter(us=user).order_by('-id')[:1]
        if user.allotdieti:
            finddieti = employeecontrol.objects.get(Q(employeetype="Dietician") & Q(alloted=user))
        else:
            finddieti = None
        if user.allotnutri:
            findnutri = employeecontrol.objects.get(Q(employeetype="Nutritionist") & Q(alloted=user))
        else:
            findnutri = None
        if user.allottrain:
            findtrain = employeecontrol.objects.get(Q(employeetype="Fitness Trainer") & Q(alloted=user))
        else:
            findtrain = None
        tmp = []
        for i in bmii:
            tmp.append(i.bmi)
        grolist = []
        try:
            grocery = grocerylist.objects.get(id=user.id)
        except ObjectDoesNotExist:
            grocery = None
        if grocery != None:
            grolist = grocery.items.all()
        meet = user.lives.all()
        flag = False
        if meet.count() == 0:
            flag = True
        if tmp == []:
            parms = {
                'title':title,
                'bmi':None,
                'grolist':grolist,
                'meet':meet,
                'flag':flag,
                'findnutri':findnutri,
                'finddieti':finddieti,
                'findtrain':findtrain,
            }
        else:
            parms = {
                'title':title,
                'bmi':tmp[0],
                'grolist':grolist,
                'meet':meet,
                'flag':flag,
                'findnutri':findnutri,
                'finddieti':finddieti,
                'findtrain':findtrain,
            }
        return render(request,'dashboard.html',parms)
    else:
        return render(request,'404.html',parms)
    
    return render(request,'dashboard.html',parms)

##Login / Signup ###

def logoutuser(request):
    logout(request)
    return redirect('login')

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

def login(request):
    title = "Login | Lifestyles"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_staff == False:
            auth.login(request,user)
            messages.info(request,'Logged In')
            return redirect('dashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    return render(request,'login.html',{'title':title})

def elogin(request):
    title = "Employee Login | lifeStyles"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_staff == True and user.is_active == True:
            auth.login(request,user)
            messages.info(request,'Logged In')
            return redirect('edashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('elogin')

    else:
        return render(request,'elogin.html',{'title':title})

def signup(request):
    title = "Register | LifeStyles"
    if request.method == 'POST':
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
                return redirect(index)
        else:
            messages.info(request,'Password not matched')
            return redirect('signup')
    return render(request,'signup.html',{'title':title})

def esignup(request):
    title = "Register | LifeStyles"
    if request.method == 'POST':
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
                user = auth.authenticate(username=username,password=password1)
                auth.login(request,user)
                employee = employeecontrol.objects.create(id=user,gender=gender,certificate=certificate,resume=resume,employeetype=employeetype,mobno=mobno)
                messages.info(request,'We will Verify and mail You with the details!')
                return redirect(index)
        else:
            messages.info(request,'Password not matched')
            return redirect('esignup')
    return render(request,'esignup.html',{'title':title})

##########################################

def edashboard(request):
    title = "Employee Dashboard | LifeStyles"
    user = request.user
    if user.is_authenticated and user.is_staff == True and user.is_active == True:
        try:
            employee = employeecontrol.objects.get(id=user)
            users = MyUser.objects.all()
            lives = user.lives.all()
            emptype = employee.employeetype
            if emptype == 'employee':
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
                    }
            return render(request,'edashboard.html',parms)
        except ObjectDoesNotExist:
            messages.error(request,'Not Authorized!')
            return redirect(elogin)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    return render(request,'edashboard.html',{'title':title})

def profile(request,id):
    title = "Profile | Lifestyles"
    user = request.user
    if user.is_authenticated:
        if user.id == id:
            if user.is_active == True:
                if request.method == 'POST':
                    user.mobno = request.POST['mobno']
                    user.target = request.POST['target']
                    user.age = request.POST['age']
                    if user.sub.plan == 'Basic Plan':
                        checknutri = request.POST['checknutri']
                        checkfitness = request.POST['checkfitness']
                        if checknutri == "yes":
                            user.allotnutri = False
                            findnut = employeecontrol.objects.get(Q(employeetype="Nutritionist") & Q(alloted=user))
                            findnut.alloted.remove(user)
                        if checkfitness == "yes":
                            user.allottrain = False
                            findfit = employeecontrol.objects.get(Q(employeetype="Fitness Trainer") & Q(alloted=user))
                            findfit.alloted.remove(user)
                    if user.sub.plan == "Semi-Premium Plan" or user.sub.plan == "Premium Plan":
                        checkdieti = request.POST['checkdieti']
                        checknutri = request.POST['checknutri']
                        checkfitness = request.POST['checkfitness']
                        if checknutri == "yes":
                            user.allotnutri = False
                            findnut = employeecontrol.objects.get(Q(employeetype="Nutritionist") & Q(alloted=user))
                            findnut.alloted.remove(user)
                        if checkfitness == "yes":
                            user.allottrain = False
                            findfit = employeecontrol.objects.get(Q(employeetype="Fitness Trainer") & Q(alloted=user))
                            findfit.alloted.remove(user)
                        if checkdieti == "yes":
                            user.allotdieti = False
                            finddieti = employeecontrol.objects.get(Q(employeetype="Dietician") & Q(alloted=user))
                            finddieti.alloted.remove(user)
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

def invoices(request):
    title = "Invoices | Lifestyles"
    parms = {
        'title':title,
    }
    return render(request,'invoice.html',parms)

def lives(request):
    user = request.user
    if user.is_authenticated and user.is_active == True:
        return redirect('https://test-chat-web-android.web.app/')
    else:
        return render(request,'404.html')

def book(request):
    title = "Book Appointment | Lifestyles"
    user = request.user
    if user.is_authenticated:
        if user.is_staff == True and user.is_active == True:
            flag = True
            findemp = employeecontrol.objects.get(id=user)
            allot = findemp.alloted.all()
            if findemp.employeetype == "Nutritionist" or findemp.employeetype == "Dietician" or findemp.employeetype == "trainee":
                if request.method == 'POST':
                    userid = request.POST['userid']
                    slottime = request.POST['slottime']
                    date = request.POST['date']
                    obj = live.objects.create(id=userid,slottime=slottime,date=date)
                    conf = MyUser.objects.get(id=userid)
                    conf.lives.add(obj.id)
                    user.lives.add(obj.id)
                    messages.success(request,"Success")
                    return redirect(edashboard)
        elif user.is_staff == False:
            flag = False
            findemp = employeecontrol.objects.get(alloted=user)
            allot = findemp.alloted.all()
            getus = MyUser.objects.get(username=findemp.id)
            if request.method == "POST":
                slottime = request.POST['slottime']
                date = request.POST['date']
                obj = live.objects.create(slottime=slottime,date=date)
                user.lives.add(obj.id)
                getus.lives.add(obj.id)
                messages.success(request,"Success")
                return redirect(dashboard)
    else:
        return redirect(login)
    parms = {
        "title":title,
        'flag':flag,
        'allot':allot,
    }

    return render(request,'book.html',parms)

def bmic(request):
    headtitle = "BMI | Lifestyles"
    bmii =0.0
    state = ""
    script = None
    div = None
    user = request.user
    if user.is_authenticated:
        objs = bmi.objects.filter(us=user)
        x = []
        y = []
        for obj in objs:
            x.append(obj.bmi)
            y.append(obj.date)
        title = 'BMI Graph'

        plot = figure(title= title , 
            x_axis_label= 'X-Axis', 
            y_axis_label= 'Y-Axis', 
            plot_width =400,
            plot_height =400)

        plot.line(x, y, legend= 'f(x)', line_width = 2)
        #Store components 
        script, div = components(plot)
        if user.is_staff == True:
            emp = employeecontrol.objects.get(id=user)
            usertype = emp.employeetype
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
        'script':script,
        'div':div,
    }
    return render(request,'bmi.html',parms)

def subs(request):
    title = "Subs Plan | Lifestyles"
    parms = {
        'title':title,
    }
    return render(request,'sub.html',parms)

def growth(request):
    title = "Growth | Lifestyles"
    parms = {
        'title':title,
    }
    return render(request,'growth.html',parms)

def grocery(request,id):
    title = "Grocery | Lifestyles"
    user = request.user
    if user.is_authenticated and user.id == id:
        try:
            grocery = grocerylist.objects.get(id=id)
            grolist = grocery.items.all()
            if grocery.billitem.invoicepdf:
                check = True
            else:
                check = False
        except ObjectDoesNotExist:
            return render(request,'404.html')
    parms = {
        'title':title,
        'grolist':grolist,
        'grocery':grocery,
        'check':check,
    }
    return render(request,'grocery.html',parms)

def fooddetail(request,fooditem):
    title = "Food Details | Lifestyles"
    user = request.user
    if user.is_authenticated:
        if user.diets.breakfast == fooditem:
            obj = foodplan.objects.get(fooditem=user.diets.breakfast)
        elif user.diets.lunch == fooditem:
            obj = foodplan.objects.get(fooditem=user.diets.lunch)
        elif user.diets.snacks == fooditem:
            obj = foodplan.objects.get(fooditem=user.diets.snacks)
        else:
            obj = foodplan.objects.get(fooditem=user.diets.dinner)
        parms = {
            'obj':obj,
            'title':title,
        }
        return render(request,'fooddetail.html',parms)
    parms = {
        'title':title,
    }
    return render(request,'fooddetail.html',parms)


def allocate(request,id):
    title = "Allocate | Lifestyles"
    user = request.user
    if user.is_authenticated and user.is_staff == True and user.is_active == True:
        target = MyUser.objects.get(id=id)
        totpeeps = employeecontrol.objects.filter(Q(employeetype="Dietician") | Q(employeetype="Nutritionist"))
        freepeeps = []
        for peep in totpeeps:
            counter = peep.alloted.count()
            if counter <= 25:
                freepeeps.append(peep)
        if request.method == 'POST':
            diet = request.POST['diet']
            for peep in freepeeps:
                tmp = str(peep.id)
                if tmp == diet:
                    getuser = employeecontrol.objects.get(id=peep.id)
                    print(getuser)
                    getuser.alloted.add(id)
                    target.allot = True
                    target.save()
                    messages.success(request,"Success")
                    return redirect(unalo)
                    break
    else:
        messages.error(request,"Not Authorized!")
    parms = {
            'title':title,
            'target':target,
            'freepeeps':freepeeps,
        } 
    return render(request, 'allocate.html',parms)

def contactus(request):
    title = "Contact | Lifestyles"
    parms = {
        "title":title,
    }
    return render(request,'contact.html',parms)


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

def unalo(request):
    title = "Unallocated Users and Free Dieticians"
    user = request.user
    if user.is_authenticated and user.is_staff == True and user.is_active == True:
        users = MyUser.objects.all()
        unal = []
        for us in users:
            if us.is_staff == False and us.allot == False:
                unal.append(us)
        totpeeps = employeecontrol.objects.filter(Q(employeetype="Dietician") | Q(employeetype="Nutritionist"))
        freepeeps = []
        for peep in totpeeps:
            counter = peep.alloted.count()
            if counter <= 25:
                freepeeps.append(peep)
    parms = {
        "title":title,
        'unal':unal,
        'freepeeps':freepeeps,
    }
    return render(request,'unalo.html',parms)

def bmrmain(weight,height,age,gender):
    heightincm=height*100
    if gender == 'male':
        bmr=66.47+(13.75*weight)+(5.003*heightincm)-(6.755*age)
    elif gender == 'female':
        bmr=655.1+(9.563*weight)+(1.85*heightincm)-(4.676*age)
    return bmr


def bmrcal(request):
    headtitle = "Life Styles | Bmr"
    user = request.user
    usertype = None
    bmrr =0.0
    
    script = None
    div = None
    if user.is_authenticated:
        objs = bmr.objects.filter(us=user)
        x = []
        y = []
        for obj in objs:
            x.append(obj.bmr)
            y.append(obj.date)
        title = 'BMR Graph'

        plot = figure(title= title , 
            x_axis_label= 'X-Axis', 
            y_axis_label= 'Y-Axis', 
            plot_width =400,
            plot_height =400)

        plot.line(x, y, legend= 'f(x)', line_width = 2)
        #Store components 
        script, div = components(plot)
        if user.is_staff == True:
            emp = employeecontrol.objects.get(id=user)
            usertype = emp.employeetype
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
        'script':script,
        'div':div,
    }

    return render(request,'bmrmain.html',parms)
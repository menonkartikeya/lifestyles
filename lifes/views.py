from django.shortcuts import render
from django.http import Http404
from .models import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import pyrebase

# Create your views here.

config = {
    'apiKey': "AIzaSyBJ33tV82IcUyz5qG3DcX53cmtNU_VZYm8",
    'authDomain': "lifestyle-kowi.firebaseapp.com",
    'projectId': "lifestyle-kowi",
    'storageBucket': "lifestyle-kowi.appspot.com",
    'messagingSenderId': "937975020079",
    'appId': "1:937975020079:web:e34c860b0f6ab87a4464da",
    'databaseURL': "https://lifestyle-kowi-default-rtdb.asia-southeast1.firebasedatabase.app",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def index(request):
    title = "Life Styles | Home"
    free_plan = database.child('subscriptions').child('free').get().val()
    basic_plan = database.child('subscriptions').child('basic').get().val()
    premium_plan = database.child('subscriptions').child('premium').get().val()
    parms = {
        'title':title,
        'free_plan':free_plan,
        'basic_plan':basic_plan,
        'premium_plan':premium_plan,
    }
    return render(request,'index.html',parms)

def dashboard(request):
    headtitle = "Life Styles | Dashboard"
    parms = {
        'title':title,
    }
    user = request.user
    if user.is_authenticated and user.is_staff == False:
        try:
            userdet = userdetail.objects.get(user)
        except ObjectDoesNotExist:
            return render(request,'404.html',parms)
        parms = {
            'title':title,
            'userdet':userdet,
            'user':user,
        }
        return render(request,'dashboard.html',parms)
    
    return render(request,'dashboard.html',parms)

##Login / Signup ###

def logoutuser(request):
    logout(request)
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
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

    else:
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
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email).save()
                user = auth.authenticate(username=username,password=password1)
                auth.login(request,user)
                us = request.user
                userdet = userdetail.objects.create(id=us,gender=gender,height=height,weight=weight,target=target,subscription=subscription,mobno=mobno,age=age)
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
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('esignup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('esignup')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email).save()
                user = auth.authenticate(username=username,password=password1)
                auth.login(request,user)
                us = request.user
                us.is_staff == True
                us.is_active == False
                us.save()
                employee = employeecontrol.objects.create(id=us,gender=gender,certificate=certificate,resume=resume,employeetype=employeetype,mobno=mobno)
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
            return render(request,'edashboard.html',{'title':title,'employee':employee})
        except ObjectDoesNotExist:
            messages.error(request,'Not Authorized!')
            return redirect(elogin)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    return render(request,'edashboard.html',{'title':title})
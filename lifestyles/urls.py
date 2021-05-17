"""lifestyles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from lifes.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('dashboard/',dashboard,name="dashboard"),
    path('edashboard/',edashboard,name="edashboard"),
    path('profile/<int:id>/',profile,name="profile"),
    path('eprofile/<int:id>/',eprofile,name="eprofile"),
    path('invoices/',invoices,name="invoices"),
    path('contactus/',contactus,name="contactus"),
    path('unalo/',unalo,name="unalo"),
    path('contactchecker/',contactchecker,name="contactchecker"),
    path('contid/<int:id>/',contid,name="contid"),
    path('lives/',lives,name="lives"),
    path('bmic/',bmic,name="bmic"),
    path('bmrcal/',bmrcal,name="bmrcal"),
    path('subs/',subs,name="subs"),
    path('grocery/<int:id>/',grocery,name="grocery"),
    path('growth/',growth,name="growth"),
    path('fooddetail/<fooditem>/',fooddetail,name="fooddetail"),
    path('allocate/<int:id>/',allocate,name="allocate"),
    url('^', include('django.contrib.auth.urls')),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('login/',login,name="login"),
    path('logoutme/',logoutuser,name="logoutme"),
    path('elogin/',elogin,name="elogin"),
    path('register/',signup,name="signup"),
    path('eregister/',esignup,name="esignup"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Life Styles"
admin.site.site_title = "Admin Area | Life Styles"
admin.site.index_title = "Admin Control | Life Styles"
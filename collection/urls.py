__author__ = 'akash'
from django.conf.urls import url
from . import views

urlpatterns = [
    url('home', views.home, name='home'),
    url('mainboard',views.mainboard, name='mainboard'),
    url('sme',views.sme,name='sme'),
    url('ipoinfo',views.ipo_info, name='ipoinfo'),
    url('subscription',views.subscription,name='subscription'),
    url('register',views.register_request,name='register'),
    url('login',views.login_request,name='login'),
    url('logout',views.logout_request,name='logout'),
    url('allotment',views.allotment,name='allotment'),
    url('dividend',views.dividend, name='dividend')
]
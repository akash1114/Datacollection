from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from collection.models import *
from django.contrib import messages
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from lxml.html import fromstring
import datetime

from urllib.parse import urlparse
import re


# Create your views here.

# Home page
def home(request):
    mainboard_data = IpoDetails.objects.filter(category='MAINBOARD')
    sme_data = IpoDetails.objects.filter(category='SME')
    status(mainboard_data)
    status(sme_data)
    return render(request, 'IPO_pages/home.html', {'sme': sme_data, 'mainboard': mainboard_data})


def mainboard(request):
    mainboard_data = IpoDetails.objects.filter(category='MAINBOARD')
    return render(request, 'IPO_pages/ipos.html', {'data': mainboard_data, 'name': 'Mainboard'})


def sme(request):
    sme_data = IpoDetails.objects.filter(category='SME')
    return render(request, 'IPO_pages/ipos.html', {'data': sme_data, 'name': 'SME'})


# IPO Details page
def ipo_info(request):
    company_id = request.GET.get('company_id')

    details = IpoDetails.objects.get(id=company_id)
    try:
        dates = TentativeDate.objects.get(tentative_id=company_id)
        asset_data = Asset.objects.filter(asset_id=company_id)
        subscription_data = IpoSubscription.objects.filter(sub_id=company_id)
    except:
        dates = None
        asset_data = None
        subscription_data = None
    print(details)
    return render(request, 'IPO_pages/details.html', {
        'dates': dates,
        'details': details,
        'asset': asset_data,
        'sub': subscription_data
    })


# Ipo status
def status(ipos):
    for ipo in ipos:
        open_date = parsedate(str(ipo.open))
        clos_date = parsedate(str(ipo.close))
        try:
            if open_date > datetime.datetime.now():
                ipo.status = 'Upcoming'
            elif clos_date >= datetime.datetime.now() >= open_date:
                ipo.status = 'Current'
            else:
                ipo.status = 'Closed'
        except:
            ipo.status = '-'


# To compare dates
def parsedate(date):
    if (str(date) == 'None'):
        return None
    return datetime.datetime.strptime(date, '%Y-%m-%d')


def subscription(request):
    company_id = request.GET.get('company_id')
    details = IpoDetails.objects.get(id=company_id)
    try:
        subscription_data = IpoSubscription.objects.get(sub_id=company_id)
        share_data = ShareOffered.objects.get(share_id=company_id)
    except:
        subscription_data = None
        share_data = None

    return render(request, 'IPO_pages/subscription.html',
                  {'details': details,
                   'sub_data': subscription_data,
                   'share_data': share_data
                   })


def allotment(request):
    company_id = request.GET.get('company_id')
    details = IpoDetails.objects.get(id=company_id)

    print(details.open)
    try:
        dates = TentativeDate.objects.get(tentative_id=company_id)
        allotment_data = Allotment.objects.get(allotment_id=company_id)
    except:
        dates = None
        allotment_data = None
    print(allotment_data)
    return render(request,'IPO_pages/allotment.html', {
        'details':details,
        'dates':dates,
        'allotment_data':allotment_data
    })


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")

        messages.error(request, form.errors)
    e_form = None
    form = NewUserForm
    return render(request=request, template_name="user/registrarion.html", context={"register_form": form, "form": e_form})



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
        else:
            error = form.error_messages
            messages.error(request, form.error_messages.get('invalid_login'))
    form = AuthenticationForm()
    return render(request=request, template_name="user/login.html", context={"login_form": form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

def dividend(request):
    data = DividendData.objects.all()
    return render(request,'dividend.html',{'data':data})
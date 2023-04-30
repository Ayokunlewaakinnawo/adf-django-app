from django.shortcuts import render
from .models import ContactInfo
from .models import RegisterEventInfo
from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')

def contact(request):
    if request.method=="POST":
        contactpost =  ContactInfo()
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        subject=request.POST.get('desc')
        contactpost.Firstname=fname
        contactpost.Lastname=lname
        contactpost.Email=email
        contactpost.Phone=phone
        contactpost.Description=subject
        contactpost.save()

    return render(request, 'contact-us.html')

def event(request):
    return render(request, 'events.html')

def register(request):
    if request.method=="POST":
        registerpost =  RegisterEventInfo()
        fname=request.POST.get('Firstname')
        lname=request.POST.get('Lastname')
        email=request.POST.get('Email')
        phone=request.POST.get('Phone')
        location=request.POST.get('Location')
        category=request.POST.get('Category')
        registerpost.Firstname=fname
        registerpost.Lastname=lname
        registerpost.Email=email
        registerpost.Phone=phone
        registerpost.Location=location
        registerpost.Category=category
        registerpost.save()

    return render(request, 'registration-form-2.html')

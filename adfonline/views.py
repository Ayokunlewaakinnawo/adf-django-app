from django.shortcuts import render
from .models import ContactUsInfo
from .models import EventRegistration
from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')

def contact(request):
    if request.method=="POST":
        contactpost =  ContactUsInfo()
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
        registerpost =  EventRegistration()
        fname=request.POST.get('Firstname')
        lname=request.POST.get('Lastname')
        nname=request.POST.get('nickname')
        country=request.POST.get('Country')
        email=request.POST.get('Email')
        phone=request.POST.get('Phone')
        ady1=request.POST.get('address1')
        ady2=request.POST.get('address2')
        city=request.POST.get('City')
        zip=request.POST.get('ZipCode')
        category=request.POST.get('Category')
        registerpost.Firstname=fname
        registerpost.Lastname=lname
        registerpost.Nickname=nname
        registerpost.Country=country
        registerpost.Email=email
        registerpost.Phone=phone
        registerpost.Address1=ady1
        registerpost.Address2=ady2
        registerpost.City=city
        registerpost.ZipCode=zip
        registerpost.Category=category
        registerpost.save()
        
    return render(request, 'registration-form.html' )

def other(request):
    return render(request, 'otherpages.html')

def privacy(request):
    return render(request, 'privacypolicy.html')

def terms(request):
    return render(request, 'termsofservice.html')

def datacont(request):
    return render(request, 'datacontent.html')

def resource(request):
    return render(request, 'resources.html')

def resourcecont(request):
    return render(request, 'resourcecontentpg.html')

#Ticket Types page
def confticket(request):
    return render(request, 'conferenceticket.html')

#
def attendee(request):
    return render(request, 'attendeepass.html')

def sponsor(request):
    return render(request, 'sponsorpass.html')

def exhibit(request):
    return render(request, 'exhibitorpass.html')

def exhibitmember(request):
    return render(request, 'exhibitormemberpass.html')

def cultural(request):
    return render(request, 'cultural.html')

def linguistics(request):
    return render(request, 'linguistics.html')

def partnership(request):
    return render(request, 'PartnershipsContentPg.html')

def politics(request):
    return render(request, 'politicscontentpg.html')

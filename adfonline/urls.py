"""
URL configuration for adfonline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf import settings

#image uploads
from django.conf.urls.static import static

#USER APP
from users.views import *
#BLOG APP
from blog.views import *
#NEWS APP
from news.views import *

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="HomePage"), #Landing Page

    path('contact/', views.contact, name="ContactPage"),
    path('learnMore/', views.event, name="EventPage"),
    path('register/', views.register, name="RegisterPage"),
    path('other/', views.other, name="UnderConstruction"),
    path('privacy/', views.privacy, name="PrivacyPolicyPage"),
    path('terms/', views.terms, name="TermsofServicePage"),
    path('datacontent/', views.datacont, name="DataContPage"),
    path('resources/', views.resource, name="ResourcePage"),
    path('resourcecontent/', views.resourcecont, name="ResourceContPage"),
    path('cultural/', views.cultural, name="CulturalPage"),
    path('linguistics/', views.linguistics, name="LingPage"),
    path('partnership/', views.partnership, name="PartnershipPg"),
    path('politics/', views.politics, name="PoliticsPage"),


    path('conferenceticket/', views.confticket, name="TicketTypes"),
    path('attendeeticket/', views.attendee, name="AttendeeTicket"),
    path('sponsorticket/', views.sponsor, name="SponsorTicket"),
    path('sponsorcheckout', views.sponsorcheckout, name="S_Checkout"),
    path('sponsorcharge/', views.sponsorcharge, name="sponsorcharge"),
    path('exhibitticket/', views.exhibit, name="ExhibitTicket"),
    path('memberticket/', views.exhibitmember, name="MemberTicket"),
    path('ticketcheckout/', views.ticketcheckout, name="T_Checkout"),
    path('ticketcharge/', views.ticketcharge, name="ticketcharge"),



    #USER
    path('signup/', sign_up, name="sign_up"),
    path('login/', log_in, name="log_in"), #<----- Load Page
    path('logout/', logout_user, name="logout_user"),
    
    
    #nothing on to here please
    #DONATIONS
    path('donate/', views.donate, name="DonatePage"),
    path('give/', views.checkout, name="checkout"),
    path('charge/', views.charge, name="charge"), #Payment Charge from the Donation Checkout<---------
    path('success/', views.successMsg, name="success"),

    #NEWS
    path('newshome/', newshome, name="newshome"),
    path('<slug:slug>/', news, name="news_detail"),
    path('scrape/', scrape, name="scrape"),

    #BLOG
    path('createpost/', createpost, name="createpost"),
    path('Profile', profile, name="ProfilePg"),
    path('blog/', bloghome, name="BlogPg"),
    path('<slug:slug>/', blog, name="blog_detail"),
    path('editpost/<slug:slug>/', edit_blog_post, name="edit_blog_post" ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'adfonline.views.custom_404'

# Add the following at the end of your urlpatterns

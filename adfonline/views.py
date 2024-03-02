from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ContactUsInfo
from .models import EventRegistration
from django.http import HttpResponse, JsonResponse

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings

#SendGrid Import
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#Stripe Payment Import
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

#Handling 404 Page
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    return render(request, 'index.html')

def contact(request):
    if request.method=="POST":
        contactpost =  ContactUsInfo()
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        mssg=request.POST.get('desc')
        contactpost.Firstname=fname
        contactpost.Lastname=lname
        contactpost.Email=email
        contactpost.Phone=phone
        contactpost.Description=mssg
        try:
            # Your existing code for saving data and sending email
            contactpost.save()
            # Send an email
            subject = 'Contact Us Form Submission - AFRICA DATA FOUNDATION'
            message = f'Name: {fname} {lname}\nEmail: {email}\nPhone: {phone}\nMessage: {mssg}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['info@africadatafoundation.org']  # Replace with your email address

            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(str(e))
        
        messages.success(request, 'Your message has successfully been sent!')
        return redirect('success')
        
    return render(request, 'contact-us.html')


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


def cultural(request):
    return render(request, 'cultural.html')

def linguistics(request):
    return render(request, 'linguistics.html')

def partnership(request):
    return render(request, 'PartnershipsContentPg.html')

def politics(request):
    return render(request, 'politicscontentpg.html')


def donate(request):
    return render(request, 'donation.html')

#=============================================================
#---- 2023 EVENT REGISTRATION -----#
def event(request):
    return render(request, 'event-archive.html')

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

#Ticket Types page
def confticket(request):
    return render(request, 'conferenceticket.html')


def exhibit(request):
    return render(request, 'exhibitorpass.html')

def exhibitmember(request):
    return render(request, 'exhibitormemberpass.html')


#================================================
#Sponsor
def sponsor(request):
    if request.method == 'POST':
        sponsortype = request.POST.get('sponsortype')

        return redirect('S_Checkout', sponsortype=sponsortype)
    return render(request, 'sponsorpass.html')

def sponsorcheckout(request):
    if request.method == 'POST':
        s_amount_packages = {
            'bronze': 5000,
            'silver': 10000,
            'gold': 25000,
            'lunch': 30000,
            'platinum': 50000,
            'emerald': 75000,
            'diamond': 100000,
        }
        sponsortype = request.POST['sponsortype']
        amount = s_amount_packages[sponsortype]

        context = { 'amount': amount,
                    'sponsortype': sponsortype}
    return render(request, 'sponsor-checkout.html', context)


def sponsorcharge(request):
    if request.method == 'POST':
        print('Data:', request.POST)
        

        amount = int(request.POST['amount'])
        #firm=request.POST['firm'],
        #phone=request.POST['phone'],

        #Charge card
        try:
            customer = stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['name'],
                source=request.POST['stripeToken']
            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=amount * 100,
                currency='usd',
                description=f"Sponsor Purchase"
            )

            # Send email to the sponsor after purchase
            try:
                subject = 'Sponsor Purchase Confirmation'
                message = f''
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email']]

                # Load and render the email template
                html_message = render(request, 'email/email_template.html', {
                    'purpose': 'sponsor_purchase',
                    'sponsor_holder': request.POST['name'],
                    'sponsor_ref': request.POST['stripeToken'],
                    'sponsor_price': int(request.POST['amount'])
                }).content.decode('utf-8')

                # Send the email with HTML content
                send_mail(subject, message, from_email, recipient_list, html_message=html_message, fail_silently=True)


                #=========================================
                #For Admin - info@africadatafoundation.org
                # Send notification email to settings.EMAIL_HOST_USER
                subject_user = '2023 Conference - Sponsor Purchase Notification'
                message_user = f''
                recipient_user = [settings.EMAIL_HOST_USER]

                # Load and render the email template
                html_message = render(request, 'email/email_template.html', {
                    'purpose': 'sponsor_notify',
                    'sponsor_holder': request.POST['name'],
                    'sponsor_ref': request.POST['stripeToken'],
                    'sponsor_price': int(request.POST['amount']),
                    'email_sponsor': request.POST['email'],
                    'sponsor_phone': request.POST['phone'],
                    'sponsor_firm': request.POST['firm']
                }).content.decode('utf-8')
                send_mail(subject_user, message_user, from_email, recipient_user, html_message=html_message, fail_silently=True)

            except Exception as e:
                print(str(e))
                #print(e.message)

            messages.success(request, 'Sponsors Pass has successfully been purchased!')
            return redirect(reverse('success'))
        
        #Handling errors from card fail to charge 
        except stripe.error.CardError as e:
            messages.error(request, 'Payment failed. Please check your card details and try again.')
            return redirect(reverse('sponsorcharge'))
        except stripe.error.InvalidRequestError as e:
            messages.error(request, 'Payment failed. Please check your card details and try again.')
            return redirect(reverse('sponsorcharge'))
        except Exception as e:
            messages.error(request, 'Payment failed. Please check your card details and try again.')
            return redirect('sponsorcharge')
        
    return render(request, 'sponsor-checkout.html')

#=================================================
#Main Ticket
def attendee(request):
    if request.method == 'POST':
        tickettype = request.POST.get('tickettype')

        return redirect('T_Checkout', tickettype=tickettype)
    return render(request, 'attendeepass.html')


def ticketcheckout(request):
    if request.method == 'POST':
        amount_packages = {
            'student': 150,
            'member': 500,
            'non-member': 700,
            'standard': 1500,
            'executive': 6000,
        }
        tickettype = request.POST['tickettype']
        amount = amount_packages[tickettype]

        context = { 'amount': amount,
                    'tickettype': tickettype}
    return render(request, 'ticket-checkout.html', context)

def ticketcharge(request):
    if request.method == 'POST':
        print('Data:', request.POST)
        

        amount = int(request.POST['amount'])

        #Charge card
        try:
            customer = stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['name'],
                source=request.POST['stripeToken']
            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=amount * 100,
                currency='usd',
                description=f"Ticket Purchase"
            )

            # Send email to the customer after ticket purchase
            try:
                subject = 'Ticket Purchase Confirmation'
                message = f''
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email']]

                # Load and render the email template
                html_message = render(request, 'email/email_template.html', {
                    'purpose': 'ticket_purchase',
                    'ticket_holder': request.POST['name'],
                    'ticket_ref': request.POST['stripeToken'],
                    'ticket_price': int(request.POST['amount'])
                }).content.decode('utf-8')

                # Send the email with HTML content
                send_mail(subject, message, from_email, recipient_list, html_message=html_message, fail_silently=True)


                #=========================================
                #For Admin - info@africadatafoundation.org
                # Send notification email to settings.EMAIL_HOST_USER
                subject_user = '2023 Conference - Ticket Purchase Notification'
                message_user = f''
                recipient_user = [settings.EMAIL_HOST_USER]

                # Load and render the email template
                html_message = render(request, 'email/email_template.html', {
                    'purpose': 'ticket_notify',
                    'ticket_holder': request.POST['name'],
                    'ticket_ref': request.POST['stripeToken'],
                    'ticket_price': int(request.POST['amount']),
                    'email_buyer': request.POST['email'],
                    'ticket_holder': request.POST['name']
                }).content.decode('utf-8')
                send_mail(subject_user, message_user, from_email, recipient_user, html_message=html_message, fail_silently=True)

            except Exception as e:
                print(str(e))
                #print(e.message)

            messages.success(request, 'Ticket has successfully been purchased!')
            return redirect(reverse('success'))
        
        #Handling errors from card fail to charge 
        except stripe.error.CardError as e:
            messages.error(request, 'Payment failed. Please check your card details and try again.')
            return redirect(reverse('ticketcharge'))
        except stripe.error.InvalidRequestError as e:
            messages.error(request, 'Payment failed. Please check your card details and try again.')
            return redirect(reverse('ticketcharge'))
        except Exception as e:
            messages.error(request, 'Payment failed. Please check your card details and try again.')
            return redirect('ticketcharge')
        
    return render(request, 'ticket-checkout.html')



def checkout(request):
    return render(request, 'checkout.html')




#======================================================================
#------CHARGE FOR DONATION--------------
def charge(request):
    if request.method == 'POST':
        print('Data:', request.POST)

        amount = int(request.POST['amount'])

        try:
            customer = stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['name'],
                source=request.POST['stripeToken']
            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=amount * 100,
                currency='usd',
                description="Donation"
            )

            # Send email to the customer after Donation
            try:
                subject = 'Donation Notification - Africa Data Foundation'
                message = f''
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email']]
            
               # Load and render the email template
                html_message = render(request, 'email/email_template.html', {
                    'purpose': 'donation',
                    'donor_name': request.POST['name'],
                    'donation_amount': int(request.POST['amount'])
                }).content.decode('utf-8')

                # Send the email with HTML content
                send_mail(subject, message, from_email, recipient_list, html_message=html_message, fail_silently=True)


                 #=========================================
                #For Admin - info@africadatafoundation.org
                # Send notification email to settings.EMAIL_HOST_USER
                subject_user = 'Donation Notification'
                message_user = f''
                recipient_user = [settings.EMAIL_HOST_USER]

                # Load and render the email template
                html_message = render(request, 'email/email_template.html', {
                    'purpose': 'donate_notify',
                    'donor_name': request.POST['name'],
                    'donation_amount': int(request.POST['amount']),
                    'donor_email': request.POST['email']
                }).content.decode('utf-8')
                send_mail(subject_user, message_user, from_email, recipient_user, html_message=html_message, fail_silently=True)

            except Exception as e:
                print(str(e))
                #print(e.message)
            #-----Send Grid Parse-----------#
                        
            #message = Mail(
                #from_email=settings.FROM_EMAIL_ADDRESS,
                #to_emails= [request.POST['email']],
                #subject='Payment Confirmation',
                #html_content=f'Thank you for your donation of ${amount:.2f}.')
            #try:
                #sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                #response = sg.send(message)
                #print(response.status_code)
                #print(response.body)
                #print(response.headers)
            #except Exception as e:
                #print(e.message)
            messages.success(request, f'Thank you for your donation of ${amount:.2f}.')
            return redirect('success')
        
        #Handling errors from card fail to charge 
        except stripe.error.CardError as e:
            messages.error(request, 'Payment failed. Please check your card details and try again.')
            return redirect(reverse('charge'))
        except stripe.error.InvalidRequestError as e:
            messages.error(request, 'Payment failed. Please check your card details and try again.')
            return redirect(reverse('charge'))
        except Exception as e:
            messages.error(request, 'Payment failed. Please check your card details and try again.')
            return redirect(reverse('charge'))
        
    return render(request, 'checkout.html')
                

def successMsg(request):
	return render(request, 'payment-success.html')




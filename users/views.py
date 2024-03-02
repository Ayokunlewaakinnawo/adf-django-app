from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.forms import  UserCreationForm
from django.conf import settings


from django.contrib.auth import authenticate, login, logout

from .forms import *
from django.contrib.auth import update_session_auth_hash #Password Reset

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.db import IntegrityError

from django.core.mail import send_mail
from django.template.loader import render_to_string



#Create your View here
from .forms import CreateUserForm

#Model from another app
from blog.models import BlogPost

# --------------------------> USER AUTHENTICATION AFICA-DATA-FOUNDATION <---------------------------------
# LOG IN 
def log_in(request):
    if request.user.is_authenticated:
        return redirect('ProfilePg')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                print("User authenticated successfully")
                login(request, user)
                return redirect('ProfilePg')
            else:
                print("User authentication failed")
                messages.error(request, 'Invalid Email or password')
                return redirect("log_in")
            
        context = {}
        return render(request, 'log-in.html', context)
  

#CREATING AN ACCOUNT
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('ProfilePg')
    else:

        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():

                try:
                    form.save()
                    
                    # Send an email
                    subject = 'Account Created'
                    message = f''
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [form.cleaned_data['email']]

                    # Load and render the email template
                    html_message = render(request, 'email/email_template.html', {
                        'purpose': 'new_user',
                        'user_fname': form.cleaned_data['first_name'],
                        'user_lname': form.cleaned_data['last_name'],
                        'user_email': form.cleaned_data['email']
                    }).content.decode('utf-8')

                    send_mail(subject, message, from_email, recipient_list, html_message=html_message, fail_silently=True)

                    messages.success(request, 'User account has been created successfully')
                    return redirect("log_in")

                except IntegrityError:
                    messages.error(request, 'User already exists. Please choose a different email.')

        context = {'form': form}  # Pass errors to context
        return render(request, "sign-up.html", context)
    
#----------------------------------------------------------------------------->


#LOG-OUT 
def logout_user(request):
    logout(request)
    return redirect("log_in")

@login_required(login_url='log_in')
def nav_active(request):
    if request.user.is_authenticated:
        return render(request, 'base/navbar_loggedin.html', {'user': request.user})


#----------------> USER PROFILE PAGE <------------------------------------------------
@login_required(login_url='log_in')
def profile(request):

    #PASSWORD RESET / CHANGE ACCOUNT PASSWORD
    if not request.user.is_authenticated:
        return redirect('log_in')

    if request.method == 'POST':
        if 'change_pwd' in request.POST:
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('ProfilePg')
    else:
        form = ChangePasswordForm(request.user)
        print(form.errors)
    
    ## Get the user's blog posts to display on user profile
    user_posts = BlogPost.objects.filter(user=request.user)



    #UPDATING EXTENDED PROFILE
    if request.method == 'POST':
        # Check if a delete request is made
        if 'update_user' in request.POST:
            update_form = UpdateProfileForm(request.POST, instance=request.user)
            if update_form.is_valid():
                update_form.save()
                print(update_form)
                return redirect('ProfilePg')  
    else:
        update_form = UpdateProfileForm(instance=request.user)



    #USER DELETE BLOG POST
    if request.method == 'POST':
        # Check if a delete request is made
        if 'delete_post' in request.POST:
            slug = request.POST.get('slug')
            try:
                post_to_delete = BlogPost.objects.get(slug=slug)

                # Get related images associated with the post
                images_to_delete = []
                if post_to_delete.image1:
                    images_to_delete.append(post_to_delete.image1)
                if post_to_delete.image2:
                    images_to_delete.append(post_to_delete.image2)
                
                # Delete each related image
                for image in images_to_delete:
                    image.delete()

                # Delete the post
                post_to_delete.delete()
                messages.success(request, 'Post deleted successfully!')
                return redirect('ProfilePg')
            except BlogPost.DoesNotExist:
                # Handle case where post with given ID does not exist
                pass
    context = {
        'user_posts': user_posts,
        'form' : form,
        'update_form':update_form,
    }
    return render(request, 'user-account.html', context)


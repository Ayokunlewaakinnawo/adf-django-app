# adf-django-app
Setup

Update the System

>sudo apt-get update -ubuntu
>

To get this repository, run the following command inside your git enabled terminal

git clone https://github.com/ayokunlewaakinnawo/adf-django-app.git

You will need django to be installed in you computer to run this app. Head over to https://www.djangoproject.com/download/ for the download guide

Download django usig pip

>sudo apt install python3-pip -y
>pip install django

>sudo yum install python3-venv

Activate a virtual env
>source myenv/bin/activate

update Package
>python -m pip install --upgrade pip


Once you have downloaded django, go to the cloned repo directory and run the following command

>python3 manage.py makemigrations

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command

>python3 manage.py migrate

One last step and then our todo App will be live. We need to create an admin user to run this App. On the terminal, type the following command and provide username, password and email for the admin user

>python3 manage.py createsuperuser

That was pretty simple, right? Now let's make the App live. We just need to start the server now and then we can start using our simple todo App. Start the server by following command

>python3 manage.py runserver


Launchin live

install Nginx, gunicorn and supervisor: web server, connecting web-server to app and maintaing the web app live at the bckgrnd respectively.
 

*************************************************


>sudo yum update - Linux distribution

If on Amazon Linux 2, you would have to upgrade you sqlite;
>wget https://www.sqlite.org/2022/sqlite-tools-linux-x86-3400000.zip
>
>unzip sqlite-tools*.zip
>
>cd sqlite-tools* 
>
>sudo cp sql* /usr/local/bin/  # Usually this directory is empty, so no need to worry about overwriting files 
>
>cd ~
>
>sudo yum update -y
>
>sudo amazon-linux-extras install epel -y 
>
>sudo yum install glibc.i686 -y
>
>sqlite3 --version 
>

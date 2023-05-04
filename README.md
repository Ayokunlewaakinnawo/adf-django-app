# Deploying adfonline 
Setup -on Amazon EC2 (Ubuntu)

Update the System

>sudo apt-get update -ubuntu
>sudo apt-get update
>sudo apt-get upgrade

install python3 virtual enviroment set up pip;
>sudo apt-get install python3-venv

Create Virtual enviroment "env" and activate it:
>python3 -m venv env
>source env/bin/activate

install dependensies and download project from git
>pip3 install django
>git clone https://github.com/Ayokunlewaakinnawo/adfonline.git
>



install gunicorn
.
install supervisor
>sudo apt-get install supervisor

configure supervisor
>cd /etc/supervisor/conf.d/
>sudo touch gunicorn.conf
>sudo nano gunicorn.conf

server{

        [program:gunicorn]
        directory=/home/ubuntu/adfonline
        command=/home/ubuntu/env/bin/gunicorn --worker 3 --bind unix:/home/ubuntu/adfonline/app.sock adfonline.wsgi:application
        autostart=true
        autorestart=true
        stderr_logfile=/var/log/gunicorn/gunicorn.err.log
        stdout_logfile=/var/log/gunicorn/gunicorn.out.log

        [group:guni]
        programs:gunicorn
}



create log dri.;
>sudi mkdir /var/log/gunicorn

read from config file(gunicorn conf)
>sudo supervisorctl reread

tell supervisor to start gunicorn in the bckgrd;
>sudo supervisorctl update

to test and see gunicorn is working;
>sudo supervisorctl status


install nginx
>sudo apt-get install -y nginx
create a file "django.conf" at dir. /etc/nginx/sites-available.
>sudo touch django.conf
>nano django.conf

edit file django.conf with;
server{

        server{

                listen 80;
                server_name 3.144.4.134;


        location / {

                include proxy_params;
                proxy_pass http://unix:/home/ubuntu/adfonline/app.sock;

        }

        location /static/ {
                alias /home/ubuntu/adfonline/web/static/;
        }
        }
}


to test your nginx syntax;
>sudo nginx -t

run to go live;
>sudo ln django.conf /etc/nginx/sites-enabled 

# Deployment Setup

This Django framework project focuses on event registration and contact information. It also includes a walkthrough for deploying the application on AWS Elastic Computing 2 instance.

**Framework** 

Django framework project on event registration and contact info.

**Deploying adfonline**

Setup -on Amazon EC2 (Ubuntu)

Update the System

> 
> 

```json
sudo apt-get update
```

install python3 virtual enviroment set up pip;

```json
sudo apt-get install python3-venv
```

> 
> 

Create Virtual enviroment "env" and activate it:

```json
python3 -m venv env
source env/bin/activate
```

install dependensies and download project from git:

```json
pip3 install django
git clone [https://github.com/Ayokunlewaakinnawo/adfonline.git](https://github.com/Ayokunlewaakinnawo/adfonline.git)
```

install nginx . install gunicorn . install supervisor

```json
install nginx
sudo apt-get install -y nginx
pip install gunicorn

```

> 
> 

connect to the ec2 pubic address and make sure the landing page of nginx is showing

install and setup supervisor ; This will keep the application running in the background.

```json
sudo apt-get install supervisor
```

configure supervisor;

```json
cd /etc/supervisor/conf.d/
```

Create gunicorn configuration file;

```json
sudo touch gunicorn.conf
sudo nano gunicorn.conf
```

```json
[program:gunicorn]

directory=/home/ubuntu/elevate

command=/home/ubuntu/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/elevate/app.sock elevate.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout_logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
programs:gunicorn

```

create log dri.;

```json
sudo mkdir /var/log/gunicorn
```

> 
> 

read from config file(gunicorn conf);

```json
sudo supervisorctl reread
```

> 
> 

tell supervisor to start gunicorn in the bckgrd;

```json
sudo supervisorctl update
```

> 
> 

To test and see gunicorn is working;

```json
sudo supervisorctl status
```

> 
> 

> cd .. to go back to etc.>
> 

To modify an existing file "nginx.cong"

```json
cd nginx
sudo nano nginx.conf
```

edit the user from wwwdata to root;save and exit

> cd .. create a file "django.conf" at dir. /etc/nginx/sites-available;
> 

```json
cd /etc/nginx/sites-available
```

> 
> 

> 
> 

Create the file;

sudo touch django.conf sudo nano django.conf edit file django.conf with;

```
listen 80;
server_name XX.XXXX.XX.X;

location / {

	include proxy_params;
	proxy_pass http://unix:/home/ubuntu/elevate/app.sock;

}
    location /static/ {
            alias /home/ubuntu/adfonline/web/static/;
    }
location /static/admin/ {
            alias /home/ubuntu/env/lib/python3.10/site-packages/django/contrib/admin/static/admin/;
    }

```

to test your nginx syntax;

```json
sudo nginx -t
```

> 
> 

run to go live;

```json
sudo ln django.conf /etc/nginx/sites-enabled
```

```json
sudo service nginx restart
```

make sure the EC2 instance public addy is included to the allowed host on the django settings file. if you make any correection to the project, restart nginx and supervior services.

```json
sudo service supervisor restart
```

> 
> 

##Setting up ssl

```json
sudo apt install snapd
sudo snap install --classic certbot
```
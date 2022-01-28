pip install django==3.2
pip install django-debug-toolbar==3.2.3
django-admin --help
django-admin startproject projectname
cd projectname
python manage.py --help

###
###urls - address dispatcher
###
###settings - allowed_host, debug,
### installed_apps - #third path apps - debug_toolbar  - add application
### 
### 

python manage.py runserver 


python manage.py startapp name_app
### add name_app in /settings.py    (installed_apps)

###

### for admin
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

### views.py -> controllers add -> add to url (import, path) /





# IPSSI Django Project

[![License](https://img.shields.io/static/v1.svg?label=license&message=proprietary&color=blue)](https://img.shields.io/puppetforge/rc/:user.svg)


#### Creating a project
```bash
django-admin startproject ipssiad
```

#### Creating the handler app
```bash
python manage.py startapp handler
```

#### Create a super user
First we’ll need to create a user who can login to the admin site. Run the following command:
```bash
python manage.py createsuperuser
```

#Instalation
    
    git clone https://github.com/Ylahjaily
    docker-compose up
    
#Initialization
    -> Open Portainer running at http://localhost:30033/
    -> Open the Ipssi-python container's console 
        -> pip-install -r requirements.txt
        -> python manage.py makemigrations
        -> pyhton manage.py migrate
        -> python manage.py runserver 0:8000
        -> python manage.py createsuperuser




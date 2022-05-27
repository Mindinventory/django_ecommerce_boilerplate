# **E-commerce Web application Using Django**

<a href="https://docs.python.org/3.10/" style="pointer-events: stroke;" target="_blank">
<img src="https://img.shields.io/badge/python-3.10-yellowgreen">
</a>
<a href="https://pip.pypa.io/en/stable/" style="pointer-events: stroke;" target="_blank">
<img src="https://img.shields.io/badge/pip%20-22.0-orange">
</a>
<a href="https://docs.djangoproject.com/en/4.0/" style="pointer-events: stroke;" target="_blank">
<img src="https://img.shields.io/badge/django%20-4.0.4-red">
</a>
<br/><br/>

A web application built in Django for purchasing products online.

## **Project setup**

Clone the repository:

````
$ git clone https://github.com/Mindinventory/django_ecommerce_boilerplate.git
````

Create virtual environment:

````
$ virtualenv venv
$ source venv/bin/activate
````

You will see in front of the prompt that the virtual environment (venv) has been activated.

Install the dependencies:

````
$ pip install -r requirements.txt
````

## **Set up a database**

Configure Database settings in settings.py folder as suggested in below documentation:

````
https://docs.djangoproject.com/en/4.0/ref/settings/#databases
````

Create a .env file in the project folder. You can find .env.example file for your reference.

Execute below command to create migrations and register models in the database:

````
python manage.py makemigrations users
python manage.py makemigrations store
python manage.py migrate
````

## **Set up the products module**

Run the below command to populate the database with products:

````
 python manage.py loaddata products.json
````

## **Starting the web server**

Run the development server using below command:

````
python manage.py runserver
````

Navigate to http://127.0.0.1:8000/


![alt text](https://github.com/rutvi-mi/django_ecommerce_boilerplate/blob/main/ecommerce.gif)


## **Create an account on stripe for accepting payments**

````
 https://dashboard.stripe.com/settings/account?support_details=true
````

##  Note: **For payment integration using stripe, add stripe required keys in .env file. You can get them from stripe Dashboard.**

````
https://dashboard.stripe.com/test/dashboard
````














# Getting started with Django


## Basic Setup

### Install Dependencies

Let's start by installing the dependencies. 
```
$ pip install django psycopg2-binary
```

### Create application
Now, let's create the application template
```
$ cd src
$ django-admin startproject app_customermgmt
```

### Update settings
Next, we will update the default database settings to use PostgreSQL
Update the default database settings in the file `settings.py` 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'microSERVICE',
        'USER': 'postgres',
        'PASSWORD': 'postgres123',
        'HOST': 'localhost',
        'PORT': '5433',
    }    
}
```

### Run migrations
Now, lets setup the database by running migrations
```
$ python manage.py makemigrations
$ python manage.py migrate
```

### Setup admin
Create an admin user for the django application
```
$ python manage.py createsuperuser
```

### Run Server
Now, we can run the server
```
$ python manage.py runserver 0.0.0.0:8000

```


## Building a REST API 

With the basic setup out of our way, let's create an application to expose a simple web API. We will use Django REST Framework to simplify development of this application.

### Install Dependencies

Let's start by installing the dependencies. 
```
$ pip install djangorestframework
```

### Create application
```
$ python manage.py startapp api_customers

```

### Update settings
We will update `settings.py` to indicate we will be using REST Framework
To do that, we will add the line `'rest_framework',` to the list of `INSTALLED_APPS` section
```
INSTALLED_APPS = (
    ...
    'rest_framework',
    'api_customers',
)
```

We will also add a section for pagination related settings
```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

Add a simple model class `api_customers/models.py`
```
# Create your models here.
class Customer(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField()

    updated_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.TextField()

    name = models.CharField(max_length=400,blank=False, default='')
    phone = models.TextField(blank=False, default='')

    deleted = models.BooleanField(default=False)
```

Run the migrations to create a database table for our entity
```
$ python manage.py makemigrations api_customers
Migrations for 'api_customers':
  api_customers/migrations/0001_initial.py
    - Create model Customer

```

Follow this tutorial for detailed step-by-step guide
https://www.django-rest-framework.org/tutorial/


## Testing 

We will use pytest, Read the docs
https://pytest-django.readthedocs.io/en/latest/tutorial.html 

### Install the following packages
pip install pytest pytest-django pytest-cov mixer

Add the following files to the main Django project 
* `test_settings.py` file for test database and other settings,
* `pytest.ini` file for pytest configuration to the application root folder
* `.coveragerc` file to state exclusions for test coverage to the application root folder

You can run the tests from the root directory of the django application using the command `pytest`. Test coverage report should be generated in a folder called `htmlcov`. Look for the report `index.html`.

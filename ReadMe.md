## Tutorial
https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5

## Conda environment
source activate django-rest-2

## create project
django-admin.py startproject woa-api .

## create app
django-admin.py startapp woa_api_pazienti

## migration and superuser
python manage.py migrate
python manage.py createsuperuser --email cristiano.deg@gmail.com --username cristiano
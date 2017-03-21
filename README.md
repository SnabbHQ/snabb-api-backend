Snabb
====

Snabb!

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)

Install Instructions
--------
In order to get your development environment up and running please follow the instructions here: [Install Guide](docs/install.md)


Settings
--------

Moved to
[settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

Basic Commands
--------------

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out
    the form. Once you submit it, you'll see a "Verify Your E-mail
    Address" page. Go to your console to see a simulated email
    verification message. Copy the link into your browser. Now the
    user's email should be verified and ready to go.
-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.

### Test coverage

To run the tests, check your test coverage, and generate an HTML
coverage report:

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with py.test

    $ pytest snabb

If you want to use pytest and coverage at the same time.

    $ pytest snabb --cov=snabb --cov-report html

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS
compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

### Sentry

Sentry is an error logging aggregator service. You can sign up for a
free account at <https://getsentry.com/signup/?code=cookiecutter> or
download and host it yourself. The system is setup with reasonable
defaults, including 404 logging and integration with the WSGI
application.

You must set the DSN url in production.

Deployment
----------

The following details how to deploy this application.

### Docker

In order to get docker working on your local machine first of all you need to bake the image:

    $docker-compose -f dev.yml build

This will setup docker compose with the development environment. If you setup it for the first time or need to run
migrations, you can run the commands in the already created image as follows:

    $docker-compose -f dev.yml run django python manage.py makemigrations
    $docker-compose -f dev.yml run django python manage.py migrate
    $docker-compose -f dev.yml run django python manage.py createsuperuser

Finally you can simply run the docker container using (Remember the first time will take a bit of time but once it is
done, will be super fast!):    

    $docker-compose -f dev.yml up


See detailed [cookiecutter-django Docker
documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-elastic-beanstalk.html).

#### Elastic Beanstalk

See detailed cookiecutter-django Elastic Beanstalk documentation\_.

#### Deploy in development server

    $ssh -i YOUR_KEY.pem ubuntu@54.246.188.31
    $sudo su snabb
    $cd ~/snabb-api-backend/
    $git pull origin develop
    $docker-compose -f dev.yml build
    $docker-compose -f dev.yml up -d
    $docker-compose -f dev.yml run django python manage.py makemigrations
    $docker-compose -f dev.yml run django python manage.py migrate
    $docker-compose -f dev.yml run django pytest snabb --cov=snabb

### Sync you local BBDD with Onfleet

    $docker-compose -f dev.yml run django python manage.py sync_onfleet

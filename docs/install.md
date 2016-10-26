Install
=======

Initial Dev Setup
-----------------

### Internationalization

Make sure your local locale is set to a valid one.

To do this you can run:

    export LC_ALL=en_US.UTF-8
    export LANG=en_US.UTF-8

This will be necessary every time the project is to be run. Consider
adding it to your bash\_profile.

### Python setup

Make sure python 3.5 is installed:

    $ brew install python3

Create a virtualenv:

    $ python3 -m venv snabb_env
    $ source snabb_env/bin/activate

### Create the Database

Install postgres:

    $ brew install postgres

Restart the postgres server:

    $ brew services restart postgresql

Create the database:

    $ createdb snabb

### Installing the dependencies

With a virtualenv activated, and from the project root, execute:

    $ pip3 install -r requirements/local.txt

### Run the migrations

With a virtualenv activated, and from the project root, execute:

    $ python3 manage.py migrate

### Running the dev server

With a virtualenv activated, and from the project root, execute:

    $ python manage.py runserver

Go to <http://localhost:8000/>

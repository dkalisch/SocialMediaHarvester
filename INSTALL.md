# Install SMH

## Requirements
To be able to run an instance of SMH the following components have to be installed on your system:
- Apache 2 (incl. wsgi)
- MongoDB (v2.6.3)
- PostgreSQL (v9.1.13)
- Python 2.7

You further need the following python modules:
- Django==1.4.3
- amqp==1.4.5
- anyjson==0.3.3
- argparse==1.2.1
- billiard==3.3.0.17
- kombu==3.0.16
- oauthlib==0.6.1
- psutil==2.1.1
- psycopg2==2.5.3
- pymongo==2.6.3
- pytz==2014.3
- requests==2.1.0
- requests-oauthlib==0.4.0
- twython==3.1.2
- wsgiref==0.1.2

## Set up virtual environment
A standard practice in web development with python is using a virtual environment. A virtual environment provides some kind of sandbox for setting up a project specific python environment. If your python installation or a specific python module is changed these changes only affect the applications that are installed inside the virtual environment. In parallel, changes to other python installations don't have an impact on your virtual environment.
To set up a virtual environment the following python modules have to be installed:
- pip
- python-dev
- virtualenv

Now you can create your virtual environment with:

```
	virtualenv <environment_name>
```

This command creates two important directories:

```
	<environment_name>/bin/python/ - python interpreter
	<environment_name>/lib/pythonX.X/site-packages – installed python modules
```

To work with the virtual environment and to change python modules the virtual environment has to be activated by running:

```
	source ./<environment_name>/bin/activate
```

It can be deactivated with:

```
	deactivate
```

To install SMH all the required python modules have to be installed. Therefore activate your virtual environment and install all the modules by running:

```
	pip install requirements.txt
```

The txt-file holds information about the modules.

## Copy source code
After setting up the environment the source code must be copied to a location inside the virtual environment.
Then check if all the paths are set correctly, especially in settings.py (and twitter.py?).

### Configure Django
Django should be able to connect to the installed PostgreSQL and MongoDB databases. To accomplish this the DATABASES variable inside settings.py file has to be edited.
To create all the tables in your database run:

```
	python manage.py syncdb
```

If a superuser was not created n snycing the db creating a superuser manually is necessary. This can be achieved with the following command:

```
	python ./manage.py shell

```python
	from django.contrib.auth.create_superuser import createsuperuser
	createsuperuser()
```

or:

```
	python ./manage.py createsuperuser
```

### Connect SMH and Apache
To make SMH accessible from the outside it has to be connected to Apache. Therefore copy the smh-file to /etc/apache2/sites-available/ and change the paths to your smh folder.
To complete restart apache with service apache2 restart . Now SMH is reachable under the name entered at “ServerName”.

### Set up cronjob
SMH checks periodically if a query has expired. For this purpose a cronjob has to be setup by editing crontab:

```
	crontab -e
```

Then enter a new job:

```
	*/5 * * * * <path to tools/query_checker.py> >> <path to logs> 2>&1
```

and save. Now the query_checker.py script is executed every 5 minutes. Print-statement will go to the file specified in 'path to logs'. Normal logging statements go to the standard SMH logfile.

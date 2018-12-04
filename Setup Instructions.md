## Setup Instructions

* Requirements: Pyhton, Anaconda3, Internet
* Open command prompt in project folder and run following commands to setup project
	* conda create --name DjangoEnv
	* activate DjangoEnv
	* pip install -r requirements.txt
	* cd django_summer_project
	* python manage.py makemigrations
	* python manage.py migrate
	* python manage.py runserver
	* Open http://127.0.0.1:8000/
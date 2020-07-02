# AKADEMIA

A platform where institution administrators, teachers, and students can share the study material with each other, and upload events details that are to happen in the institution.

## Setup Instructions

* Requirements: Python, Anaconda3, Internet
* Open project folder in command prompt and run following commands to setup project
	* conda create --name DjangoEnv
	* activate DjangoEnv
	* pip install -r requirements.txt
	* cd django_summer_project
	* python manage.py makemigrations
	* python manage.py migrate
	* python manage.py runserver
	* Open http://127.0.0.1:8000/

## Ideas

### Users

* Student
* Teacher
* Moderator (Admin)


### LogIn/Registration

* **Student**
  * Username (Roll No.)
    * if password null , random password generated and sent to registered mail (Pop-Up)
    * if not null, log-in with registered mail and password
    * if username not present, error "User not registered.Contact Administrator"
  * Profile Completion (Boolean)
    * True -> Edit Profile page not displayed
    * False -> Edit Profile Page displayed

* **Teacher** (Similarly to student login)
  * Email and Password

* **Moderator** (By Default - superuser)

### Dashboard

* **Student**
  * Navigation Bar
    * Dashboard link
    * Features Link
    * User Profile
  * Navigation Menu
    * User Info
    * Points Info
  * Main Body
    * Welcome meassage
    * Features Card View

* **Teacher**
  * Navigation Bar
    * Dashboard link
    * Features Link
    * User Profile
  * Navigation Menu
    * User Info
  * Main Body
    * Welcome meassage
    * Features Card View

### Profile (inherit dashboard template)

* **Student**
  * Name
  * Parent's Name
  * Email and Password
  * Manage Password
  * Department
  * Semester
  * Batch (fixed)
  * Profile Pic
  * Roll No. (fixed)
  * Contact Number

* **Teacher**
  * Name
  * Designation
  * Educational Qualification
  * Area of Specialization
  * Email and Password
  * Manage Password
  * Department
  * Profile Pic
  * Additional Role
  * Website Link
  * Contact Number

### Study Corner
  
#### Student Database

* Notes -> Batch -> Semester -> Subjects -> Files
* Question Paper -> Batch -> Semester -> Subjects -> Files
* Study Material -> Subjects -> Teachers -> Material/Files

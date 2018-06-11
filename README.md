# Ideas

## Users

* Student
* Teacher
* Moderator (Admin)


## LogIn/Registration

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

## Dashboard

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

## Profile (inherit dashboard template)

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

## Study Corner
  
### Student Database

* Notes -> Batch -> Semester -> Subjects -> Files
* Question Paper -> Batch -> Semester -> Subjects -> Files
* Study Material -> Subjects -> Teachers -> Material/Files

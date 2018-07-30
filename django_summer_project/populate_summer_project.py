import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_summer_project.settings')

import django

django.setup()

from faker import Faker
from summer_project.models import MyCustomUser, MyCustomUserManager, StudentInfo, TeacherInfo, Batch

fakegen = Faker()


def populate_teachers(N=5):
    for entry in range(N):
        first_name = fakegen.first_name()
        last_name = fakegen.last_name()
        fake_username = fakegen.user_name()
        fake_email = fakegen.email()
        fake_password = first_name + last_name
        new_teacher = MyCustomUser.objects.create_teacher_user(username=fake_username,
                                                               email=fake_email, password=fake_password,
                                                               first_name=first_name
                                                               , last_name=last_name)
        if new_teacher:
            print(new_teacher, " Created Successfully", "Entry:", entry)
        else:
            print("User Not Created for entry", entry)


def createMultipleUsers(start, end, year, dept, semester):
    department = None
    if dept.find("ME") > -1 or dept.find("Mechanical") > -1:
        department = "ME"
        dept = "Mechanical"
    elif dept.find("CE") > -1 or dept.find("Civil") > -1:
        department = "CE"
        dept = "Civil"
    elif dept.find("EE") > -1 or dept.find("Electrical") > -1:
        department = "EE"
        dept = "Electrical"
    elif dept.find("CSE") > -1 or dept.find("Computer") > -1:
        department = "CO"
        dept = "CSE"

    year = year - 2000

    for entry in range(start, end + 1):
        first_name = None
        last_name = None
        if entry < 10:
            username = "{dep}{year}30{entry}".format(dep=department, year=str(year), entry=str(entry))
        else:
            username = "{dep}{year}3{entry}".format(dep=department, year=str(year), entry=str(entry))
        student_email = "{user}@gmail.com".format(user=username)
        student_password = username
        print(student_password)
        new_student = MyCustomUser.objects.create_student_user(username=username,
                                                               email=student_email, password=student_password,
                                                               first_name=first_name
                                                               , last_name=last_name)
        batch = Batch.objects.get_or_create(batchYear=year)[0]
        student_info = StudentInfo.objects.create(user=new_student, father_name=None, semester=semester, batch=batch,
                                                  department=dept, roll_no=username, contact=None)
        if new_student:
            print(
                "Created Successfully - Student {student} , Info {info}".format(student=new_student, info=student_info))
        else:
            print("User Not Created for entry", entry)


def populate_students(start, end):
    for entry in range(start, end + 1):
        first_name = None
        last_name = None
        if entry < 10:
            fake_username = "CO1630" + str(entry)
        else:
            fake_username = "CO163" + str(entry)
        fake_email = fakegen.email()
        fake_password = fake_username
        new_student = MyCustomUser.objects.create_student_user(username=fake_username,
                                                               email=fake_email, password=fake_password,
                                                               first_name=first_name
                                                               , last_name=last_name)
        if new_student:
            print(new_student, " Created Successfully", "Entry:", entry)
        else:
            print("User Not Created for entry", entry)


def populate_super_user(N):
    for entry in range(N):
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        first_name = input("First Name: ")
        last_Name = input("Last Name: ")
        if first_name.__len__() == 0:
            first_name = None
        if last_Name.__len__() == 0:
            last_Name = None
        new_user = MyCustomUser.objects.create_superuser(username=username, email=email, password=password,
                                                         first_name=first_name, last_name=last_Name)

        if new_user:
            print("SuperUser successfully created!!")
        else:
            print("SuperUser Not created")


if __name__ == '__main__':
    print("POPULATING SCRIPT!!!!")
    # createMultipleUsers(99,99,2018,"Electrical",1)
    nTeachers = int(input("Enter How many New Fake Teachers You want to create?"))
    nStudents = int(input("Enter How many New Fake Students You want to create?"))
    nUsers = int(input("Enter How many New SuperUser's You want to create?"))
    if nTeachers > 0:
        populate_teachers(nTeachers)
        print("Teachers Database Created!!")
    else:
        print("No new Teachers created !!!!")

    if nUsers > 0:
        populate_super_user(nUsers)
        print("SuperUser's Database Created!!")
    else:
        print("No new Users created !!!!")

    if nStudents > 0:
        starting_roll_no = int(input("Student 1 Roll No. Last 2 digits - "))
        end_roll_no = int(input("Last Student Roll No. Last 2 digits - "))
        populate_students(start=starting_roll_no, end=end_roll_no)
        print("Students Database Created!!")

    else:
        print("No new Students created!!!")

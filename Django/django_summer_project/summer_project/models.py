from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator

USERNAME_REGEX = '^[0-9a-zA-Z.+-]*$'
NAME_REGEX = '^[a-zA-Z.+-]*$'

class MyCustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None,**kwargs):
        if not email:
            raise ValueError("Please Provide Email!!")

        user = self.model(username=username,
                          email=self.normalize_email(email),**kwargs)

        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None,**kwargs):
        user = self.create_user(username, email, password=password,**kwargs)

        user.is_admin = True
        user.is_staff = True
        user.is_student = True

        user.save(using=self._db)

        return user

    def create_student_user(self, username, email, password=None,**kwargs):
        user = self.create_user( username, email, password=password,**kwargs)
        user.is_student = True
        user.save(using = self._db)
        return user

    def create_teacher_user(self, username, email, password=None,**kwargs):
        user = self.create_user( username, email, password=password,**kwargs)
        user.is_staff = True
        user.save(using = self._db)
        return user


class MyCustomUser(AbstractBaseUser):
    username = models.CharField(max_length=300,
                                unique=True,
                                validators=[RegexValidator(regex=USERNAME_REGEX,
                                                           message='Incorrect Username - Should be Alphanumeric.',
                                                           code='Invalid Username.Please Check It!!!')])
    email = models.EmailField(max_length=50, unique=True, verbose_name='email address')

    first_name = models.CharField(max_length=50,default=None,null=True,blank=True,
                                  validators=[RegexValidator(regex=NAME_REGEX,
                                                             message="First Name shouldn't contains Numbers, Special Characters etc.")])

    last_name = models.CharField(max_length=50,default=None,null=True,blank=True,
                                  validators=[RegexValidator(regex=NAME_REGEX,
                                                             message="Last Name shouldn't contains Numbers, Special Characters etc.")])

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = MyCustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def full_name(self):
        return "{} {}".format(self.first_name,self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, alwaysL̥
        return True


    def get_absolute_url(self):
        return reverse('index')


class TeacherInfo(models.Model):
    user = models.OneToOneField(MyCustomUser, on_delete=models.CASCADE)
    designation = models.CharField(max_length=30)
    education_qualification = models.CharField(max_length=200)
    specialization_area = models.CharField(max_length=100)
    department = models.CharField(max_length=30)
    add_role = models.CharField(max_length=40, blank=True)
    web_link = models.URLField(blank=True)
    contact = models.PositiveIntegerField()
    pic = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return self.user.username


class StudentInfo(models.Model):
    user = models.OneToOneField(MyCustomUser, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=30)
    semester = models.CharField(max_length=10)
    batch = models.PositiveIntegerField()
    department = models.CharField(max_length=30)
    roll_no = models.CharField(max_length=10)
    contact = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username

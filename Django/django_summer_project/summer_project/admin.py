from django.contrib import admin
from .models import TeacherInfo,StudentInfo
from django.contrib.auth.admin import Group
from .forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyCustomUser

# Register your models here.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('username','email','is_admin','is_staff','is_student')
    list_filter = ['is_admin','is_staff','is_student']
    filter_horizontal = ()
    fieldsets = (
        (None,{'fields':('username','email','password','first_name','last_name')}),
        ('Permisssions',{'fields':('is_admin','is_staff','is_student')})
    )
    search_fields = ('username','email')
    ordering = ('username','email')


admin.site.register(MyCustomUser,UserAdmin)
admin.site.register(TeacherInfo)
admin.site.register(StudentInfo)
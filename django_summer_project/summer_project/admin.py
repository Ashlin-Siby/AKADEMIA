from django.contrib import admin
from django.contrib.auth.admin import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models
from .forms import UserCreationForm

# Register your models here.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ("username", "email", "is_staff", "is_teacher", "is_student")
    list_filter = ["is_staff", "is_teacher", "is_student"]
    filter_horizontal = ()
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "first_name", "last_name")}),
        ("Permisssions", {"fields": ("is_staff", "is_teacher", "is_student")})
    )
    search_fields = ("username", "email")
    ordering = ("username", "email")


class FilesAdmin(admin.ModelAdmin):
    model = models.Files
    list_display = [field.name for field in models.Files._meta.get_fields()]


class BatchAdmin(admin.ModelAdmin):
    model = models.Batch
    list_display = ["batchYear"]


class SemesterAdmin(admin.ModelAdmin):
    model = models.Semester
    list_display = ["semesterNo", "batchYear"]


class TeacherInfoAdmin(admin.ModelAdmin):
    model = models.TeacherInfo
    list_display = [field.name for field in models.TeacherInfo._meta.get_fields()]


class StudentInfoAdmin(admin.ModelAdmin):
    model = models.StudentInfo
    list_display = [field.name for field in models.StudentInfo._meta.get_fields()]


class SubjectsAdmin(admin.ModelAdmin):
    model = models.Subjects
    list_display = ["subjectCode", "subjectName", "semesterNo", "teacherName"]


admin.site.register(models.MyCustomUser, UserAdmin)
admin.site.register(models.TeacherInfo, TeacherInfoAdmin)
admin.site.register(models.StudentInfo, StudentInfoAdmin)
admin.site.register(models.Batch, BatchAdmin)
admin.site.register(models.Semester, SemesterAdmin)
admin.site.register(models.Subjects, SubjectsAdmin)
admin.site.register(models.Files, FilesAdmin)

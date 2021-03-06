from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.validators import ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DeleteView, FormView
from populate_summer_project import createMultipleUsers
from summer_project.forms import FileUploaderForm
from summer_project.models import MyCustomUser, StudentInfo, TeacherInfo, Batch, Semester, Subjects, Files

from .forms import MultiUsersForms


class StudyCornerView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    redirect_field_name = "study_corner/studyCorner.html"
    template_name = "study_corner/studyCorner.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            context["current_sem"] = studentUser.semester
            context["studentUser"] = studentUser
        elif user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            context["teacherUser"] = teacherUser
        return context


class BatchListView(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    model = Batch
    template_name = "study_corner/batchList.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BatchListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            context["current_sem"] = studentUser.semester
            context["studentUser"] = studentUser
        context["type"] = self.kwargs["type_pk"]
        return context

    def get_queryset(self):
        return Batch.objects.all().order_by("-batchYear")


class SemesterListView(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    model = Semester
    template_name = "study_corner/semesterList.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        year_pk = self.kwargs["year_pk"]
        type = self.kwargs["type_pk"]
        semester_list = Semester.objects.filter(batchYear=year_pk)
        user = self.request.user
        context = {"semester_list": semester_list, "year": year_pk, "type": type}
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            context["current_sem"] = studentUser.semester
            context["studentUser"] = studentUser
        elif user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            context["teacherUser"] = teacherUser

        return context


class SubjectsListView(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    model = Subjects
    template_name = "study_corner/subjectList.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        year_pk = self.kwargs["year_pk"]
        sem_pk = self.kwargs["sem_pk"]
        type = self.kwargs["type_pk"]
        semesterObject = Semester.objects.get(semesterNo=sem_pk, batchYear=year_pk)
        subject_list = Subjects.objects.filter(semesterNo=semesterObject)
        data = {"subject_list": subject_list, "year": year_pk, "semester": sem_pk, "type": type}
        user = self.request.user
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            data["current_sem"] = studentUser.semester
            data["studentUser"] = studentUser
        elif user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            data["teacherUser"] = teacherUser
        return data


class SubjectsList(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    model = Subjects
    template_name = "study_corner/subjectList.html"

    def get(self, request, *args, **kwargs):
        type = self.kwargs["sm_pk"]
        user = self.request.user
        subject_list = Subjects.objects.all().values_list("subjectName", "subjectCode").distinct()
        data = {"subjects_list": subject_list, "type": type}
        if user.is_student and user.is_teacher == False:
            studentUser = StudentInfo.objects.get(user=user)
            data["current_sem"] = studentUser.semester
            data["studentUser"] = studentUser
        return render(request, "study_corner/subjectList.html", context=data)


class TeachersList(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    model = Subjects
    template_name = "study_corner/teacherList.html"

    def get(self, request, *args, **kwargs):
        type = self.kwargs["sm_pk"]
        code = self.kwargs["code_pk"]
        user = self.request.user
        teacher_list = Subjects.objects.filter(subjectCode=code).values_list("teacherName").distinct()
        data = {"teacher_list": teacher_list, "type": type, "code": code}
        if user.is_student and user.is_teacher == False:
            studentUser = StudentInfo.objects.get(user=user)
            data["current_sem"] = studentUser.semester
            data["studentUser"] = studentUser
        return render(request, "study_corner/teacherList.html", context=data)


class FilesList(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    model = Files
    template_name = "study_corner/fileList.html"

    def get(self, request, *args, **kwargs):
        type = self.kwargs["sm_pk"]
        code = self.kwargs["code_pk"]
        teacher_name = self.kwargs["teacher_name_pk"]
        user = self.request.user
        subjectObjects = Subjects.objects.filter(teacherName=teacher_name, subjectCode=code)
        fileObjects = Files.objects.filter(teacherName__in=subjectObjects, fileType=type)
        print(fileObjects)
        data = {"files_list": fileObjects, "type": type, "code_pk": code, "teacherName": teacher_name}
        if user.is_student and user.is_teacher == False:
            studentUser = StudentInfo.objects.get(user=user)
            data["current_sem"] = studentUser.semester
            data["studentUser"] = studentUser
        return render(request, "study_corner/fileList.html", context=data)


class FilesListView(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    model = Files
    template_name = "study_corner/fileList.html"

    def get(self, request, *args, **kwargs):
        year_pk = self.kwargs["year_pk"]
        sem_pk = self.kwargs["sem_pk"]
        code_pk = self.kwargs["code_pk"]
        type = self.kwargs["type_pk"]
        semesterObject = Semester.objects.get(semesterNo=sem_pk, batchYear=year_pk)
        subjectObject = Subjects.objects.get(semesterNo=semesterObject, subjectCode=code_pk)
        files_list = Files.objects.filter(subjCode=subjectObject, fileType=type)
        user = self.request.user
        MEDIA_DIR = settings.MEDIA_ROOT + "/"
        data = {"file_list": files_list, "year": year_pk, "semester": sem_pk, "subj_code": code_pk, "type": type,
                "media_dir": MEDIA_DIR}
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            data["current_sem"] = studentUser.semester
            data["studentUser"] = studentUser
        elif user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            data["teacherUser"] = teacherUser
        return render(request, "study_corner/fileList.html", context=data)


class TeachersSubjectsList(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    template_name = "study_corner/subjectList.html"
    model = Subjects

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = self.kwargs["t_type_pk"]
        user = self.request.user
        if user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            context["teacherUser"] = teacherUser
        return context

    def get_queryset(self):
        return Subjects.objects.all()


class TeachersFilesList(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    template_name = "study_corner/fileList.html"
    model = Files

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = self.kwargs["t_type_pk"]
        context["code_pk"] = self.kwargs["code_pk"]
        user = self.request.user
        if user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            context["teacherUser"] = teacherUser
            context["teacherName"] = user.first_name + " " + user.last_name
            teacherVerify = Subjects.objects.filter(subjectCode=self.kwargs["code_pk"],
                                                    teacherName__contains=self.request.user.first_name)
            if teacherVerify or user.is_staff:
                context["teacherVerify"] = True
            else:
                context["teacherVerify"] = False
            print(context["teacherVerify"])
        return context

    def get_queryset(self):
        SubjectsObjects = Subjects.objects.filter(subjectCode=self.kwargs["code_pk"])
        FileObjects = Files.objects.filter(fileType=self.kwargs["t_type_pk"], subjCode__in=SubjectsObjects)
        return FileObjects


class TeacherFileUploader(LoginRequiredMixin, CreateView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    template_name = "study_corner/files_form.html"
    form_class = FileUploaderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["type"] = self.kwargs["t_type_pk"]
        context["code_pk"] = self.kwargs["t_code_pk"]
        if user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            context["teacherUser"] = teacherUser
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        Subject_Code = self.kwargs["t_code_pk"]
        user = self.request.user
        if user.is_teacher:
            Teacher_Name = user.first_name + " " + user.last_name
        else:
            Teacher_Name = self.kwargs["teacherName_pk"]
        object = Subjects.objects.filter(subjectCode=Subject_Code, teacherName__contains=Teacher_Name)
        file_uploaded = Files(
            filePath=self.get_form_kwargs().get("files")["filePath"],
            fileName=self.get_form_kwargs().get("files")["filePath"].name,
            fileType=form.cleaned_data.get("fileType"),
            fileURL=form.cleaned_data.get("fileURL"),
            teacherName=object[0],
            subjCode=object[0],
            uploadedBy=user,
        )
        file_uploaded.save()
        messages.success(self.request, "File uploaded!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("summer_project:dashboard")


class StudentFileUploader(LoginRequiredMixin, CreateView):
    login_url = "login"
    redirect_field_name = "summer_project/dashboard.html"
    template_name = "study_corner/files_form.html"
    form_class = FileUploaderForm
    type = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_pk"] = self.kwargs["year_pk"]
        context["sem_pk"] = self.kwargs["sem_pk"]
        context["code_pk"] = self.kwargs["code_pk"]
        context["type"] = self.kwargs["type_pk"]
        user = self.request.user
        if user.is_student and user.is_teacher == False:
            studentUser = StudentInfo.objects.get(user=user)
            context["current_sem"] = studentUser.semester
            context["studentUser"] = studentUser
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user, "type_pk": type})
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        batch_object = Batch.objects.filter(batchYear=self.kwargs["year_pk"])
        semester_object = Semester.objects.filter(semesterNo=self.kwargs["sem_pk"], batchYear=batch_object[0])
        object = Subjects.objects.filter(subjectCode=self.kwargs["code_pk"], semesterNo=semester_object[0])
        file_uploaded = Files(
            filePath=self.get_form_kwargs().get("files")["filePath"],
            fileName=self.get_form_kwargs().get("files")["filePath"].name,
            fileType=form.cleaned_data.get("fileType"),
            fileURL=form.cleaned_data.get("fileURL"),
            teacherName=object[0],
            subjCode=object[0],
            uploadedBy=user
        )
        file_uploaded.save()
        messages.success(self.request, "File uploaded!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("summer_project:dashboard")


class UploadedFileListView(LoginRequiredMixin, ListView):
    login_url = "login"
    redirect_field_name = "summer_project:dashboard"
    template_name = "study_corner/uploadedFileList.html"
    model = Files

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # print(user.is_student,user.is_teacher)
        if user.is_student:
            context["year_pk"] = self.kwargs["year_pk"]
            context["sem_pk"] = self.kwargs["sem_pk"]
            context["code_pk"] = self.kwargs["code_pk"]
            context["type"] = self.kwargs["type_pk"]
            studentUser = StudentInfo.objects.get(user=user)
            context["current_sem"] = studentUser.semester
            context["studentUser"] = studentUser
        elif user.is_teacher:
            context["code_pk"] = self.kwargs["t_code_pk"]
            context["type"] = self.kwargs["t_type_pk"]
            teacherUser = TeacherInfo.objects.get(user=user)
            context["teacherUser"] = teacherUser
        return context

    def get_queryset(self):
        user = self.request.user
        adminUsers = MyCustomUser.objects.filter(is_staff=True)
        type = None
        try:
            type = self.kwargs["type_pk"]
        except:
            type = self.kwargs["t_type_pk"]
        else:
            print(type)
        finally:
            print(type)
            if type == "notes" or type == "question_paper":
                batch_object = Batch.objects.filter(batchYear=self.kwargs["year_pk"])
                semester_object = Semester.objects.filter(semesterNo=self.kwargs["sem_pk"],
                                                          batchYear=batch_object[0])
                object = Subjects.objects.filter(subjectCode=self.kwargs["code_pk"], semesterNo=semester_object[0])
                if user.is_staff == False:
                    file_objects = Files.objects.filter((Q(uploadedBy=user) | Q(uploadedBy__in=adminUsers)), fileType=type,
                                                        teacherName=object[0], subjCode=object[0])
                else:
                    file_objects = Files.objects.filter(fileType=type,teacherName=object[0], subjCode=object[0])
                return file_objects
            elif type == "study_material":
                Subject_Code = self.kwargs["t_code_pk"]
                if user.is_teacher:
                    Teacher_Name = user.first_name + " " + user.last_name
                else:
                    Teacher_Name = self.kwargs["teacherName_pk"]
                object = Subjects.objects.filter(subjectCode=Subject_Code, teacherName__contains=Teacher_Name)
                if object:
                    if user.is_staff:
                        file_objects = Files.objects.filter(fileType=type, teacherName=object[0], subjCode=object[0])
                    else:
                        file_objects = Files.objects.filter((Q(uploadedBy=user) | Q(uploadedBy__in=adminUsers)),
                                                            fileType=type, teacherName=object[0], subjCode=object[0])
                else:
                    file_objects = None
                return file_objects


class DeleteFileObjects(LoginRequiredMixin, DeleteView):
    login_url = "login"
    redirect_field_name = "summer_project:dashboard"
    model = Files
    success_url = reverse_lazy("summer_project:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        user = self.request.user
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            context["current_sem"] = studentUser.semester
            context["studentUser"] = studentUser
        elif user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            context["teacherUser"] = teacherUser
        return context


class CreateMultiUsers(LoginRequiredMixin, FormView):
    login_url = "login"
    redirect_field_name = "summer_project:dashboard"
    form_class = MultiUsersForms
    success_url = reverse_lazy("summer_project:dashboard")
    template_name = "study_corner/MultipleUsersForm.html"

    def form_valid(self, form):
        start = form.cleaned_data.get("start")
        end = form.cleaned_data.get("end")
        department = form.cleaned_data.get("department")
        year = form.cleaned_data.get("year")
        semester = form.cleaned_data.get("semester")
        try:
            createMultipleUsers(start=start, end=end, year=year, dept=department, semester=semester)
            print("Users Created")
            return HttpResponseRedirect(self.get_success_url())
        except:
            print("Error in creating users!!")
            raise ValidationError("Incorrect Details!!")

    def get_success_url(self):
        return reverse("summer_project:dashboard")

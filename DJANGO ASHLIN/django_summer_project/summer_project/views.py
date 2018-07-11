from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, View, ListView, DeleteView, FormView , DetailView
from django.core.validators import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .forms import UserCreationForm, FileUploaderForm
from .models import MyCustomUser, StudentInfo, TeacherInfo, Batch, Semester, Subjects, Files
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


class index(View):
    template_name = 'summer_project/login.html'

    def get(self, request):
        return render(request, 'summer_project/login.html',
                      {'MyCustomUser': MyCustomUser, 'hidden': 'hidden', 'visible': 'password'})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            print("Authentication Successful")
            login(request, user)
            if user.is_admin and user.is_student and user.is_staff:
                # return render(request,'summer_project/dashboard_student.html',context={})
                return HttpResponse("Admin Login Successful")
            elif user.is_student:
                studentUser = StudentInfo.objects.get(user=user)
                profile_data = {'current_sem': studentUser.semester,'studentUser_pk':studentUser.pk}
                return render(request, 'summer_project/dashboard_student.html', context=profile_data)
            elif user.is_staff:
                teacherUser = TeacherInfo.objects.get(user=user)
                teacher_profile_data = {'teacherUser_pk':teacherUser.pk}
                return render(request, 'summer_project/dashboard_student.html', context=teacher_profile_data)

        else:
            if username in MyCustomUser.objects.all():
                print(username, " Entered Wrong Passowrd. User Authentication failed!!")
            else:
                print("User Doesn't Exist!!! Contact Administrator.")
                return render(request, 'summer_project/login.html',
                              {'MyCustomUser': MyCustomUser, 'hidden': 'hidden', 'visible': 'password'})


class StudyCornerView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    template_name = 'summer_project/studyCorner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_student:
            studentUser = StudentInfo.objects.get(user=user)
            context['current_sem'] = studentUser.semester
        return context


class BatchListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    model = Batch
    template_name = 'summer_project/batchList.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BatchListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_student:
            studentUser = StudentInfo.objects.get(user=user)
            context['current_sem'] = studentUser.semester
        context['type'] = self.kwargs['type_pk']
        return context

    def get_queryset(self):
        return Batch.objects.all().order_by('-batchYear')


class SemesterListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    model = Semester
    template_name = 'summer_project/semesterList.html'

    def get(self, request, *args, **kwargs):
        year_pk = self.kwargs['year_pk']
        type = self.kwargs['type_pk']
        semester_list = Semester.objects.filter(batchYear=year_pk)
        print(semester_list)
        user = self.request.user
        if user.is_student:
            studentUser = StudentInfo.objects.get(user=user)
            return render(request, 'summer_project/semesterList.html',
                          context={'semester_list': semester_list, 'year': year_pk, 'type': type,
                                   'current_sem': studentUser.semester})
        else:
            return render(request, 'summer_project/semesterList.html',
                          context={'semester_list': semester_list, 'year': year_pk, 'type': type})


class SubjectsListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    model = Subjects
    template_name = 'summer_project/subjectList.html'

    def get(self, request, *args, **kwargs):
        year_pk = self.kwargs['year_pk']
        sem_pk = self.kwargs['sem_pk']
        type = self.kwargs['type_pk']
        semesterObject = Semester.objects.get(semesterNo=sem_pk, batchYear=year_pk)
        subject_list = Subjects.objects.filter(semesterNo=semesterObject)
        print(subject_list)
        user = self.request.user
        if user.is_student:
            studentUser = StudentInfo.objects.get(user=user)
            return render(request, 'summer_project/subjectList.html',
                          context={'subject_list': subject_list, 'year': year_pk, 'semester': sem_pk, 'type': type,
                                   'current_sem': studentUser.semester})
        else:
            return render(request, 'summer_project/subjectList.html',
                          context={'subject_list': subject_list, 'year': year_pk, 'semester': sem_pk, 'type': type})


class SubjectsList(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    model = Subjects
    template_name = 'summer_project/subjectList.html'

    def get(self, request, *args, **kwargs):
        type = self.kwargs['sm_pk']
        user = self.request.user
        subject_list = Subjects.objects.all().values_list('subjectName', 'subjectCode').distinct()
        print(subject_list)
        studentUser = StudentInfo.objects.get(user=user)
        return render(request, 'summer_project/subjectList.html',
                      context={'subjects_list': subject_list, 'type': type, 'current_sem': studentUser.semester})


class TeachersList(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    model = Subjects
    template_name = 'summer_project/teacherList.html'

    def get(self, request, *args, **kwargs):
        type = self.kwargs['sm_pk']
        code = self.kwargs['code_pk']
        user = self.request.user
        teacher_list = Subjects.objects.filter(subjectCode=code).values_list('teacherName').distinct()
        print(teacher_list)
        studentUser = StudentInfo.objects.get(user=user)
        return render(request, 'summer_project/teacherList.html',
                      context={'teacher_list': teacher_list, 'type': type, 'code': code,
                               'current_sem': studentUser.semester})


class FilesList(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    model = Files
    template_name = 'summer_project/fileList.html'

    def get(self, request, *args, **kwargs):
        type = self.kwargs['sm_pk']
        code = self.kwargs['code_pk']
        teacher_name = self.kwargs['teacher_name_pk']
        user = self.request.user
        subjectObjects = Subjects.objects.filter(teacherName=teacher_name, subjectCode=code)
        print(subjectObjects)
        fileObjects = Files.objects.filter(teacherName__in=subjectObjects, fileType=type)
        studentUser = StudentInfo.objects.get(user=user)
        return render(request, 'summer_project/fileList.html',
                      context={'files_list': fileObjects, 'type': type, 'code_pk': code,
                               'current_sem': studentUser.semester})


class FilesListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    model = Files
    template_name = 'summer_project/fileList.html'

    def get(self, request, *args, **kwargs):
        year_pk = self.kwargs['year_pk']
        sem_pk = self.kwargs['sem_pk']
        code_pk = self.kwargs['code_pk']
        type = self.kwargs['type_pk']
        semesterObject = Semester.objects.get(semesterNo=sem_pk, batchYear=year_pk)
        subjectObject = Subjects.objects.get(semesterNo=semesterObject, subjectCode=code_pk)
        files_list = Files.objects.filter(subjCode=subjectObject, fileType=type)
        print(files_list)
        user = self.request.user
        MEDIA_DIR = settings.MEDIA_ROOT + '/'
        if user.is_student:
            studentUser = StudentInfo.objects.get(user=user)
            return render(request, 'summer_project/fileList.html',
                          context={'file_list': files_list, 'year': year_pk, 'semester': sem_pk, 'subj_code': code_pk,
                                   'current_sem': studentUser.semester, 'type': type, 'media_dir':MEDIA_DIR})
        else:
            return render(request, 'summer_project/fileList.html',
                          context={'file_list': files_list, 'year': year_pk, 'semester': sem_pk, 'subj_code': code_pk,
                                   'type': type,'media_dir':MEDIA_DIR})


class TeachersSubjectsList(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    template_name = 'summer_project/subjectList.html'
    model = Subjects

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.kwargs['t_type_pk']
        return context

    def get_queryset(self):
        return Subjects.objects.all()


class TeachersFilesList(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    template_name = 'summer_project/fileList.html'
    model = Files

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.kwargs['t_type_pk']
        print(context['type'])
        context['code_pk'] = self.kwargs['code_pk']
        print(context['code_pk'])
        return context

    def get_queryset(self):
        SubjectsObjects = Subjects.objects.filter(subjectCode=self.kwargs['code_pk'])
        FileObjects = Files.objects.filter(fileType=self.kwargs['t_type_pk'], subjCode__in=SubjectsObjects)
        print(FileObjects)
        return FileObjects


class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    template_name = 'summer_project/dashboard_student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_student:
            studentUser = StudentInfo.objects.get(user=user)
            context['current_sem'] = studentUser.semester
            context['studentUser_pk'] = studentUser.pk
            print(context['current_sem'])
        elif user.is_staff:
            teacherUser = TeacherInfo.objects.get(user=user)
            context['teacherUser_pk'] = teacherUser.pk
        return context


class RegisterView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'summer_project/login.html'
    form_class = UserCreationForm
    template_name = 'summer_project/registration.html'


class TeacherFileUploader(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    template_name = 'summer_project/files_form.html'
    form_class = FileUploaderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.kwargs['t_type_pk']
        context['code_pk'] = self.kwargs['t_code_pk']
        return context

    def form_valid(self, form):
        Subject_Code = self.kwargs['t_code_pk']
        user = self.request.user
        Teacher_Name = user.first_name + " " + user.last_name
        print(Subject_Code, Teacher_Name)
        object = Subjects.objects.filter(subjectCode=Subject_Code, teacherName__contains=Teacher_Name)
        print(object[0])
        file_uploaded = Files(
            filePath=self.get_form_kwargs().get('files')['filePath'],
            fileName=self.get_form_kwargs().get('files')['filePath'].name,
            fileType=form.cleaned_data.get('fileType'),
            fileURL=form.cleaned_data.get('fileURL'),
            teacherName=object[0],
            subjCode=object[0],
            uploadedBy=user,
        )
        file_uploaded.save()
        messages.success(self.request, 'File uploaded!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('summer_project:dashboard')


class StudentFileUploader(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard_student.html'
    template_name = 'summer_project/files_form.html'
    form_class = FileUploaderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year_pk'] = self.kwargs['year_pk']
        context['sem_pk'] = self.kwargs['sem_pk']
        context['code_pk'] = self.kwargs['code_pk']
        context['type'] = self.kwargs['type_pk']
        return context

    def form_valid(self, form):
        user = self.request.user
        print(self.kwargs['year_pk'], self.kwargs['sem_pk'], self.kwargs['code_pk'], self.kwargs['type_pk'])
        batch_object = Batch.objects.filter(batchYear=self.kwargs['year_pk'])
        print(batch_object)
        semester_object = Semester.objects.filter(semesterNo=self.kwargs['sem_pk'], batchYear=batch_object[0])
        print(semester_object)
        object = Subjects.objects.filter(subjectCode=self.kwargs['code_pk'], semesterNo=semester_object[0])
        print(object[0])
        file_uploaded = Files(
            filePath=self.get_form_kwargs().get('files')['filePath'],
            fileName=self.get_form_kwargs().get('files')['filePath'].name,
            fileType=form.cleaned_data.get('fileType'),
            fileURL=form.cleaned_data.get('fileURL'),
            teacherName=object[0],
            subjCode=object[0],
            uploadedBy=user
        )
        print(self.get_form_kwargs().get('files')['filePath'].name)
        file_uploaded.save()
        messages.success(self.request, 'File uploaded!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('summer_project:dashboard')


class UploadedFileListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'summer_project:dashboard'
    template_name = 'summer_project/uploadedFileList.html'
    model = Files

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.user.is_student):
            context['year_pk'] = self.kwargs['year_pk']
            context['sem_pk'] = self.kwargs['sem_pk']
            context['code_pk'] = self.kwargs['code_pk']
            context['type'] = self.kwargs['type_pk']
        elif self.request.user.is_staff:
            context['code_pk'] = self.kwargs['t_code_pk']
            context['type'] = self.kwargs['t_type_pk']
        return context

    def get_queryset(self):
        if (self.request.user.is_student):
            print(self.kwargs['year_pk'], self.kwargs['sem_pk'], self.kwargs['code_pk'], self.kwargs['type_pk'])
            batch_object = Batch.objects.filter(batchYear=self.kwargs['year_pk'])
            print(batch_object)
            semester_object = Semester.objects.filter(semesterNo=self.kwargs['sem_pk'], batchYear=batch_object[0])
            print(semester_object)
            object = Subjects.objects.filter(subjectCode=self.kwargs['code_pk'], semesterNo=semester_object[0])
            print(object, object[0])
            file_objects = Files.objects.filter(uploadedBy=self.request.user, fileType=self.kwargs['type_pk'],
                                                teacherName=object[0], subjCode=object[0])
            print(file_objects)
            return file_objects

        elif self.request.user.is_staff:
            print(self.kwargs['t_code_pk'], self.kwargs['t_type_pk'])
            Subject_Code = self.kwargs['t_code_pk']
            user = self.request.user
            Teacher_Name = user.first_name + " " + user.last_name
            print(Subject_Code, Teacher_Name)
            object = Subjects.objects.filter(subjectCode=Subject_Code, teacherName__contains=Teacher_Name)
            print(object[0])
            file_objects = Files.objects.filter(uploadedBy=user, fileType=self.kwargs['t_type_pk'],
                                                teacherName=object[0], subjCode=object[0])
            print(file_objects)
            return file_objects


class DeleteFileObjects(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'summer_project:dashboard'
    model = Files
    success_url = reverse_lazy('summer_project:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class StudProfileView(DetailView):
    context_object_name = 'student_details'
    model = StudentInfo
    template_name = 'summer_project/stud_profile_detail.html'


class TeachProfileView(DetailView):
        context_object_name = 'teacher_details'
        model = TeacherInfo
        template_name = 'summer_project/teach_profile_detail.html'

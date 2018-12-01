from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, View, FormView, UpdateView, DetailView
from django.core.validators import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .forms import UserCreationForm, ChangePasswordForm
from .models import MyCustomUser, StudentInfo, TeacherInfo
from django.conf import settings


# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


class index(View):
    template_name = 'summer_project/login.html'

    def get(self, request):
        return render(request, 'summer_project/login.html', {'MyCustomUser': MyCustomUser, 'msg': None})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('summer_project:dashboard'))

        else:
            if MyCustomUser.objects.get(username=username):
                raise ValidationError("Entered Wrong Passowrd. User Authentication failed!!")
            else:
                raise ValidationError("User Doesn't Exist!!! Contact Administrator.")


class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard.html'
    template_name = 'summer_project/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            context['current_sem'] = studentUser.semester
            context['studentUser'] = studentUser
        elif user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            context['teacherUser'] = teacherUser
        return context


class RegisterView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'summer_project/login.html'
    form_class = UserCreationForm
    template_name = 'summer_project/registration.html'


class StudProfileView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard.html'
    context_object_name = 'student_details'
    model = StudentInfo
    template_name = 'summer_project/stud_profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            context['media_dir'] = settings.MEDIA_ROOT
            context['current_sem'] = studentUser.semester
            context['studentUser'] = studentUser
        return context


class TeachProfileView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard.html'
    context_object_name = 'teacher_details'
    model = TeacherInfo
    template_name = 'summer_project/teach_profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_teacher:
            teacherUser = TeacherInfo.objects.get(user=user)
            print(teacherUser.pic)
            context['teacherUser'] = teacherUser
        return context


class StudentProfileEdit(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard.html'
    model = StudentInfo
    fields = ("father_name", "department", "contact", "pic",)
    template_name = 'summer_project/student_profile_edit.html'
    success_url = reverse_lazy('summer_project:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            context['media_dir'] = settings.MEDIA_ROOT
            context['current_sem'] = studentUser.semester
            context['studentUser'] = studentUser
        return context


class TeacherProfileEdit(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard.html'
    model = TeacherInfo
    fields = ("designation", "education_qualification", "specialization_area",
              "department",
              "add_role", "web_link",
              "web_link", "pic")
    template_name = 'summer_project/teacher_profile_edit.html'
    success_url = reverse_lazy('summer_project:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['media_dir'] = settings.MEDIA_ROOT
        if user.is_teacher:
            teacherUser = TeacherInfo.objects.get(user=user)
            context['teacherUser'] = teacherUser
        return context


class ChangePasswordView(LoginRequiredMixin, FormView):
    login_url = 'login'
    redirect_field_name = 'summer_project/dashboard.html'
    model = MyCustomUser
    form_class = ChangePasswordForm
    template_name = 'summer_project/change_password.html'

    def form_valid(self, form):
        password = form.cleaned_data.get("newPassword")
        user = self.request.user
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('summer_project:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_student and user.is_staff == False:
            studentUser = StudentInfo.objects.get(user=user)
            context['studentUser'] = studentUser
        elif user.is_teacher and user.is_staff == False:
            teacherUser = TeacherInfo.objects.get(user=user)
            context['teacherUser'] = teacherUser
        return context

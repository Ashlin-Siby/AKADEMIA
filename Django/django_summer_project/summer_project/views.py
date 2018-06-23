from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView
from django.core.validators import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import UserCreationForm
from .models import MyCustomUser

# Create your views here.
def index(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        try:
            password = request.POST['password']
        except :
            password = "Hello"
        user = authenticate(username=username,password=password)
        if user:
            print("Authentication Successful")
        else:
            print(username,password," user authentication failed!!")
    else:
        return render(request, 'summer_project/login.html', {})

    return render(request, 'summer_project/login.html', {})


class dashboard(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'summer_project/dashboard_student.html'
    template_name = 'summer_project/dashboard_student.html'


class registerView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'summer_project/login.html'
    form_class = UserCreationForm
    template_name = 'summer_project/registration.html'

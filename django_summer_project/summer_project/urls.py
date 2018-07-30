from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'summer_project'

urlpatterns = [
                  url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
                  url(r'^register/$', views.RegisterView.as_view(), name='register'),
                  url(r'^student/(?P<pk>\d+)/$', views.StudProfileView.as_view(), name='studprofile'),
                  url(r'^student/edit/(?P<pk>\d+)/$', views.StudentProfileEdit.as_view(), name='studprofileedit'),
                  url(r'^teacher/edit/(?P<pk>\d+)/$', views.TeacherProfileEdit.as_view(), name='teachprofileedit'),
                  url(r'^teacher/(?P<pk>\d+)/$', views.TeachProfileView.as_view(), name='teachprofile'),
                  # url(r'^password/$', views.change_password, name='adminDjangoDashboard'),
                  url(r'^changePassword/(?P<pk>\d+)/$', views.ChangePasswordView.as_view(), name='changepassword')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

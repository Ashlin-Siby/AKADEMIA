from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from summer_project import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'summer_project'

urlpatterns = [
                  url(r'^$', views.index.as_view(), name='login'),
                  url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
                  url(r'^register/$', views.RegisterView.as_view(), name='register'),
                  url(r'^studycorner/$', views.StudyCornerView.as_view(), name='studyCorner'),
                  url(r'^studycorner/(?P<type_pk>[-\w]+)/$', views.BatchListView.as_view(), name='batchlist'),
                  url(r'^studycorner/(?P<sm_pk>[-\w]+)/subjectslist/$', views.SubjectsList.as_view(),
                      name='sm_subjects'),
                  url(r'^studycorner/(?P<sm_pk>[-\w]+)/subjectslist/(?P<code_pk>[-\w]+)/teacherslist/$',
                      views.TeachersList.as_view(),
                      name='teacherslist'),
                  url(r'^studycorner/(?P<sm_pk>[-\w]+)/subjectslist/(?P<code_pk>[-\w]+)/teacherslist/(?P<teacher_name_pk>[-\w\s.]+)/$',
                      views.FilesList.as_view(), name='fileslist'),
                  url(r'^studycorner/(?P<type_pk>[-\w]+)/(?P<year_pk>\d+)/$', views.SemesterListView.as_view(),
                      name='semesterlist'),
                  url(r'^studycorner/(?P<type_pk>[-\w]+)/(?P<year_pk>\d+)/(?P<sem_pk>\d+)/$',
                      views.SubjectsListView.as_view(),
                      name='subjectslist'),
                  url(r'^studycorner/(?P<type_pk>[-\w]+)/(?P<year_pk>\d+)/(?P<sem_pk>\d+)/(?P<code_pk>[-\w]+)/$',
                      views.FilesListView.as_view(), name='fileslist'),
                  url(r'^studycorner/(?P<type_pk>[-\w]+)/(?P<year_pk>\d+)/(?P<sem_pk>\d+)/(?P<code_pk>[-\w]+)/upload/$',
                      views.StudentFileUploader.as_view(), name='filesuploader'),
                  url(r'^studycorner/(?P<type_pk>[-\w]+)/(?P<year_pk>\d+)/(?P<sem_pk>\d+)/(?P<code_pk>[-\w]+)/deletelist/$',
                      views.UploadedFileListView.as_view(), name='filesdeleter'),
                  url(r'^(?P<pk>\d+)/delete/$', views.DeleteFileObjects.as_view(), name='file_delete'),
                  url(r'^studycorner/(?P<t_type_pk>[-\w]+)/(?P<t_code_pk>[-\w]+)/deletelist/$',
                      views.UploadedFileListView.as_view(), name='deletefile'),
                  url(r'^StudyCorner/(?P<t_type_pk>[-\w]+)/$', views.TeachersSubjectsList.as_view(),
                      name='t_subjectslist'),
                  url(r'^studycorner/(?P<t_type_pk>[-\w]+)/(?P<code_pk>[-\w]+)/$', views.TeachersFilesList.as_view(),
                      name='t_fileslist'),
                  url(r'^add_file/(?P<t_type_pk>[-\w]+)/(?P<t_code_pk>[-\w]+)/$', views.TeacherFileUploader.as_view(),
                      name='uploadfile'),
                  url(r'^student/(?P<pk>\d+)/$', views.StudProfileView.as_view(), name='studprofile'),
                  url(r'^teacher/(?P<pk>\d+)/$', views.TeachProfileView.as_view(), name='teachprofile'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

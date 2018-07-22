from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'study_corner'

urlpatterns = [
                  url(r'^$', views.StudyCornerView.as_view(), name='studyCorner'),
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
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""django_summer_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from summer_project import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index.as_view(), name='login'),
    url(r'^logout/',views.logout_view,name='logout'),
    path('admin/', admin.site.urls),
    url(r'^project_name/', include('summer_project.urls')),
    url(r'^study_corner/', include('study_corner.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL configuration for course_registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from course_registration import views

urlpatterns = [
    path('', views.root_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashbord/', views.admin_dashbord, name='admin_dashbord'),
    path('materials/', views.materials_page, name='materials_page'),
    path('students/', views.students_page, name='students_page'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('sections/', views.sections_page, name='sections_page'),
    path('reports/', views.reports_page, name='reports_page'),
    path('students/add/', views.add_student, name='add_student'),
    path('sections/add/', views.add_section, name='add_section'),
    path('materials/add/', views.add_material_page, name='add_material_page'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

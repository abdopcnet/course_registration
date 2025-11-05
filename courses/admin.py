from django.contrib import admin
from .models import Student, Section

# إدارة الأقسام
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

# إدارة الطلاب
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id_student', 'name', 'section', 'email', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'id_student')
    list_filter = ('is_active', 'section')
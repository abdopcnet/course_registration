from django.db import models

# جدول الأقسام
class Section(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sections'

    def __str__(self):
        return self.name


# جدول الطلاب
class Student(models.Model):
    id_student = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'students'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.id_student})"


# جدول المواد
class Material(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    hours = models.IntegerField(default=3)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'materials'
        verbose_name = "مادة"
        verbose_name_plural = "المواد"

    def __str__(self):
        return f"{self.name} ({self.code})"


# تنزيل المواد (Enrollment)
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.CharField(max_length=20, null=True, blank=True)  # مثال: "السمستر الأول"
    year = models.CharField(max_length=10, null=True, blank=True)      # مثال: "2025"
    date_registered = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'enrollments'
        verbose_name = "تنزيل مادة"
        verbose_name_plural = "تنزيل المواد"
        unique_together = ('student', 'material', 'semester', 'year')

    def __str__(self):
        return f"{self.student.name} - {self.material.name} ({self.semester} {self.year})"
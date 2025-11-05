from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from courses.models import Student, Section, Material, Enrollment
from django.contrib import messages
from django.db import IntegrityError

# --- صفحة رئيسية
def root_redirect(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashbord')
    return redirect('login')


# --- تسجيل الدخول
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashbord')
        return render(request, 'login.html', {'error': 'بيانات الدخول غير صحيحة أو ليس لديك صلاحية.'})
    return render(request, 'login.html')


# --- تسجيل الخروج
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# --- لوحة تحكم الادمن
@login_required
def admin_dashbord(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'admin_dashbord.html')


# --- صفحة المواد
@login_required
def materials_page(request):
    if not request.user.is_staff:
        return redirect('login')

    materials = Material.objects.all()

    code = request.GET.get('code', '').strip()
    name = request.GET.get('name', '').strip()
    hours = request.GET.get('hours', '').strip()

    if code:
        materials = materials.filter(code__icontains=code)
    if name:
        materials = materials.filter(name__icontains=name)
    if hours:
        materials = materials.filter(hours=hours)

    return render(request, 'materials.html', {'materials': materials})


# --- صفحة الطلاب
@login_required
def students_page(request):
    if not request.user.is_staff:
        return redirect('login')

    students = Student.objects.all()

    # قراءة الفلاتر
    id_student = request.GET.get('id_student', '').strip()
    name = request.GET.get('name', '').strip()
    section = request.GET.get('section', '').strip()

    # تطبيق الفلاتر بطريقة ديناميكية فقط إذا القيم موجودة
    if id_student:
        try:
            students = students.filter(id_student=int(id_student))
        except ValueError:
            students = students.none()  # إدخال غير صالح
    if name:
        students = students.filter(name__icontains=name)
    if section:
        try:
            students = students.filter(section_id=int(section))
        except ValueError:
            pass  # إذا القيمة غير صالحة نتجاهلها

    sections = Section.objects.all()  # لملء dropdown
    return render(request, 'students.html', {'students': students, 'sections': sections})


# --- صفحة الأقسام
def sections_page(request):
    if not request.user.is_staff:
        return redirect('login')

    sections = Section.objects.all()

    # قراءة الفلاتر
    id_section = request.GET.get('id_section', '').strip()
    name = request.GET.get('name', '').strip()
    description = request.GET.get('description', '').strip()

    # تطبيق الفلاتر
    if id_section:
        try:
            sections = sections.filter(id=int(id_section))
        except ValueError:
            sections = sections.none()

    if name:
        sections = sections.filter(name__icontains=name)

    if description:
        sections = sections.filter(description__icontains=description)

    return render(request, 'sections.html', {'sections': sections})

# --- صفحة التقارير
@login_required
def reports_page(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'reports.html')


# --- صفحة تفاصيل الطالب
@login_required
def student_detail(request, student_id):
    if not request.user.is_staff:
        return redirect('login')

    student = get_object_or_404(Student, id_student=student_id)
    sections = Section.objects.all()

    # حفظ تعديل البيانات الشخصية أو الدرجات
    if request.method == 'POST':
        student.name = request.POST.get('name', student.name)
        section_id = request.POST.get('section')
        student.section = Section.objects.get(id=section_id) if section_id else student.section
        student.email = request.POST.get('email', student.email)
        student.save()

        for key, value in request.POST.items():
            if key.startswith('grade_'):
                enrollment_id = key.split('_')[1]
                try:
                    enrollment = Enrollment.objects.get(id=enrollment_id)
                    enrollment.grade = float(value) if value else None
                    enrollment.save()
                except Enrollment.DoesNotExist:
                    pass
        return redirect('student_detail', student_id=student.id_student)

    # جلب جميع التنزيلات للطالب
    enrollments = Enrollment.objects.filter(student=student).select_related('material').order_by('year', 'semester')

    # تنظيم المواد حسب السمستر
    semesters = {}
    for e in enrollments:
        sem_name = f"{e.semester} ({e.year})"
        if sem_name not in semesters:
            semesters[sem_name] = []
        semesters[sem_name].append(e)

    # حساب المعدل لكل سمستر والمعدل التراكمي
    semester_gpa = {}
    total_points = 0
    total_hours = 0
    for sem, courses in semesters.items():
        sem_points = sum([c.grade * c.material.hours for c in courses if c.grade is not None])
        sem_hours = sum([c.material.hours for c in courses if c.grade is not None])
        semester_gpa[sem] = round(sem_points / sem_hours, 2) if sem_hours > 0 else 0
        total_points += sem_points
        total_hours += sem_hours

    cumulative_gpa = round(total_points / total_hours, 2) if total_hours > 0 else 0

    context = {
        'student': student,
        'sections': sections,
        'semesters': semesters,
        'semester_gpa': semester_gpa,
        'cumulative_gpa': cumulative_gpa
    }

    return render(request, 'student_detail.html', context)


@login_required
def add_student(request):
    sections = Section.objects.all()
    if request.method == 'POST':
        id_student = request.POST.get('id_student')
        name = request.POST.get('name')
        section_id = request.POST.get('section')
        email = request.POST.get('email')
        password = request.POST.get('password')

        section = Section.objects.get(id=section_id)
        Student.objects.create(
            id_student=id_student,
            name=name,
            section=section,
            email=email,
            password=password
        )
        return redirect('students_page')

    return render(request, 'student_add.html', {'sections': sections})





def add_section(request):
    if request.method == "POST":
        section_id = request.POST.get("id")
        name = request.POST.get("name")
        
        if section_id and name:
            Section.objects.create(id=section_id, name=name)
            return redirect('sections_page') 
    return render(request, 'add_section.html')  



def add_material_page(request):
    if not request.user.is_staff:
        return redirect('login')

    sections = Section.objects.all()
    field_errors = {}  # لتخزين الأخطاء الخاصة بكل حقل

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        name = request.POST.get('name', '').strip()
        section_id = request.POST.get('section')
        hours = request.POST.get('hours', '').strip()
        description = request.POST.get('description', '').strip()

        # التحقق من الحقول الفارغة
        if not code:
            field_errors['code'] = " يرجى إدخال رمز المادة"
        elif Material.objects.filter(code=code).exists():
            field_errors['code'] = " رمز المادة موجود مسبقًا"

        if not name:
            field_errors['name'] = " يرجى إدخال اسم المادة"

        if not section_id:
            field_errors['section'] = " يرجى اختيار القسم"

        if not hours:
            field_errors['hours'] = " يرجى إدخال عدد الساعات"

        # إذا فيه أخطاء
        if field_errors:
            return render(request, 'add_material.html', {
                'sections': sections,
                'field_errors': field_errors,
                'form_data': request.POST
            })

        # إنشاء المادة الجديدة
        section = Section.objects.get(id=section_id)
        Material.objects.create(
            code=code,
            name=name,
            section=section,
            hours=hours or 0,
            description=description
        )

        messages.success(request, f"تمت إضافة المادة ({name}) بنجاح ✅")
        return redirect('materials_page')

    return render(request, 'add_material.html', {'sections': sections})
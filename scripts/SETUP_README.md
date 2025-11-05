# Course Registration Project - Setup Guide

## Quick Setup

لتثبيت المشروع وإنشاء قاعدة البيانات والمستخدم المدير، قم بتشغيل:

```bash
sudo /var/www/course_registration/scripts/setup.sh
```

أو بدون sudo (إذا كان لديك الصلاحيات):

```bash
/var/www/course_registration/scripts/setup.sh
```

## ما يقوم به Script التثبيت:

1. ✅ التحقق من وجود البيئة الافتراضية (virtual environment)
2. ✅ تفعيل البيئة الافتراضية
3. ✅ التحقق من تشغيل PostgreSQL
4. ✅ إنشاء قاعدة البيانات `courseruniversty` (إذا لم تكن موجودة)
5. ✅ إنشاء مستخدم قاعدة البيانات `abdalla` (إذا لم يكن موجوداً)
6. ✅ تشغيل Django migrations
7. ✅ إنشاء المستخدم المدير (admin) في Django

## بيانات المستخدم المدير (Admin):

- **Username:** `admin`
- **Password:** `123123`
- **Email:** `admin@example.com`

## بعد التثبيت:

### تشغيل الخادم:

```bash
cd /var/www/course_registration
source .venv/bin/activate
python3 manage.py runserver 0.0.0.0:8000
```

### الوصول إلى لوحة التحكم:

- **URL:** http://192.168.100.102:8000/admin/
- **Username:** admin
- **Password:** 123123

## ملاحظات:

- إذا كان المستخدم المدير موجوداً مسبقاً، سيتم تحديث كلمة المرور فقط
- Script التثبيت آمن للتشغيل المتكرر (idempotent)
- جميع الملفات المطلوبة موجودة في المشروع

## استكشاف الأخطاء:

### إذا فشل التثبيت:

1. تأكد من تشغيل PostgreSQL:
   ```bash
   sudo systemctl status postgresql
   ```

2. تأكد من وجود البيئة الافتراضية:
   ```bash
   ls -la /var/www/course_registration/.venv
   ```

3. تحقق من الصلاحيات:
   ```bash
   ls -la /var/www/course_registration/scripts/setup.sh
   ```


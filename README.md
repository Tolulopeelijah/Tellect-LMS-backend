# Tellect LMS Backend

An MVP implementation of the Tellect Learning Management System backend built with Django REST Framework.

## Features Implemented
### 1. Authentication & Authorization
- User model extended with `role` (STUDENT, INSTRUCTOR, ADMIN) enforcing RBAC.
- Avatar and Profile fields implemented.
- JWT-based login using `djangorestframework-simplejwt`.
- Password reset mock flow using email generation.

### 2. Course Management
- Overhauled course models with hierarchical structure: `Category` -> `Course` -> `CourseSection` -> `Lesson` -> Content.
- Search and filtering via `django-filter`.
- Course Enrolment tracking the student's progress and lesson completion tracking.

### 3. Content Delivery
- Lessons accept PDF and Video content natively.
- Basic watch progress and PDF read progress mocked using API endpoints for the respective content viewing tracking.

### 4. Enrollment & Payments
- Checkout endpoints and Webhook endpoints established for Paystack integration (`apps/payments/`).
- Webhook signature verification guarantees secure requests from Paystack to update Transaction metadata and auto-enroll students (NFR-13).

### 5. Assessments & Quizzes
- Simple Computer Based Testing (CBT) integrated. Instructors can define questions directly mapped to courses/lessons, with automated grading available.

### High-Priority Non-Functional Requirements (NFRs)
- **NFR-11 & NFR-12**: DRF global input validation built-in; AnonRateThrottle and UserRateThrottle established to cap requests per minute in production.
- **NFR-18**: Load balancer health checks (`/health/`, `/ready/`) implemented at root level.
- **NFR-21**: `drf-spectacular` is pre-configured to automatically generate Swagger OpenAPI 3.0 API Documentation (`/api/schema/`, `/api/docs/`).
- **NFR-22**: Django structured JSON logging configured using `logging.StreamHandler` so logs output to console in easily ingestible JSON format for monitoring agents.

## Getting Started

1. Install requirements using your preferred virtual environment manager:
```bash
python -m venv venv
source venv/bin/activate  # Or `.\venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

2. Generate the migrations and apply them over SQLite3 (local fallback config):
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Run Server:
```bash
python manage.py runserver
```

## Production Migration Steps

> **IMPORTANT:** In moving towards production compliance, the following migrations and changes must be manually executed to meet the scale criteria stated in NFR-04, NFR-06, and NFR-07.

**Step 1: Database Migration (SQLite3  → PostgreSQL)**
Configure `settings.py` for `DATABASES` natively:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='postgres://user:password@localhost/lms_db')
}
```
*Note*: Don't forget to run `pip install psycopg2-binary` and update `requirements.txt`.

**Step 2: Caching System Implementation (Redis)**
Implement Django caching backend backed by Redis:
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

**Step 3: Object Storage Enablement (S3/Cloudinary)**
Instead of relying on the local `./media` directory currently active via `models.ImageField/FileField`:
```bash
pip install django-storages boto3
```
Add to `settings.py`:
```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

**Step 4: Celery Background Job Workers**
As Webhooks and emails expand, wrap handlers in `celery` workers communicating through Redis natively.
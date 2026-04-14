# Tellect LMS Backend — API Documentation

## Base URL

- Local dev: `http://127.0.0.1:8000`
- All API endpoints are under: `/api/`

## Root

### Get service root

- **GET** `/`
- **Auth**: Public
- **Response**: Small service “welcome” payload + pointer to `/api/`.

## Authentication

This backend uses **JWT Bearer tokens** (SimpleJWT).

- **Header** (for protected endpoints):

```http
Authorization: Bearer <access_token>
```

### Auth flow (typical)

1. Register → `POST /api/auth/register/`
2. Verify OTP → `POST /api/auth/verify-otp/` (returns access + refresh)
3. Login → `POST /api/auth/login/` (returns access + refresh)
4. Refresh access token → `POST /api/auth/token/refresh/`

### Permissions quick reference

The global default is `IsAuthenticated`, but many endpoints explicitly override it:

- **Public (`AllowAny`)**:
  - Courses list/detail
  - Auth register/login/verify/token refresh
  - API “home” endpoints (module discovery)
- **Protected (`IsAuthenticated`)**:
  - Profile, logout
  - Enroll course, my courses
  - Videos/PDFs progress endpoints
  - CBT attempts endpoints
  - Dashboard and Groups endpoints
- **Admin-only (`IsAdminUser`)**:
  - Video approve/reject
  - PDF upload

## Common response patterns

- **Errors** are generally returned like:

```json
{ "error": "Message here." }
```

- **Validation errors** follow DRF serializer format (field → list of messages).

---

## API Home (Discovery)

### Get API home

- **GET** `/api/`
- **Auth**: Public
- **Response**: Lists module base URLs.

---

## Auth (`/api/auth/`)

### Auth module home

- **GET** `/api/auth/`
- **Auth**: Public
- **Response**: Lists available auth endpoints.

### Register

- **POST** `/api/auth/register/`
- **Auth**: Public
- **Body**

```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "phone_number": "+1234567890",
  "university": "Example University",
  "department": "Computer Science",
  "level": "300",
  "password": "strongpassword",
  "confirm_password": "strongpassword"
}
```

- **Success (201)**:
  - Returns `email` and an `otp` (currently returned for testing).

### Verify OTP

- **POST** `/api/auth/verify-otp/`
- **Auth**: Public
- **Body**

```json
{ "email": "jane@example.com", "code": "123456" }
```

- **Success (200)**:

```json
{
  "message": "Email verified successfully.",
  "access": "<jwt_access>",
  "refresh": "<jwt_refresh>"
}
```

### Login

- **POST** `/api/auth/login/`
- **Auth**: Public
- **Body**

```json
{ "email": "jane@example.com", "password": "strongpassword" }
```

- **Success (200)**:

```json
{
  "access": "<jwt_access>",
  "refresh": "<jwt_refresh>",
  "user": {
    "id": 1,
    "full_name": "Jane Doe",
    "email": "jane@example.com",
    "phone_number": "+1234567890",
    "university": "Example University",
    "department": "Computer Science",
    "level": "300",
    "is_verified": true,
    "date_joined": "2026-03-17T00:00:00Z"
  }
}
```

### Logout

- **POST** `/api/auth/logout/`
- **Auth**: Bearer token required
- **Response (200)**:

```json
{ "message": "Logged out successfully." }
```

### Refresh access token

- **POST** `/api/auth/token/refresh/`
- **Auth**: Public
- **Body**

```json
{ "refresh": "<jwt_refresh>" }
```

- **Success (200)**:

```json
{ "access": "<jwt_access>" }
```

### Profile (get/update)

- **GET** `/api/auth/profile/`
- **PUT** `/api/auth/profile/`
- **Auth**: Bearer token required
- **PUT body**: Any subset of profile fields (partial update).

---

## Courses (`/api/courses/`)

### List courses

- **GET** `/api/courses/`
- **Auth**: Public
- **Response**: Array of courses.

### My courses

- **GET** `/api/courses/my-courses/`
- **Auth**: Bearer token required
- **Response**: Array of enrollments (includes nested `course`).

### Course detail

- **GET** `/api/courses/<int:pk>/`
- **Auth**: Public
- **Response**: Course object.
  - If authenticated and enrolled, response includes an `enrollment` object.

### Enroll in a course

- **POST** `/api/courses/<int:pk>/enroll/`
- **Auth**: Bearer token required
- **Response**: Enrollment created, or “Already enrolled.”

---

## Videos (`/api/videos/`)

### Videos module home

- **GET** `/api/videos/`
- **Auth**: Public

### List videos for a course

- **GET** `/api/videos/course/<int:course_id>/`
- **Auth**: Bearer token required

### Upload a video

- **POST** `/api/videos/upload/`
- **Auth**: Bearer token required
- **Notes**:
  - Expects multipart form data (video file + optional thumbnail).

### Recently watched

- **GET** `/api/videos/recently-watched/`
- **Auth**: Bearer token required

### Video detail

- **GET** `/api/videos/<int:pk>/`
- **Auth**: Bearer token required

### Update watch progress

- **POST** `/api/videos/<int:pk>/update-progress/`
- **Auth**: Bearer token required
- **Body**

```json
{ "watched_seconds": 120 }
```

### Approve / Reject video (admin)

- **POST** `/api/videos/<int:pk>/approve/`
- **POST** `/api/videos/<int:pk>/reject/`
- **Auth**: Admin user required
- **Reject body**

```json
{ "reason": "Copyright issue" }
```

---

## PDFs (`/api/pdfs/`)

### PDFs module home

- **GET** `/api/pdfs/`
- **Auth**: Public

### List PDFs for a course

- **GET** `/api/pdfs/course/<int:course_id>/`
- **Auth**: Bearer token required

### Upload a PDF (admin)

- **POST** `/api/pdfs/upload/`
- **Auth**: Admin user required
- **Notes**:
  - Expects multipart form data (PDF file).

### My PDF progress

- **GET** `/api/pdfs/my-progress/`
- **Auth**: Bearer token required

### PDF detail

- **GET** `/api/pdfs/<int:pk>/`
- **Auth**: Bearer token required

### Update PDF progress

- **POST** `/api/pdfs/<int:pk>/update-progress/`
- **Auth**: Bearer token required
- **Body**

```json
{
  "pages_read": 10,
  "total_pages": 100,
  "time_spent_minutes": 15
}
```

---

## CBT (`/api/cbt/`)

### CBT module home

- **GET** `/api/cbt/`
- **Auth**: Public

### List exams for a course

- **GET** `/api/cbt/course/<int:course_id>/`
- **Auth**: Bearer token required

### Exam detail

- **GET** `/api/cbt/<int:exam_id>/`
- **Auth**: Bearer token required

### Start exam

- **POST** `/api/cbt/<int:exam_id>/start/`
- **Auth**: Bearer token required
- **Response**: Creates (or reuses) an in-progress attempt and returns attempt + questions.

### Attempt detail

- **GET** `/api/cbt/attempt/<int:attempt_id>/`
- **Auth**: Bearer token required

### Save an answer

- **POST** `/api/cbt/attempt/<int:attempt_id>/answer/`
- **Auth**: Bearer token required
- **Body**

```json
{
  "question_id": 1,
  "selected_option": "A",
  "time_taken_seconds": 12
}
```

### Submit / Auto-submit

- **POST** `/api/cbt/attempt/<int:attempt_id>/submit/`
- **POST** `/api/cbt/attempt/<int:attempt_id>/auto-submit/`
- **Auth**: Bearer token required

---

## Dashboard (`/api/dashboard/`)

### Dashboard home (summary)

- **GET** `/api/dashboard/`
- **Auth**: Bearer token required
- **Response**: Enrolled courses, recently watched, pdf stats, today’s timetable, today’s todos.

### Timetable

- **GET** `/api/dashboard/timetable/`
- **POST** `/api/dashboard/timetable/`
- **PUT** `/api/dashboard/timetable/<int:pk>/`
- **DELETE** `/api/dashboard/timetable/<int:pk>/`
- **Auth**: Bearer token required

### Todos

- **GET** `/api/dashboard/todos/`
- **POST** `/api/dashboard/todos/`
- **PUT** `/api/dashboard/todos/<int:pk>/`
- **DELETE** `/api/dashboard/todos/<int:pk>/`
- **POST** `/api/dashboard/todos/<int:pk>/complete/`
- **Auth**: Bearer token required

---

## Groups (`/api/groups/`)

### List / create groups

- **GET** `/api/groups/`
- **POST** `/api/groups/`
- **Auth**: Bearer token required

### Group detail

- **GET** `/api/groups/<int:pk>/`
- **Auth**: Bearer token required

### Join / leave

- **POST** `/api/groups/<int:pk>/join/`
- **POST** `/api/groups/<int:pk>/leave/`
- **Auth**: Bearer token required

### Members progress

- **GET** `/api/groups/<int:pk>/members-progress/`
- **Auth**: Bearer token required
- **Response**: Per-member stats (PDF totals, recent CBT scores).

---

## Placeholder Modules (Scaffolded)

These modules are present and routed, but only expose a discovery endpoint for now:

### Payments

- **GET** `/api/payments/`
- **Auth**: Public

### Notifications

- **GET** `/api/notifications/`
- **Auth**: Public

### Certificates

- **GET** `/api/certificates/`
- **Auth**: Public

### Analytics

- **GET** `/api/analytics/`
- **Auth**: Public

### Announcements

- **GET** `/api/announcements/`
- **Auth**: Public

### Support

- **GET** `/api/support/`
- **Auth**: Public


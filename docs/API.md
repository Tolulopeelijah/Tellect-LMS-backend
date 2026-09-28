/api/groups/{pk}/members-progress/# Tellect LMS Backend — Complete API Reference

Base URL (local): `http://127.0.0.1:8000`

All JSON requests should use:

```http
Content-Type: application/json
```

File uploads use:

```http
Content-Type: multipart/form-data
```

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

---

## Table of Contents

1. [Conventions](#conventions)
2. [Reusable Schemas](#reusable-schemas)
3. [Root & System](#root--system)
4. [Auth (`/api/auth/`)](#auth-apiauth)
5. [Courses (`/api/courses/`)](#courses-apicourses)
6. [Videos (`/api/videos/`)](#videos-apivideos)
7. [PDFs (`/api/pdfs/`)](#pdfs-apipdfs)
8. [CBT (`/api/cbt/`)](#cbt-apicbt)
9. [Dashboard (`/api/dashboard/`)](#dashboard-apidashboard)
10. [Groups (`/api/groups/`)](#groups-apigroups)
11. [Payments (`/api/payments/`)](#payments-apipayments)
12. [Placeholder Modules](#placeholder-modules)

---

## Conventions

### Data types


| Type                | Description                                  |
| ------------------- | -------------------------------------------- |
| `string`            | Text value                                   |
| `integer`           | Whole number                                 |
| `float`             | Decimal number                               |
| `boolean`           | `true` or `false`                            |
| `string (email)`    | Valid email address                          |
| `string (uri)`      | URL (e.g. media file path)                   |
| `string (date)`     | `YYYY-MM-DD`                                 |
| `string (time)`     | `HH:MM:SS`                                   |
| `string (datetime)` | ISO 8601, e.g. `2026-06-27T12:00:00Z`        |
| `string (decimal)`  | Decimal serialized as string, e.g. `"49.99"` |
| `file`              | Binary upload via `multipart/form-data`      |
| `object`            | JSON object                                  |
| `array`             | JSON array                                   |


### Required vs optional

- **Required** — must be present in the request body.
- **Optional** — may be omitted; defaults apply where noted.
- **Read-only** — returned in responses only; ignored on write.

### Pagination

List endpoints using DRF `PageNumberPagination` return:

```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/courses/?page=2",
  "previous": null,
  "results": []
}
```

Default page size: **20**.

### Validation errors (`400`)

```json
{
  "field_name": ["Error message."]
}
```

### Simple errors

```json
{ "error": "Error message." }
```

or

```json
{ "message": "Informational message." }
```

### Roles


| Value        | Description                |
| ------------ | -------------------------- |
| `STUDENT`    | Default learner role       |
| `INSTRUCTOR` | Can manage course content  |
| `ADMIN`      | Full administrative access |


### User level choices

`100` | `200` | `300` | `400` | `500`

---

## Reusable Schemas

### UserProfile


| Field          | Type                | Notes                                         |
| -------------- | ------------------- | --------------------------------------------- |
| `id`           | integer             | Read-only                                     |
| `full_name`    | string              |                                               |
| `email`        | string (email)      | Read-only                                     |
| `phone_number` | string              | Optional                                      |
| `university`   | string              | Optional                                      |
| `department`   | string              | Optional                                      |
| `level`        | string              | One of `100`–`500`                            |
| `role`         | string              | `STUDENT` | `INSTRUCTOR` | `ADMIN`, read-only |
| `bio`          | string | null       | Optional                                      |
| `avatar`       | string (uri) | null | Image URL                                     |
| `is_verified`  | boolean             | Read-only                                     |
| `date_joined`  | string (datetime)   | Read-only                                     |


### Category


| Field         | Type    | Notes              |
| ------------- | ------- | ------------------ |
| `id`          | integer | Read-only          |
| `name`        | string  | Required on create |
| `description` | string  | Optional           |


### Course (list/create/update)


| Field                | Type                | Notes                                |
| -------------------- | ------------------- | ------------------------------------ |
| `id`                 | integer             | Read-only                            |
| `title`              | string              | Required on create                   |
| `description`        | string              | Required on create                   |
| `thumbnail`          | string (uri) | null | Optional, image upload               |
| `instructor`         | integer             | User ID; set automatically on create |
| `instructor_details` | UserProfile         | Read-only nested object              |
| `category`           | integer | null      | Category ID                          |
| `category_details`   | Category            | Read-only nested object              |
| `price`              | string (decimal)    | Default `"0.00"`                     |
| `is_published`       | boolean             | Default `false`                      |
| `created_at`         | string (datetime)   | Read-only                            |
| `is_active`          | boolean             | Default `true`                       |


### CourseDetail

Extends **Course** with:


| Field      | Type                   | Notes            |
| ---------- | ---------------------- | ---------------- |
| `sections` | array of CourseSection | Read-only nested |


### CourseSection


| Field     | Type            | Notes               |
| --------- | --------------- | ------------------- |
| `id`      | integer         | Read-only           |
| `course`  | integer         | Course ID, required |
| `title`   | string          | Required            |
| `order`   | integer         | Default `0`         |
| `lessons` | array of Lesson | Read-only nested    |


### Lesson


| Field     | Type    | Notes                         |
| --------- | ------- | ----------------------------- |
| `id`      | integer | Read-only                     |
| `section` | integer | Section ID, required          |
| `title`   | string  | Required                      |
| `content` | string  | HTML/JSON rich text, optional |
| `order`   | integer | Default `0`                   |


### CourseEnrollment


| Field                 | Type              | Notes                      |
| --------------------- | ----------------- | -------------------------- |
| `id`                  | integer           | Read-only                  |
| `student`             | integer           | User ID, read-only         |
| `course`              | Course            | Nested course object       |
| `enrolled_at`         | string (datetime) | Read-only                  |
| `progress_percentage` | float             | Read-only, default `0`     |
| `is_completed`        | boolean           | Read-only, default `false` |


### Video


| Field              | Type                | Notes                                          |
| ------------------ | ------------------- | ---------------------------------------------- |
| `id`               | integer             | Read-only                                      |
| `section`          | integer | null      | Section ID                                     |
| `course`           | integer | null      | Course ID                                      |
| `title`            | string              |                                                |
| `description`      | string              | Optional                                       |
| `video_file`       | string (uri)        | Video file URL                                 |
| `thumbnail`        | string (uri) | null | Optional                                       |
| `duration_seconds` | integer             | Default `0`                                    |
| `is_downloadable`  | boolean             | Default `false`                                |
| `status`           | string              | `pending` | `approved` | `rejected`, read-only |
| `rejection_reason` | string              | Read-only                                      |
| `uploaded_by`      | integer             | User ID, read-only                             |
| `created_at`       | string (datetime)   | Read-only                                      |
| `file_size_mb`     | float               | Read-only                                      |


### VideoWatchProgress


| Field             | Type              | Notes                           |
| ----------------- | ----------------- | ------------------------------- |
| `id`              | integer           | Read-only                       |
| `video`           | integer           | Video ID                        |
| `watched_seconds` | integer           |                                 |
| `last_watched`    | string (datetime) | Read-only                       |
| `is_completed`    | boolean           | Auto-calculated at ≥90% watched |


### PDFMaterial


| Field             | Type              | Notes          |
| ----------------- | ----------------- | -------------- |
| `id`              | integer           | Read-only      |
| `lesson`          | integer | null    | Lesson ID      |
| `title`           | string            | Required       |
| `description`     | string            | Optional       |
| `pdf_file`        | string (uri)      | PDF file URL   |
| `is_downloadable` | boolean           | Default `true` |
| `uploaded_by`     | integer           | Read-only      |
| `created_at`      | string (datetime) | Read-only      |


### PDFReadProgress


| Field                | Type              | Notes           |
| -------------------- | ----------------- | --------------- |
| `id`                 | integer           | Read-only       |
| `student`            | integer           | Read-only       |
| `pdf`                | integer           | PDF ID          |
| `pages_read`         | integer           |                 |
| `total_pages`        | integer           |                 |
| `time_spent_minutes` | integer           |                 |
| `last_read`          | string (datetime) | Read-only       |
| `is_completed`       | boolean           | Auto-calculated |


### CBTExam


| Field              | Type    | Notes                     |
| ------------------ | ------- | ------------------------- |
| `id`               | integer | Read-only                 |
| `course`           | integer | Course ID                 |
| `title`            | string  |                           |
| `description`      | string  | Optional                  |
| `duration_minutes` | integer | Default `60`              |
| `total_questions`  | integer | Default `0`               |
| `pass_score`       | integer | Default `50` (percentage) |
| `is_active`        | boolean | Default `true`            |


### Question


| Field      | Type    | Notes         |
| ---------- | ------- | ------------- |
| `id`       | integer | Read-only     |
| `text`     | string  | Question text |
| `option_a` | string  |               |
| `option_b` | string  |               |
| `option_c` | string  |               |
| `option_d` | string  |               |
| `order`    | integer | Display order |


> Note: `correct_option` is **not** exposed in API responses.

### CBTAttempt


| Field                | Type                     | Notes                                     |
| -------------------- | ------------------------ | ----------------------------------------- |
| `id`                 | integer                  | Read-only                                 |
| `exam`               | integer                  | Exam ID                                   |
| `started_at`         | string (datetime)        | Read-only                                 |
| `submitted_at`       | string (datetime) | null | Read-only                                 |
| `status`             | string                   | `in_progress` | `submitted` | `timed_out` |
| `score`              | integer                  | Percentage 0–100                          |
| `total_questions`    | integer                  |                                           |
| `correct_answers`    | integer                  |                                           |
| `time_taken_seconds` | integer                  |                                           |
| `answers`            | array of QuestionAnswer  | Nested                                    |


### QuestionAnswer


| Field                | Type          | Notes                 |
| -------------------- | ------------- | --------------------- |
| `id`                 | integer       | Read-only             |
| `question`           | Question      | Nested                |
| `selected_option`    | string | null | `A` | `B` | `C` | `D` |
| `is_correct`         | boolean       |                       |
| `time_taken_seconds` | integer       |                       |


### ReadingTimetable


| Field         | Type          | Notes                   |
| ------------- | ------------- | ----------------------- |
| `id`          | integer       | Read-only               |
| `day_of_week` | integer       | `0`=Monday … `6`=Sunday |
| `start_time`  | string (time) |                         |
| `end_time`    | string (time) |                         |
| `subject`     | string        |                         |
| `is_active`   | boolean       | Default `true`          |


### TodoItem


| Field            | Type                 | Notes           |
| ---------------- | -------------------- | --------------- |
| `id`             | integer              | Read-only       |
| `title`          | string               | Required        |
| `description`    | string               | Optional        |
| `scheduled_time` | string (time) | null | Optional        |
| `scheduled_date` | string (date)        | Required        |
| `is_completed`   | boolean              | Default `false` |
| `created_at`     | string (datetime)    | Read-only       |


### StudyGroup


| Field         | Type                     | Notes              |
| ------------- | ------------------------ | ------------------ |
| `id`          | integer                  | Read-only          |
| `name`        | string                   | Required on create |
| `description` | string                   | Optional           |
| `created_by`  | UserProfile              | Read-only          |
| `memberships` | array of GroupMembership | Read-only          |
| `created_at`  | string (datetime)        | Read-only          |
| `is_active`   | boolean                  | Default `true`     |


### GroupMembership


| Field       | Type              | Notes              |
| ----------- | ----------------- | ------------------ |
| `id`        | integer           | Read-only          |
| `student`   | UserProfile       | Read-only          |
| `joined_at` | string (datetime) | Read-only          |
| `role`      | string            | `member` | `admin` |


### Transaction


| Field        | Type              | Notes                                         |
| ------------ | ----------------- | --------------------------------------------- |
| `id`         | integer           | Read-only                                     |
| `user`       | integer           | User ID, read-only                            |
| `course`     | integer           | Course ID                                     |
| `amount`     | string (decimal)  | Read-only                                     |
| `reference`  | string            | Gateway reference, read-only                  |
| `gateway`    | string            | `PAYSTACK` | `FLUTTERWAVE` | `STRIPE`         |
| `status`     | string            | `PENDING` | `SUCCESS` | `FAILED` | `REFUNDED` |
| `created_at` | string (datetime) | Read-only                                     |
| `updated_at` | string (datetime) | Read-only                                     |


---

## Root & System

### GET `/`

**Auth:** Public  
**Request body:** None

**Response `200`**


| Field                        | Type              |
| ---------------------------- | ----------------- |
| `name`                       | string            |
| `tagline`                    | string            |
| `version`                    | string            |
| `api.url`                    | string (uri)      |
| `api.documentation`          | string (uri)      |
| `api.status`                 | string            |
| `quick_links.login`          | string (uri)      |
| `quick_links.register`       | string (uri)      |
| `quick_links.browse_courses` | string (uri)      |
| `quick_links.health_check`   | string (uri)      |
| `health.status`              | string            |
| `health.timestamp`           | string (datetime) |
| `company.name`               | string            |
| `company.website`            | string (uri)      |
| `company.support_email`      | string (email)    |


---

### GET `/health/`

**Auth:** Public

**Response `200`**


| Field    | Type   |
| -------- | ------ |
| `status` | string |


---

### GET `/ready/`

**Auth:** Public

**Response `200`**


| Field    | Type   |
| -------- | ------ |
| `status` | string |


---

### GET `/api/`

**Auth:** Public

**Response `200`**


| Field                         | Type              |
| ----------------------------- | ----------------- |
| `name`                        | string            |
| `version`                     | string            |
| `description`                 | string            |
| `documentation.swagger`       | string (uri)      |
| `documentation.redoc`         | string (uri)      |
| `documentation.postman`       | string (uri)      |
| `status.environment`          | string            |
| `status.timestamp`            | string (datetime) |
| `status.maintenance_mode`     | boolean           |
| `authentication.status`       | string            |
| `authentication.user`         | object | null     |
| `authentication.login_url`    | string (uri)      |
| `authentication.register_url` | string (uri)      |
| `authentication.docs`         | string            |
| `modules`                     | object            |
| `pagination.default_limit`    | integer           |
| `pagination.max_limit`        | integer           |
| `rate_limits.anonymous`       | string            |
| `rate_limits.authenticated`   | string            |
| `links.self`                  | string (uri)      |
| `links.health_check`          | string (uri)      |
| `links.metrics`               | string (uri)      |


---

### GET `/api/docs/` · GET `/api/redoc/` · GET `/api/schema/`

**Auth:** Public  
Interactive OpenAPI documentation (Swagger UI / ReDoc / raw schema).

---

## Auth (`/api/auth/`)

### GET `/api/auth/`

**Auth:** Public

**Response `200`**


| Field                              | Type   |
| ---------------------------------- | ------ |
| `name`                             | string |
| `endpoints.register`               | string |
| `endpoints.verify_otp`             | string |
| `endpoints.login`                  | string |
| `endpoints.logout`                 | string |
| `endpoints.token_refresh`          | string |
| `endpoints.profile`                | string |
| `endpoints.password_reset`         | string |
| `endpoints.password_reset_confirm` | string |


---

### POST `/api/auth/register/`

**Auth:** Public

**Request body**


| Field              | Type           | Required |
| ------------------ | -------------- | -------- |
| `full_name`        | string         | Yes      |
| `email`            | string (email) | Yes      |
| `phone_number`     | string         | No       |
| `university`       | string         | No       |
| `department`       | string         | No       |
| `level`            | string         | No       |
| `role`             | string         | No       |
| `password`         | string         | Yes      |
| `confirm_password` | string         | Yes      |


**Response `201`**


| Field     | Type           |
| --------- | -------------- |
| `message` | string         |
| `email`   | string (email) |
| `otp`     | string         |


**Response `400`:** Validation errors

---

### POST `/api/auth/verify-otp/`

**Auth:** Public

**Request body**


| Field   | Type           | Required |
| ------- | -------------- | -------- |
| `email` | string (email) | Yes      |
| `code`  | string         | Yes      |


**Response `200`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |
| `access`  | string |
| `refresh` | string |


**Response `400`:** Invalid/expired OTP  
**Response `404`:** `{ "error": "User not found." }`

---

### POST `/api/auth/login/`

**Auth:** Public

**Request body**


| Field      | Type           | Required |
| ---------- | -------------- | -------- |
| `email`    | string (email) | Yes      |
| `password` | string         | Yes      |


**Response `200`**


| Field     | Type        |
| --------- | ----------- |
| `access`  | string      |
| `refresh` | string      |
| `user`    | UserProfile |


**Response `401`:** `{ "error": "Invalid credentials." }`  
**Response `403`:** `{ "error": "Please verify your email before logging in." }`

---

### POST `/api/auth/logout/`

**Auth:** Bearer token required  
**Request body:** None

**Response `200`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |


---

### POST `/api/auth/token/refresh/`

**Auth:** Public

**Request body**


| Field     | Type   | Required |
| --------- | ------ | -------- |
| `refresh` | string | Yes      |


**Response `200`**


| Field    | Type   |
| -------- | ------ |
| `access` | string |


**Response `400`:** `{ "error": "Refresh token required." }`  
**Response `401`:** `{ "error": "Invalid or expired refresh token." }`

---

### GET `/api/auth/profile/`

**Auth:** Bearer token required  
**Request body:** None

**Response `200`:** UserProfile object

---

### PUT `/api/auth/profile/`

**Auth:** Bearer token required  
**Content-Type:** `application/json` or `multipart/form-data` (if uploading `avatar`)

**Request body** (all optional — partial update)


| Field          | Type   |
| -------------- | ------ |
| `full_name`    | string |
| `phone_number` | string |
| `university`   | string |
| `department`   | string |
| `level`        | string |
| `bio`          | string |
| `avatar`       | file   |


**Response `200`:** UserProfile object  
**Response `400`:** Validation errors

---

### POST `/api/auth/password/reset/`

**Auth:** Public

**Request body**


| Field   | Type           | Required |
| ------- | -------------- | -------- |
| `email` | string (email) | Yes      |


**Response `200`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |
| `otp`     | string |


---

### POST `/api/auth/password/reset/confirm/`

**Auth:** Public

**Request body**


| Field              | Type           | Required |
| ------------------ | -------------- | -------- |
| `email`            | string (email) | Yes      |
| `otp`              | string         | Yes      |
| `new_password`     | string         | Yes      |
| `confirm_password` | string         | Yes      |


**Response `200`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |


**Response `400`:** Invalid OTP or validation errors

---

## Courses (`/api/courses/`)

All course router endpoints support pagination unless noted.

### Categories

#### GET `/api/courses/categories/`

**Auth:** Public

**Response `200`:** Paginated array of **Category**

#### POST `/api/courses/categories/`

**Auth:** Instructor or Admin

**Request body**


| Field         | Type   | Required |
| ------------- | ------ | -------- |
| `name`        | string | Yes      |
| `description` | string | No       |


**Response `201`:** Category object

#### GET `/api/courses/categories/{id}/`

**Auth:** Public  
**Response `200`:** Category object

#### PUT / PATCH `/api/courses/categories/{id}/`

**Auth:** Instructor or Admin

**Request body:** Same as POST (partial allowed on PATCH)  
**Response `200`:** Category object

#### DELETE `/api/courses/categories/{id}/`

**Auth:** Instructor or Admin  
**Response `204`:** No content

---

### Courses

#### GET `/api/courses/`

**Auth:** Public

**Query parameters**


| Param          | Type    | Description                                    |
| -------------- | ------- | ---------------------------------------------- |
| `category`     | integer | Filter by category ID                          |
| `is_published` | boolean | Filter by publish status                       |
| `search`       | string  | Search `title`, `description`                  |
| `ordering`     | string  | `created_at`, `-created_at`, `price`, `-price` |
| `page`         | integer | Page number                                    |


**Response `200`:** Paginated array of **Course**

> Unauthenticated users only see published courses.

#### POST `/api/courses/`

**Auth:** Instructor or Admin

**Request body**


| Field          | Type             | Required |
| -------------- | ---------------- | -------- |
| `title`        | string           | Yes      |
| `description`  | string           | Yes      |
| `thumbnail`    | file             | No       |
| `category`     | integer          | No       |
| `price`        | string (decimal) | No       |
| `is_published` | boolean          | No       |


**Response `201`:** Course object (`instructor` set to current user)

#### GET `/api/courses/{id}/`

**Auth:** Public  
**Response `200`:** **CourseDetail** object (includes `sections` with nested `lessons`)

#### PUT / PATCH `/api/courses/{id}/`

**Auth:** Instructor or Admin  
**Request body:** Same fields as POST  
**Response `200`:** Course object

#### DELETE `/api/courses/{id}/`

**Auth:** Instructor or Admin  
**Response `204`:** No content

#### POST `/api/courses/{id}/enroll/`

**Auth:** Bearer token required  
**Request body:** None

**Response `201`**


| Field        | Type             |
| ------------ | ---------------- |
| `message`    | string           |
| `enrollment` | CourseEnrollment |


**Response `200`:** `{ "message": "Already enrolled." }`  
**Response `402`:** `{ "error": "Payment required to enroll in this course." }` (when `price > 0`)

---

### Sections

#### GET `/api/courses/sections/`

**Auth:** Instructor or Admin  
**Response `200`:** Paginated array of **CourseSection**

#### POST `/api/courses/sections/`

**Auth:** Instructor or Admin

**Request body**


| Field    | Type    | Required |
| -------- | ------- | -------- |
| `course` | integer | Yes      |
| `title`  | string  | Yes      |
| `order`  | integer | No       |


**Response `201`:** CourseSection object

#### GET / PUT / PATCH / DELETE `/api/courses/sections/{id}/`

**Auth:** Instructor or Admin  
Standard CRUD; response types match **CourseSection**

---

### Lessons

#### GET `/api/courses/lessons/`

**Auth:** Instructor or Admin  
**Response `200`:** Paginated array of **Lesson**

#### POST `/api/courses/lessons/`

**Auth:** Instructor or Admin

**Request body**


| Field     | Type    | Required |
| --------- | ------- | -------- |
| `section` | integer | Yes      |
| `title`   | string  | Yes      |
| `content` | string  | No       |
| `order`   | integer | No       |


**Response `201`:** Lesson object

#### GET / PUT / PATCH / DELETE `/api/courses/lessons/{id}/`

**Auth:** Instructor or Admin  
Standard CRUD; response types match **Lesson**

---

### My Courses

#### GET `/api/courses/my-courses/`

**Auth:** Bearer token required  
**Response `200`:** Paginated array of **CourseEnrollment**

#### GET `/api/courses/my-courses/{id}/`

**Auth:** Bearer token required  
**Response `200`:** CourseEnrollment object

---

## Videos (`/api/videos/`)

### GET `/api/videos/`

**Auth:** Public

**Response `200`**


| Field       | Type   |
| ----------- | ------ |
| `name`      | string |
| `endpoints` | object |


---

### GET `/api/videos/course/{course_id}/`

**Auth:** Bearer token required

**Path params**


| Param       | Type    |
| ----------- | ------- |
| `course_id` | integer |


**Response `200`:** Array of **Video** (only `status=approved`)

---

### POST `/api/videos/upload/`

**Auth:** Bearer token required  
**Content-Type:** `multipart/form-data`

**Request body**


| Field             | Type    | Required |
| ----------------- | ------- | -------- |
| `course`          | integer | Yes      |
| `section`         | integer | No       |
| `title`           | string  | Yes      |
| `description`     | string  | No       |
| `video_file`      | file    | Yes      |
| `thumbnail`       | file    | No       |
| `is_downloadable` | boolean | No       |


**Response `201`:** Video object (`status` = `pending`)

---

### GET `/api/videos/recently-watched/`

**Auth:** Bearer token required  
**Response `200`:** Array of **VideoWatchProgress** (max 10)

---

### GET `/api/videos/{pk}/`

**Auth:** Bearer token required

**Path params**


| Param | Type    |
| ----- | ------- |
| `pk`  | integer |


**Response `200`:** Video object  
**Response `404`:** `{ "error": "Video not found." }`

---

### POST `/api/videos/{pk}/update-progress/`

**Auth:** Bearer token required

**Request body**


| Field             | Type    | Required |
| ----------------- | ------- | -------- |
| `watched_seconds` | integer | No       |


**Response `200`:** VideoWatchProgress object

---

### POST `/api/videos/{pk}/approve/`

**Auth:** Admin user required  
**Request body:** None

**Response `200`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |


---

### POST `/api/videos/{pk}/reject/`

**Auth:** Admin user required

**Request body**


| Field    | Type   | Required |
| -------- | ------ | -------- |
| `reason` | string | No       |


**Response `200`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |


---

## PDFs (`/api/pdfs/`)

### GET `/api/pdfs/`

**Auth:** Public — module discovery response (same shape as Videos home)

---

### GET `/api/pdfs/course/{course_id}/`

**Auth:** Bearer token required  
**Response `200`:** Array of **PDFMaterial**

---

### POST `/api/pdfs/upload/`

**Auth:** Admin user required  
**Content-Type:** `multipart/form-data`

**Request body**


| Field             | Type    | Required |
| ----------------- | ------- | -------- |
| `lesson`          | integer | No       |
| `title`           | string  | Yes      |
| `description`     | string  | No       |
| `pdf_file`        | file    | Yes      |
| `is_downloadable` | boolean | No       |


**Response `201`:** PDFMaterial object

---

### GET `/api/pdfs/my-progress/`

**Auth:** Bearer token required  
**Response `200`:** Array of **PDFReadProgress**

---

### GET `/api/pdfs/{pk}/`

**Auth:** Bearer token required  
**Response `200`:** PDFMaterial object  
**Response `404`:** `{ "error": "PDF not found." }`

---

### POST `/api/pdfs/{pk}/update-progress/`

**Auth:** Bearer token required

**Request body**


| Field                | Type    | Required |
| -------------------- | ------- | -------- |
| `pages_read`         | integer | No       |
| `total_pages`        | integer | No       |
| `time_spent_minutes` | integer | No       |


**Response `200`:** PDFReadProgress object

---

## CBT (`/api/cbt/`)

### GET `/api/cbt/`

**Auth:** Public — module discovery response

---

### GET `/api/cbt/course/{course_id}/`

**Auth:** Bearer token required  
**Response `200`:** Array of **CBTExam**

---

### GET `/api/cbt/{exam_id}/`

**Auth:** Bearer token required  
**Response `200`:** CBTExam object  
**Response `404`:** `{ "error": "Exam not found." }`

---

### POST `/api/cbt/{exam_id}/start/`

**Auth:** Bearer token required  
**Request body:** None

**Response `200` or `201`:** CBTAttempt + extra field:


| Field       | Type              |
| ----------- | ----------------- |
| `questions` | array of Question |


Reuses existing in-progress attempt if one exists.

---

### GET `/api/cbt/attempt/{attempt_id}/`

**Auth:** Bearer token required  
**Response `200`:** CBTAttempt object (includes `answers`)

---

### POST `/api/cbt/attempt/{attempt_id}/answer/`

**Auth:** Bearer token required

**Request body**


| Field                | Type    | Required |
| -------------------- | ------- | -------- |
| `question_id`        | integer | Yes      |
| `selected_option`    | string  | Yes      |
| `time_taken_seconds` | integer | No       |


**Response `200`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |


---

### POST `/api/cbt/attempt/{attempt_id}/submit/`

**Auth:** Bearer token required  
**Request body:** None

**Response `200`**


| Field             | Type       |
| ----------------- | ---------- |
| `message`         | string     |
| `score`           | integer    |
| `correct_answers` | integer    |
| `total_questions` | integer    |
| `passed`          | boolean    |
| `attempt`         | CBTAttempt |


---

### POST `/api/cbt/attempt/{attempt_id}/auto-submit/`

**Auth:** Bearer token required  
Same response shape as submit; sets attempt `status` to `timed_out`.

---

## Dashboard (`/api/dashboard/`)

### GET `/api/dashboard/`

**Auth:** Bearer token required

**Response `200`**


| Field                                | Type                        |
| ------------------------------------ | --------------------------- |
| `enrolled_courses`                   | array of CourseEnrollment   |
| `recently_watched`                   | array of VideoWatchProgress |
| `pdf_stats.total_pdfs_read`          | integer                     |
| `pdf_stats.total_time_spent_minutes` | integer                     |
| `todays_timetable`                   | array of ReadingTimetable   |
| `todays_todos`                       | array of TodoItem           |


---

### GET `/api/dashboard/timetable/`

**Auth:** Bearer token required  
**Response `200`:** Array of **ReadingTimetable**

---

### POST `/api/dashboard/timetable/`

**Auth:** Bearer token required

**Request body**


| Field         | Type          | Required |
| ------------- | ------------- | -------- |
| `day_of_week` | integer       | Yes      |
| `start_time`  | string (time) | Yes      |
| `end_time`    | string (time) | Yes      |
| `subject`     | string        | Yes      |
| `is_active`   | boolean       | No       |


**Response `201`:** ReadingTimetable object

---

### PUT `/api/dashboard/timetable/{pk}/`

**Auth:** Bearer token required  
**Request body:** Any subset of ReadingTimetable fields (partial update)  
**Response `200`:** ReadingTimetable object  
**Response `404`:** `{ "error": "Not found." }`

---

### DELETE `/api/dashboard/timetable/{pk}/`

**Auth:** Bearer token required  
**Response `204`:** No content

---

### GET `/api/dashboard/todos/`

**Auth:** Bearer token required  
**Response `200`:** Array of **TodoItem**

---

### POST `/api/dashboard/todos/`

**Auth:** Bearer token required

**Request body**


| Field            | Type          | Required |
| ---------------- | ------------- | -------- |
| `title`          | string        | Yes      |
| `description`    | string        | No       |
| `scheduled_time` | string (time) | No       |
| `scheduled_date` | string (date) | Yes      |
| `is_completed`   | boolean       | No       |


**Response `201`:** TodoItem object

---

### PUT `/api/dashboard/todos/{pk}/`

**Auth:** Bearer token required  
Partial update of TodoItem fields  
**Response `200`:** TodoItem object

---

### DELETE `/api/dashboard/todos/{pk}/`

**Auth:** Bearer token required  
**Response `204`:** No content

---

### POST `/api/dashboard/todos/{pk}/complete/`

**Auth:** Bearer token required  
**Request body:** None

**Response `200`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |


---

## Groups (`/api/groups/`)

### GET `/api/groups/`

**Auth:** Bearer token required  
**Response `200`:** Array of **StudyGroup**

---

### POST `/api/groups/`

**Auth:** Bearer token required

**Request body**


| Field         | Type   | Required |
| ------------- | ------ | -------- |
| `name`        | string | Yes      |
| `description` | string | No       |


**Response `201`:** StudyGroup object (creator added as `admin` member)

---

### GET `/api/groups/{pk}/`

**Auth:** Bearer token required  
**Response `200`:** StudyGroup object  
**Response `404`:** `{ "error": "Group not found." }`

---

### POST `/api/groups/{pk}/join/`

**Auth:** Bearer token required  
**Request body:** None

**Response `201`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |


**Response `200`:** `{ "message": "Already a member." }`

---

### POST `/api/groups/{pk}/leave/`

**Auth:** Bearer token required  
**Request body:** None

**Response `200`**


| Field     | Type   |
| --------- | ------ |
| `message` | string |


---

### GET `/api/groups/{pk}/members-progress/`

**Auth:** Bearer token required

**Response `200`:** Array of:


| Field                                | Type                                            |
| ------------------------------------ | ----------------------------------------------- |
| `student.id`                         | integer                                         |
| `student.full_name`                  | string                                          |
| `student.email`                      | string (email)                                  |
| `role`                               | string                                          |
| `pdf_stats.total_pdfs_read`          | integer                                         |
| `pdf_stats.total_time_spent_minutes` | integer                                         |
| `recent_cbt_scores`                  | array of `{ "exam": string, "score": integer }` |


---

## Payments (`/api/payments/`)

### POST `/api/payments/checkout/`

**Auth:** Bearer token required

**Request body**


| Field       | Type    | Required |
| ----------- | ------- | -------- |
| `course_id` | integer | Yes      |


**Response `200`**


| Field          | Type             |
| -------------- | ---------------- |
| `message`      | string           |
| `checkout_url` | string (uri)     |
| `reference`    | string           |
| `amount`       | string (decimal) |


**Response `400`:** Already enrolled — `{ "message": "Already enrolled" }`  
**Response `404`:** `{ "error": "Course not found" }`

---

### POST `/api/payments/webhook/paystack/`

**Auth:** Public (Paystack signature required)

**Headers**


| Header                 | Required |
| ---------------------- | -------- |
| `x-paystack-signature` | Yes      |


**Request body:** Raw Paystack webhook JSON payload

**Response `200`**


| Field    | Type   |
| -------- | ------ |
| `status` | string |


On `charge.success`, enrolls the user in the course.

---

### GET `/api/payments/history/`

**Auth:** Bearer token required  
**Response `200`:** Array of **Transaction**

---

## Placeholder Modules

These modules are routed but only expose a discovery endpoint for now.

### GET `/api/notifications/`

**Auth:** Public


| Field       | Type   |
| ----------- | ------ |
| `name`      | string |
| `status`    | string |
| `endpoints` | object |


Same response shape for:

- `GET /api/certificates/`
- `GET /api/analytics/`
- `GET /api/announcements/`
- `GET /api/support/`

---

## HTTP Status Code Summary


| Code  | Meaning                                   |
| ----- | ----------------------------------------- |
| `200` | Success                                   |
| `201` | Created                                   |
| `204` | Deleted (no content)                      |
| `400` | Bad request / validation error            |
| `401` | Unauthorized                              |
| `402` | Payment required (paid course enrollment) |
| `403` | Forbidden                                 |
| `404` | Not found                                 |


---

## JWT Token Lifetimes


| Token   | Lifetime |
| ------- | -------- |
| Access  | 1 day    |
| Refresh | 7 days   |



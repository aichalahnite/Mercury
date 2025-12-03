# Mercury Backend

**Documentation Version:** 2025-12-03
**Project:** Mercury Email Scanner Backend

---

## Overview

The Mercury Backend is a **Django 5.2-based REST API service** responsible for:

* Managing users and authentication
* Receiving emails and scanning their content
* Storing scan logs
* Exposing mock services for email sending and AI scanning

> **Purpose:** This backend provides a **contract for frontend and other services** to interact with email scanning functionality, regardless of whether the real mail server or AI scanner exists. Mock services are used for development and testing.

---

## Architecture & Flow

```
   +----------------+          +----------------+
   |                |          |                |
   |  Frontend /    |  POST    |  Backend API   |
   |  Other Service |--------->|  (Django REST) |
   |                |          |                |
   +----------------+          +----------------+
                                      |
                                      | Calls
                                      v
                          +----------------------+
                          | Email / Scan Service |
                          |  - Mock or Real     |
                          +----------------------+
                                      |
                                      v
                               +------------+
                               |  Database  |
                               | (Postgres) |
                               +------------+
```

1. The **frontend or another service** sends email content to the backend API.
2. The backend decides whether to use **mock services** or **real services** based on the `USE_REAL_SERVICES` environment variable.
3. The **scan result** is stored in the database (`ScanLog`) and returned to the caller.
4. Users can fetch **recent scan logs**, restricted by authentication.

---

## Users & Authentication

* **Custom User Model** (`users.User`) with roles:

  * `admin`
  * `user`
* **Authentication:** JWT (JSON Web Token)
* **Endpoints for users:**

  * `POST /auth/token/` – obtain JWT
  * `POST /auth/token/refresh/` – refresh JWT
  * `GET /users/me/` – get current user details

> Only authenticated users can see scan logs and send mock emails.

---

## API Endpoints & Data Contracts

### 1. Email Scanning

**Endpoint:** `POST /scanner/scan/`
**Authentication:** Required

**Request Body:**

```json
{
  "from": "user@example.com",
  "subject": "Test email",
  "body": "This is a test email content"
}
```

**Response:**

```json
{
  "id": 123,
  "result": "malicious",          // "safe" or "malicious"
  "confidence": 0.87,             // float between 0 and 1
  "used": "mock"                  // "mock" or "real"
}
```

**Notes:**

* The backend will **automatically choose mock or real scanning**.
* Logs are saved in `ScanLog`.

---

### 2. Scan Logs

**Endpoint:** `GET /scanner/logs/`
**Authentication:** Required

**Response:**

```json
[
  {
    "id": 123,
    "sender": "user@example.com",
    "subject": "Test email",
    "result": "malicious",
    "confidence": 0.87,
    "scanned_at": "2025-12-03T12:34:56Z"
  },
  ...
]
```

**Notes:**

* Currently **all authenticated users** can see logs.
* In the future, logs can be **filtered per user** by sender or user email.

---

### 3. Mock Email Sending (Development Only)

**Endpoint:** `POST /emails/mock/send/`
**Authentication:** Required

**Request Body:**

```json
{
  "to": "recipient@example.com",
  "subject": "Hello",
  "body": "This is a mock email"
}
```

**Response:**

```json
{
  "id": 4567,
  "to": "recipient@example.com",
  "subject": "Hello",
  "status": "sent_mock"
}
```

---

### 4. Mock Email Scanning (Development Only)

**Endpoint:** `POST /emails/mock/scan/`
**Authentication:** Required

**Request Body:**

```json
{
  "content": "This is the content of the email"
}
```

**Response:**

```json
{
  "scan_id": 7890,
  "malicious": false,
  "confidence": 0.42
}
```

---

## Interacting With the Backend

1. **Authenticate** using JWT:

   ```bash
   POST /auth/token/ { "username": "admin", "password": "adminpass" }
   ```

   → receive `access` token

2. **Include JWT** in the `Authorization` header for all requests:

   ```
   Authorization: Bearer <access_token>
   ```

3. **Send email content for scanning:**

   ```bash
   POST /scanner/scan/
   {
     "from": "user@example.com",
     "subject": "Hello",
     "body": "This is a test email"
   }
   ```

4. **Retrieve logs:**

   ```bash
   GET /scanner/logs/
   ```

---

## Notes for Colleagues

* **Data Contracts** are clearly defined in the endpoints above — this is what the frontend and other services should expect.
* Mock services **do not run continuously** yet; results are generated per request.
* Environment variable `USE_REAL_SERVICES=false` ensures development uses mock services only.
* Any changes to the mock contract (field names, types) must be updated in this documentation.

---

## Getting Started

### Docker Compose

```bash
docker-compose up --build
```

* Backend available at `http://localhost:8000/`
* PostgreSQL at `localhost:5432`

> Superuser created automatically: `admin / adminpass`

---

## Versioning & Documentation Date

* Version: 1.0
* Documentation Date: 2025-12-03


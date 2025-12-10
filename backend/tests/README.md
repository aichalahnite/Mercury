# Backend Tests Documentation

This directory contains comprehensive test suites for the Mercury backend application. Tests are organized by functionality and cover authentication, email services, middleware, routing, and AI scanning features.

## Test Structure

### Test Files Overview

#### `test_emails.py`
Tests for the email service API endpoints.

**Tests:**
- `test_mock_send_email()` - Verifies mock email sending functionality
  - Creates authenticated client
  - Sends email payload with `to`, `subject`, and `body`
  - Validates response status (200) and mock send confirmation

**Requirements:**
- Authenticated user (JWT token)
- Email service mock endpoint (`/emails/mock/send/`)

---

#### `test_middleware.py`
Tests for custom middleware components that handle request/response processing.

**Tests:**
- `test_security_gateway_adds_trace_id()` - Validates SecurityGatewayMiddleware
  - Ensures each request gets a unique trace ID
  - Verifies trace ID is a valid UUID format
  
- `test_router_sets_service_route()` - Validates IntelligentServiceRouterMiddleware
  - Confirms service routing decision is set on requests
  - Verifies service route contains "scanner" key
  - Checks route value is either "mock" or "real"
  
- `test_response_logger_injects_trace()` - Validates ResponseLoggingMiddleware
  - Confirms trace ID is injected into response JSON
  - Tests with anonymous users

**Key Middleware:**
- **SecurityGatewayMiddleware** - Adds request tracing
- **IntelligentServiceRouterMiddleware** - Routes requests to mock/real services
- **ResponseLoggingMiddleware** - Logs responses with trace ID

---

#### `test_routing.py`
Tests for the intelligent service router's configuration handling.

**Tests:**
- `test_router_mock_mode()` - Validates mock service mode
  - Sets `USE_REAL_SERVICES=false`
  - Verifies scanner routes to "mock" service
  - Uses module reload to apply environment changes
  
- `test_router_real_mode()` - Validates real service mode
  - Sets `USE_REAL_SERVICES=true`
  - Verifies scanner routes to "real" service
  - Demonstrates environment-based routing

**Environment Variables:**
- `USE_REAL_SERVICES` - Controls routing behavior
  - `"true"` or `"auto"` - Routes to real services (mailserver, AI scanner)
  - `"false"` - Routes to mock services

---

#### `test_scanner.py`
Tests for the AI scanner API endpoints.

**Tests:**
- `test_scan_creates_log()` - Validates scanning functionality
  - Creates authenticated client
  - Sends scan request with `from`, `subject`, and `body`
  - Verifies response status (200)
  - Confirms ScanLog record is created in database
  - Validates response contains "result" field
  
- `test_logs_list()` - Validates log retrieval endpoint
  - Creates multiple scan logs
  - Fetches logs via `/scanner/logs/` endpoint
  - Verifies status (200) and log list is populated

**Requirements:**
- Authenticated user (JWT token)
- Scanner endpoints (`/scanner/scan/`, `/scanner/logs/`)

---

#### `test_users.py`
Tests for user authentication and profile endpoints.

**Tests:**
- `test_user_me()` - Validates user profile endpoint
  - Creates test user with credentials
  - Authenticates via token endpoint (`/auth/token/`)
  - Fetches user profile via `/users/me/` with JWT token
  - Verifies response contains correct username

**Key Endpoints:**
- `POST /auth/token/` - Obtain JWT access token
- `GET /users/me/` - Retrieve current user profile

---

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_emails.py
```

### Run Specific Test Function
```bash
pytest tests/test_scanner.py::test_scan_creates_log
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage Report
```bash
pytest --cov=.
```

### Run with Django Database
```bash
pytest --ds=backend.settings
```

## Test Configuration

Tests use the following tools and frameworks:

- **pytest** - Test runner and framework
- **pytest-django** - Django integration for pytest
- **pytest-cov** - Coverage reporting
- **Django REST Framework TestClient** - API testing
- **Django RequestFactory** - Middleware testing
- **monkeypatch** - Environment variable mocking

### pytest.ini Configuration
The project includes `pytest.ini` configuration for:
- Django settings module configuration
- Test discovery patterns
- Coverage settings
- Output formatting

## Authentication Flow

Most tests use JWT token-based authentication:

1. Create a test user with `User.objects.create_user()`
2. Authenticate via `POST /auth/token/` with username/password
3. Extract `access` token from response
4. Add token to client headers: `HTTP_AUTHORIZATION="Bearer {token}"`
5. Make authenticated API requests

Example:
```python
user = User.objects.create_user("testuser", "test@example.com", "password")
response = client.post("/auth/token/", {
    "username": "testuser", 
    "password": "password"
})
token = response.data["access"]
client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
```

## Database Testing

Tests marked with `@pytest.mark.django_db` decorator:
- Have access to the test database
- Can create model instances
- Are automatically rolled back after execution

Example:
```python
@pytest.mark.django_db
def test_example():
    user = User.objects.create_user("test", "test@example.com", "pass")
    assert User.objects.count() == 1
```

## Environment Variables

The test suite respects these environment variables:

| Variable | Values | Purpose |
|----------|--------|---------|
| `USE_REAL_SERVICES` | `true`, `false`, `auto` | Determines service routing (real vs mock) |
| `DJANGO_SECRET_KEY` | string | Django security key |
| `POSTGRES_HOST` | hostname | Database host |
| `POSTGRES_PORT` | port number | Database port |

See `.env` file for default values.

## Service Integration

### Mock Services
- **Email Service** - Returns mocked success response
- **AI Scanner** - Returns mocked scan results

### Real Services
- **Mailserver** - Actual mail sending via external service
- **AI Scanner** - Real AI scanning via external service

The middleware intelligently routes requests based on `USE_REAL_SERVICES` setting.

## Best Practices

1. **Use `@pytest.mark.django_db`** - Required for database access
2. **Authenticate properly** - Follow token-based auth pattern
3. **Clean assertions** - Use clear, specific assertions
4. **Test isolation** - Each test should be independent
5. **Mock environment** - Use monkeypatch for env vars
6. **Descriptive names** - Test names should describe what they test

## Troubleshooting

### "django.db.ProgrammingError" during tests
- Ensure `@pytest.mark.django_db` decorator is present
- Run migrations: `python manage.py migrate --run-syncdb`

### Tests fail with authentication errors
- Verify token endpoint is accessible
- Check user creation is successful
- Ensure JWT credentials are properly formatted

### Service routing tests fail
- Use `importlib.reload()` after monkeypatching env vars
- Verify environment variables are set before middleware initialization

## Related Documentation

- [Backend README](../README.md) - General backend setup
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [DRF Testing Documentation](https://www.django-rest-framework.org/api-guide/testing/)

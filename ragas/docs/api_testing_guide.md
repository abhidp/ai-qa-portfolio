# API Testing Guide

## REST API Testing Fundamentals

API testing validates that application programming interfaces work correctly, reliably, and securely. Unlike UI testing, API tests interact directly with the backend services, making them faster and more stable.

## HTTP Methods and Status Codes

### Common HTTP Methods
- GET: Retrieve a resource. Should be idempotent and safe (no side effects).
- POST: Create a new resource. Returns 201 Created on success with a Location header.
- PUT: Replace an entire resource. Returns 200 OK or 204 No Content.
- PATCH: Partially update a resource. Only send the fields that need changing.
- DELETE: Remove a resource. Returns 204 No Content on success.

### Status Code Categories
- 2xx Success: 200 OK, 201 Created, 204 No Content
- 3xx Redirection: 301 Moved Permanently, 304 Not Modified
- 4xx Client Errors: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests
- 5xx Server Errors: 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable

## Contract Testing

Contract testing verifies that APIs conform to their documented specification (OpenAPI/Swagger). This prevents breaking changes from reaching production. Tools like Pact enable consumer-driven contract testing where the API consumer defines the expected contract and the provider verifies it.

## Authentication Testing

Test all authentication flows:
- Valid credentials return a token/session
- Invalid credentials return 401
- Expired tokens are rejected
- Token refresh works correctly
- Rate limiting kicks in after too many failed attempts

For OAuth 2.0 flows, test the authorization code flow, token exchange, and refresh token rotation.

## Error Handling Validation

Every API should return consistent error responses. Validate that:
- Error responses include a meaningful error code and message
- Sensitive information is never leaked in error messages (no stack traces in production)
- The API returns appropriate status codes (not 200 OK with an error body)
- Validation errors list all invalid fields, not just the first one

## Load Testing APIs

Use K6 or similar tools to test API performance under load. Define virtual user scenarios that simulate real usage patterns. Key thresholds to set:
- P95 response time under 500ms for read operations
- P95 response time under 1000ms for write operations
- Error rate under 1%
- Throughput meets expected concurrent user count

## API Test Automation Structure

Organize API tests by resource and operation:
- tests/api/users/test_create_user.py
- tests/api/users/test_get_user.py
- tests/api/orders/test_create_order.py

Use a base client class that handles authentication, headers, and base URL configuration. This keeps individual test files focused on the specific endpoint behavior being validated.

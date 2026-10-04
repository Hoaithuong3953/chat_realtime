# URLs
REGISTER_URL = "/api/v1/auth/register"

# Account test data
TEST_EMAIL = "test@example.com"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "Password123!"
TEST_FULL_NAME = "Test User"

EXISTING_EMAIL = "existing@example.com"
EXISTING_USERNAME = "existinguser"

NEW_EMAIL = "new@example.com"
NEW_USERNAME = "newuser"

INVALID_EMAIL = "invalid-email"

# Error codes
EMAIL_ALREADY_EXISTS_ERROR_CODE = "EMAIL_ALREADY_EXISTS"
USERNAME_ALREADY_EXISTS_ERROR_CODE = "USERNAME_ALREADY_EXISTS"

# Integrity error messages
ACCOUNT_EMAIL_UNIQUE_CONSTRAINT = (
    'duplicate key value violates unique constraint "accounts_email_key"'
)
ACCOUNT_USERNAME_UNIQUE_CONSTRAINT = (
    'duplicate key value violates unique constraint "accounts_username_key"'
)
UNEXPECTED_INTEGRITY_ERROR_MESSAGE = (
    'duplicate key value violates unique constraint "some_other_constraint"'
)
USER_CREATION_INTEGRITY_ERROR_MESSAGE = (
    "unexpected user constraint violation"
)

# HTTP status
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_CONFLICT = 409
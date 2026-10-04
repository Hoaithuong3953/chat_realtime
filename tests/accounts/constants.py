# URLs
REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
LOGOUT_URL = "/api/v1/auth/logout"

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

# Login test data
INVALID_IDENTIFIER = "notfound@example.com"
WRONG_PASSWORD = "WrongPassword!"
SHORT_IDENTIFIER = "ab"
SHORT_PASSWORD = "123"

# Refresh token test data
INVALID_REFRESH_TOKEN = "invalid-refresh-token"
REFRESH_TOKEN_EXPIRES_DAYS = 7
OLD_REFRESH_TOKEN = "old-refresh-token"
VALID_REFRESH_TOKEN = "valid-refresh-token"

# Response keys
ACCESS_TOKEN_KEY = "access_token"
EXPIRES_IN_KEY = "expires_in"

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
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_OK = 200

# Cookie
REFRESH_COOKIE_PATH = "/api/v1/auth"
REFRESH_COOKIE_MAX_AGE_DELETED = "0"
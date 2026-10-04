# URLs
REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
LOGOUT_URL = "/api/v1/auth/logout"
REFRESH_URL = "/api/v1/auth/refresh"
ME_URL = "/api/v1/auth/me"
ACCOUNTS_URL = "/api/v1/accounts/"

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
NON_EXISTENT_ACCOUNT_ID = "00000000-0000-0000-0000-000000000000"

# Get all accounts test data
ACCOUNT_1_EMAIL = "john.doe@example.com"
ACCOUNT_1_USERNAME = "john123"
ACCOUNT_1_FULL_NAME = "Jonathan Doe"

ACCOUNT_2_EMAIL = "jane@example.com"
ACCOUNT_2_USERNAME = "jane123"
ACCOUNT_2_FULL_NAME = "Jane Doe"

ACCOUNT_3_EMAIL = "john3@example.com"
ACCOUNT_3_USERNAME = "john789"
ACCOUNT_3_FULL_NAME = "John Brown"

ACCOUNT_AVATAR_URL = "https://example.com/avatar1.jpg"

SEARCH_JOHN = "john"
SEARCH_JONATHAN = "jonathan"
SEARCH_SUPER = "SUPER"
SEARCH_PARTIAL_EMAIL = "ohn.do"
SEARCH_NOT_FOUND = "not-found"

PAGINATION_PAGE = 1
PAGINATION_PAGE_SIZE = 20
PAGINATION_TEST_PAGE = 2
PAGINATION_TEST_PAGE_SIZE = 2
PAGINATION_TOTAL_ITEMS = 5
PAGINATION_TOTAL_PAGES = 3

# Account view test data
ADMIN_EMAIL = "admin@example.com"
ADMIN_USERNAME = "admin"
ADMIN_FULL_NAME = "Admin User"

INACTIVE_EMAIL = "inactive@example.com"
INACTIVE_USERNAME = "inactive"
INACTIVE_FULL_NAME = "Inactive User"

INVALID_VALUE = "invalid"
MIN_INVALID_PAGE = 0
MAX_INVALID_PAGE_SIZE = 101

# Login test data
INVALID_IDENTIFIER = "notfound@example.com"
WRONG_PASSWORD = "WrongPassword!"
SHORT_IDENTIFIER = "ab"
SHORT_PASSWORD = "123"

# Refresh token test data
INVALID_REFRESH_TOKEN = "invalid-refresh-token"
REVOKED_REFRESH_TOKEN = "revoked-refresh-token"
EXPIRED_REFRESH_TOKEN = "expired-refresh-token"
REFRESH_TOKEN_EXPIRES_DAYS = 7
REFRESH_TOKEN_EXPIRED_SECONDS = 1
OLD_REFRESH_TOKEN = "old-refresh-token"
VALID_REFRESH_TOKEN = "valid-refresh-token"

# Me test data
INVALID_ACCESS_TOKEN = "invalid-token"
UPDATED_USERNAME = "updateduser"

# Auth
AUTHORIZATION_TYPE = "Bearer"

# Response keys
ACCESS_TOKEN_KEY = "access_token"
EXPIRES_IN_KEY = "expires_in"
REFRESH_TOKEN_KEY = "refresh_token"

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
HTTP_NOT_FOUND = 404

# Cookie
REFRESH_COOKIE_PATH = "/api/v1/auth"
REFRESH_COOKIE_MAX_AGE_DELETED = "0"
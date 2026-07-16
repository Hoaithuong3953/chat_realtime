"""
Constants used by the auth module
"""

# Validation field account model constants
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 30
FULL_NAME_MIN_LENGTH = 2
FULL_NAME_MAX_LENGTH = 100
PASSWORD_MIN_LENGTH = 8
IDENTIFIER_MIN_LENGTH = 3

USERNAME_PATTERN = r"^[A-Za-z][A-Za-z0-9._-]*$"
PASSWORD_UPPERCASE_PATTERN = r"[A-Z]"
PASSWORD_LOWERCASE_PATTERN = r"[a-z]"
PASSWORD_DIGIT_PATTERN = r"\d"
PASSWORD_SPECIAL_PATTERN = r"[!@#$%^&*()_\-+=\[{\]};:'\",.<>/?\\|`~]"
"""
Constants used by the users module
"""

# Validation field account model constants
FULL_NAME_MIN_LENGTH = 2
FULL_NAME_MAX_LENGTH = 100
AVATAR_URL_MAX_LENGTH = 500
PHONE_NUMBER_MAX_LENGTH = 20
ADDRESS_MAX_LENGTH = 255
BIO_MAX_LENGTH = 1000

PHONE_NUMBER_PATTERN = r"^(0|\+84)[3-9]\d{8}$"
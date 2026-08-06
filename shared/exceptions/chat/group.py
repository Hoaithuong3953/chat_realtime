from uuid import UUID
from shared.exceptions.base.common import ConflictException, ForbiddenException, NotFoundException

class GroupNotFoundException(NotFoundException):
    """
    Exception raised when group chat not found
    HTTP status code: 404 Not Found
    """
    error_code = "GROUP_NOT_FOUND"
    message = "Group chat not found."

class NotGroupOwnerException(ForbiddenException):
    """
    Exception raised when the user is not the owner of the group
    HTTP status code: 403 Forbidden
    """
    error_code = "NOT_GROUP_OWNER"
    message = "Only the group owner can perform this action."

class OwnerRequiredException(ConflictException):
    """
    Exception raised when remove the last owner from the group
    HTTP status code: 409 Conflict
    """
    error_code = "OWNER_REQUIRED"
    message = "Cannot remove the last owner from the group."

class OwnerMustTransferException(ConflictException):
    """
    Exception raised when member is the group owner and wants to leave group
    HTTP status code: 409 Conflict
    """
    error_code = "OWNER_MUST_TRANSFER"
    message = "The group owner must transfer ownership before leaving the group."

class InvalidMemberException(NotFoundException):
    """
    Exception raised when member is invalid
    HTTP status code: 404 Not Found
    """
    error_code = "INVALID_MEMBERS"
    
    def __init__(self, member_ids: list[UUID], message: str):
        super().__init__(
            message=message,
            details={
                "member_ids": member_ids,
            }
        )

class MemberAlreadyExistsException(ConflictException):
    """
    Exception raised when the user already exists in the group
    HTTP status code: 409 Conflict
    """
    error_code = "MEMBER_ALREADY_EXISTS"
    message = "One or more users are already group members."

    def __init__(self, *, member_ids: list[UUID]):
        super().__init__(
            details={
                "member_ids": member_ids,
            }
        )

class MemberNotFoundException(NotFoundException):
    """
    Exception raised when cannot find the member in the group
    HTTP status code: 404 Not Found
    """
    error_code = "MEMBER_NOT_FOUND"
    message = "Member does not exist in group."

class MemberAlreadyOwnerException(ConflictException):
    """
    Exception raised when member is already the group owner
    HTTP status code: 409 Conflict
    """
    error_code = "MEMBER_ALREADY_OWNER"
    message = "Member is already the group owner."
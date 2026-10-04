from uuid import UUID
from django.core.paginator import Paginator

from apps.accounts.dtos import (
    GetAccountResponse,
    GetAccountsRequest,
    AccountItemResponse,
    GetAccountsResponse,
    UpdateAccountResponse,
)
from apps.accounts.models import Account
from shared.exceptions.auth.account import AccountNotFoundException
from shared.pagination_dto import PaginationResponse

class AccountService:
    """Service for managing user accounts"""

    @staticmethod
    def get_all(dto: GetAccountsRequest) -> GetAccountsResponse:
        """
        Get a paginated list of accounts

        Args:
            dto: Search and pagination parameters

        Returns:
            A paginated list of accounts
        """
        queryset = Account.objects.search_accounts(
            q=dto.q,
            role=dto.role,
            is_active=dto.is_active,
        )

        paginator = Paginator(
            queryset,
            dto.page_size,
        )

        page = paginator.get_page(dto.page)

        return GetAccountsResponse(
            items=[
                AccountItemResponse(
                    id=account.id,
                    email=account.email,
                    username=account.username,
                    role=account.role,
                    is_active=account.is_active,
                    full_name=account.user_profile.full_name,
                    avatar_url=account.user_profile.avatar_url,
                )
                for account in page.object_list
            ],
            pagination=PaginationResponse(
                page=page.number,
                page_size=dto.page_size,
                total_items=paginator.count,
                total_pages=paginator.num_pages,
            ),
        )

    @staticmethod
    def get_account(account_id: UUID) -> GetAccountResponse:
        """
        Get account information by ID

        Args:
            account_id: The account ID

        Returns:
            The account information

        Raises:
            AccountNotFoundException: If the account does not exist
        """
        account = Account.objects.get_by_id_with_profile(account_id=account_id)

        if not account:
            raise AccountNotFoundException()

        return GetAccountResponse(
            id=account.id,
            email=account.email,
            username=account.username,
            role=account.role,
            is_active=account.is_active,
            full_name=account.user_profile.full_name,
            avatar_url=account.user_profile.avatar_url,
            created_at=account.created_at,
            updated_at=account.updated_at,
        )

    @staticmethod
    def update_account(account_id: UUID, is_active: bool) -> UpdateAccountResponse:
        """
        Update an account's active status

        Args:
            account_id: The account ID
            is_active: The new active status

        Returns:
            The updated account status

        Raises:
            AccountNotFoundException: If the account does not exist
        """
        account = Account.objects.update_status(
            account_id=account_id,
            is_active=is_active,
        )

        if not account:
            raise AccountNotFoundException()

        return UpdateAccountResponse(
            id=account.id,
            is_active=account.is_active,
        )
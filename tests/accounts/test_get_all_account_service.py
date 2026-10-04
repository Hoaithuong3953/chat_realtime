import pytest

from apps.accounts.dtos import GetAccountsRequest
from apps.accounts.enums import Role
from apps.accounts.services import AccountService

from .constants import (
    ACCOUNT_1_EMAIL,
    ACCOUNT_1_FULL_NAME,
    ACCOUNT_1_USERNAME,
    ACCOUNT_2_EMAIL,
    ACCOUNT_2_FULL_NAME,
    ACCOUNT_2_USERNAME,
    ACCOUNT_3_EMAIL,
    ACCOUNT_3_FULL_NAME,
    ACCOUNT_3_USERNAME,
    ACCOUNT_AVATAR_URL,
    PAGINATION_PAGE,
    PAGINATION_PAGE_SIZE,
    PAGINATION_TEST_PAGE,
    PAGINATION_TEST_PAGE_SIZE,
    PAGINATION_TOTAL_ITEMS,
    PAGINATION_TOTAL_PAGES,
    SEARCH_JOHN,
    SEARCH_JONATHAN,
    SEARCH_NOT_FOUND,
    SEARCH_PARTIAL_EMAIL,
    SEARCH_SUPER,
)


@pytest.mark.django_db
class TestGetAllAccountService:
    def test_get_all_returns_accounts_ordered_by_created_at_desc(
        self,
        account_factory,
    ):
        account_1 = account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            full_name=ACCOUNT_1_FULL_NAME,
            avatar_url=ACCOUNT_AVATAR_URL,
        )
        account_2 = account_factory(
            email=ACCOUNT_2_EMAIL,
            username=ACCOUNT_2_USERNAME,
            role=Role.ADMIN,
            full_name=ACCOUNT_2_FULL_NAME,
        )

        result = AccountService.get_all(
            GetAccountsRequest(
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert len(result.items) == 2

        assert result.items[0].id == account_2.id
        assert result.items[0].email == account_2.email
        assert result.items[0].username == account_2.username
        assert result.items[0].role == account_2.role
        assert result.items[0].is_active is True
        assert result.items[0].full_name == account_2.user.full_name
        assert result.items[0].avatar_url is None

        assert result.items[1].id == account_1.id
        assert result.items[1].email == account_1.email
        assert result.items[1].username == account_1.username
        assert result.items[1].role == account_1.role
        assert result.items[1].is_active is True
        assert result.items[1].full_name == account_1.user.full_name
        assert result.items[1].avatar_url == ACCOUNT_AVATAR_URL

        assert result.pagination.page == PAGINATION_PAGE
        assert result.pagination.page_size == PAGINATION_PAGE_SIZE
        assert result.pagination.total_items == 2
        assert result.pagination.total_pages == 1

    def test_get_all_searches_by_email(self, account_factory):
        account = account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
        )
        account_factory(
            email=ACCOUNT_2_EMAIL,
            username=ACCOUNT_2_USERNAME,
            full_name=ACCOUNT_2_FULL_NAME,
        )

        result = AccountService.get_all(
            GetAccountsRequest(
                q=ACCOUNT_1_EMAIL.upper(),
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert len(result.items) == 1
        assert result.items[0].id == account.id

    def test_get_all_searches_by_username(self, account_factory):
        account = account_factory(
            email=ACCOUNT_1_EMAIL,
            username="john_superuser",
        )
        account_factory(
            email=ACCOUNT_2_EMAIL,
            username=ACCOUNT_2_USERNAME,
        )

        result = AccountService.get_all(
            GetAccountsRequest(
                q=SEARCH_SUPER,
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert len(result.items) == 1
        assert result.items[0].id == account.id

    def test_get_all_searches_by_full_name(self, account_factory):
        account = account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            full_name=ACCOUNT_1_FULL_NAME,
        )
        account_factory(
            email=ACCOUNT_2_EMAIL,
            username=ACCOUNT_2_USERNAME,
            full_name=ACCOUNT_2_FULL_NAME,
        )

        result = AccountService.get_all(
            GetAccountsRequest(
                q=SEARCH_JONATHAN,
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert len(result.items) == 1
        assert result.items[0].id == account.id

    def test_get_all_search_is_case_insensitive(self, account_factory):
        account = account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            full_name=ACCOUNT_1_FULL_NAME,
        )

        result = AccountService.get_all(
            GetAccountsRequest(
                q=SEARCH_JOHN.upper(),
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert len(result.items) == 1
        assert result.items[0].id == account.id

    def test_get_all_search_matches_partial_value(self, account_factory):
        account = account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            full_name=ACCOUNT_1_FULL_NAME,
        )

        result = AccountService.get_all(
            GetAccountsRequest(
                q=SEARCH_PARTIAL_EMAIL,
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert len(result.items) == 1
        assert result.items[0].id == account.id

    def test_get_all_filters_by_role(self, account_factory):
        account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            role=Role.USER,
        )
        account = account_factory(
            email=ACCOUNT_2_EMAIL,
            username=ACCOUNT_2_USERNAME,
            role=Role.ADMIN,
        )

        result = AccountService.get_all(
            GetAccountsRequest(
                role=Role.ADMIN,
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert len(result.items) == 1
        assert result.items[0].id == account.id
        assert result.items[0].role == Role.ADMIN

    def test_get_all_filters_by_active_status(self, account_factory):
        account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            is_active=True,
        )
        account = account_factory(
            email=ACCOUNT_2_EMAIL,
            username=ACCOUNT_2_USERNAME,
            is_active=False,
        )

        result = AccountService.get_all(
            GetAccountsRequest(
                is_active=False,
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert len(result.items) == 1
        assert result.items[0].id == account.id
        assert result.items[0].is_active is False

    def test_get_all_filters_by_search_role_and_active_status(
        self,
        account_factory,
    ):
        account = account_factory(
            email=ACCOUNT_1_EMAIL,
            username=ACCOUNT_1_USERNAME,
            role=Role.ADMIN,
            is_active=True,
            full_name=ACCOUNT_1_FULL_NAME,
        )
        account_factory(
            email=ACCOUNT_2_EMAIL,
            username=ACCOUNT_2_USERNAME,
            role=Role.ADMIN,
            is_active=False,
            full_name="John Smith",
        )
        account_factory(
            email=ACCOUNT_3_EMAIL,
            username=ACCOUNT_3_USERNAME,
            role=Role.USER,
            is_active=True,
            full_name=ACCOUNT_3_FULL_NAME,
        )

        result = AccountService.get_all(
            GetAccountsRequest(
                q=SEARCH_JOHN,
                role=Role.ADMIN,
                is_active=True,
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert len(result.items) == 1
        assert result.items[0].id == account.id

    def test_get_all_returns_empty_list_when_no_account_matches(self):
        result = AccountService.get_all(
            GetAccountsRequest(
                q=SEARCH_NOT_FOUND,
                page=PAGINATION_PAGE,
                page_size=PAGINATION_PAGE_SIZE,
            )
        )

        assert result.items == []
        assert result.pagination.page == PAGINATION_PAGE
        assert result.pagination.page_size == PAGINATION_PAGE_SIZE
        assert result.pagination.total_items == 0
        assert result.pagination.total_pages == 1

    def test_get_all_paginates_accounts(self, account_factory):
        accounts = [
            account_factory(
                email=f"user{i}@example.com",
                username=f"user{i}",
                full_name=f"User {i}",
            )
            for i in range(PAGINATION_TOTAL_ITEMS)
        ]

        result = AccountService.get_all(
            GetAccountsRequest(
                page=PAGINATION_TEST_PAGE,
                page_size=PAGINATION_TEST_PAGE_SIZE,
            )
        )

        assert len(result.items) == 2
        assert result.pagination.page == PAGINATION_TEST_PAGE
        assert result.pagination.page_size == PAGINATION_TEST_PAGE_SIZE
        assert result.pagination.total_items == PAGINATION_TOTAL_ITEMS
        assert result.pagination.total_pages == PAGINATION_TOTAL_PAGES
        assert result.items[0].id == accounts[2].id
        assert result.items[1].id == accounts[1].id

    def test_get_all_returns_last_page_with_remaining_accounts(
        self,
        account_factory,
    ):
        accounts = [
            account_factory(
                email=f"user{i}@example.com",
                username=f"user{i}",
                full_name=f"User {i}",
            )
            for i in range(PAGINATION_TOTAL_ITEMS)
        ]

        result = AccountService.get_all(
            GetAccountsRequest(
                page=PAGINATION_TOTAL_PAGES,
                page_size=PAGINATION_TEST_PAGE_SIZE,
            )
        )

        assert len(result.items) == 1
        assert result.items[0].id == accounts[0].id
        assert result.pagination.page == PAGINATION_TOTAL_PAGES
        assert result.pagination.page_size == PAGINATION_TEST_PAGE_SIZE
        assert result.pagination.total_items == PAGINATION_TOTAL_ITEMS
        assert result.pagination.total_pages == PAGINATION_TOTAL_PAGES
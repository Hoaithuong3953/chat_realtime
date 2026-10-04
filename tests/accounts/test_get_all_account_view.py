import pytest
from rest_framework.test import APIClient

from apps.accounts.enums import Role
from apps.accounts.models import Account
from apps.users.models import User

@pytest.mark.django_db
class TestGetAllAccountView:
    def test_get_all_accounts_success_for_admin(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        user_account = Account.objects.create(
            email="user@example.com",
            username="user",
            role=Role.USER,
            is_active=True,
        )
        User.objects.create(
            account=user_account,
            full_name="Test User",
            avatar_url="https://example.com/avatar.jpg",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get("/api/v1/accounts/")

        assert response.status_code == 200

        data = response.json()

        assert data["message"] == "Get accounts successfully."
        assert len(data["data"]["items"]) == 2

        # Account.objects.search_accounts() orders by -created_at,
        # so the second-created account appears first.
        assert data["data"]["items"][0]["id"] == str(user_account.id)
        assert data["data"]["items"][0]["email"] == "user@example.com"
        assert data["data"]["items"][0]["username"] == "user"
        assert data["data"]["items"][0]["role"] == Role.USER
        assert data["data"]["items"][0]["is_active"] is True
        assert data["data"]["items"][0]["full_name"] == "Test User"
        assert data["data"]["items"][0]["avatar_url"] == (
            "https://example.com/avatar.jpg"
        )

        assert data["data"]["items"][1]["id"] == str(admin_account.id)
        assert data["data"]["items"][1]["email"] == "admin@example.com"
        assert data["data"]["items"][1]["username"] == "admin"
        assert data["data"]["items"][1]["role"] == Role.ADMIN
        assert data["data"]["items"][1]["is_active"] is True
        assert data["data"]["items"][1]["full_name"] == "Admin User"
        assert data["data"]["items"][1]["avatar_url"] is None

        assert data["data"]["pagination"]["page"] == 1
        assert data["data"]["pagination"]["page_size"] == 20
        assert data["data"]["pagination"]["total_items"] == 2
        assert data["data"]["pagination"]["total_pages"] == 1

    def test_get_all_accounts_unauthorized_without_authentication(self):
        client = APIClient()

        response = client.get("/api/v1/accounts/")

        assert response.status_code == 401

    def test_get_all_accounts_forbidden_for_non_admin(self):
        account = Account.objects.create(
            email="user@example.com",
            username="user",
            role=Role.USER,
            is_active=True,
        )
        User.objects.create(
            account=account,
            full_name="Normal User",
        )

        client = APIClient()
        client.force_authenticate(user=account)

        response = client.get("/api/v1/accounts/")

        assert response.status_code == 403

    def test_get_all_accounts_searches_by_email(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        account = Account.objects.create(
            email="john@example.com",
            username="john",
            role=Role.USER,
            is_active=True,
        )
        User.objects.create(
            account=account,
            full_name="John Doe",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"q": "john@example.com"},
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["id"] == str(account.id)

    def test_get_all_accounts_searches_by_username(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        account = Account.objects.create(
            email="john@example.com",
            username="johnny",
            role=Role.USER,
            is_active=True,
        )
        User.objects.create(
            account=account,
            full_name="John Doe",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"q": "johnny"},
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["id"] == str(account.id)

    def test_get_all_accounts_searches_by_full_name(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        account = Account.objects.create(
            email="john@example.com",
            username="john",
            role=Role.USER,
            is_active=True,
        )
        User.objects.create(
            account=account,
            full_name="John Doe",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"q": "John Doe"},
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["id"] == str(account.id)

    def test_get_all_accounts_filters_by_role(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        account = Account.objects.create(
            email="user@example.com",
            username="user",
            role=Role.USER,
            is_active=True,
        )
        User.objects.create(
            account=account,
            full_name="Normal User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"role": Role.USER},
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["id"] == str(account.id)
        assert data["data"]["items"][0]["role"] == Role.USER

    def test_get_all_accounts_filters_by_active_status(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        account = Account.objects.create(
            email="inactive@example.com",
            username="inactive",
            role=Role.USER,
            is_active=False,
        )
        User.objects.create(
            account=account,
            full_name="Inactive User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"is_active": "false"},
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["id"] == str(account.id)
        assert data["data"]["items"][0]["is_active"] is False

    def test_get_all_accounts_filters_by_multiple_parameters(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        account1 = Account.objects.create(
            email="john@example.com",
            username="john",
            role=Role.USER,
            is_active=True,
        )
        User.objects.create(
            account=account1,
            full_name="John Doe",
        )

        account2 = Account.objects.create(
            email="john2@example.com",
            username="john2",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=account2,
            full_name="John Admin",
        )

        account3 = Account.objects.create(
            email="jane@example.com",
            username="jane",
            role=Role.USER,
            is_active=False,
        )
        User.objects.create(
            account=account3,
            full_name="Jane User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {
                "q": "john",
                "role": Role.USER,
                "is_active": "true",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["id"] == str(account1.id)
        assert data["data"]["items"][0]["email"] == "john@example.com"
        assert data["data"]["items"][0]["username"] == "john"
        assert data["data"]["items"][0]["role"] == Role.USER
        assert data["data"]["items"][0]["is_active"] is True
        assert data["data"]["items"][0]["full_name"] == "John Doe"

    def test_get_all_accounts_returns_empty_items_when_no_account_matches(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"q": "not-found"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["data"]["items"] == []
        assert data["data"]["pagination"]["page"] == 1
        assert data["data"]["pagination"]["page_size"] == 20
        assert data["data"]["pagination"]["total_items"] == 0
        assert data["data"]["pagination"]["total_pages"] == 1

    def test_get_all_accounts_supports_pagination(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        for i in range(5):
            account = Account.objects.create(
                email=f"user{i}@example.com",
                username=f"user{i}",
                role=Role.USER,
                is_active=True,
            )
            User.objects.create(
                account=account,
                full_name=f"User {i}",
            )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {
                "page": 2,
                "page_size": 2,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data["data"]["items"]) == 2
        assert data["data"]["pagination"]["page"] == 2
        assert data["data"]["pagination"]["page_size"] == 2
        assert data["data"]["pagination"]["total_items"] == 6
        assert data["data"]["pagination"]["total_pages"] == 3

    def test_get_all_accounts_uses_default_page(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get("/api/v1/accounts/")

        assert response.status_code == 200

        data = response.json()

        assert data["data"]["pagination"]["page"] == 1

    def test_get_all_accounts_uses_default_page_size(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get("/api/v1/accounts/")

        assert response.status_code == 200

        data = response.json()

        assert data["data"]["pagination"]["page_size"] == 20

    def test_get_all_accounts_rejects_invalid_role(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"role": "invalid-role"},
        )

        assert response.status_code == 400

    def test_get_all_accounts_rejects_invalid_is_active(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"is_active": "invalid"},
        )

        assert response.status_code == 400

    def test_get_all_accounts_rejects_page_less_than_one(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"page": 0},
        )

        assert response.status_code == 400

    def test_get_all_accounts_rejects_invalid_page(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"page": "invalid"},
        )

        assert response.status_code == 400

    def test_get_all_accounts_rejects_page_size_less_than_one(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"page_size": 0},
        )

        assert response.status_code == 400

    def test_get_all_accounts_rejects_page_size_greater_than_one_hundred(self):
        admin_account = Account.objects.create(
            email="admin@example.com",
            username="admin",
            role=Role.ADMIN,
            is_active=True,
        )
        User.objects.create(
            account=admin_account,
            full_name="Admin User",
        )

        client = APIClient()
        client.force_authenticate(user=admin_account)

        response = client.get(
            "/api/v1/accounts/",
            {"page_size": 101},
        )

        assert response.status_code == 400
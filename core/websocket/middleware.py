from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

from apps.users.models import User

class TokenAuthMiddleware:
    """
    Authenticate websocket connections using JWT access token
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        token = self.get_token(scope)

        if token:
            scope["user"] = await self.get_user(token)
        else:
            scope["user"] = AnonymousUser()

        return await self.app(
            scope,
            receive,
            send,
        )

    def get_token(self, scope) -> str | None:
        """
        Get access token from websocket query string
        Example:
            ws://localhost:8000/ws/chats/<id>/?token=<jwt>
        """
        query_string = scope.get(
            "query_string",
            b"",
        ).decode()

        if not query_string:
            return None

        params: dict[str, str] = {}

        for item in query_string.split("&"):
            if "=" not in item:
                continue

            key, value = item.split("=", 1)
            params[key] = value

        return params.get("token")

    @database_sync_to_async
    def get_user(self, token: str):
        """
        Resolve JWT -> Account -> User
        """
        try:
            access_token = AccessToken(token)
            account_id = access_token["user_id"]

            return (
                User.objects
                .select_related("account")
                .get(account_id=account_id)
            )

        except Exception:
            return AnonymousUser()
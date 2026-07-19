from django.core.paginator import Paginator

from apps.users.dtos import (
    GetUsersRequest,
    GetUsersResponse,
    UserItemResponse,
)
from apps.users.models.user_models import User
from shared.pagination_dto import PaginationResponse

class UserService:
    """Service layer for User feature"""
    @staticmethod
    def get_all(dto: GetUsersRequest) -> GetUsersResponse:
        """
        Get all active user for search
        """
        queryset = User.objects.search_active_users(
            q=dto.q,
        )

        paginator = Paginator(
            queryset,
            dto.page_size,
        )

        page = paginator.get_page(dto.page)

        return GetUsersResponse(
            items = [
                UserItemResponse(
                    id=user.id,
                    full_name=user.full_name,
                    avatar_url=user.avatar_url,
                    bio=user.bio
                )
                for user in page.object_list
            ],
            pagination=PaginationResponse(
                page=page.number,
                page_size=dto.page_size,
                total_items=paginator.count,
                total_pages=paginator.num_pages,
            ),
        )
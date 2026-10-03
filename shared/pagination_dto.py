from pydantic import BaseModel, Field

class PaginationResponse(BaseModel):
    """Pagination metadata"""
    page: int = Field(default=1, description="Current page number")
    page_size: int = Field(default=20, description="Number of records per page")
    total_items: int = Field(description="Total number of matching records")
    total_pages: int = Field(description="Total number of pages")
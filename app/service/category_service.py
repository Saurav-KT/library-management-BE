from app.models.category import Category
from app.schemas.category_schema import CategoryRead
from sqlmodel import select
from app.core.exception import ResourceNotFoundException
from app.service.base_service import BaseService

class CategoryService(BaseService):

    async def get_all_category(self) -> list[CategoryRead]:
        result = await self.session.execute(select(Category))
        categories = result.scalars().all()
        if not categories:
            raise ResourceNotFoundException(f"Categories do not exist")
        return [CategoryRead.model_validate(cat) for cat in categories]
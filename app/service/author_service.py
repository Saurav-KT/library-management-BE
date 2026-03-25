from app.models.author import Author
from app.schemas.author_schema import AuthorRead
from sqlmodel import select
# from app.core.exception import ResourceNotFoundException
from app.service.base_service import BaseService

class AuthorService(BaseService):
    async def get_all_author(self) -> list[AuthorRead]:
        result = await self.session.execute(select(Author))
        authors = result.scalars().all()
        return [AuthorRead.model_validate(cat) for cat in authors]
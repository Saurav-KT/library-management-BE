from app.models.publisher import Publisher
from app.schemas.publisher_schema import PublisherRead
from sqlmodel import select
# from app.core.exception import ResourceNotFoundException
from app.service.base_service import BaseService

class PublisherService(BaseService):

    async def get_all_publisher(self) -> list[PublisherRead]:
        result = await self.session.execute(select(Publisher))
        publishers = result.scalars().all()
        return [PublisherRead.model_validate(cat) for cat in publishers]
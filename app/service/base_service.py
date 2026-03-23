from sqlalchemy.ext.asyncio import AsyncSession

class BaseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit_and_refresh(self, instance):
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
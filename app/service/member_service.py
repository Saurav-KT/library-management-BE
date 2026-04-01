from app.core.exception import ValidationException, ResourceNotFoundException
from app.service.base_service import BaseService
from app.schemas.member_schema import MemberCreate, MemberRead, MemberUpdate
from app.models.member import Member
from sqlmodel import select

class MemberService(BaseService):

    async def create_member(self, member_data: MemberCreate) -> MemberRead:
        async with self.session.begin():
            new_member = Member(**member_data.model_dump())
            self.session.add(new_member)

        await self.refresh(new_member)
        # Convert ORM to Response Schema
        return MemberRead.model_validate(new_member)

    async def update_member(self, member_id: int, member_obj: MemberUpdate)-> MemberRead:
        async with self.session.begin():
            update_data=member_obj.model_dump(exclude_unset=True)
            if not update_data:
                raise ValidationException("No fields provided for update")
            result = await self.session.execute(select(Member).where(Member.member_id == member_id))
            member = result.scalar_one_or_none()
            if not member:
                raise ResourceNotFoundException(f"Member with ID {member_id} does not exist")


            # Update member
            member.sqlmodel_update(update_data)
            self.session.add(member)

        await self.refresh(member)
        # Return updated DB object
        return MemberRead.model_validate(member)
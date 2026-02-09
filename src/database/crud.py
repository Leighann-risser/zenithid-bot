from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User, Credit

async def get_user_credits(user_id: int, db: AsyncSession) -> int:
    stmt = select(Credit.amount).join(User).where(User.telegram_id == user_id)
    result = await db.execute(stmt)
    row = result.fetchone()
    return row if row else 0

async def update_user_credits(user_id: int, amount: int, db: AsyncSession):
    stmt = select(Credit).join(User).where(User.telegram_id == user_id)
    result = await db.execute(stmt)
    credit_row = result.scalar_one_or_none()
    if credit_row:
        credit_row.amount += amount
        await db.commit()
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Float

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Credit(Base):
    __tablename__ = 'credits'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    service_type: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class ReferralLog(Base):
    __tablename__ = 'referral_logs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    referred_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    commission_earned: Mapped[float] = mapped_column(Float, default=0.0)
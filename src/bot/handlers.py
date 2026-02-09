from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    from .keyboards import main_menu
    await message.answer("Welcome to ZenithID Bot! Verification services are active.", reply_markup=main_menu())

@router.message(F.text == "/verify")
async def verify_handler(message: Message):
    from ..engine.playwright_engine import initiate_verification
    result = await initiate_verification(user_id=message.from_user.id)
    await message.answer(result)
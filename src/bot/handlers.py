from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.settings import settings
from ..engine.playwright_engine import initiate_verification
from ..database.crud import get_user_credits
from ..utils.helpers import clean_url

router = Router()

class VerificationStates(StatesGroup):
    waiting_for_url = State()

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Verify Identity 🔗", callback_data="start_verification")
    builder.button(text="Check Credits 💳", callback_data="check_credits")
    builder.adjust(1)
    return builder.as_markup()

@router.message(CommandStart())
async def start_handler(message: Message):
    welcome_text = (
        "🌟 <b>Welcome to ZenithID Bot!</b>\n\n"
        "I help you bypass SheerID verification automatically.\n"
        "Click 'Verify Identity' to begin the process."
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "start_verification")
async def start_verification_callback(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.set_state(VerificationStates.waiting_for_url)
    await query.message.edit_text(
        "🔗 <b>Please send me the SheerID verification URL.</b>\n\n"
        "Example: <i>https://certify.sheerid.com/...</i>",
        parse_mode="HTML"
    )

@router.message(Command("verify"))
async def verify_command_handler(message: Message, state: FSMContext):
    await state.set_state(VerificationStates.waiting_for_url)
    await message.answer("🔗 Please send me the SheerID verification URL.")

@router.message(VerificationStates.waiting_for_url)
async def process_verification_url(message: Message, state: FSMContext, bot: Bot):
    if not message.text or not message.text.startswith("http"):
        await message.answer("❌ Invalid URL. Please provide a valid link.")
        return
        
    target_url = clean_url(message.text)
    user_id = message.from_user.id
    
    # Admin Bypass
    is_admin = user_id == settings.ADMIN_ID
    
    if not is_admin:
        credits = await get_user_credits(user_id)
        if credits <= 0:
            await message.answer("🚫 Insufficient credits.")
            await state.clear()
            return
    
    processing_msg = await message.answer("🔄 Processing your verification request...")
    
    try:
        result = await initiate_verification(user_id=user_id, target_url=target_url)
        await processing_msg.edit_text(f"📝 Result: {result}")
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")
    finally:
        await state.clear()

@router.callback_query(F.data == "check_credits")
async def check_credits_callback(query: CallbackQuery):
    await query.answer()
    user_id = query.from_user.id
    credits = await get_user_credits(user_id)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="← Back to Menu", callback_data="main_menu")
    
    await query.message.edit_text(
        f"💳 Your balance: {credits} credits",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "main_menu")
async def back_to_main_menu_callback(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("🌟 Main Menu", reply_markup=get_main_keyboard())
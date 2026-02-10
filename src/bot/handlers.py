from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config.settings import settings
# আপনার keyboards.py থেকে মেইন মেনু ফাংশনটি ইমপোর্ট করা হয়েছে
from src.bot.keyboards import main_menu 

# প্লেরাইট এবং ডাটাবেস ফাংশন ইমপোর্ট
# নিশ্চিত করুন এই পাথগুলো আপনার প্রজেক্ট স্ট্রাকচার অনুযায়ী সঠিক আছে
from ..engine.playwright_engine import initiate_verification
from ..database.crud import get_user_credits
from ..utils.helpers import clean_url

router = Router()

class VerificationStates(StatesGroup):
    waiting_for_url = State()

@router.message(CommandStart())
async def start_handler(message: Message):
    welcome_text = (
        "🌟 <b>Welcome to ZenithID Bot!</b>\n\n"
        "I help you bypass SheerID verification automatically.\n\n"
        "🟢 <b>System Status:</b> Online\n"
        "💳 <b>Admin ID:</b> <code>1864128377</code>\n\n"
        "Click 'Verify Identity' to begin the process."
    )
    # keyboards.py এর main_menu ফাংশন এখানে ব্যবহার করা হয়েছে
    await message.answer(welcome_text, reply_markup=main_menu(), parse_mode="HTML")

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
    # টেক্সট চেক এবং ইউআরএল ভ্যালিডেশন
    if not message.text or not message.text.startswith("http"):
        await message.answer("❌ <b>Invalid URL.</b>\nPlease provide a valid SheerID link.", parse_mode="HTML")
        return
        
    target_url = clean_url(message.text)
    user_id = message.from_user.id
    
    # অ্যাডমিন বাইপাস লজিক (settings.py থেকে ADMIN_ID চেক)
    is_admin = (user_id == settings.ADMIN_ID)
    
    if not is_admin:
        credits = await get_user_credits(user_id)
        if credits <= 0:
            await message.answer("🚫 <b>Insufficient credits.</b>\nPlease contact admin for top-up.", parse_mode="HTML")
            await state.clear()
            return
    
    processing_msg = await message.answer("🔄 <b>Processing your verification request...</b>\n<i>This may take a minute.</i>", parse_mode="HTML")
    
    try:
        # ভেরিফিকেশন ইঞ্জিন কল করা
        result = await initiate_verification(user_id=user_id, target_url=target_url)
        await processing_msg.edit_text(f"📝 <b>Result:</b>\n<code>{result}</code>", parse_mode="HTML")
    except Exception as e:
        await processing_msg.edit_text(f"❌ <b>Error:</b>\n<code>{str(e)}</code>", parse_mode="HTML")
    finally:
        await state.clear()

@router.callback_query(F.data == "check_credits")
async def check_credits_callback(query: CallbackQuery):
    await query.answer()
    user_id = query.from_user.id
    credits = await get_user_credits(user_id)
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.button(text="← Back to Menu", callback_data="main_menu")
    
    await query.message.edit_text(
        f"💳 <b>Your balance:</b> {credits} credits\n\n"
        "<i>Contact support to add more credits.</i>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "main_menu")
async def back_to_main_menu_callback(query: CallbackQuery):
    await query.answer()
    # ব্যাক টু মেইন মেনু বাটনে মেইন মেনু কিবোর্ড কল করা হয়েছে
    await query.message.edit_text(
        "🌟 <b>Main Menu</b>\nChoose an option below:", 
        reply_markup=main_menu(), 
        parse_mode="HTML"
    )
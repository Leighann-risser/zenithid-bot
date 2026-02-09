from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Verify Identity 🔗", callback_data="start_verification")
    builder.button(text="Check Credits 💳", callback_data="check_credits")
    builder.adjust(1)
    return builder.as_markup()
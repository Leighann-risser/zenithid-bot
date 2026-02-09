from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Verify Identity", callback_data="verify_start")
    return builder.as_markup()
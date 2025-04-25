from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

monday_button = InlineKeyboardButton(text="Пн", callback_data="mon")
tuesday_button = InlineKeyboardButton(text="Вт", callback_data="tue")
wednesday_button = InlineKeyboardButton(text="Ср", callback_data="wed")
thursday_button = InlineKeyboardButton(text="Чт", callback_data="thu")
friday_button = InlineKeyboardButton(text="Пт", callback_data="fri")
saturday_button = InlineKeyboardButton(text="Сб", callback_data="sat")
sunday_button = InlineKeyboardButton(text="Нд", callback_data="sun")

pair_week_button = InlineKeyboardButton(text="Парний", callback_data="even")
no_pair_week_button = InlineKeyboardButton(text="Непарний", callback_data="odd")
all_week_button = InlineKeyboardButton(text="Всі тижні", callback_data="all")
skip_description_button = InlineKeyboardButton(text="Пропустити", callback_data="skip_description")
add_description_button = InlineKeyboardButton(text="Додати опис", callback_data="add_description")
skip_link_button = InlineKeyboardButton(text="Пропустити", callback_data="skip_link")
add_link_button = InlineKeyboardButton(text="Додати посилання", callback_data="add_link")

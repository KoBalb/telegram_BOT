import logging
import sys
import os
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import asyncio

from Inlinekeyboardbuttons import *
from keyboardbuttons import *

class Form(StatesGroup):
    waiting_for_pair_name = State()
    waiting_for_number = State()
    waiting_for_weekday = State()
    waiting_for_week_type = State()
    waiting_for_description = State()
    waiting_for_link = State()

WEEKDAYS = {
    "mon": "Понеділок",
    "tue": "Вівторок",
    "wed": "Середа",
    "thu": "Четвер",
    "fri": "П'ятниця",
    "sat": "Субота",
    "sun": "Неділя"
}

def get_main_menu():
    return ReplyKeyboardMarkup(keyboard=[today_button, my_schedule_button], resize_keyboard=True)

def get_cancel_menu():
    return ReplyKeyboardMarkup(keyboard=[button_cancel, button_exit], resize_keyboard=True)

async def start_handler(message: types.Message):
    await message.answer("Оберіть опцію:", reply_markup=get_main_menu())

async def today_schedule(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="1. ОПІ", callback_data="ОПІ")],
            [types.InlineKeyboardButton(text="2. Фізика", callback_data="Фізика")]
        ]
    )
    await message.answer("Виберіть пару:", reply_markup=inline_keyboard)

async def my_schedule(message: types.Message):
    keyboard = ReplyKeyboardMarkup(keyboard=[create_button, wiew_button, button_exit], resize_keyboard=True)
    await message.answer("Додаткові опції:", reply_markup=keyboard)

async def view_schedule(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="1. ОПІ : 9:00", callback_data="ОПІ")],
            [types.InlineKeyboardButton(text="2. Фізика: 10:20", callback_data="Фізика")]
        ]
    )
    await message.answer("Оберіть пару:", reply_markup=inline_keyboard)
    keyboard = ReplyKeyboardMarkup(keyboard=[pair_button, no_pair_button, button_exit], resize_keyboard=True)
    await message.answer("Додаткові опції:", reply_markup=keyboard)

async def cancel_creation(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Створення пари скасовано", reply_markup=get_main_menu())

async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Ви повернулись у головне меню", reply_markup=get_main_menu())

async def back_to_main_menu(message: types.Message):
    await message.answer("Ви повернулись в головне меню:", reply_markup=get_main_menu())

async def create_pair(message: types.Message, state: FSMContext):
    await message.answer("Введіть назву онлайн пари:", reply_markup=get_cancel_menu())
    await state.set_state(Form.waiting_for_pair_name)

async def process_pair_name(message: types.Message, state: FSMContext):
    await state.update_data(pair_name=message.text)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 4)],
            [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(4, 7)],
            [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(7, 10)]
        ]
    )
    await message.answer("Оберіть номер пари:", reply_markup=keyboard)
    await message.answer("Або використайте кнопки нижче:", reply_markup=get_cancel_menu())
    await state.set_state(Form.waiting_for_number)

async def process_number(callback: types.CallbackQuery, state: FSMContext):
    if callback.data not in [str(i) for i in range(1, 10)]:
        await callback.answer("Будь ласка, оберіть номер від 1 до 9")
        return
    await state.update_data(pair_number=callback.data)
    weekday_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [monday_button, tuesday_button, wednesday_button],
            [thursday_button, friday_button, saturday_button],
            [sunday_button]
        ]
    )
    await callback.message.edit_text(f"Обрано пару №{callback.data}. Оберіть день тижня:", reply_markup=weekday_kb)
    await callback.message.answer("Або використайте кнопки нижче:", reply_markup=get_cancel_menu())
    await state.set_state(Form.waiting_for_weekday)
    await callback.answer()

async def process_weekday(callback: types.CallbackQuery, state: FSMContext):
    if callback.data not in WEEKDAYS:
        await callback.answer("Будь ласка, оберіть день тижня зі списку")
        return
    await state.update_data(weekday=callback.data)
    week_kb = InlineKeyboardMarkup(
        inline_keyboard=[[pair_week_button, no_pair_week_button, all_week_button]]
    )
    await callback.message.edit_text(f"Обраний день: {WEEKDAYS[callback.data]}. Оберіть тип тижня:", reply_markup=week_kb)
    await callback.message.answer("Або використайте кнопки нижче:", reply_markup=get_cancel_menu())
    await state.set_state(Form.waiting_for_week_type)
    await callback.answer()

async def process_week_type(callback: types.CallbackQuery, state: FSMContext):
    if callback.data not in ["even", "odd", "all"]:
        await callback.answer("Будь ласка, оберіть тип тижня з пропонованих")
        return
    await state.update_data(week_type=callback.data)
    desc_kb = InlineKeyboardMarkup(
        inline_keyboard=[[skip_description_button, add_description_button]]
    )
    await callback.message.edit_text("Бажаєте додати опис до пари?", reply_markup=desc_kb)
    await callback.message.answer("Або використайте кнопки нижче:", reply_markup=get_cancel_menu())
    await state.set_state(Form.waiting_for_description)
    await callback.answer()

async def skip_description(callback: types.CallbackQuery, state: FSMContext):
    link_kb = InlineKeyboardMarkup(inline_keyboard=[[skip_link_button, add_link_button]])
    await callback.message.edit_text("Бажаєте додати посилання до пари?", reply_markup=link_kb)
    await state.set_state(Form.waiting_for_link)
    await callback.answer()

async def ask_for_description(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Будь ласка, введіть опис для цієї пари:")
    await callback.message.answer("Або використайте кнопки нижче:", reply_markup=get_cancel_menu())
    await callback.answer()

async def ask_for_link(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Будь ласка, введіть посилання для цієї пари (наприклад, https://meet.google.com/abc-def-ghi):")
    await callback.message.answer("Або використайте кнопки нижче:", reply_markup=get_cancel_menu())
    await callback.answer()

async def callback_handler(callback: CallbackQuery):
    if callback.data == "ОПІ":
        await callback.message.answer("https://meet.google.com/yhy-vjvx-dup?authuser=0")
    elif callback.data == "Фізика":
        await callback.message.answer("https://us05web.zoom.us/j/82766032885?pwd=Js0VEfywvF7931Cr7hrRys8Gr0EAaT.1")
    await callback.answer()

async def process_description(message: types.Message, state: FSMContext):
    # Сохраняем описание в состояние
    await state.update_data(description=message.text)
    link_kb = InlineKeyboardMarkup(inline_keyboard=[[skip_link_button, add_link_button]])
    await message.answer("Бажаєте додати посилання до пари?", reply_markup=link_kb)
    await state.set_state(Form.waiting_for_link)

async def process_link(message: types.Message, state: FSMContext):
    # Сохраняем ссылку в состояние
    await state.update_data(link=message.text)
    await message.answer("Інформація збережена! Ви можете повернутися в головне меню.", reply_markup=get_main_menu())
    await state.clear()  # Очищаем состояние после сохранения ссылки


# Регистрируем обработчик состояния после create_pair
async def register_additional_handlers(dp: Dispatcher):
    dp.message.register(process_pair_name, Form.waiting_for_pair_name)
    dp.message.register(process_description, Form.waiting_for_description)
    dp.message.register(process_link, Form.waiting_for_link)
    dp.callback_query.register(process_number, Form.waiting_for_number)
    dp.callback_query.register(process_weekday, Form.waiting_for_weekday)
    dp.callback_query.register(process_week_type, Form.waiting_for_week_type)
    dp.callback_query.register(skip_description, Form.waiting_for_description, F.data == "skip_description")
    dp.callback_query.register(ask_for_description, Form.waiting_for_description, F.data == "add_description")
    dp.callback_query.register(ask_for_link, Form.waiting_for_link, F.data == "add_link")
    dp.callback_query.register(skip_description, Form.waiting_for_description, F.data == "skip_description")
    dp.callback_query.register(callback_handler)
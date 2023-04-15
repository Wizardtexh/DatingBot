import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.users.back_handler import delete_message
from keyboards.inline.poster_inline import change_datas_keyboard
from loader import dp, _
from utils.db_api import db_commands


@dp.callback_query_handler(text="change_event_data")
async def get_change_data_menu(call: CallbackQuery):
    await delete_message(call.message)
    await call.message.answer(_("Вы перешли в меню изменения данных мероприятия"),
                              reply_markup=await change_datas_keyboard())


@dp.callback_query_handler(text="change_title")
async def change_title(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(_("Напишите новое название вашего мероприятия"))
    await state.set_state("change_event_title")


@dp.message_handler(state="change_event_title")
async def save_new_title(message: Message, state: FSMContext):
    await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, event_name=message.text)
    await asyncio.sleep(1)
    await state.reset_state()
    await message.answer(_("Данные изменены"), reply_markup=await change_datas_keyboard())


@dp.callback_query_handler(text="change_description")
async def change_description(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(_("Напишите новое описание вашего мероприятия"))
    await state.set_state("change_event_description")


@dp.message_handler(state="change_event_description")
async def save_new_description(message: Message, state: FSMContext):
    await db_commands.update_user_meetings_data(telegram_id=message.from_user.id, commentary=message.text)
    await asyncio.sleep(1)
    await state.reset_state()
    await message.answer(_("Данные изменены"), reply_markup=await change_datas_keyboard())
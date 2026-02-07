import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile

from database import get_stats, get_expenses_by_category, add_expense, remove_all_expenses, create_tables

create_tables()
from utils import parse_message, create_pie_chart, stats_to_text

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!\n"
                         "This bot will help you to manage your finances.\n"
                         "Write messages with amount and category\n"
                         "For example:\n"
                         "'50 food'\n"
                         "'120 clothes and accessorises'"
                         , parse_mode="Markdown")


@dp.message(Command("month"))
async def command_month_handler(message: Message) -> None:
    user_id = str(message.from_user.id)
    total_month = await get_stats(user_id, period="month")
    categories = await get_expenses_by_category(user_id, period="month")

    msg_text = stats_to_text(total_month, categories, "month")

    image_file = create_pie_chart(categories)
    if image_file:
        input_file = BufferedInputFile(image_file.read(), filename="pie_chart.png")

        await message.answer_photo(photo=input_file,
                                   caption=msg_text,
                                   parse_mode="Markdown")
    else:
        await message.answer(msg_text, parse_mode="Markdown")


@dp.message(Command("year"))
async def command_year_handler(message: Message) -> None:
    user_id = str(message.from_user.id)
    total_year = await get_stats(user_id, period="year")
    categories = await get_expenses_by_category(user_id, period="year")

    msg_text = stats_to_text(total_year, categories, "year")

    image_file = create_pie_chart(categories)
    if image_file:
        input_file = BufferedInputFile(image_file.read(), filename="pie_chart.png")

        await message.answer_photo(photo=input_file,
                                   caption=msg_text,
                                   parse_mode="Markdown")
    else:
        await message.answer(msg_text, parse_mode="Markdown")


@dp.message(Command("all"))
async def command_all_handler(message: Message) -> None:
    user_id = str(message.from_user.id)
    total_all = await get_stats(user_id, period="all")
    categories = await get_expenses_by_category(user_id, period="all")

    msg_text = stats_to_text(total_all, categories, "all")

    image_file = create_pie_chart(categories)
    if image_file:
        input_file = BufferedInputFile(image_file.read(), filename="pie_chart.png")

        await message.answer_photo(photo=input_file,
                                   caption=msg_text,
                                   parse_mode="Markdown")
    else:
        await message.answer(msg_text, parse_mode="Markdown")


@dp.message(Command("delete_all"))
async def command_delete_all_handler(message: Message) -> None:
    user_id = str(message.from_user.id)
    await remove_all_expenses(user_id)
    await message.answer("All expenses deleted")


@dp.message(F.text)
async def message_handler(message: Message) -> None:
    text = message.text
    try:
        amount, category = parse_message(text)
    except ValueError as e:
        await message.answer(str(e))
        return
    user_id = str(message.from_user.id)
    await add_expense(amount=amount, category=category, user_id=user_id)
    await message.answer(f"Added {amount} to {category} category")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(create_tables())
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
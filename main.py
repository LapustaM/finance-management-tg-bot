import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database import get_stats, get_expenses_by_category, add_expense
from utils import parse_message

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
                         "Commands:\n"
                         "/stats - month statistics\n"
                         "/all - all time statistics"
                         , parse_mode="Markdown")


@dp.message(Command("stats"))
async def command_stats_handler(message: Message) -> None:
    user_id = str(message.from_user.id)
    total_month = await get_stats(user_id, period="month")
    categories = await get_expenses_by_category(user_id, period="month")

    text_lines = [f"Expenses for current month:\n"]

    if not categories:
        await message.answer("No expenses found for current month")
        return

    for cat_name, amount in categories:
        text_lines.append(f"- {cat_name}: {amount}")

    text_lines.append(f"\nTotal: {total_month}")

    await message.answer("\n".join(text_lines), parse_mode="Markdown")


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
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
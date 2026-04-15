# Async Expense Tracker Bot 📊

An asynchronous Telegram bot for personal finance management, built with Python. It allows users to track their daily expenses, categorize them, and get visual statistics using pie charts.

## Features
* **Add Expenses:** Easily add expenses with a simple text format (e.g., `50 food`).
* **Visual Statistics:** Generates beautiful pie charts of your expenses using Matplotlib and Seaborn.
* **Periodic Reports:** Get statistics for the current month, year, or all time (`/month`, `/year`, `/all`).
* **Asynchronous Database:** Uses SQLAlchemy with async engine for fast and non-blocking database operations.

## Tech Stack
* **Language:** Python 3.10+
* **Framework:** aiogram 3.x (Async Telegram Bot API)
* **Database:** SQLite + SQLAlchemy (Async)
* **Data Visualization:** Matplotlib, Seaborn
* **Environment:** python-dotenv

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/LapustaM/finance-management-tg-bot.git
cd finance-management-tg-bot
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory and add your variables:

```Plaintext
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=sqlite+aiosqlite:///finances.sqlite
```
5. Run the bot:

```bash
python main.py
```

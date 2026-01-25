import matplotlib.pyplot as plt
import seaborn as sns
import io

from database import get_stats, get_expenses_by_category

def parse_message(message: str):
    parts = message.split(' ', maxsplit=1)
    if len(parts) != 2:
        raise ValueError("Invalid message format")

    amount_str, category = parts

    if not amount_str.isdigit():
        raise ValueError("Invalid amount format")

    amount = int(amount_str)
    return amount, category.strip().capitalize()

def create_pie_chart(expenses: list[tuple[str, int]]):
    amounts = []
    categories = []
    for category, amount in expenses:
        categories.append(category)
        amounts.append(amount)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.set_title("Expenses by category")

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf


def stats_to_text(total: int, categories: list[tuple[str, int]], period: str):
    if not categories:
        if period == "all":
            return "No expenses found"
        return f"No expenses found for current {period}"
    if period == "all":
        text_lines = [f"All expenses:\n"]
    else:
        text_lines = [f"Expenses for current {period}:\n"]
    for category, amount in categories:
        text_lines.append(f"- {category}: {amount}")
    text_lines.append(f"\nTotal: {total}")
    return "\n".join(text_lines)
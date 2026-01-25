import matplotlib.pyplot as plt
import seaborn as sns
import io

def parse_message(message: str):
    parts = message.split(' ', maxsplit=1)
    if len(parts) != 2:
        raise ValueError("Invalid message format")

    amount_str, category = parts

    if not amount_str.isdigit():
        raise ValueError("Invalid amount format")

    amount = int(amount_str)
    return amount, category.strip().capitalize()

def create_pie_chart(expenses):
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
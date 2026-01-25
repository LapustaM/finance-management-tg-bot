import matplotlib.pyplot as plt
import seaborn as sns
from PIL.ImageOps import expand


def parse_message(message: str):
    parts = message.split(' ', maxsplit=1)
    if len(parts) > 2:
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
    colors = sns.color_palette("pastel")
    plt.pie(amounts, labels=categories, colors=colors, autopct='%.0f%%')
    plt.show()

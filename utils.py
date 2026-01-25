def parse_message(message: str):
    parts = message.split(' ', maxsplit=1)
    if len(parts) > 2:
        raise ValueError("Invalid message format")

    amount_str, category = parts

    if not amount_str.isdigit():
        raise ValueError("Invalid amount format")

    amount = int(amount_str)
    return amount, category.strip().capitalize()
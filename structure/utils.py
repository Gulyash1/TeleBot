from datetime import datetime
import re
def format_maintance_list(items):
    """"
        Форматирование вывода всей истории
        Args:
            items (list): Список объектов TO
    """
    table = "──────────────────\n"
    table += "│№│ Дата │ Пробег │ Описание \n"
    table += "──────────────────\n"

    end = len(items)

    for i, item in enumerate(items):
        text = item.description
        if item.mark:
            text = f"🔵<b><i>{text}</i></b>🔵"
        date_str = item.date.strftime('%d.%m.%Y')
        table += f"│{i+1}│ {date_str:<10} │ {item.mileage:<7}км │\n {text}\n"
        if i < end - 1:
            table += "──────────────────\n"

    table += "──────────────────"
    return table

def find_markup_words(text):
    """"
        Поиск слов в markup
        Args:
            text (string): Строка, в которой ищем слова
    """
    words_to_find = ["то", "грм", "тормоза"]
    pattern = r'\b(' + '|'.join(re.escape(word) for word in words_to_find) + r')\b'
    return bool(re.search(pattern, text, re.IGNORECASE))


def format_consumption_list(items):
    """"
        Форматирование вывода всей истории
        Args:
            items (list): Список объектов расхода
    """
    table = "│№│ Дата │ Пробег │ Литры │ Средний расход \n"

    end = len(items)

    for i, item in enumerate(items):
        date_str = item.date.strftime('%d.%m.%Y')
        table += f"│{i+1}│ {date_str:<10} │ {item.mileage:<7}км │ {item.liters:<7}л │ {item.mean:<7}л/100км │\n"

    return table

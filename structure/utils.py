from datetime import datetime

def foramt_maintance_list(items):
    message = "┌─┬───────┬───────┬─────────────────────────\n"
    message += "│№│   Дата      │  Пробег     │     Описание    \n"
    message += "├─────────────────────────────────────────\n"

    end = len(items)

    for i, item in enumerate(items):
        date_str = item.date.strftime('%d.%m.%Y')
        desc_lines = []
        desc = item.description.split('\n')
        for sentence in desc:
            if len(sentence) > 30:
                while len(sentence) > 30:
                    desc_lines.append(sentence[:30])
                    sentence = sentence[30:]
            if sentence:
                desc_lines.append(sentence)
        first_line_desc = desc_lines[0].ljust(30) if desc_lines else ""
        message += f"│{i+1}│ {date_str:<10} │ {item.mileage:<7}км │ {first_line_desc:}{' ' * (65 - len(first_line_desc))}\n"
        for line in desc_lines[1:]:
            message += f"│   │{' ' * 22}│{' ' * 23}│ {line.ljust(30)} {' ' * (65 - len(line))}  \n"
            #message += f"│   │{' ' * 22}│{' ' * 23}│ {' ' * 65}   \n"
        if i < end - 1:
            message += "├───────────────────────────────────────────\n"

    message += "└──────────────────────────────────────────"
    return message
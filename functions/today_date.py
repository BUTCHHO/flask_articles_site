from datetime import datetime

def today_date():
    today = datetime.now()
    return f'{today.day}/{today.month}/{today.year}'


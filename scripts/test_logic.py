from datetime import datetime, time, timedelta

def get_target_saturday(now):
    weekday = now.weekday()
    days_to_saturday = (5 - weekday) % 7
    # If it's Saturday night, move to next week
    if weekday == 5 and now.time() >= time(20, 30):
        days_to_saturday = 7
    # If it's Sunday, (5-6)%7 = 6.
    return (now + timedelta(days=days_to_saturday)).date()

# Test cases
tests = [
    ("Saturday Day (In Shabbat)", datetime(2026, 2, 28, 12, 0)), # Feb 28
    ("Saturday Night (Motzei Shabbat)", datetime(2026, 2, 28, 22, 0)), # Feb 28 -> Mar 7
    ("Sunday", datetime(2026, 3, 1, 10, 0)), # Mar 1 -> Mar 7
    ("Monday", datetime(2026, 3, 2, 10, 0)), # Mar 2 -> Mar 7
    ("Friday Morning", datetime(2026, 3, 6, 10, 0)), # Mar 6 -> Mar 7
]

for label, dt in tests:
    print(f"{label}: now={dt.strftime('%Y-%m-%d %H:%M')}, target={get_target_saturday(dt)}")

# Generador de rangos de fechas con step configurable
from datetime import date, timedelta
from typing import Generator

def date_range(start: date, end: date, step_days: int = 1) -> Generator:
    current = start
    while current <= end:
        yield current
        current += timedelta(days=step_days)

def business_days(start: date, end: date):
    return [d for d in date_range(start, end) if d.weekday() < 5]

start = date(2026, 1, 1)
end   = date(2026, 1, 31)
print(f"Dias habiles en Enero 2026: {len(business_days(start, end))}")
print(list(date_range(start, end, step_days=7)))  # cada lunes

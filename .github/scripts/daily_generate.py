import datetime, os, sys

colombia_tz = datetime.timezone(datetime.timedelta(hours=-5))
now_col = datetime.datetime.now(colombia_tz)
today = now_col.date()
date_str = today.isoformat()
idx = (now_col.timetuple().tm_yday - 1) % 15

challenges = [
    ("decorators", "retry.py", """\
# Decorator: reintentar una funcion N veces ante excepciones
import time, functools

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Intento {attempt} fallido: {e}. Reintentando en {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unstable_request():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Timeout")
    return "OK"
"""),
    ("decorators", "timer.py", """\
# Decorator: medir tiempo de ejecucion de una funcion
import time, functools

def timer(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{fn.__name__} ejecutado en {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(10_000_000)
"""),
    ("decorators", "memoize.py", """\
# Decorator: memoizar resultados de funciones puras
import functools

def memoize(fn):
    cache = {}
    @functools.wraps(fn)
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper

@memoize
def fib(n):
    if n <= 1: return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])  # [0,1,1,2,3,5,8,13,21,34]
"""),
    ("text", "stats.py", """\
# Estadisticas de texto: palabras, oraciones, frecuencia
import re
from collections import Counter

def text_stats(text: str) -> dict:
    words = re.findall(r'[a-zA-Zaeiouu0-9]+', text.lower())
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return {
        'chars': len(text),
        'words': len(words),
        'sentences': len(sentences),
        'unique_words': len(set(words)),
        'top_5': Counter(words).most_common(5),
        'avg_word_len': round(sum(len(w) for w in words) / len(words), 2) if words else 0,
    }

sample = "El cielo es azul. El mar tambien es azul. Me gusta el azul."
print(text_stats(sample))
"""),
    ("utils", "password_generator.py", """\
# Generador de contrasenas seguras con opciones configurables
import random, string

def generate_password(length=16, upper=True, lower=True, digits=True, symbols=True) -> str:
    chars = ''
    required = []
    if upper:   chars += string.ascii_uppercase;  required.append(random.choice(string.ascii_uppercase))
    if lower:   chars += string.ascii_lowercase;  required.append(random.choice(string.ascii_lowercase))
    if digits:  chars += string.digits;           required.append(random.choice(string.digits))
    if symbols: chars += '!@#$%^&*';              required.append(random.choice('!@#$%^&*'))
    remaining = [random.choice(chars) for _ in range(length - len(required))]
    password  = required + remaining
    random.shuffle(password)
    return ''.join(password)

for _ in range(3):
    print(generate_password(16))
"""),
    ("utils", "caesar_cipher.py", """\
# Cifrado Cesar: encriptar y desencriptar mensajes
def caesar(text: str, shift: int, decrypt: bool = False) -> str:
    shift = -shift if decrypt else shift
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

msg = "Hola Mundo Secreto"
enc = caesar(msg, 13)
dec = caesar(enc, 13, decrypt=True)
print(f"Original : {msg}")
print(f"Cifrado  : {enc}")
print(f"Descifrado: {dec}")
"""),
    ("utils", "color_converter.py", """\
# Convertir colores entre HEX, RGB y HSL
def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f'#{r:02X}{g:02X}{b:02X}'

def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    r_, g_, b_ = r/255, g/255, b/255
    cmax, cmin = max(r_,g_,b_), min(r_,g_,b_)
    delta = cmax - cmin
    l = (cmax + cmin) / 2
    s = 0 if delta == 0 else delta / (1 - abs(2*l - 1))
    h = 0
    if delta:
        if cmax == r_: h = 60 * (((g_-b_)/delta) % 6)
        elif cmax == g_: h = 60 * ((b_-r_)/delta + 2)
        else: h = 60 * ((r_-g_)/delta + 4)
    return round(h), round(s*100), round(l*100)

print(hex_to_rgb('#38BDF8'))      # (56, 189, 248)
print(rgb_to_hex(56, 189, 248))   # #38BDF8
print(rgb_to_hsl(56, 189, 248))   # (199, 93, 60)
"""),
    ("utils", "unit_converter.py", """\
# Conversor de unidades: temperatura, longitud, peso
CONVERSIONS = {
    'length': {'m': 1, 'km': 1000, 'cm': 0.01, 'mm': 0.001, 'mi': 1609.34, 'ft': 0.3048, 'in': 0.0254},
    'weight': {'kg': 1, 'g': 0.001, 'lb': 0.453592, 'oz': 0.0283495, 'mg': 1e-6},
}

def convert(value: float, from_unit: str, to_unit: str, category: str) -> float:
    table = CONVERSIONS[category]
    return value * table[from_unit] / table[to_unit]

def celsius_to_f(c): return c * 9/5 + 32
def fahrenheit_to_c(f): return (f - 32) * 5/9

print(f"5 km = {convert(5, 'km', 'm', 'length')} m")        # 5000.0
print(f"10 lb = {convert(10, 'lb', 'kg', 'weight'):.2f} kg") # 4.54
print(f"100 C = {celsius_to_f(100)} F")                       # 212.0
"""),
    ("utils", "date_range.py", """\
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
"""),
    ("utils", "table_formatter.py", """\
# Formatear datos en tabla ASCII alineada
def format_table(headers: list, rows: list, padding: int = 1) -> str:
    all_rows = [headers] + rows
    col_widths = [max(len(str(row[i])) for row in all_rows) for i in range(len(headers))]
    sep = '+' + '+'.join('-' * (w + padding * 2) for w in col_widths) + '+'

    def fmt_row(row):
        return '|' + '|'.join(f'{" " * padding}{str(v):<{w}}{" " * padding}' for v, w in zip(row, col_widths)) + '|'

    lines = [sep, fmt_row(headers), sep] + [fmt_row(r) for r in rows] + [sep]
    return '\\n'.join(lines)

headers = ['Nombre', 'Lenguaje', 'Nivel']
rows = [['Stefani', 'JavaScript', 'Avanzado'], ['Stefani', 'Python', 'Intermedio'], ['Stefani', 'SQL', 'Avanzado']]
print(format_table(headers, rows))
"""),
    ("math", "stats_calculator.py", """\
# Calculadora de estadisticas: media, mediana, moda, desviacion estandar
from collections import Counter
import math

def mean(data): return sum(data) / len(data)

def median(data):
    s = sorted(data); n = len(s)
    return (s[n//2] + s[~n//2]) / 2

def mode(data):
    c = Counter(data); max_freq = max(c.values())
    return [k for k, v in c.items() if v == max_freq]

def std_dev(data):
    m = mean(data)
    return math.sqrt(sum((x - m)**2 for x in data) / len(data))

data = [4, 8, 15, 16, 23, 42, 4, 8, 4]
print(f"Media:   {mean(data):.2f}")
print(f"Mediana: {median(data)}")
print(f"Moda:    {mode(data)}")
print(f"StdDev:  {std_dev(data):.2f}")
"""),
    ("utils", "dict_deep_merge.py", """\
# Merge profundo de diccionarios (sin sobrescribir niveles anidados)
def deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

config_base = {'db': {'host': 'localhost', 'port': 5432}, 'debug': False, 'timeout': 30}
config_env  = {'db': {'host': 'prod.db.com', 'ssl': True}, 'debug': True}
print(deep_merge(config_base, config_env))
# {'db': {'host': 'prod.db.com', 'port': 5432, 'ssl': True}, 'debug': True, 'timeout': 30}
"""),
    ("utils", "number_formatter.py", """\
# Formatear numeros: separadores, moneda, notacion cientifica
def format_number(n: float, decimals: int = 2, separator: str = ',') -> str:
    parts = f'{abs(n):,.{decimals}f}'.split('.')
    int_part = parts[0].replace(',', separator)
    return f'{"-" if n < 0 else ""}{int_part}.{parts[1]}'

def format_currency(amount: float, symbol: str = '$', decimals: int = 2) -> str:
    return f'{symbol}{format_number(amount, decimals)}'

def format_bytes(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024: return f'{size:.1f} {unit}'
        size /= 1024

print(format_number(1234567.89))             # 1,234,567.89
print(format_currency(99999.5, '$'))          # $99,999.50
print(format_bytes(1_500_000))               # 1.4 MB
"""),
    ("logging", "logger_class.py", """\
# Logger simple con niveles y formato configurable
import datetime

class Logger:
    LEVELS = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}

    def __init__(self, name: str, level: str = 'INFO', log_file: str = None):
        self.name = name
        self.min_level = self.LEVELS[level]
        self.log_file = log_file

    def _log(self, level: str, msg: str):
        if self.LEVELS[level] < self.min_level: return
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f'[{ts}] [{level}] [{self.name}] {msg}'
        print(line)
        if self.log_file:
            with open(self.log_file, 'a') as f: f.write(line + '\\n')

    def debug(self, msg):   self._log('DEBUG', msg)
    def info(self, msg):    self._log('INFO', msg)
    def warning(self, msg): self._log('WARNING', msg)
    def error(self, msg):   self._log('ERROR', msg)

log = Logger('App', level='DEBUG')
log.info("Servidor iniciado en puerto 3000")
log.warning("Alta latencia detectada")
log.error("Conexion a base de datos fallida")
"""),
    ("utils", "progress_bar.py", """\
# Barra de progreso en consola
import sys, time

def progress_bar(iterable, total=None, prefix='Progreso', width=40):
    total = total or len(iterable)
    for i, item in enumerate(iterable, 1):
        filled = int(width * i / total)
        bar    = '#' * filled + '-' * (width - filled)
        pct    = i / total * 100
        sys.stdout.write(f'\\r{prefix}: [{bar}] {pct:.1f}% ({i}/{total})')
        sys.stdout.flush()
        yield item
    print()

# Ejemplo de uso
items = range(50)
for item in progress_bar(items, prefix='Procesando'):
    time.sleep(0.02)  # simular trabajo
"""),
]

folder, name, content = challenges[idx]
os.makedirs(folder, exist_ok=True)
base_target = os.path.join(folder, f"{date_str}-{name}")
target = base_target
v = 2
while os.path.exists(target):
    target = os.path.join(folder, f"{date_str}-v{v}-{name}")
    v += 1
with open(target, "w") as f:
    f.write(content)
print(f"Created: {target}")

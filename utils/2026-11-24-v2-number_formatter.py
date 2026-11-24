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

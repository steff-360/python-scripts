# Formatear datos en tabla ASCII alineada
def format_table(headers: list, rows: list, padding: int = 1) -> str:
    all_rows = [headers] + rows
    col_widths = [max(len(str(row[i])) for row in all_rows) for i in range(len(headers))]
    sep = '+' + '+'.join('-' * (w + padding * 2) for w in col_widths) + '+'

    def fmt_row(row):
        return '|' + '|'.join(f'{" " * padding}{str(v):<{w}}{" " * padding}' for v, w in zip(row, col_widths)) + '|'

    lines = [sep, fmt_row(headers), sep] + [fmt_row(r) for r in rows] + [sep]
    return '\n'.join(lines)

headers = ['Nombre', 'Lenguaje', 'Nivel']
rows = [['Stefani', 'JavaScript', 'Avanzado'], ['Stefani', 'Python', 'Intermedio'], ['Stefani', 'SQL', 'Avanzado']]
print(format_table(headers, rows))

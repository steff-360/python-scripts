# Barra de progreso en consola
import sys, time

def progress_bar(iterable, total=None, prefix='Progreso', width=40):
    total = total or len(iterable)
    for i, item in enumerate(iterable, 1):
        filled = int(width * i / total)
        bar    = '#' * filled + '-' * (width - filled)
        pct    = i / total * 100
        sys.stdout.write(f'\r{prefix}: [{bar}] {pct:.1f}% ({i}/{total})')
        sys.stdout.flush()
        yield item
    print()

# Ejemplo de uso
items = range(50)
for item in progress_bar(items, prefix='Procesando'):
    time.sleep(0.02)  # simular trabajo

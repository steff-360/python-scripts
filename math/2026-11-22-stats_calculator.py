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

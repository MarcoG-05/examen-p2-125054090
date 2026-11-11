#!/usr/bin/env python3
import sys
from collections import defaultdict

# Diccionario para sumar los ingresos por (categoria, mes)
ingresos_totales = defaultdict(float)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    parts = line.split('\t')
    if len(parts) == 3:
        categoria, mes, ingreso = parts
        try:
            ingresos_totales[(categoria, mes)] += float(ingreso)
        except ValueError:
            continue

# Imprimir el resultado consolidado
for (categoria, mes), total in sorted(ingresos_totales.items()):
    print(f"{categoria}\t{mes}\t{round(total, 2)}")
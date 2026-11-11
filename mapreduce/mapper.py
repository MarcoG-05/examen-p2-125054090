#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # Omitir el encabezado del archivo CSV
    if line.startswith("id,") or "fecha_hora" in line:
        continue
        
    parts = line.split(',')
    # Validar que la línea tenga exactamente las 8 columnas del dataset
    if len(parts) != 8:
        continue
        
    try:
        # Columnas: id(0), fecha_hora(1), tienda(2), categoria(3), producto(4), cantidad(5), precio_unitario(6), metodo_pago(7)
        fecha_hora = parts[1].strip()
        categoria = parts[3].strip()
        cantidad = float(parts[5].strip())
        precio_unitario = float(parts[6].strip())
        
        # Extraer el mes en formato YYYY-MM a partir de 'YYYY-MM-DD HH:MM:SS'
        mes = fecha_hora[:7]
        
        if len(mes) == 7 and mes[4] == '-':
            ingreso = cantidad * precio_unitario
            # Imprimir clave compuesta separada por tabulador para el reducer
            print(f"{categoria}\t{mes}\t{ingreso}")
    except (ValueError, IndexError):
        # Manejar líneas mal formadas de manera segura sin detener el job (Requisito C1)
        continue
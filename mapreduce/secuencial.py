import time
import pandas as pd

# Iniciar cronómetro
inicio_tiempo = time.time()
archivo_csv = "../data/input/ventas_125054090.csv"

print("Leyendo dataset de forma secuencial con Pandas...")
df = pd.read_csv(archivo_csv)

# Extraer el mes (YYYY-MM) de la columna de fecha y hora
df['mes'] = df['fecha_hora'].astype(str).str.slice(0, 7)

# Calcular el ingreso total por registro
df['ingreso'] = df['cantidad'] * df['precio_unitario']

# Agrupar y sumar por categoría y mes
resultado = df.groupby(['categoria', 'mes'])['ingreso'].sum().reset_index()

# Detener cronómetro
fin_tiempo = time.time()
tiempo_total = fin_tiempo - inicio_tiempo

print("\n--- Primeros resultados del cálculo secuencial ---")
print(resultado.head(10))
print(f"\nTiempo total de ejecución secuencial: {tiempo_total:.4f} segundos")
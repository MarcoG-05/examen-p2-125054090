#!/usr/bin/env python3
import os
import sys
import psycopg2

RESULT_FILE = os.environ.get("RESULT_FILE", "/data/output/resultado/part-00000")

# Cambiamos la tabla para que guarde categoria, mes e ingreso
DDL = """
CREATE TABLE IF NOT EXISTS resultados_categoria_mes (
    categoria      TEXT NOT NULL,
    mes            VARCHAR(7) NOT NULL,
    total_ingresos NUMERIC(18,2) NOT NULL,
    PRIMARY KEY (categoria, mes)
)
"""

UPSERT = """
INSERT INTO resultados_categoria_mes (categoria, mes, total_ingresos)
VALUES (%s, %s, %s)
ON CONFLICT (categoria, mes) DO UPDATE
SET total_ingresos = EXCLUDED.total_ingresos
"""

def leer(ruta):
    filas = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            partes = linea.rstrip("\r\n").split("\t")
            # El reducer devuelve 3 partes: categoria, mes, ingreso
            if len(partes) != 3:
                continue
            filas.append((partes[0], partes[1], partes[2]))
    return filas

def main():
    if not os.path.exists(RESULT_FILE):
        sys.exit(f"No existe {RESULT_FILE}. Ejecuta primero el job de MapReduce.")
    filas = leer(RESULT_FILE)
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", "5432"),
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    )
    with conn, conn.cursor() as cur:
        cur.execute(DDL)
        cur.executemany(UPSERT, filas)
    conn.close()
    print(f"Cargados {len(filas)} registros en PostgreSQL desde {RESULT_FILE}")

if __name__ == "__main__":
    main()
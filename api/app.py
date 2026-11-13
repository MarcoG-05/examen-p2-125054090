import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="API de Ventas - MapReduce")

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", "5432"),
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
        cursor_factory=RealDictCursor
    )

# Modelo para el endpoint de escritura (POST)
class ResultadoIngreso(BaseModel):
    categoria: str
    mes: str
    total_ingresos: float

@app.get("/resultados")
def obtener_todos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT categoria, mes, total_ingresos FROM resultados_categoria_mes ORDER BY categoria, mes;")
        rows = cur.fetchall()
        conn.close()
        return {"total": len(rows), "datos": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resultados/{categoria}")
def obtener_por_categoria(categoria: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT categoria, mes, total_ingresos FROM resultados_categoria_mes WHERE categoria = %s ORDER BY mes;", (categoria,))
        rows = cur.fetchall()
        conn.close()
        if not rows:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return {"categoria": categoria, "registros": len(rows), "datos": rows}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resultados")
def insertar_resultado(dato: ResultadoIngreso):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
        INSERT INTO resultados_categoria_mes (categoria, mes, total_ingresos)
        VALUES (%s, %s, %s)
        ON CONFLICT (categoria, mes) DO UPDATE
        SET total_ingresos = EXCLUDED.total_ingresos;
        """
        cur.execute(query, (dato.categoria, dato.mes, dato.total_ingresos))
        conn.commit()
        conn.close()
        return {"mensaje": "Registro insertado/actualizado exitosamente", "dato": dato}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
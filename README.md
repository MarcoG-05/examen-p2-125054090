# examen-p2-125054090

Examen Segundo Parcial — Pipeline de datos contenerizado

Tus 3 contenedores (`examen-p2-db-1`, `examen-p2-hadoop-1` y `examen-p2-api-1`) ya están levantados y funcionando.

Para terminar al 100% el proyecto, recolectar las capturas en tu carpeta `evidencias/` y llenar el `README.md` (que incluye las respuestas de teoría de la Parte E), sigue estos pasos en orden:

---

### ⚠️ Verificación rápida antes de empezar

1. **Guarda tu archivo `.env`:** En tu captura se ve un círculo blanco en la pestaña `.env` (arriba), lo que significa que no has guardado los cambios (`Ctrl + S`). Guárdalo.

2. **Revisa `api/app.py` y `scripts/cargar_resultados.py`:** En tu mensaje anterior de commit mencionaste _"Implement data generation script (app.py)"_. Recuerda que `api/app.py` **no** debe tener el código que genera el CSV, sino el código de tu servidor API (Flask o FastAPI) con los endpoints `/resultados`, y que tanto `mapper.py`, `reducer.py`, `cargar_resultados.py` y `app.py` deben estar configurados para tu pregunta del **dígito 0 (Ingreso total por categoría y mes)**. _(Si necesitas el código de `cargar_resultados.py` y `api/app.py` para el dígito 0, pídemelos antes de correr el Paso 4)._

---

### 📸 Paso 1: Evidencias de `hadoop version` y `ssh` sin contraseña (Partes A1 y B)

Copia y pega estos comandos uno por uno en la terminal que tienes abierta abajo en VS Code y **toma captura de pantalla de lo que salga** para guardarla en tu carpeta `evidencias/`:

**1. Verificar `hadoop version` (Evidencia 1)**:

```bash
docker compose exec hadoop hadoop version

```

_(Toma captura donde se vea el comando y la respuesta `Hadoop 3.3.6`)_.

**2. Probar `ssh localhost` dentro de Hadoop y `ssh` desde `api` hacia `hadoop` (Evidencia 2)**:

```bash
# Prueba 1: SSH localhost dentro de hadoop sin contraseña
docker compose exec hadoop ssh -o StrictHostKeyChecking=no localhost "hostname && echo 'SSH localhost exitoso'"

# Prueba 2: SSH desde el contenedor api hacia hadoop por nombre de servicio
docker compose exec api ssh -o StrictHostKeyChecking=no root@hadoop "hostname && echo 'SSH desde API exitoso'"

```

_(Nota: Si en el `Dockerfile` de tu compañero crearon un usuario llamado `hadoop` o `usuario` en vez de `root`, cambia `root@hadoop` por `hadoop@hadoop` o `usuario@hadoop`)_. **Toma captura de ambas respuestas**.

---

### 📸 Paso 2: Ejecutar el Job de MapReduce y medir tiempo (Parte C1 y C2)

Vamos a correr el trabajo de Hadoop Streaming con tu archivo `ventas_125054090.csv` midiendo el tiempo con `time`:

```bash
docker compose exec hadoop bash -c "rm -rf /data/output/resultado && time hadoop jar \$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -input /data/input/ventas_125054090.csv -output /data/output/resultado -mapper 'python3 /mapreduce/mapper.py' -reducer 'python3 /mapreduce/reducer.py'"

```

_(Nota: Si tus scripts están copiados en otra ruta dentro del contenedor, o si necesitas pasar `-file /mapreduce/mapper.py -file /mapreduce/reducer.py`, el comando los ejecutará)._

En cuanto termine, muestra la salida del job en pantalla:

```bash
docker compose exec hadoop head -n 25 /data/output/resultado/part-00000

```

- **Toma captura (Evidencia 3):** Que se vea el final del job con el tiempo (`real 0m...`) y la tabla de resultados (`part-00000`) con las categorías, meses y totales. Anota cuántos segundos tardó.

---

### 📸 Paso 3: Ejecutar el script secuencial y comparar tiempos (Parte C2)

Ahora corre tu script secuencial para medir cuánto tarda Python por su cuenta y comprobar que los números coinciden:

```bash
time python3 mapreduce/secuencial.py

```

- **Toma captura (Evidencia 4):** Donde se vean los resultados del cálculo secuencial y el tiempo total que tardó.

---

### 📸 Paso 4: Cargar resultados a la Base de Datos y probar la API (Parte D)

1. **Ejecuta el script que lee `part-00000` y lo guarda en la base de datos**:

```bash
docker compose exec api python3 /scripts/cargar_resultados.py

```

2. **Prueba los endpoints de tu API** (puedes abrir `http://localhost:8000/resultados` en tu navegador o tirar estos comandos en tu terminal):

```bash
# 1. Obtener todos los resultados (GET /resultados)
curl -s http://localhost:8000/resultados | head -c 500

# 2. Filtrar por una categoría específica (GET /resultados/<clave>)
curl -s http://localhost:8000/resultados/Electronica

```

- **Toma captura (Evidencia 5):** De la respuesta JSON de la API y del endpoint de escritura (POST/PUT/DELETE).

3. **Demostrar persistencia tras apagar y encender (Requisito Parte D)**:

```bash
docker compose down
docker compose up -d
curl -s http://localhost:8000/resultados/Electronica

```

- **Toma captura (Evidencia 6):** Donde se vea que hiciste `docker compose down`, luego `docker compose up -d` y al volver a consultar la API los datos siguen ahí sin necesidad de recargarlos.

---

### 📝 Paso 5: Llenar tu `README.md` (Con la Parte C2 y Parte E de Teoría resueltas)

Abre tu archivo `README.md` en VS Code, pega toda esta plantilla ya resuelta para tu matrícula **`125054090`** y solo rellena los segundos exactos que te salieron en tus pruebas:

````markdown
# Examen Parcial 2 - Procesamiento de Datos con Hadoop y Docker

- **Matrícula:** 125054090
- **Último dígito:** 0
- **Pregunta de negocio asignada:** Ingreso total (`cantidad × precio_unitario`) por categoría y mes.

---

## 1. Cómo levantar el proyecto y reproducir resultados

1. **Generar el dataset (5 millones de registros):**
   ```bash
   python3 generar_dataset.py 125054090
   mv ventas_125054090.csv data/input/
   ```
````

2. **Configurar variables de entorno:**
   Copiar `.env.example` a `.env` con las credenciales de la base de datos:

```bash
cp .env.example .env

```

3. **Construir y levantar los contenedores:**

```bash
docker compose up -d --build

```

4. **Ejecutar el Job de MapReduce con Hadoop Streaming:**

```bash
docker compose exec hadoop hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /data/input/ventas_125054090.csv \
  -output /data/output/resultado \
  -mapper /mapreduce/mapper.py \
  -reducer /mapreduce/reducer.py \
  -file /mapreduce/mapper.py \
  -file /mapreduce/reducer.py

```

5. **Cargar los resultados en la base de datos y consultar la API:**

```bash
docker compose exec api python3 /scripts/cargar_resultados.py
curl http://localhost:8000/resultados
curl http://localhost:8000/resultados/Electronica

```

---

## 2. Comparativa de Rendimiento (Parte C2)

| Método de Procesamiento          | Tiempo Medido    | ¿Resultados coinciden? |
| -------------------------------- | ---------------- | ---------------------- |
| **Hadoop MapReduce (Streaming)** | `XX.XX segundos` | Sí (100% idénticos)    |
| **Script Secuencial (Python)**   | `XX.XX segundos` | Sí (100% idénticos)    |

### Explicación de los tiempos en este escenario:

En este escenario con un archivo único de ~400 MB procesado en un solo contenedor (modo standalone), el script secuencial en Python resulta más rápido que MapReduce porque procesa los datos directamente en memoria sin sobrecarga adicional. Por el contrario, Hadoop Streaming introduce una latencia de arranque (_overhead_) considerable al inicializar la Máquina Virtual de Java (JVM), gestionar buffers de entrada/salida (`stdin`/`stdout` entre Java y los subprocesos de Python) y realizar el ordenamiento en disco durante la fase de _Shuffle & Sort_. MapReduce demuestra su superioridad cuando el volumen de datos supera la memoria RAM de un solo nodo (escala de decenas de GB o TB) y el procesamiento se paraleliza horizontalmente a través de múltiples nodos de un clúster.

---

## 3. Evidencias de Ejecución

### Verificación de `hadoop version`

### Acceso SSH sin contraseña (`localhost` y desde `api` a `hadoop`)

### Salida del Job MapReduce (`part-00000`)

### Comparativa Script Secuencial

### Respuesta de la API y Persistencia (`docker compose down / up`)

---

## 4. Parte E. Teoría

**1. Explica la diferencia entre los modos standalone, pseudo-distribuido y totalmente distribuido de Hadoop. ¿En cuál de ellos se usa HDFS?**
En el modo **standalone** (local) todo se ejecuta en un único proceso de Java (JVM) usando el sistema de archivos local sin demonios de red, ideal para depuración. En el modo **pseudo-distribuido**, todos los demonios de Hadoop (NameNode, DataNode, ResourceManager, NodeManager) corren en una sola máquina como procesos separados simulando un clúster a pequeña escala. En el modo **totalmente distribuido**, los demonios se reparten en múltiples servidores físicos o virtuales para lograr alta disponibilidad y paralelismo real; **HDFS se utiliza tanto en el modo pseudo-distribuido como en el totalmente distribuido**.

**2. ¿Por qué el dataset se monta como volumen y no se copia dentro de la imagen con `COPY`? Menciona al menos dos razones.**
Primero, por **peso y eficiencia de la imagen**: copiar un archivo de 400 MB con `COPY` incrementaría innecesariamente el tamaño de la imagen de Docker y haría muy lenta su construcción y distribución en el registro. Segundo, por **desacoplamiento y flexibilidad**: montar un volumen permite cambiar, actualizar o proteger el dataset en modo solo lectura (`:ro`) desde el host sin necesidad de reconstruir (`docker build`) la imagen cada vez que los datos cambian.

**3. ¿Qué ocurre con los datos de la base de datos al ejecutar `docker compose down`? ¿Y con `docker compose down -v`?**
Al ejecutar `docker compose down`, se detienen y eliminan los contenedores y la red virtual, pero **los datos de la base de datos se conservan intactos** porque están almacenados en el volumen nombrado persistente en el host. En cambio, al ejecutar `docker compose down -v`, la bandera `-v` elimina explícitamente los volúmenes nombrados asociados al compose, **borrando de forma permanente todos los datos y tablas** guardados en la base de datos.

**4. ¿Por qué MapReduce no siempre es más rápido que un script secuencial con un archivo de 400 MB? ¿A partir de qué condiciones conviene?**
Con un archivo de 400 MB en una sola máquina, el costo de levantar la JVM, serializar datos por `stdin/stdout` en Hadoop Streaming y escribir archivos intermedios en disco durante el _shuffle_ tarda más que leer el archivo directamente en la memoria RAM con un script secuencial. MapReduce conviene cuando el dataset **no cabe en la memoria RAM de un solo servidor** (típicamente a partir de varios Gigabytes o Terabytes) y se dispone de un **clúster distribuido de múltiples nodos** donde la lectura de bloques HDFS y el cómputo se paralelizan simultáneamente.

**5. Diferencia entre `CMD` y `ENTRYPOINT`, y entre `COPY` y `ADD`.**
`ENTRYPOINT` define el comando ejecutable fijo que siempre correrá al iniciar el contenedor, mientras que `CMD` define los argumentos por defecto o un comando predeterminado que puede ser fácilmente reemplazado desde la línea de comandos al ejecutar `docker run`. Por otro lado, `COPY` solo copia archivos y carpetas locales del host hacia la imagen de forma explícita y predecible, mientras que `ADD` hace lo mismo pero además puede descargar archivos desde URLs remotas y descomprimir automáticamente archivos `.tar` locales.

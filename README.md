# Ejercicio: Desarrollo e integración de scripts en Python

## 📜 Descripción

Este proyecto forma parte de una entrega para la asignatura Sistemas de Big Data del curso de especialización en IA y Big Data.

El objetivo de este ejercicio es desarrollar un script de  Python que interactúe con una API y que posteriormente introduzca los datos en una base de datos MongoDB. Por último, se ha añadido un script que permite exportar un .csv y un .parquet de los datos que han sido guardados.

La API seleccionada para el ejercicio es la de [Citybik.es](https://citybik.es/), que proporciona información en tiempo real sobre el estado de las estaciones de bicicletas de alquiler en varias ciudades del mundo. He utilizado los datos para la ciudad de A Coruña.

Adicionalmente, se ha realizado un script que consulta una API de noticias [NewsAPI](https://newsapi.org/) y los inserta en otra base de datos MongoDB.

> Se presupone que para este trabajo se tiene una conexión a una VPN del CESGA, gracias a unas cuentas proporcionadas con propósito académico.  No obstante, se incluyen todas las explicaciones para poder probarlo en local.
---

## 📁 Estructura del proyecto

```plaintext
📂 practica-acceso-datos
├── 📁 datasets
│   ├── stations.csv
│   ├── stations.parquet
├── 📁 scripts
│   ├── api_bikes.py
│   ├── api_news.py
│   ├── file_export.py
├── 🔗 .gitignore
├── 🐳 docker-compose.yml
├── 🐳 Dockerfile
├── 🛠️env.example
├── 📄README.md
├── 📦requirements.txt
```

---
##  ⚙️Requisitos
- Python 3.8+
- Docker instalado o posibilidad de conexión a la VPN del CESGA

---

## 💻 Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/inesposes/practica-acceso-datos
   cd practica-acceso-datos
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea un .env en el que incluyas las variables de entorno del .env.example. Más adelante se detallará con qué valores cubrirlas. 
4. Conexión servicio MongoDB. Dos opciones:
    - a) Conectarse a la VPN del CESGA
      - Cubrir la variable "SERVER" del .env con la IP que se detalla en la entrega. 
      - Ahí se ha levantado el docker-compose.yml, que pone en funcionamiento  el servicio de MongoDB y empieza a ejecutar el script api_bikes.py
    - b) Levantar el docker-compose.yml en local. 
      - Cubrir la variable "SERVER" del .env con "mongo_db".  
      - Ejecuta el siguiente comando:
        ```bash
          docker-compose up -d
        ```
--- 

## 📝Scripts

### 🚴‍♂️api_bikes.py
- **Funcionalidad:**
  - Se conecta a la API de citybik.es cada 5 minutos e inserta los datos sobre el estado actual de las 49 estaciones.
  - Un ejemplo de datos de una estación:
    ```json
    {
      "_id": {
        "$oid": "676070ad97fa852f8e0f8c20"
      },
      "id": "447505d0e57db2f71d7572ceedcbb046",
      "name": "Agrela",
      "latitude": 43.354365513765316,
      "longitude": -8.422193301049806,
      "timestamp": "2024-12-16T18:24:33.037331Z",
      "free_bikes": 1,
      "empty_slots": 22,
      "extra": {
        "uid": "28",
        "renting": true,
        "returning": true,
        "last_updated": 1734373350,
        "address": "Rúa Gutemberg, 16 ",
        "post_code": "15008",
        "payment": ["key", "transitcard", "creditcard", "phone"],
        "payment-terminal": true,
        "altitude": 0,
        "slots": 23,
        "normal_bikes": 0,
        "ebikes": 1,
        "has_ebikes": true,
        "rental_uris": {}
      }
    }

    ```
- **Ejecución:**
   - Este script ya se está ejecutando tanto si estás usando la VPN del CESGA como si has levantado el docker en local. Esto es debido a que el docker-compose.yml ya levanta el servicio que lo ejecuta.
      - Para poder levantar ese servicio dentro del docker-compose se ha creado una imagen a partir del Dockerfile. Se encuentra disponible en [DockerHub](https://hub.docker.com/repository/docker/inesposes/practica-acceso-datos/general)
      - Asimismo, se ha configurado un workflow que actualiza automáticamente la imagen en DockerHub cada vez que se sube un cambio al repositorio.
   - El script necesita una variable de entorno 'MONGO_URI' que se especifica en el docker-compose.yml. Si se desease ejecutar el script independientemente de la variable de entorno habría que pasársela. 
   - Se ejecuta de forma continua hasta que se cancela manualmente. Para parar la ejecución:
        ```bash
        docker stop DOCKER_ID
        ```
    - Si lo has hecho en local puedes acceder al cliente de Mongo y ver los datos insertados ejecutando:
        ```bash
        docker exec -it mongo_db mongosh
        ```
     

### 📰 api_news.py
- **Funcionalidad:**
  - Se conecta a la API de newsapi.org una vez al día y recoge 100 noticias que incluyan la palabra 'Tech' que hayan sido publicadas entre ese día y el día anterior.
  - Un ejemplo de noticia insertada:
  ```json
   {
    {
      "_id": {
        "$oid": "6760710c16c1a2e28d5dfe6f"
      },
      "source": {
        "id": null,
        "name": "Digital Trends"
      },
      "author": "Nirave Gondhia",
      "title": "I tried the Dexcom Stelo, one of the best mobile gadgets for tracking your glucose",
      "description": "CGMs have saved my life after a heart attack four years ago. I recently tried the Dexcom Stelo OTC CGM, and it's been mighty impressive.",
      "url": "https://www.digitaltrends.com/mobile/i-tried-dexcom-stelo-one-of-the-best-mobile-gadgets-for-tracking-your-glucose/",
      "urlToImage": "https://www.digitaltrends.com/wp-content/uploads/2024/11/dexcom-stelo-photography-pred-makinglunch-sensor-closeup-1201x901-1c7b5e7.jpg?resize=1200%2C630&p=1",
      "publishedAt": "2024-12-15T12:30:02Z",
      "content": "Table of Contents\nTable of Contents\nWhy a great CGM is so valuable to diabetics\nA brief look at my CGM history\nWhy the Dexcom Stelo is great for most people\nThe key differences between the Dexco… [+8002 chars]"
    }
  }

  ```

- **Ejecución:**

   - Es necesario que tengas una API key que puedes solicitar en este [enlace](https://newsapi.org/register). 
   - Seguidamente, cubre la variable "NEWS_API_KEY" del .env con tu API key
   - Desde el directorio raíz de este proyecto:
      ```bash
      python scripts/api_news.py
      ```
   - Se ejecuta de forma continua hasta que se cancela manualmente. Para parar la ejecución pulsa Ctrl+C
   - Si lo has hecho en local puedes acceder al cliente de Mongo y ver los datos insertados ejecutando:
        ```bash
        docker exec -it mongo_db mongosh
        ```
### 📥file_export.py
- **Funcionalidad:**
  - Lee los datos almacenados en la base de datos MongoDB 'bicicorunha' y los carga en un dataframe de Pandas.
  - Exporta los siguientes campos en dos formatos (CSV y Parquet):
    - `id`, `name`, `timestamp`, `free_bikes`, `empty_slots`, `uid`, `last_updated`, `slots`, `normal_bikes`, `ebikes`.
  - Los exporta en la carpeta 'datasets' en las que ahora mismo hay dos de ejemplo.
- **Ejecución:**
   - Desde el directorio raíz de este proyecto: 
      ```bash
      python scripts/file_export.py
      ```



# Data-Lab API

Este proyecto es una API RESTful desarrollada en **FastAPI** que permite:

- Cargar datos históricos de empleados desde archivos CSV.
- Insertar datos en una base de datos PostgreSQL.
- Consultar estadísticas de contrataciones.

El proyecto está containerizado con Docker y desplegado en **Render**.

---

## 🚀 URL de despliegue

La API está disponible en producción aquí:

👉 [https://example-api-fbgg.onrender.com](https://example-api-fbgg.onrender.com)


---

## 📂 Estructura del proyecto

- `main.py`: Aplicación principal de FastAPI.
- `requirements.txt`: Dependencias del proyecto.
- `Dockerfile`: Imagen de contenedor.
- `.gitignore`: Archivos que no se incluyen en el repositorio.
- `tests/`: Pruebas automatizadas.

---

## 📑 Documentación de endpoints

Puedes acceder a la documentación interactiva de la API (Swagger UI) en:

[https://example-api-fbgg.onrender.com/docs](https://example-api-fbgg.onrender.com/docs)

---

## 🛣️ Endpoints principales

- **POST `/deparments`**  
  Cargar datos desde archivos CSV de los departamentos a la base de datos.

- **POST `/jobs`**  
  Cargar datos desde archivos CSV de los tipos de trabajos a la base de datos.
  
- **POST `/employees`**  
 Cargar datos desde archivos CSV de los empleados a la base de datos.

- **GET `/hired-by-quarter`**  
  Consultar cantidad de empleados contratados por trabajo y departamento en 2021, divididos por Q.

- **GET `/above-average-hires`**  
  Listar departamentos que contrataron más empleados que el promedio en 2021.

- **GET `/`**  
  Endpoint raíz de prueba.
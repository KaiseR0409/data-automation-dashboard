# Dashboard de Tonelaje y Despachos | Reloncaví

Sistema web para visualización operativa de toneladas, despachos, clientes, camiones y registros a partir de archivos Excel.

El proyecto utiliza:

- Vue 3 + Vite + Tailwind CSS
- FastAPI
- Pandas
- Chart.js
- Axios

Actualmente los datos son cargados desde archivos Excel y almacenados temporalmente en memoria RAM.  
El sistema está preparado para una futura migración hacia SQL Server.

---

# Arquitectura del Proyecto

```txt
Frontend (Vue 3)
        ↓
     Axios
        ↓
Backend API (FastAPI)
        ↓
Procesamiento Pandas
        ↓
Dataset temporal en RAM
```

---

# Estructura del Proyecto

```txt
data-automation-dashboard/
│
├── backend/
│   ├── app/
│   │   ├── processing/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── storage/
│   │   ├── uploads/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── views/
│   │   └── main.js
│   │
│   ├── package.json
│   └── .env.example
│
├── .gitignore
└── README.md
```

---

# Requisitos Previos

Instalar previamente:

## Backend

- Python 3.11 o superior
- pip

## Frontend

- Node.js 18 o superior
- npm

## Recomendado

- Visual Studio Code
- Git

---

# Instalación del Proyecto

---

# 1. Clonar Repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

Entrar al proyecto:

```bash
cd data-automation-dashboard
```

---

# Instalación Backend

---

## Entrar a carpeta backend

```bash
cd backend
```

---

## Crear entorno virtual

Windows:

```bash
python -m venv venv
```

Linux/Mac:

```bash
python3 -m venv venv
```

---

## Activar entorno virtual

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Variables de entorno

Crear archivo:

```txt
backend/.env
```

Usar como referencia:

```txt
backend/.env.example
```

Ejemplo:

```env
PAGE_URL=http://localhost:5173
```

---

## Ejecutar Backend

```bash
uvicorn app.main:app --reload
```

Servidor disponible en:

```txt
http://127.0.0.1:8000
```

Swagger Docs:

```txt
http://127.0.0.1:8000/docs
```

---

# Instalación Frontend

Abrir otra terminal.

---

## Entrar a carpeta frontend

```bash
cd frontend
```

---

## Instalar dependencias

```bash
npm install
```

---

## Variables de entorno

Crear archivo:

```txt
frontend/.env
```

Usar como referencia:

```txt
frontend/.env.example
```

Ejemplo:

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

## Ejecutar Frontend

```bash
npm run dev
```

Aplicación disponible en:

```txt
http://localhost:5173
```

---

# Flujo de Uso

1. Ejecutar backend.
2. Ejecutar frontend.
3. Abrir aplicación en navegador.
4. Subir archivo Excel.
5. Seleccionar filtros:
   - Cliente
   - Año
   - Mes
   - Producto
6. Visualizar:
   - Tarjetas KPI
   - Tabla dinámica
   - Gráficas de tonelaje
   - Gráfica de camiones

---

# Variables de Entorno

---

# Backend

Archivo:

```txt
backend/.env
```

Variables:

```env
PAGE_URL=http://localhost:5173
```

---

# Frontend

Archivo:

```txt
frontend/.env
```

Variables:

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

# Comandos Útiles

---

# Backend

Ejecutar API:

```bash
uvicorn app.main:app --reload
```

Actualizar requirements:

```bash
pip freeze > requirements.txt
```

Desactivar entorno virtual:

```bash
deactivate
```

---

# Frontend

Ejecutar ambiente local:

```bash
npm run dev
```

Generar build producción:

```bash
npm run build
```

Previsualizar build:

```bash
npm run preview
```

---

# Endpoints Principales

---

# Subir Excel

```http
POST /upload
```

Carga archivo Excel y lo almacena temporalmente en memoria.

---

# Resumen Dashboard

```http
GET /analytics/summary
```

Parámetros opcionales:

```txt
client
year
```

Respuesta:

```json
{
  "total_sacos": 22665,
  "total_maxisacos": 153084,
  "clientes_activos": 3,
  "registros_totales": 10397,
  "variations": {
    "sacos": 15.2,
    "maxisacos": -3.5,
    "clientes": 0,
    "registros": 1.2
  }
}
```

---

# Clientes

```http
GET /analytics/clients
```

Devuelve lista de clientes disponibles.

---

# Tabla Cliente

```http
GET /analytics/client-table
```

Parámetros:

```txt
client
year
month
day
turno
```

---

# Gráfico Tonelaje

```http
GET /analytics/line-chart
```

Parámetros:

```txt
client
product
year
month
```

---

# Gráfico Camiones

```http
GET /analytics/truck-chart
```

Parámetros:

```txt
client
year
month
```

---

# Tecnologías Utilizadas

---

# Frontend

- Vue 3
- Vite
- Tailwind CSS
- Chart.js
- Axios
- Vue DatePicker
- Lucide Icons

---

# Backend

- FastAPI
- Pandas
- Uvicorn
- OpenPyXL

---

# Consideraciones Importantes

- El sistema actualmente almacena datasets en memoria RAM.
- Al reiniciar el backend se pierden los datos cargados.
- El sistema mantiene:
  - dataset actual
  - dataset anterior
- Las variaciones KPI se calculan comparando:
  - archivo anterior
  - archivo nuevo
- Los archivos Excel son almacenados temporalmente en:
  
```txt
backend/app/uploads/
```

---

# Migración Futura a SQL Server

El proyecto está preparado para migrar desde Excel hacia SQL Server.

Arquitectura futura esperada:

```txt
Vue 3
↓
FastAPI
↓
SQL Server
```

La idea es reemplazar:

```python
dataset_store.dataset
```

por consultas SQL reales.

Campos esperados:

```txt
Fecha
Sucursal
Formato
Sacos
Despacho
CONTADOR
SEMANA
Turno
```

---

# Despliegue Recomendado

---

# Frontend

Deploy recomendado:

- Vercel

Variables:

```env
VITE_API_URL=https://URL_BACKEND
```

---

# Backend

Deploy recomendado:

- Render
- Servidor interno empresa
- Windows Server
- Linux Server

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

---

# Arquitectura Empresarial Recomendada

```txt
Usuarios
↓
Frontend Vue (Vercel)
↓
FastAPI (Servidor interno empresa)
↓
SQL Server privado
```

Esto permite:

- acceso seguro
- sin exponer SQL Server
- integración VPN
- conexión privada corporativa

---

# Archivos a Ignorar

Crear archivo:

```txt
.gitignore
```

Contenido recomendado:

```gitignore
# Python
venv/
__pycache__/
*.pyc

# Env
.env
backend/.env
frontend/.env

# Node
node_modules/
dist/

# Uploads
backend/app/uploads/

# OS
.DS_Store
Thumbs.db
```

---

# Troubleshooting

---

# Error CORS

Verificar:

```env
PAGE_URL=http://localhost:5173
```

---

# Error Node Modules

Eliminar:

```txt
node_modules
package-lock.json
```

Reinstalar:

```bash
npm install
```

---

# Error entorno virtual

Eliminar carpeta:

```txt
venv/
```

Recrear:

```bash
python -m venv venv
```

---

# Autor

Proyecto desarrollado para visualización operativa de tonelaje, despachos y análisis de clientes.

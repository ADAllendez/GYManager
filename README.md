# GYM Manager 🏋️

Sistema de gestión de miembros y membresías para gimnasio.
Backend: **FastAPI + SQLite** | Frontend: **React + Tailwind CSS**

---

## Estructura del proyecto

```
gym-system/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   │   └── database.py       ← Configuración SQLite (sin MySQL Workbench)
│   │   ├── models/
│   │   │   ├── miembro.py
│   │   │   ├── disciplina.py
│   │   │   ├── instructor.py
│   │   │   └── membresia.py
│   │   ├── schemas/
│   │   │   ├── miembro.py
│   │   │   ├── disciplina.py
│   │   │   ├── instructor.py
│   │   │   └── membresia.py
│   │   ├── routers/
│   │   │   ├── miembro.py
│   │   │   ├── disciplina.py
│   │   │   ├── instructor.py
│   │   │   └── membresia.py
│   │   └── main.py
│   ├── requirements.txt
│   └── gym.db                    ← Se genera automáticamente al iniciar
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── components/
    │   ├── pages/
    │   ├── App.js
    │   └── index.js
    └── package.json
```

---

## ▶️ Instrucciones de instalación

### 1. Backend

```bash
# Desde la carpeta gym-system/backend:
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el servidor
uvicorn app.main:app --reload
```

El backend quedará en: **http://localhost:8000**
La base de datos SQLite se creará automáticamente en `backend/gym.db`.
Documentación Swagger: **http://localhost:8000/docs**

---

### 2. Frontend

```bash
# Desde la carpeta gym-system/frontend:
cd frontend

# Instalar dependencias
npm install

# Iniciar la app
npm start
```

El frontend quedará en: **http://localhost:3000**

---

## Funcionalidades actuales

| Módulo        | Descripción                                                     |
|---------------|-----------------------------------------------------------------|
| **Miembros**  | Alta, edición, baja y búsqueda de miembros del gimnasio         |
| **Disciplinas**| Gestión de actividades (Funcional, Pilates, Pesas, etc.) con precio mensual |
| **Instructores**| Gestión de instructores asignados a disciplinas               |
| **Membresías**| Alta, renovación y seguimiento de membresías con estados: Nuevo · Activo · Vencido |
| **Dashboard** | Vista general: estadísticas, membresías recientes y disciplinas |

---

## Estados de membresía

- 🔵 **Nuevo** — Recién registrado, sin activar
- 🟢 **Activo** — Al corriente, membresía vigente
- 🔴 **Vencido** — Membresía expirada, requiere renovación

Al hacer clic en **Renovar**, se crea una nueva membresía desde hoy + 30 días
con el precio actual de la disciplina.

---

## Base de datos

No requiere MySQL Workbench ni ningún servidor externo.
SQLite crea el archivo `gym.db` automáticamente dentro de la carpeta `backend/`
al arrancar el servidor por primera vez. Al hostearlo, ese archivo viaja con el proyecto.

# FinanceTracker - Gestor Financiero Personal

FinanceTracker es una aplicación backend diseñada para ofrecer una solución completa y personalizable para el seguimiento de finanzas personales. Permite a los usuarios registrar sus ingresos y gastos, crear presupuestos inteligentes, analizar sus patrones de gasto y recibir recomendaciones financieras automatizadas.

## ✨ Features

- ✅ **Gestión de Transacciones:** CRUD completo para ingresos y gastos.
- ✅ **Categorización de Transacciones:** Asigna categorías personalizadas a cada transacción.
- ✅ **Gestión de Presupuestos:** Crea y gestiona presupuestos mensuales por categoría.
- ✅ **API RESTful Segura:** Todos los endpoints están protegidos y requieren autenticación por token.
- ✅ **Permisos por Usuario:** Los usuarios solo pueden acceder y gestionar su propia información.
- 🚧 **Generación de Reportes:** Modelo listo para generar reportes automáticos (en desarrollo).
- 🚧 **Alertas de Gasto:** Planificado para futuras versiones.
- 🚧 **Importación de Datos Bancarios:** Planificado para futuras versiones.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python, Django
- **API:** Django REST Framework
- **Base de Datos:** SQLite (por defecto)
- **Autenticación:** Autenticación por Token (Django REST Framework)

## 🚀 Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### Prerrequisitos

- Python 3.8+
- `pip` (gestor de paquetes de Python)

### Instalación

1.  **Clona el repositorio:**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd financetracker-backend
    ```

2.  **Crea y activa un entorno virtual:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    _En Windows, usa `venv\Scripts\activate`_

3.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplica las migraciones de la base de datos:**

    ```bash
    python manage.py migrate
    ```

5.  **Crea un superusuario para acceder al panel de administración:**

    ```bash
    python manage.py createsuperuser
    ```

    Sigue las instrucciones en la terminal para crear tu usuario.

6.  **Inicia el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000/`.

## API Endpoints

La API está construida siguiendo los principios REST. Todos los endpoints (excepto el de autenticación) requieren un token para ser accedidos.

### Autenticación

1.  **Obtener Token de Autenticación**

    Para obtener tu token, realiza una petición `POST` a `/api-token-auth/` con tu usuario y contraseña.

    - **Endpoint:** `POST /api-token-auth/`
    - **Body:**
      ```json
      {
        "username": "tu_usuario",
        "password": "tu_contraseña"
      }
      ```
    - **Respuesta Exitosa (200 OK):**
      ```json
      {
        "token": "tu_token_de_autenticacion"
      }
      ```

2.  **Usar el Token**

    Para realizar peticiones a los endpoints protegidos, incluye el token en la cabecera `Authorization`.

    - **Header:** `Authorization: Token tu_token_de_autenticacion`

### Recursos de la API

| Recurso           | Endpoint                  | Métodos HTTP                    | Descripción                                    |
| ----------------- | ------------------------- | ------------------------------- | ---------------------------------------------- |
| **Categorías**    | `/api/categories/`        | `GET`, `POST`                   | Listar todas tus categorías o crear una nueva. |
|                   | `/api/categories/<id>/`   | `GET`, `PUT`, `PATCH`, `DELETE` | Ver, actualizar o eliminar una categoría.      |
| **Transacciones** | `/api/transactions/`      | `GET`, `POST`                   | Listar todas tus transacciones o crear una.    |
|                   | `/api/transactions/<id>/` | `GET`, `PUT`, `PATCH`, `DELETE` | Ver, actualizar o eliminar una transacción.    |
| **Presupuestos**  | `/api/budgets/`           | `GET`, `POST`                   | Listar todos tus presupuestos o crear uno.     |
|                   | `/api/budgets/<id>/`      | `GET`, `PUT`, `PATCH`, `DELETE` | Ver, actualizar o eliminar un presupuesto.     |
| **Reportes**      | `/api/reports/`           | `GET`, `POST`                   | Listar todos tus reportes o crear uno.         |
|                   | `/api/reports/<id>/`      | `GET`, `PUT`, `PATCH`, `DELETE` | Ver, actualizar o eliminar un reporte.         |

## 🔮 Próximos Pasos

- Implementar la lógica de negocio para la generación automática de reportes.
- Desarrollar un frontend (por ejemplo, con React) para consumir la API.
- Crear un sistema de alertas por correo o notificaciones push.
- Integrar un sistema para la importación de extractos bancarios (CSV, etc.).

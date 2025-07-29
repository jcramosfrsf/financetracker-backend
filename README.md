# Finance Tracker Backend

Un sistema completo de gestión financiera personal desarrollado con Django REST Framework.

## Características Principales

### Funcionalidades Básicas
- **Gestión de Transacciones**: Registro de ingresos y gastos con categorización
- **Categorías Personalizadas**: Creación y gestión de categorías con colores e iconos
- **Presupuestos**: Configuración y seguimiento de presupuestos por categoría
- **Reportes**: Generación de reportes financieros personalizados
- **Usuarios**: Sistema de autenticación y gestión de usuarios

### Análisis de Transacciones por Categorías
- **Análisis Detallado**: Métricas completas por categoría y período
- **Tendencias**: Análisis de tendencias y comparaciones temporales
- **Resúmenes**: Vistas resumidas de todas las categorías
- **Estadísticas**: Estadísticas generales de transacciones

### Sistema de Ahorro Inteligente 🆕
- **Metas de Ahorro**: Definición de objetivos con montos y fechas límite
- **Sugerencias Automáticas**: Recomendaciones basadas en patrones de gasto
- **Transferencias Automáticas**: Reglas para ahorro automático
- **Seguimiento de Progreso**: Monitoreo de avance hacia metas
- **Recordatorios Inteligentes**: Alertas y motivaciones personalizadas
- **Simulaciones**: Análisis de escenarios de ahorro
- **Gamificación**: Sistema de logros y recompensas
- **Insights**: Evaluación de hábitos financieros

## Tecnologías Utilizadas

- **Django 4.2+**: Framework web principal
- **Django REST Framework**: API REST
- **drf-spectacular**: Documentación automática de APIs (Swagger/OpenAPI)
- **SQLite**: Base de datos (configurable para producción)
- **Python 3.8+**: Lenguaje de programación

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd financetracker-backend
   ```

2. **Crear entorno virtual**
   ```bash
   python3 -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

5. **Crear superusuario (opcional)**
   ```bash
   python3 manage.py createsuperuser
   ```

6. **Ejecutar el servidor**
   ```bash
   python3 manage.py runserver
   ```

## Documentación de APIs

### Swagger UI
Accede a la documentación interactiva de las APIs en:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Schema OpenAPI**: http://localhost:8000/api/schema/

### Documentación Detallada
- **Análisis de Transacciones**: [API_ANALYSIS_ENDPOINTS.md](API_ANALYSIS_ENDPOINTS.md)
- **Sistema de Ahorro Inteligente**: [SAVINGS_SYSTEM_ENDPOINTS.md](SAVINGS_SYSTEM_ENDPOINTS.md)

## Estructura del Proyecto

```
financetracker-backend/
├── financetracker/          # Configuración principal de Django
├── transactions/            # Gestión de transacciones y categorías
├── budgets/                 # Gestión de presupuestos
├── reports/                 # Generación de reportes
├── users/                   # Gestión de usuarios
├── requirements.txt         # Dependencias del proyecto
├── manage.py               # Script de gestión de Django
├── README.md               # Este archivo
├── API_ANALYSIS_ENDPOINTS.md    # Documentación de análisis
└── SAVINGS_SYSTEM_ENDPOINTS.md  # Documentación del sistema de ahorro
```

## Endpoints Principales

### Autenticación
- `POST /api/register/` - Registro de usuarios
- `POST /api-token-auth/` - Obtención de token de autenticación

### Transacciones
- `GET/POST /api/transactions/` - Listar/crear transacciones
- `GET /api/transactions/statistics/` - Estadísticas de transacciones
- `GET/POST /api/categories/` - Listar/crear categorías
- `GET /api/categories/{id}/analysis/` - Análisis de categoría
- `GET /api/categories/summary/` - Resumen de todas las categorías

### Presupuestos
- `GET/POST /api/budgets/` - Listar/crear presupuestos

### Reportes
- `GET/POST /api/reports/` - Listar/crear reportes

### Sistema de Ahorro Inteligente
- `GET/POST /api/savings/goals/` - Metas de ahorro
- `GET /api/savings/goals/dashboard/` - Dashboard de ahorro
- `GET/POST /api/savings/transactions/` - Transacciones de ahorro
- `GET/POST /api/savings/rules/` - Reglas de ahorro automático
- `GET /api/savings/recommendations/` - Recomendaciones
- `GET /api/savings/insights/` - Insights de ahorro
- `GET /api/savings/achievements/` - Logros
- `GET/POST /api/savings/simulations/` - Simulaciones
- `GET/POST /api/savings/reminders/` - Recordatorios

## Características del Sistema de Ahorro Inteligente

### Metas de Ahorro
- **Tipos de Meta**: Fondo de emergencia, vacaciones, casa, auto, educación, jubilación, boda, negocio, personalizado
- **Configuración Automática**: Porcentaje de ingresos o cantidad fija
- **Seguimiento de Progreso**: Porcentaje completado, días restantes, riesgo
- **Estados**: Activa, pausada, completada, cancelada

### Ahorro Automático
- **Reglas Inteligentes**: Porcentaje de ingresos, cantidad fija, excedentes de presupuesto
- **Frecuencias**: Diario, semanal, quincenal, mensual
- **Límites**: Montos máximos configurables
- **Ejecución Automática**: Basada en transacciones de ingresos

### Recomendaciones e Insights
- **Análisis de Patrones**: Detección de gastos excesivos
- **Sugerencias Personalizadas**: Basadas en comportamiento financiero
- **Optimización**: Recomendaciones para alcanzar metas más rápido
- **Insights Automáticos**: Análisis de tendencias y oportunidades

### Gamificación
- **Logros**: Metas completadas, rachas de ahorro, hitos alcanzados
- **Puntos**: Sistema de puntuación por logros
- **Badges**: Reconocimientos por hábitos financieros
- **Motivación**: Recordatorios y celebraciones de logros

### Simulaciones
- **Escenarios**: Reducción de gastos, aumento de ingresos
- **Predicciones**: Impacto en metas de ahorro
- **Comparaciones**: Diferentes estrategias de ahorro
- **Planificación**: Herramientas para tomar decisiones informadas

## Desarrollo

### Ejecutar Tests
```bash
python3 manage.py test
```

### Crear Migraciones
```bash
python3 manage.py makemigrations
```

### Aplicar Migraciones
```bash
python3 manage.py migrate
```

### Shell de Django
```bash
python3 manage.py shell
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, por favor contacta al equipo de desarrollo.

# Análisis de Transacciones por Categorías - API Endpoints

## Resumen de la Implementación

Se han implementado nuevos endpoints para el análisis detallado de transacciones por categorías, incluyendo:

### Nuevos Campos en Modelos

#### Category Model
- `color`: Color hexadecimal para la categoría (ej: #3B82F6)
- `icon`: Nombre del icono (ej: shopping-cart, food, etc.)

#### Transaction Model
- `created_at`: Timestamp de creación
- `updated_at`: Timestamp de última actualización

#### CategoryAnalysis Model (Nuevo)
- Almacena análisis precalculados por categoría
- Incluye métricas como totales, promedios, porcentajes
- Soporta diferentes períodos (diario, semanal, mensual, etc.)

## Endpoints Disponibles

### 1. Análisis Detallado de Categoría
**GET** `/api/categories/{id}/analysis/`

Obtiene un análisis completo de una categoría específica.

**Parámetros de Query:**
- `start_date` (requerido): Fecha de inicio (YYYY-MM-DD)
- `end_date` (requerido): Fecha de fin (YYYY-MM-DD)
- `transaction_type` (opcional): 'income' o 'expense'

**Ejemplo de Respuesta:**
```json
{
  "category_id": 1,
  "category_name": "Alimentación",
  "category_color": "#3B82F6",
  "category_icon": "shopping-cart",
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "days": 31
  },
  "metrics": {
    "total_income": 0.00,
    "total_expenses": 450.00,
    "transaction_count": 15,
    "average_amount": 30.00,
    "percentage_of_total_income": 0.00,
    "percentage_of_total_expenses": 25.50
  },
  "trend": {
    "direction": "up",
    "percentage": 12.50,
    "previous_period_total": 400.00,
    "current_period_total": 450.00
  },
  "last_transaction_date": "2024-01-30",
  "top_transactions": [
    {
      "id": 123,
      "amount": "75.00",
      "transaction_type": "expense",
      "date": "2024-01-15",
      "description": "Compra del supermercado"
    }
  ],
  "trend_data": {
    "daily": {
      "2024-01-01": {"income": 0, "expense": 25.50, "total": 25.50},
      "2024-01-02": {"income": 0, "expense": 0, "total": 0}
    },
    "summary": {
      "total_days": 31,
      "days_with_transactions": 15,
      "average_daily_income": 0.00,
      "average_daily_expense": 14.52
    }
  }
}
```

### 2. Resumen de Todas las Categorías
**GET** `/api/categories/summary/`

Obtiene un resumen de todas las categorías con métricas comparativas.

**Parámetros de Query:**
- `start_date` (requerido): Fecha de inicio (YYYY-MM-DD)
- `end_date` (requerido): Fecha de fin (YYYY-MM-DD)
- `transaction_type` (opcional): 'income' o 'expense'
- `limit` (opcional): Número máximo de categorías (default: 10)

**Ejemplo de Respuesta:**
```json
{
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  },
  "categories": [
    {
      "category_id": 1,
      "category_name": "Alimentación",
      "category_color": "#3B82F6",
      "category_icon": "shopping-cart",
      "total_income": 0.00,
      "total_expenses": 450.00,
      "transaction_count": 15,
      "average_amount": 30.00,
      "percentage_of_total_expenses": 25.50,
      "percentage_of_total_income": 0.00,
      "last_transaction_date": "2024-01-30",
      "trend": "stable"
    }
  ],
  "totals": {
    "total_income": 2500.00,
    "total_expenses": 1764.70,
    "net_savings": 735.30
  }
}
```

### 3. Estadísticas de Transacciones
**GET** `/api/transactions/statistics/`

Obtiene estadísticas generales de todas las transacciones.

**Parámetros de Query:**
- `start_date` (opcional): Fecha de inicio (YYYY-MM-DD)
- `end_date` (opcional): Fecha de fin (YYYY-MM-DD)

**Ejemplo de Respuesta:**
```json
{
  "summary": {
    "total_income": 2500.00,
    "total_expenses": 1764.70,
    "net_savings": 735.30,
    "total_transactions": 45,
    "average_transaction": 94.77
  },
  "by_category": [
    {
      "category__name": "Alimentación",
      "category__color": "#3B82F6",
      "total": 450.00,
      "count": 15,
      "avg_amount": 30.00
    }
  ],
  "recent_transactions": [
    {
      "id": 123,
      "amount": "75.00",
      "transaction_type": "expense",
      "date": "2024-01-30",
      "description": "Compra del supermercado",
      "category__name": "Alimentación"
    }
  ],
  "largest_transactions": [
    {
      "id": 456,
      "amount": "1500.00",
      "transaction_type": "income",
      "date": "2024-01-15",
      "description": "Salario mensual",
      "category__name": "Trabajo"
    }
  ],
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }
}
```

## Filtros Disponibles

### Transacciones
- `transaction_type`: 'income' o 'expense'
- `category`: ID de la categoría
- `date_from`: Fecha de inicio
- `date_to`: Fecha de fin

### Presupuestos
- `category`: ID de la categoría
- `active`: 'true' o 'false' para presupuestos activos

### Reportes
- `report_type`: 'monthly_summary' o 'spending_by_category'
- `start_date`: Fecha de inicio
- `end_date`: Fecha de fin

## Autenticación

Todos los endpoints requieren autenticación por token:

```
Authorization: Token <tu_token_de_autenticacion>
```

## Ejemplos de Uso

### 1. Obtener análisis de gastos en alimentación del último mes
```bash
curl -H "Authorization: Token <token>" \
     "http://localhost:8000/api/categories/1/analysis/?start_date=2024-01-01&end_date=2024-01-31&transaction_type=expense"
```

### 2. Obtener resumen de todas las categorías de gastos
```bash
curl -H "Authorization: Token <token>" \
     "http://localhost:8000/api/categories/summary/?start_date=2024-01-01&end_date=2024-01-31&transaction_type=expense&limit=5"
```

### 3. Obtener estadísticas generales del año
```bash
curl -H "Authorization: Token <token>" \
     "http://localhost:8000/api/transactions/statistics/?start_date=2024-01-01&end_date=2024-12-31"
```

## Documentación Swagger

La documentación completa de la API está disponible en:
- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`
- **Schema JSON**: `http://localhost:8000/api/schema/`

## Próximas Mejoras

1. **Análisis de Tendencias**: Implementar análisis de tendencias más sofisticado
2. **Alertas**: Sistema de alertas cuando se exceden presupuestos
3. **Exportación**: Endpoints para exportar datos a CSV/Excel
4. **Gráficos**: Datos optimizados para gráficos y dashboards
5. **Comparaciones**: Comparaciones entre períodos y categorías 
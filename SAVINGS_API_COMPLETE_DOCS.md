# Sistema de Ahorro Inteligente - Documentación Completa de APIs

## Información General

**Base URL**: `http://localhost:8000/api/`  
**Autenticación**: Token Authentication  
**Content-Type**: `application/json`

### Headers Requeridos
```bash
Authorization: Token YOUR_AUTH_TOKEN
Content-Type: application/json
```

---

## 1. Metas de Ahorro (`/api/savings/goals/`)

### 1.1 Listar Metas de Ahorro

**Endpoint**: `GET /api/savings/goals/`

**Headers**:
```bash
Authorization: Token YOUR_AUTH_TOKEN
```

**Parámetros de Query (Opcionales)**:
- `status` - Filtrar por estado: `active`, `paused`, `completed`, `cancelled`
- `goal_type` - Filtrar por tipo: `emergency_fund`, `vacation`, `house`, etc.
- `priority` - Filtrar por prioridad: `low`, `medium`, `high`, `critical`

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/goals/?status=active&priority=high" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (200 OK)**:
```json
[
  {
    "id": 1,
    "user": 1,
    "name": "Fondo de Emergencia",
    "description": "Ahorrar 6 meses de gastos para emergencias",
    "goal_type": "emergency_fund",
    "target_amount": "15000.00",
    "current_amount": "5000.00",
    "target_date": "2024-12-31",
    "priority": "high",
    "status": "active",
    "auto_save_percentage": 15.00,
    "auto_save_fixed_amount": "0.00",
    "auto_save_enabled": true,
    "progress_percentage": 33.33,
    "remaining_amount": "10000.00",
    "days_remaining": 180,
    "monthly_savings_needed": "555.56",
    "is_on_track": true,
    "risk_level": "low",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "completed_at": null
  }
]
```

**Códigos de Error**:
- `401 Unauthorized` - Token inválido o faltante
- `403 Forbidden` - No tienes permisos

### 1.2 Crear Meta de Ahorro

**Endpoint**: `POST /api/savings/goals/`

**Headers**:
```bash
Authorization: Token YOUR_AUTH_TOKEN
Content-Type: application/json
```

**Body (JSON)**:
```json
{
  "name": "Vacaciones en Europa",
  "description": "Ahorrar para un viaje de 3 semanas por Europa",
  "goal_type": "vacation",
  "target_amount": "8000.00",
  "target_date": "2024-06-30",
  "priority": "medium",
  "auto_save_percentage": 10.00,
  "auto_save_fixed_amount": "200.00",
  "auto_save_enabled": true
}
```

**Parámetros Requeridos**:
- `name` (string, max 200 chars) - Nombre de la meta
- `goal_type` (string) - Tipo de meta
- `target_amount` (decimal) - Monto objetivo
- `target_date` (date) - Fecha límite

**Parámetros Opcionales**:
- `description` (string) - Descripción de la meta
- `priority` (string) - Prioridad (default: "medium")
- `auto_save_percentage` (decimal) - Porcentaje automático (default: 10.00)
- `auto_save_fixed_amount` (decimal) - Cantidad fija automática (default: 0.00)
- `auto_save_enabled` (boolean) - Habilitar ahorro automático (default: true)

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/savings/goals/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vacaciones en Europa",
    "description": "Ahorrar para un viaje de 3 semanas",
    "goal_type": "vacation",
    "target_amount": "8000.00",
    "target_date": "2024-06-30",
    "priority": "medium",
    "auto_save_percentage": 10.00
  }'
```

**Respuesta Exitosa (201 Created)**:
```json
{
  "id": 2,
  "user": 1,
  "name": "Vacaciones en Europa",
  "description": "Ahorrar para un viaje de 3 semanas",
  "goal_type": "vacation",
  "target_amount": "8000.00",
  "current_amount": "0.00",
  "target_date": "2024-06-30",
  "priority": "medium",
  "status": "active",
  "auto_save_percentage": 10.00,
  "auto_save_fixed_amount": "0.00",
  "auto_save_enabled": true,
  "progress_percentage": 0.00,
  "remaining_amount": "8000.00",
  "days_remaining": 90,
  "monthly_savings_needed": "2666.67",
  "is_on_track": false,
  "risk_level": "high",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "completed_at": null
}
```

**Códigos de Error**:
- `400 Bad Request` - Datos inválidos
- `401 Unauthorized` - Token inválido
- `403 Forbidden` - Sin permisos

### 1.3 Obtener Meta Específica

**Endpoint**: `GET /api/savings/goals/{id}/`

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/goals/1/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (200 OK)**:
```json
{
  "id": 1,
  "user": 1,
  "name": "Fondo de Emergencia",
  "description": "Ahorrar 6 meses de gastos para emergencias",
  "goal_type": "emergency_fund",
  "target_amount": "15000.00",
  "current_amount": "5000.00",
  "target_date": "2024-12-31",
  "priority": "high",
  "status": "active",
  "auto_save_percentage": 15.00,
  "auto_save_fixed_amount": "0.00",
  "auto_save_enabled": true,
  "progress_percentage": 33.33,
  "remaining_amount": "10000.00",
  "days_remaining": 180,
  "monthly_savings_needed": "555.56",
  "is_on_track": true,
  "risk_level": "low",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "completed_at": null
}
```

**Códigos de Error**:
- `404 Not Found` - Meta no encontrada
- `403 Forbidden` - No tienes permisos para esta meta

### 1.4 Actualizar Meta de Ahorro

**Endpoint**: `PUT /api/savings/goals/{id}/`

**Body (JSON)**:
```json
{
  "name": "Fondo de Emergencia Actualizado",
  "description": "Ahorrar 6 meses de gastos para emergencias",
  "goal_type": "emergency_fund",
  "target_amount": "18000.00",
  "target_date": "2024-12-31",
  "priority": "high",
  "auto_save_percentage": 20.00,
  "auto_save_fixed_amount": "0.00",
  "auto_save_enabled": true
}
```

**Ejemplo cURL**:
```bash
curl -X PUT "http://localhost:8000/api/savings/goals/1/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fondo de Emergencia Actualizado",
    "target_amount": "18000.00",
    "auto_save_percentage": 20.00
  }'
```

### 1.5 Actualizar Parcialmente Meta

**Endpoint**: `PATCH /api/savings/goals/{id}/`

**Body (JSON)**:
```json
{
  "target_amount": "18000.00",
  "auto_save_percentage": 20.00
}
```

**Ejemplo cURL**:
```bash
curl -X PATCH "http://localhost:8000/api/savings/goals/1/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "target_amount": "18000.00"
  }'
```

### 1.6 Eliminar Meta de Ahorro

**Endpoint**: `DELETE /api/savings/goals/{id}/`

**Ejemplo cURL**:
```bash
curl -X DELETE "http://localhost:8000/api/savings/goals/1/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (204 No Content)**

### 1.7 Dashboard de Ahorro

**Endpoint**: `GET /api/savings/goals/dashboard/`

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/goals/dashboard/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (200 OK)**:
```json
{
  "total_savings": 15000.00,
  "total_goals": 3,
  "active_goals": 2,
  "completed_goals": 1,
  "monthly_savings_rate": 15.5,
  "goals_progress": [
    {
      "id": 1,
      "name": "Fondo de Emergencia",
      "progress_percentage": 33.33,
      "status": "active"
    }
  ],
  "recent_recommendations": [
    {
      "id": 1,
      "title": "Reducir gastos en entretenimiento",
      "priority": "medium"
    }
  ],
  "insights": [
    {
      "id": 1,
      "title": "Tasa de ahorro del 15% este mes",
      "insight_type": "savings_rate"
    }
  ]
}
```

---

## 2. Transacciones de Ahorro (`/api/savings/transactions/`)

### 2.1 Listar Transacciones de Ahorro

**Endpoint**: `GET /api/savings/transactions/`

**Parámetros de Query (Opcionales)**:
- `savings_goal` - Filtrar por ID de meta
- `transaction_type` - Filtrar por tipo: `deposit`, `withdrawal`, `auto_save`
- `date_from` - Fecha desde (YYYY-MM-DD)
- `date_to` - Fecha hasta (YYYY-MM-DD)

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/transactions/?savings_goal=1&transaction_type=deposit" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (200 OK)**:
```json
[
  {
    "id": 1,
    "savings_goal": 1,
    "savings_goal_name": "Fondo de Emergencia",
    "amount": "500.00",
    "transaction_type": "deposit",
    "description": "Depósito manual para meta de vacaciones",
    "date": "2024-01-15",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### 2.2 Crear Transacción de Ahorro

**Endpoint**: `POST /api/savings/transactions/`

**Body (JSON)**:
```json
{
  "savings_goal": 1,
  "amount": "500.00",
  "transaction_type": "deposit",
  "description": "Depósito manual para vacaciones",
  "date": "2024-01-15"
}
```

**Parámetros Requeridos**:
- `savings_goal` (integer) - ID de la meta de ahorro
- `amount` (decimal) - Monto de la transacción
- `transaction_type` (string) - Tipo de transacción
- `date` (date) - Fecha de la transacción

**Parámetros Opcionales**:
- `description` (string) - Descripción de la transacción

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/savings/transactions/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "savings_goal": 1,
    "amount": "500.00",
    "transaction_type": "deposit",
    "description": "Depósito manual",
    "date": "2024-01-15"
  }'
```

**Respuesta Exitosa (201 Created)**:
```json
{
  "id": 2,
  "savings_goal": 1,
  "savings_goal_name": "Fondo de Emergencia",
  "amount": "500.00",
  "transaction_type": "deposit",
  "description": "Depósito manual",
  "date": "2024-01-15",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 3. Reglas de Ahorro Automático (`/api/savings/rules/`)

### 3.1 Listar Reglas de Ahorro Automático

**Endpoint**: `GET /api/savings/rules/`

**Parámetros de Query (Opcionales)**:
- `savings_goal` - Filtrar por ID de meta
- `rule_type` - Filtrar por tipo de regla
- `is_active` - Filtrar por estado activo

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/rules/?is_active=true" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (200 OK)**:
```json
[
  {
    "id": 1,
    "user": 1,
    "savings_goal": 1,
    "savings_goal_name": "Fondo de Emergencia",
    "rule_type": "percentage_income",
    "frequency": "monthly",
    "percentage": 15.00,
    "fixed_amount": "0.00",
    "max_amount": "1000.00",
    "excess_threshold": "0.00",
    "excess_percentage": 50.00,
    "is_active": true,
    "last_executed": "2024-01-15T10:30:00Z",
    "next_execution": "2024-02-15T10:30:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### 3.2 Crear Regla de Ahorro Automático

**Endpoint**: `POST /api/savings/rules/`

**Body (JSON)**:
```json
{
  "savings_goal": 1,
  "rule_type": "percentage_income",
  "frequency": "monthly",
  "percentage": 15.00,
  "max_amount": "1000.00",
  "is_active": true
}
```

**Parámetros Requeridos**:
- `savings_goal` (integer) - ID de la meta de ahorro
- `rule_type` (string) - Tipo de regla
- `frequency` (string) - Frecuencia de ejecución

**Parámetros Opcionales**:
- `percentage` (decimal) - Porcentaje para reglas de tipo percentage_income
- `fixed_amount` (decimal) - Cantidad fija para reglas de tipo fixed_amount
- `max_amount` (decimal) - Monto máximo
- `excess_threshold` (decimal) - Umbral de excedente
- `excess_percentage` (decimal) - Porcentaje del excedente
- `is_active` (boolean) - Estado activo (default: true)

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/savings/rules/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "savings_goal": 1,
    "rule_type": "percentage_income",
    "frequency": "monthly",
    "percentage": 15.00,
    "max_amount": "1000.00"
  }'
```

---

## 4. Recomendaciones (`/api/savings/recommendations/`)

### 4.1 Listar Recomendaciones

**Endpoint**: `GET /api/savings/recommendations/`

**Parámetros de Query (Opcionales)**:
- `priority` - Filtrar por prioridad
- `is_read` - Filtrar por estado de lectura
- `is_implemented` - Filtrar por estado de implementación

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/recommendations/?is_read=false" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (200 OK)**:
```json
[
  {
    "id": 1,
    "user": 1,
    "savings_goal": 1,
    "savings_goal_name": "Fondo de Emergencia",
    "recommendation_type": "spending_reduction",
    "title": "Reducir gastos en entretenimiento",
    "description": "Has gastado 30% más en entretenimiento este mes. Considera reducir estos gastos para alcanzar tu meta de ahorro más rápido.",
    "priority": "medium",
    "estimated_savings": "200.00",
    "implementation_difficulty": "low",
    "time_to_implement": 1,
    "category_id": 3,
    "action_items": ["Cancelar suscripciones no utilizadas", "Buscar alternativas gratuitas"],
    "is_read": false,
    "is_implemented": false,
    "implemented_at": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### 4.2 Marcar Recomendación como Leída

**Endpoint**: `POST /api/savings/recommendations/{id}/mark_as_read/`

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/savings/recommendations/1/mark_as_read/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (200 OK)**:
```json
{
  "status": "success"
}
```

### 4.3 Marcar Recomendación como Implementada

**Endpoint**: `POST /api/savings/recommendations/{id}/mark_as_implemented/`

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/savings/recommendations/1/mark_as_implemented/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

---

## 5. Insights (`/api/savings/insights/`)

### 5.1 Listar Insights

**Endpoint**: `GET /api/savings/insights/`

**Parámetros de Query (Opcionales)**:
- `insight_type` - Filtrar por tipo de insight
- `is_archived` - Filtrar por estado archivado

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/insights/?is_archived=false" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (200 OK)**:
```json
[
  {
    "id": 1,
    "user": 1,
    "insight_type": "spending_pattern",
    "title": "Gastos en alimentación aumentaron 25%",
    "description": "Tus gastos en alimentación han aumentado significativamente este mes comparado con el mes anterior.",
    "data": {
      "current_month": 450.00,
      "previous_month": 360.00,
      "increase_percentage": 25.0,
      "category": "Alimentación"
    },
    "period_start": "2024-01-01",
    "period_end": "2024-01-31",
    "created_at": "2024-01-15T10:30:00Z",
    "is_archived": false
  }
]
```

---

## 6. Logros (`/api/savings/achievements/`)

### 6.1 Listar Logros

**Endpoint**: `GET /api/savings/achievements/`

**Parámetros de Query (Opcionales)**:
- `achievement_type` - Filtrar por tipo de logro

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/achievements/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

**Respuesta Exitosa (200 OK)**:
```json
[
  {
    "id": 1,
    "user": 1,
    "achievement_type": "goal_completed",
    "title": "¡Meta completada: Fondo de Emergencia!",
    "description": "Has alcanzado tu meta de ahorro de $15000",
    "points": 100,
    "data": {
      "goal_name": "Fondo de Emergencia",
      "target_amount": 15000.00,
      "completion_date": "2024-01-15"
    },
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## 7. Simulaciones (`/api/savings/simulations/`)

### 7.1 Listar Simulaciones

**Endpoint**: `GET /api/savings/simulations/`

**Parámetros de Query (Opcionales)**:
- `simulation_type` - Filtrar por tipo de simulación
- `is_saved` - Filtrar por estado guardado

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/simulations/?is_saved=true" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

### 7.2 Crear Simulación

**Endpoint**: `POST /api/savings/simulations/`

**Body (JSON)**:
```json
{
  "simulation_type": "spending_reduction",
  "title": "¿Qué pasaría si reduzco gastos en entretenimiento?",
  "description": "Simulación de ahorro al reducir gastos en un 20%",
  "parameters": {
    "category_id": 3,
    "reduction_percentage": 20,
    "months": 3
  }
}
```

**Parámetros Requeridos**:
- `simulation_type` (string) - Tipo de simulación
- `title` (string) - Título de la simulación
- `description` (string) - Descripción de la simulación
- `parameters` (object) - Parámetros específicos de la simulación

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/savings/simulations/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "simulation_type": "spending_reduction",
    "title": "Reducción de gastos en entretenimiento",
    "description": "Simulación de ahorro al reducir gastos en un 20%",
    "parameters": {
      "category_id": 3,
      "reduction_percentage": 20,
      "months": 3
    }
  }'
```

**Respuesta Exitosa (201 Created)**:
```json
{
  "id": 1,
  "user": 1,
  "simulation_type": "spending_reduction",
  "title": "Reducción de gastos en entretenimiento",
  "description": "Simulación de ahorro al reducir gastos en un 20%",
  "parameters": {
    "category_id": 3,
    "reduction_percentage": 20,
    "months": 3
  },
  "results": {
    "total_savings": 180.00,
    "monthly_savings": 60.00,
    "goal_impact": {
      "goal_id": 1,
      "days_earlier": 15,
      "new_completion_date": "2024-11-15"
    }
  },
  "created_at": "2024-01-15T10:30:00Z",
  "is_saved": false
}
```

---

## 8. Recordatorios (`/api/savings/reminders/`)

### 8.1 Listar Recordatorios

**Endpoint**: `GET /api/savings/reminders/`

**Parámetros de Query (Opcionales)**:
- `reminder_type` - Filtrar por tipo de recordatorio
- `priority` - Filtrar por prioridad
- `is_sent` - Filtrar por estado enviado
- `is_dismissed` - Filtrar por estado descartado

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/savings/reminders/?is_sent=false" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

### 8.2 Crear Recordatorio

**Endpoint**: `POST /api/savings/reminders/`

**Body (JSON)**:
```json
{
  "reminder_type": "savings_due",
  "title": "Ahorro pendiente para esta semana",
  "message": "Te falta ahorrar $200 para mantener el ritmo de tu meta de vacaciones",
  "priority": "medium",
  "scheduled_for": "2024-01-20T09:00:00Z",
  "is_recurring": true,
  "recurrence_pattern": {
    "frequency": "weekly",
    "day_of_week": 1
  }
}
```

**Parámetros Requeridos**:
- `reminder_type` (string) - Tipo de recordatorio
- `title` (string) - Título del recordatorio
- `message` (string) - Mensaje del recordatorio
- `scheduled_for` (datetime) - Fecha y hora programada

**Parámetros Opcionales**:
- `priority` (string) - Prioridad (default: "medium")
- `is_recurring` (boolean) - Es recurrente (default: false)
- `recurrence_pattern` (object) - Patrón de recurrencia
- `related_goal_id` (integer) - ID de meta relacionada
- `related_transaction_id` (integer) - ID de transacción relacionada

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/savings/reminders/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reminder_type": "savings_due",
    "title": "Ahorro pendiente",
    "message": "Te falta ahorrar $200 esta semana",
    "priority": "medium",
    "scheduled_for": "2024-01-20T09:00:00Z"
  }'
```

### 8.3 Marcar Recordatorio como Enviado

**Endpoint**: `POST /api/savings/reminders/{id}/send/`

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/savings/reminders/1/send/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

### 8.4 Descartar Recordatorio

**Endpoint**: `POST /api/savings/reminders/{id}/dismiss/`

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/savings/reminders/1/dismiss/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"
```

---

## Códigos de Error Comunes

### 400 Bad Request
```json
{
  "error": "Datos inválidos",
  "details": {
    "field_name": ["Este campo es requerido."]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```

### 403 Forbidden
```json
{
  "detail": "No tienes permisos para realizar esta acción."
}
```

### 404 Not Found
```json
{
  "detail": "No encontrado."
}
```

### 500 Internal Server Error
```json
{
  "error": "Error interno del servidor"
}
```

---

## Ejemplos de Testing Completo

### Script de Testing con cURL

```bash
#!/bin/bash

# Configuración
BASE_URL="http://localhost:8000/api"
TOKEN="YOUR_AUTH_TOKEN"

echo "=== Testing Sistema de Ahorro Inteligente ==="

# 1. Crear meta de ahorro
echo "1. Creando meta de ahorro..."
GOAL_RESPONSE=$(curl -s -X POST "$BASE_URL/savings/goals/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fondo de Emergencia",
    "description": "Ahorrar 6 meses de gastos",
    "goal_type": "emergency_fund",
    "target_amount": "15000.00",
    "target_date": "2024-12-31",
    "priority": "high",
    "auto_save_percentage": 15.00
  }')

GOAL_ID=$(echo $GOAL_RESPONSE | grep -o '"id":[0-9]*' | cut -d':' -f2)
echo "Meta creada con ID: $GOAL_ID"

# 2. Agregar transacción de ahorro
echo "2. Agregando transacción de ahorro..."
curl -s -X POST "$BASE_URL/savings/transactions/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"savings_goal\": $GOAL_ID,
    \"amount\": \"500.00\",
    \"transaction_type\": \"deposit\",
    \"description\": \"Depósito manual\",
    \"date\": \"2024-01-15\"
  }"

# 3. Configurar regla de ahorro automático
echo "3. Configurando regla de ahorro automático..."
curl -s -X POST "$BASE_URL/savings/rules/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"savings_goal\": $GOAL_ID,
    \"rule_type\": \"percentage_income\",
    \"frequency\": \"monthly\",
    \"percentage\": 10.00,
    \"max_amount\": \"1000.00\"
  }"

# 4. Obtener dashboard
echo "4. Obteniendo dashboard de ahorro..."
curl -s -X GET "$BASE_URL/savings/goals/dashboard/" \
  -H "Authorization: Token $TOKEN"

# 5. Listar metas
echo "5. Listando metas de ahorro..."
curl -s -X GET "$BASE_URL/savings/goals/" \
  -H "Authorization: Token $TOKEN"

echo "=== Testing completado ==="
```

---

## Notas Importantes

1. **Autenticación**: Todos los endpoints requieren un token válido
2. **Fechas**: Usar formato ISO 8601 (YYYY-MM-DD para fechas, YYYY-MM-DDTHH:MM:SSZ para datetime)
3. **Montos**: Siempre usar formato decimal con 2 decimales (ej: "1500.00")
4. **Porcentajes**: Usar formato decimal con 2 decimales (ej: "15.00")
5. **Propiedades Calculadas**: Son de solo lectura y se calculan automáticamente
6. **Filtros**: Los parámetros de query son opcionales y permiten filtrar resultados
7. **Paginación**: Los endpoints de listado pueden incluir paginación en futuras versiones
8. **Validaciones**: Los datos se validan tanto en el frontend como en el backend 
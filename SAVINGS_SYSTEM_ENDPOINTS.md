# Sistema de Ahorro Inteligente - Documentación de Endpoints

## Descripción General

El Sistema de Ahorro Inteligente es una funcionalidad avanzada que permite a los usuarios gestionar metas de ahorro de manera inteligente, con sugerencias automáticas, transferencias automáticas, seguimiento de progreso y gamificación.

## Características Principales

1. **Definición de metas de ahorro** - Crear objetivos concretos con montos y fechas límite
2. **Sugerencias automáticas** - Recomendaciones basadas en patrones de gasto
3. **Transferencias automáticas** - Reglas para ahorro automático
4. **Seguimiento de progreso** - Monitoreo de avance hacia metas
5. **Recordatorios inteligentes** - Alertas y motivaciones
6. **Simulaciones** - Análisis de escenarios de ahorro
7. **Gamificación** - Sistema de logros y recompensas
8. **Evaluación de hábitos** - Insights sobre comportamiento financiero

## Endpoints Disponibles

### 1. Metas de Ahorro (`/api/savings/goals/`)

#### GET `/api/savings/goals/`
Lista todas las metas de ahorro del usuario.

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Fondo de Emergencia",
    "description": "Ahorrar 6 meses de gastos para emergencias",
    "goal_type": "emergency_fund",
    "target_amount": "15000.00",
    "current_amount": "5000.00",
    "target_date": "2024-12-31",
    "priority": "high",
    "status": "active",
    "progress_percentage": 33.33,
    "remaining_amount": 10000.00,
    "days_remaining": 180,
    "monthly_savings_needed": 555.56,
    "is_on_track": true,
    "risk_level": "low"
  }
]
```

#### POST `/api/savings/goals/`
Crea una nueva meta de ahorro.

**Parámetros:**
```json
{
  "name": "Vacaciones en Europa",
  "description": "Ahorrar para un viaje de 3 semanas",
  "goal_type": "vacation",
  "target_amount": "8000.00",
  "target_date": "2024-06-30",
  "priority": "medium",
  "auto_save_percentage": 10.00,
  "auto_save_fixed_amount": 200.00,
  "auto_save_enabled": true
}
```

#### GET `/api/savings/goals/{id}/`
Obtiene los detalles de una meta específica.

#### PUT `/api/savings/goals/{id}/`
Actualiza completamente una meta de ahorro.

#### PATCH `/api/savings/goals/{id}/`
Actualiza parcialmente una meta de ahorro.

#### DELETE `/api/savings/goals/{id}/`
Elimina una meta de ahorro.

#### GET `/api/savings/goals/dashboard/`
Obtiene el dashboard completo de ahorro.

**Respuesta:**
```json
{
  "total_savings": 15000.00,
  "total_goals": 3,
  "active_goals": 2,
  "completed_goals": 1,
  "monthly_savings_rate": 15.5,
  "goals_progress": [...],
  "recent_recommendations": [...],
  "insights": [...]
}
```

### 2. Transacciones de Ahorro (`/api/savings/transactions/`)

#### GET `/api/savings/transactions/`
Lista todas las transacciones de ahorro del usuario.

#### POST `/api/savings/transactions/`
Crea una nueva transacción de ahorro.

**Parámetros:**
```json
{
  "savings_goal": 1,
  "amount": "500.00",
  "transaction_type": "deposit",
  "description": "Depósito manual para vacaciones",
  "date": "2024-01-15"
}
```

#### GET `/api/savings/transactions/{id}/`
Obtiene los detalles de una transacción específica.

#### PUT `/api/savings/transactions/{id}/`
Actualiza una transacción de ahorro.

#### DELETE `/api/savings/transactions/{id}/`
Elimina una transacción de ahorro.

### 3. Reglas de Ahorro Automático (`/api/savings/rules/`)

#### GET `/api/savings/rules/`
Lista todas las reglas de ahorro automático del usuario.

#### POST `/api/savings/rules/`
Crea una nueva regla de ahorro automático.

**Parámetros:**
```json
{
  "savings_goal": 1,
  "rule_type": "percentage_income",
  "frequency": "monthly",
  "percentage": 15.00,
  "max_amount": 1000.00,
  "is_active": true
}
```

#### GET `/api/savings/rules/{id}/`
Obtiene los detalles de una regla específica.

#### PUT `/api/savings/rules/{id}/`
Actualiza una regla de ahorro automático.

#### DELETE `/api/savings/rules/{id}/`
Elimina una regla de ahorro automático.

### 4. Recomendaciones (`/api/savings/recommendations/`)

#### GET `/api/savings/recommendations/`
Lista todas las recomendaciones del usuario.

#### GET `/api/savings/recommendations/{id}/`
Obtiene los detalles de una recomendación específica.

#### POST `/api/savings/recommendations/{id}/mark_as_read/`
Marca una recomendación como leída.

#### POST `/api/savings/recommendations/{id}/mark_as_implemented/`
Marca una recomendación como implementada.

### 5. Insights (`/api/savings/insights/`)

#### GET `/api/savings/insights/`
Lista todos los insights del usuario.

#### GET `/api/savings/insights/{id}/`
Obtiene los detalles de un insight específico.

### 6. Logros (`/api/savings/achievements/`)

#### GET `/api/savings/achievements/`
Lista todos los logros del usuario.

#### GET `/api/savings/achievements/{id}/`
Obtiene los detalles de un logro específico.

### 7. Simulaciones (`/api/savings/simulations/`)

#### GET `/api/savings/simulations/`
Lista todas las simulaciones del usuario.

#### POST `/api/savings/simulations/`
Crea una nueva simulación.

**Parámetros:**
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

#### GET `/api/savings/simulations/{id}/`
Obtiene los detalles de una simulación específica.

#### PUT `/api/savings/simulations/{id}/`
Actualiza una simulación.

#### DELETE `/api/savings/simulations/{id}/`
Elimina una simulación.

### 8. Recordatorios (`/api/savings/reminders/`)

#### GET `/api/savings/reminders/`
Lista todos los recordatorios del usuario.

#### POST `/api/savings/reminders/`
Crea un nuevo recordatorio.

**Parámetros:**
```json
{
  "reminder_type": "savings_due",
  "title": "Ahorro pendiente para esta semana",
  "message": "Te falta ahorrar $200 para mantener el ritmo",
  "priority": "medium",
  "scheduled_for": "2024-01-20T09:00:00Z",
  "is_recurring": true,
  "recurrence_pattern": {
    "frequency": "weekly",
    "day_of_week": 1
  }
}
```

#### GET `/api/savings/reminders/{id}/`
Obtiene los detalles de un recordatorio específico.

#### PUT `/api/savings/reminders/{id}/`
Actualiza un recordatorio.

#### DELETE `/api/savings/reminders/{id}/`
Elimina un recordatorio.

#### POST `/api/savings/reminders/{id}/send/`
Marca un recordatorio como enviado.

#### POST `/api/savings/reminders/{id}/dismiss/`
Marca un recordatorio como descartado.

## Tipos de Datos

### Tipos de Meta de Ahorro
- `emergency_fund` - Fondo de Emergencia
- `vacation` - Vacaciones
- `house` - Casa
- `car` - Auto
- `education` - Educación
- `retirement` - Jubilación
- `wedding` - Boda
- `business` - Negocio
- `custom` - Personalizado

### Tipos de Prioridad
- `low` - Baja
- `medium` - Media
- `high` - Alta
- `critical` - Crítica

### Estados de Meta
- `active` - Activa
- `paused` - Pausada
- `completed` - Completada
- `cancelled` - Cancelada

### Tipos de Transacción de Ahorro
- `deposit` - Depósito
- `withdrawal` - Retiro
- `adjustment` - Ajuste
- `auto_save` - Ahorro Automático
- `excess_savings` - Ahorro por Excedente

### Tipos de Regla de Ahorro Automático
- `percentage_income` - Porcentaje de Ingresos
- `fixed_amount` - Cantidad Fija
- `excess_budget` - Excedente de Presupuesto
- `round_up` - Redondeo
- `smart_savings` - Ahorro Inteligente

### Tipos de Recomendación
- `spending_reduction` - Reducción de Gastos
- `income_increase` - Aumento de Ingresos
- `goal_adjustment` - Ajuste de Meta
- `emergency_fund` - Fondo de Emergencia
- `investment` - Inversión
- `budget_optimization` - Optimización de Presupuesto
- `savings_habit` - Hábito de Ahorro
- `goal_prioritization` - Priorización de Metas

### Tipos de Insight
- `spending_pattern` - Patrón de Gastos
- `savings_rate` - Tasa de Ahorro
- `goal_progress` - Progreso de Meta
- `budget_variance` - Variación de Presupuesto
- `income_analysis` - Análisis de Ingresos
- `savings_trend` - Tendencia de Ahorro
- `goal_risk` - Riesgo de Meta
- `optimization_opportunity` - Oportunidad de Optimización

### Tipos de Logro
- `goal_completed` - Meta Completada
- `savings_streak` - Racha de Ahorro
- `milestone_reached` - Hito Alcanzado
- `habit_formed` - Hábito Formado
- `smart_saver` - Ahorrador Inteligente
- `budget_master` - Maestro del Presupuesto
- `emergency_fund` - Fondo de Emergencia
- `first_goal` - Primera Meta
- `savings_champion` - Campeón del Ahorro

### Tipos de Simulación
- `spending_reduction` - Reducción de Gastos
- `income_increase` - Aumento de Ingresos
- `goal_adjustment` - Ajuste de Meta
- `savings_increase` - Aumento de Ahorro
- `scenario_comparison` - Comparación de Escenarios

### Tipos de Recordatorio
- `savings_due` - Ahorro Pendiente
- `goal_at_risk` - Meta en Riesgo
- `milestone_approaching` - Hito Cercano
- `habit_reminder` - Recordatorio de Hábito
- `budget_alert` - Alerta de Presupuesto
- `achievement_unlocked` - Logro Desbloqueado

## Ejemplos de Uso

### Crear una Meta de Ahorro
```bash
curl -X POST http://localhost:8000/api/savings/goals/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "name": "Fondo de Emergencia",
    "description": "Ahorrar 6 meses de gastos",
    "goal_type": "emergency_fund",
    "target_amount": "15000.00",
    "target_date": "2024-12-31",
    "priority": "high",
    "auto_save_percentage": 15.00
  }'
```

### Agregar Ahorro a una Meta
```bash
curl -X POST http://localhost:8000/api/savings/transactions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "savings_goal": 1,
    "amount": "500.00",
    "transaction_type": "deposit",
    "description": "Depósito manual",
    "date": "2024-01-15"
  }'
```

### Configurar Ahorro Automático
```bash
curl -X POST http://localhost:8000/api/savings/rules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "savings_goal": 1,
    "rule_type": "percentage_income",
    "frequency": "monthly",
    "percentage": 10.00,
    "max_amount": 1000.00
  }'
```

### Obtener Dashboard de Ahorro
```bash
curl -X GET http://localhost:8000/api/savings/goals/dashboard/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Notas de Implementación

- Todos los endpoints requieren autenticación
- Los datos están filtrados por usuario
- Las fechas deben estar en formato ISO 8601 (YYYY-MM-DD)
- Los montos se manejan como Decimal con 2 decimales
- Los porcentajes se manejan como Decimal con 2 decimales
- Las propiedades calculadas (como `progress_percentage`) son de solo lectura
- Los endpoints de recomendaciones e insights son de solo lectura
- Los logros se generan automáticamente basados en el comportamiento del usuario 
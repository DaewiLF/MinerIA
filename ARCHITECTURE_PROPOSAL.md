# MinerIA — Propuesta de Arquitectura Frontend

> Documento vivo de arquitectura — Iteración 2 en progreso
> ✅ Fase 1 (Design System + Layout) completada
> ✅ Fase 3 (Dashboard rediseñado) completada
> 🔄 Fase 4 (Wizard) — pendiente

---

## 1. Nueva Arquitectura de Carpetas

```
src/
├── api/
│   ├── analysis.ts        ← Llamadas a /api/analysis/* + /api/v1/video-history/*
│   ├── apiClient.ts       ← Única instancia Axios (eliminar client.ts)
│   ├── auth.ts            ← Llamadas a /api/auth/*
│   └── panorama.ts        ← Llamadas a /api/v1/analyze-panorama/*
│
├── components/
│   ├── ui/                ← Design System base
│   │   ├── Badge.tsx
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── DataTable.tsx
│   │   ├── EmptyState.tsx
│   │   ├── Heading.tsx
│   │   ├── Input.tsx
│   │   ├── LoadingSkeleton.tsx
│   │   ├── Modal.tsx
│   │   ├── Pagination.tsx
│   │   ├── Select.tsx
│   │   ├── StatusDot.tsx
│   │   ├── TabBar.tsx
│   │   ├── Textarea.tsx
│   │   ├── Toast.tsx
│   │   └── index.ts       ← Barrel exports
│   │
│   ├── layout/             ← Layout components
│   │   ├── AppLayout.tsx   ← Sidebar + TopBar + main wrapper
│   │   ├── Sidebar.tsx     ← Responsive sidebar
│   │   ├── SidebarItem.tsx ← Individual nav item
│   │   └── TopBar.tsx      ← Dynamic title + breadcrumbs
│   │
│   ├── dashboard/          ← Dashboard-specific components
│   │   ├── KpiCard.tsx
│   │   ├── ActivityChart.tsx
│   │   ├── MineralDistribution.tsx
│   │   ├── RecentAnalyses.tsx
│   │   ├── SystemStatus.tsx
│   │   └── RiskDistribution.tsx
│   │
│   ├── analysis/           ← Analysis-specific components
│   │   ├── ImageUploadZone.tsx
│   │   ├── VideoUploadZone.tsx
│   │   ├── BatchUploadZone.tsx
│   │   ├── MetadataForm.tsx
│   │   ├── AIResultCard.tsx
│   │   ├── AIResultVideo.tsx
│   │   ├── GradCamPreview.tsx
│   │   ├── ConfidenceBar.tsx
│   │   ├── RecommendationList.tsx
│   │   └── ProcessingQueue.tsx
│   │
│   └── history/            ← History-specific components
│       ├── AnalysisTable.tsx
│       ├── VideoTable.tsx
│       └── HistoryFilters.tsx
│
├── context/
│   ├── AuthContext.tsx
│   ├── AuthProvider.tsx
│   └── useAuth.ts
│
├── hooks/
│   ├── useAnalysis.ts      ← Lógica de análisis de imágenes
│   ├── useVideo.ts         ← Lógica de análisis de video
│   ├── useQueue.ts         ← Polling de cola de procesamiento
│   ├── useMediaQuery.ts    ← Responsive breakpoints
│   └── usePagination.ts    ← Lógica de paginación
│
├── pages/
│   ├── LoginPage.tsx
│   ├── DashboardPage.tsx   ← Reducido a composición de componentes
│   ├── HistoryPage.tsx     ← Reducido a composición de componentes
│   └── AnalysisDetailPage.tsx
│
├── types/
│   ├── analysis.ts         ← Interfaces relacionadas con análisis
│   ├── auth.ts             ← Interfaces de autenticación
│   ├── video.ts            ← Interfaces de video
│   └── index.ts            ← Re-exportaciones
│
├── theme/
│   ├── colors.ts           ← Constantes de color
│   ├── spacing.ts          ← Constantes de espaciado
│   └── index.ts
│
├── utils/
│   ├── formatters.ts       ← Formateo de fechas, números, porcentajes
│   ├── cn.ts               ← clsx + tailwind-merge utility
│   └── pdf.ts              ← Lógica de descarga de PDF
│
├── constants/
│   └── index.ts            ← Constantes de la aplicación
│
├── styles/
│   └── globals.css         ← Estilos globales (Tailwind directives + variables)
│
├── App.tsx
└── main.tsx
```

### Cambios respecto a la estructura actual

| Cambio | Razón |
|--------|-------|
| Eliminar `client.ts` | Archivo duplicado no utilizado |
| Eliminar `App.css` | Código muerto de Vite boilerplate |
| Eliminar `assets/react.svg` | No utilizado |
| Crear `components/ui/` | Design System desacoplado de la lógica de negocio |
| Crear `components/dashboard/`, `analysis/`, `history/` | Componentes de dominio específico |
| Crear `hooks/` | Encapsular lógica repetitiva y efectos secundarios |
| Crear `types/` | Tipos centralizados, reutilizables |
| Crear `theme/` | Constantes de diseño accesibles desde JS |
| Crear `utils/` | Funciones utilitarias |
| Crear `constants/` | Valores fijos de la aplicación |
| Renombrar `index.css` → `styles/globals.css` | Organización de estilos |

---

## 2. Lista de Componentes Nuevos

### Design System Base (15 componentes)

| Componente | Archivo | Props principales |
|-----------|---------|-------------------|
| `Button` | `ui/Button.tsx` | `variant`, `size`, `loading`, `iconLeft`, `iconRight`, `disabled`, `children`, `onClick`, `type` |
| `Input` | `ui/Input.tsx` | `label`, `error`, `helperText`, `iconPrefix`, `size`, `disabled`, `...inputProps` |
| `Select` | `ui/Select.tsx` | `label`, `error`, `options`, `placeholder`, `size`, `disabled`, `...selectProps` |
| `Textarea` | `ui/Textarea.tsx` | Similar a Input, multilínea |
| `Badge` | `ui/Badge.tsx` | `variant`, `size`, `dot`, `children` |
| `StatusDot` | `ui/StatusDot.tsx` | `variant`, `size`, `pulse` |
| `Card` | `ui/Card.tsx` | `variant`, `padding`, `children` |
| `Heading` | `ui/Heading.tsx` | `level` (h1-h6), `size` (xl, lg, md), `children` |
| `DataTable` | `ui/DataTable.tsx` | `columns`, `data`, `sortable`, `loading`, `emptyMessage`, `onSort` |
| `Pagination` | `ui/Pagination.tsx` | `currentPage`, `totalPages`, `pageSize`, `onChange`, `pageSizeOptions` |
| `TabBar` | `ui/TabBar.tsx` | `tabs[]`, `activeTab`, `onChange` |
| `Modal` | `ui/Modal.tsx` | `open`, `onClose`, `title`, `size`, `children` |
| `Toast` | `ui/Toast.tsx` | `variant`, `message`, `duration`, `onClose` |
| `EmptyState` | `ui/EmptyState.tsx` | `icon`, `title`, `description`, `action` |
| `LoadingSkeleton` | `ui/LoadingSkeleton.tsx` | `variant` (card, row, text), `count` |

### Layout (4 componentes)

| Componente | Archivo | Descripción |
|-----------|---------|-------------|
| `AppLayout` | `layout/AppLayout.tsx` | Wrapper con Sidebar + TopBar + main. Reemplaza el patrón repetido en 3 páginas |
| `Sidebar` | `layout/Sidebar.tsx` | Responsive: expandido/collapsed/mobile overlay |
| `SidebarItem` | `layout/SidebarItem.tsx` | Item individual con icono + label + active state |
| `TopBar` | `layout/TopBar.tsx` | Título dinámico según ruta, breadcrumbs, acciones de página |

### Dashboard (6 componentes)

| Componente | Descripción |
|-----------|-------------|
| `KpiCard` | Tarjeta con icono, valor, descripción, variación, hover state |
| `ActivityChart` | Gráfico de barras/línea de actividad diaria |
| `MineralDistribution` | Gráfico de donut/barra de distribución de minerales |
| `RiskDistribution` | Gráfico de distribución de niveles de riesgo |
| `RecentAnalyses` | Lista de los últimos análisis realizados |
| `SystemStatus` | Estado del sistema: modelos activos, cola, uptime |

### Analysis (9 componentes)

| Componente | Descripción |
|-----------|-------------|
| `ImageUploadZone` | Drag & drop + click para imágenes, preview, botón analizar |
| `VideoUploadZone` | Selector de video con nombre de archivo, botón analizar |
| `BatchUploadZone` | Selector múltiple, indicador de archivos seleccionados, botón procesar |
| `MetadataForm` | Formulario de metadatos del análisis (categoría, riesgo, ubicación, etc.) |
| `AIResultCard` | Resultado IA formateado: mineral, confianza, probabilidades |
| `AIResultVideo` | Resultado de video: hallazgos, duración, frames, PDF |
| `GradCamPreview` | Imagen del Grad-CAM con overlay de calor |
| `ConfidenceBar` | Barra de confianza visual (0-100%) |
| `RecommendationList` | Lista de recomendaciones con iconos |
| `ProcessingQueue` | Cola de procesamiento en tiempo real |

### History (3 componentes)

| Componente | Descripción |
|-----------|-------------|
| `AnalysisTable` | DataTable de análisis de imágenes con acciones |
| `VideoTable` | DataTable de análisis de video con acciones |
| `HistoryFilters` | Barra de filtros: fecha, modelo, riesgo, búsqueda |

### Hooks nuevos (5)

| Hook | Descripción |
|------|-------------|
| `useAnalysis` | Encapsula lógica de upload, análisis, resultado |
| `useVideo` | Encapsula lógica de upload de video, análisis, resultado |
| `useQueue` | Polling cada 5s de la cola de procesamiento |
| `useMediaQuery` | Detecta breakpoints responsive |
| `usePagination` | Lógica de paginación: currentPage, totalPages, handlers |

---

## 3. Wireframe del Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│ Sidebar  │  TopBar: "Dashboard"                     │ User │
│ ─────────│──────────────────────────────────────────────────│
│ ⛏ MinerIA│                                                  │
│          │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│ Inicio   │  │Análisis│ │Zonas │ │Conf. │ │Alertas│ │Videos│  │
│ Historial│  │ hoy  │ │cobre │ │prom. │ │críticas│ │proc. │  │
│          │  │  47  │ │  12  │ │ 87%  │ │   3   │ │  5   │  │
│          │  │ +8 vs │ │+3 vs │ │+2% vs│ │ -1 vs │ │+2 vs │  │
│ ─────────│  │ ayer  │ │ ayer │ │ ayer │ │ ayer  │ │ ayer │  │
│ user@... │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │
│ admin    │                                                  │
│ Cerrar   │  ┌─────────────────┐ ┌────────────────────────┐  │
│          │  │ Actividad       │ │ Distribución minerales │  │
│          │  │ ┌─────────────┐ │ │ ┌────────────────────┐ │  │
│          │  │ │ Barras      │ │ │ │ Donut / barras     │ │  │
│          │  │ │ diarias     │ │ │ │                    │ │  │
│          │  │ └─────────────┘ │ │ └────────────────────┘ │  │
│          │  └─────────────────┘ └────────────────────────┘  │
│          │                                                  │
│          │  ┌─────────────────┐ ┌────────────────────────┐  │
│          │  │ Riesgos         │ │ Últimos análisis       │  │
│          │  │ ┌─────────────┐ │ │ ┌────────────────────┐ │  │
│          │  │ │ Barras      │ │ │ │ Lista de tarjetas  │ │  │
│          │  │ │ Alto/Med/Baj│ │ │ │ con resultado IA   │ │  │
│          │  │ └─────────────┘ │ │ └────────────────────┘ │  │
│          │  └─────────────────┘ └────────────────────────┘  │
│          │                                                  │
│          │  ┌────────────────────────────────────────────┐  │
│          │  │ Estado del sistema                         │  │
│          │  │ Modelos activos: 2 · Cola: 0 · Uptime: 12h│  │
│          │  └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Comportamiento KPIs
- Cada KPI es un `KpiCard` animado al hover
- El valor principal es grande y bold
- La variación (vs ayer) tiene indicador visual: flecha verde ↑ o roja ↓
- Click en KPI filtra/explora ese aspecto

---

## 4. Wireframe del Historial

```
┌─────────────────────────────────────────────────────────────┐
│ Sidebar  │  TopBar: "Historial"                     │ User │
│ ─────────│──────────────────────────────────────────────────│
│          │  ┌──────────────────────────────────────────────┐│
│ Inicio   │  │ [Buscar...]    [Filtros ▾] [▤ Exportar]    ││
│ Historial│  └──────────────────────────────────────────────┘│
│          │                                                  │
│          │  [Imágenes] [Videos]                             │
│          │                                                  │
│          │  ┌──────────────────────────────────────────────┐│
│          │  │ Fecha ▲ │ Zona │ Categoría │ Riesgo │ Estado││
│          │  ├──────────────────────────────────────────────┤│
│          │  │ 26/06   │ Mina  │ Clasif.   │ ● Bajo │ ✅   ││
│          │  │ 25/06   │ Tajo  │ Prod.     │ ● Alto │ ❌   ││
│          │  │ 24/06   │ Zona  │ Análisis  │ ● Medio│ ⏳   ││
│          │  │ ...     │ ...   │ ...       │ ...    │ ...  ││
│          │  └──────────────────────────────────────────────┘│
│          │                                                  │
│          │  ┌──────────────────────────────────────────────┐│
│          │  │ ← Anterior  1 2 3 ... 12  Siguiente →       ││
│          │  │ Mostrando 10 de 120 análisis                 ││
│          │  └──────────────────────────────────────────────┘│
│          │                                                  │
│          │  ┌──────────────────────────────────────────────┐│
│          │  │ Resumen rápido                                ││
│          │  │ Últimos 7 días: 45 análisis · 12 con cobre  ││
│          │  │ Precisión promedio: 89.5%                    ││
│          │  └──────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Funcionalidades
- **Search**: Búsqueda por zona, categoría, responsable
- **Filters**: Por fecha (rango), riesgo, modelo, resultado
- **Sort**: Click en header de columna para ordenar
- **Pagination**: Selector de página + tamaño de página
- **Export**: Exportar a CSV/PDF (preparar estructura)
- **Responsive**: Tabla con scroll horizontal en mobile
- **Select**: Checkbox para acciones masivas (eliminar, re-analizar)

---

## 5. Roadmap de Implementación (Estado actual)

### ✅ Fase 1 — Design System y Setup (Completada)
| Actividad | Estado |
|-----------|--------|
| Configurar Tailwind extend con el Design System | ✅ |
| Implementar componentes base: Button, Input, Select, Badge | ✅ |
| Implementar Card, Heading, StatusDot, EmptyState | ✅ |
| Implementar LoadingSkeleton, Toast, Modal, TabBar | ✅ |

**Entregable:** 15 componentes UI en `src/componentes/ui/`.

### ✅ Fase 2 — Layout (Completada)
| Actividad | Estado |
|-----------|--------|
| Crear AppLayout (Disposicion), refactorizar páginas | ✅ |
| Sidebar responsivo (colapso + overlay mobile) | ✅ |
| TopBar con breadcrumbs, título dinámico | ✅ |

**Entregable:** Layout responsivo con `h-screen` corregido.

### ✅ Fase 3 — Dashboard (Completada — Iteración 2)
| Actividad | Estado |
|-----------|--------|
| KPI Strip con métricas de IA (6 KPIs) | ✅ |
| ActivityChart (gráfico de barras SVG) | ✅ |
| MineralDistribution (barras horizontales) | ✅ |
| RecentAnalyses (lista compacta) | ✅ |
| SystemAlerts (estado del sistema) | ✅ |
| Sidebar con atajo "Nuevo análisis" | ✅ |
| Código muerto eliminado (client.ts, App.css) | ✅ |
| Sidebar h-full corregido a h-screen | ✅ |

**Entregable:** Dashboard informativo con KPIs de IA, gráficos y estado del sistema.

### 🔄 Fase 4 — Wizard de análisis (Pendiente)
| Actividad | Prioridad |
|-----------|-----------|
| Crear PaginaAsistenteAnalisis con 3 pasos | Alta |
| Paso 1: Seleccionar entrada (imagen/video/lote) | Alta |
| Paso 2: Configurar (modelo + metadatos) | Alta |
| Paso 3: Resultados con visualización IA | Alta |
| Hook useWizard para estado del asistente | Media |

### ⏳ Fase 5 — Historial (Pendiente)
| Actividad | Prioridad |
|-----------|-----------|
| Barra de búsqueda + filtros | Media |
| Resumen estadístico (total, confianza prom.) | Baja |
| Acciones masivas | Baja |

### ⏳ Fase 6 — Resultados IA (Pendiente)
| Actividad | Prioridad |
|-----------|-----------|
| Rediseñar AnalysisDetailPage con ConfidenceBar | Media |
| GradCamPreview más grande | Media |
| RecommendationList visual | Baja |

### ⏳ Fase 7 — Pulido (Pendiente)
| Actividad | Prioridad |
|-----------|-----------|
| Accesibilidad (ARIA, focus, labels) | Baja |
| Animaciones y micro-interacciones | Baja |
| Lazy loading y optimización | Baja |

---

## 6. Riesgos del Refactor

| Riesgo | Probabilidad | Impacto | Plan de Mitigación |
|--------|-------------|---------|-------------------|
| **Regresión en upload de archivos** | Alta | Crítico | Pruebas manuales después de cada fase. Mantener lógica de negocio intacta. |
| **Sidebar colapsable rompe layout** | Media | Alto | Implementar con transiciones CSS, testear en 3 navegadores. |
| **DataTable no mantiene estado con backend** | Media | Medio | Paginación y filtros del lado del cliente inicialmente, migrar a server-side si es necesario. |
| **Dependencia de chart.js aumenta bundle** | Baja | Medio | Lazy loading del componente de gráficos, tree-shaking. |
| **CSS del Design System entra en conflicto** | Media | Alto | Usar Tailwind exclusivamente, no CSS personalizado. Namespacing en variables. |
| **Migración de tipos causa import errors** | Alta | Medio | Migración progresiva: crear types/ primero, luego actualizar imports uno por uno. |
| **Componentes genéricos muy rígidos** | Media | Bajo | Props extensibles con `...rest` y `className` merge. |
| **Pérdida de estado de autenticación** | Baja | Crítico | No modificar AuthProvider, solo refactorizar imports. |

---

## 7. Principios de Implementación

1. **No mezclar responsabilidades** — Un componente = una responsabilidad
2. **Composición sobre herencia** — Componentes pequeños que se componen
3. **Props explícitas** — Sin `any`, sin `defaultProps` obsoletas
4. **Extraer lógica** — Side effects a hooks, UI a componentes
5. **Tailwind primero** — Sin CSS modules, sin styled-components, sin archivos .css adicionales (excepto globals.css)
6. **Sin dependencias nuevas innecesarias** — Solo Lucide React + chart.js si es necesario
7. **Cada fase deployable** — Cada fase debe funcionar independientemente
8. **Sin cambios en backend** — No tocar ninguna ruta, endpoint, modelo o respuesta

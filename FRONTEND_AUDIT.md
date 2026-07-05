# MinerIA Frontend Audit

> Auditoría completa del frontend de MinerIA
> Fecha: 2026-06-30
> Versión del código: Iteración 2 — Dashboard rediseñado

---

## Resumen Ejecutivo

MinerIA es una aplicación React 19 + TypeScript + Vite 7 con TailwindCSS 3.4, desarrollada como un sistema de análisis de imágenes mineras con IA. El frontend actual es funcional pero presenta problemas significativos de arquitectura, escalabilidad, experiencia de usuario y calidad visual que impiden que sea percibido como un producto comercial.

**Estado actual:** 5 páginas, 20+ componentes UI, 5 hooks, 35+ archivos fuente.

---

## Arquitectura General

### Stack Tecnológico
| Capa | Tecnología | Versión |
|------|-----------|---------|
| Framework | React | 19.2.0 |
| Lenguaje | TypeScript | 5.9.3 |
| Build | Vite | 7.2.2 |
| Routing | React Router DOM | 7.9.6 |
| HTTP | Axios | 1.13.2 |
| Estilos | TailwindCSS | 3.4.18 |
| Estado | Context API | — |

### Estructura Actual
```
src/
├── api/
│   ├── analysis.ts         ← API calls + types
│   ├── apiClient.ts        ← Axios instance
│   └── auth.ts             ← Auth API + types
├── componentes/
│   ├── ui/                 ← Design System (15 componentes)
│   │   ├── BarraPestanas.tsx
│   │   ├── Boton.tsx
│   │   ├── Encabezado.tsx
│   │   ├── Entrada.tsx
│   │   ├── Esqueleto.tsx
│   │   ├── EstadoVacio.tsx
│   │   ├── Insignia.tsx
│   │   ├── Modal.tsx
│   │   ├── Notificacion.tsx
│   │   ├── Paginacion.tsx
│   │   ├── Seleccion.tsx
│   │   ├── TablaDatos.tsx
│   │   ├── Tarjeta.tsx
│   │   └── index.ts
│   ├── layout/              ← Layout components
│   │   ├── Disposicion.tsx  ← AppLayout (h-screen corregido)
│   │   ├── BarraLateral.tsx ← Sidebar responsivo
│   │   └── BarraSuperior.tsx← TopBar con breadcrumbs
│   ├── dashboard/           ← Dashboard components (NUEVO)
│   │   ├── TarjetaKpi.tsx
│   │   ├── ActividadReciente.tsx
│   │   ├── DistribucionMineral.tsx
│   │   ├── UltimosAnalisis.tsx
│   │   ├── AlertasSistema.tsx
│   │   └── index.ts
│   └── panel/               ← Legacy analysis components
│       ├── CuadriculaKpi.tsx
│       ├── CamposFormularioMeta.tsx
│       ├── SeccionSubidaImagen.tsx
│       ├── SeccionSubidaVideo.tsx
│       ├── SeccionSubidaLote.tsx
│       ├── PanelResultado.tsx
│       ├── PanelResultadoVideo.tsx
│       └── PanelCola.tsx
├── context/
│   ├── AuthContext.tsx
│   ├── AuthProvider.tsx
│   └── useAuth.ts
├── hooks/
│   ├── usarMediaQuery.ts
│   ├── usarSidebar.ts
│   └── index.ts
├── paginas/
│   ├── PaginaInicioSesion.tsx ← Login
│   ├── PaginaPanel.tsx        ← Dashboard (rediseñado, ~100 líneas)
│   ├── PaginaNuevoAnalisis.tsx← Wizard placeholder (Fase 4)
│   ├── PaginaHistorial.tsx    ← DataTable con sort/paginación
│   ├── PaginaDetalleAnalisis.tsx ← Resultados IA
│   └── PaginaNoEncontrada.tsx ← 404
├── styles/
├── theme/                     ← (vacío, preparado)
├── types/                     ← (vacío, preparado)
├── constants/                 ← (vacío, preparado)
├── utils/
│   └── cn.ts
├── App.tsx                    ← Routing + App shell
├── index.css                  ← Tailwind directives + CSS variables
└── main.tsx                   ← Entry point
```

---

## Problemas Encontrados

### 🔴 Críticos (Historial — Resueltos en Iteración 1)

#### ~~1. DashboardPage monolítico~~ ✅ RESUELTO
Dashboard refactorizado a componentes modulares. Ahora ~100 líneas de composición pura.

#### ~~2. Layout repetido~~ ✅ RESUELTO
Extraído a `Disposicion.tsx` (AppLayout) con `<Outlet />`.

#### ~~3. Axios client duplicado~~ ✅ RESUELTO
`client.ts` eliminado.

#### ~~5. Sin sistema de diseño~~ ✅ RESUELTO
Tailwind extend completo con colores, tipografía, sombras, radios. 15 componentes UI.

### 🟡 Pendientes de Iteración 2

### 🟡 Altos

#### 6. Sin tipografía definida
Usa `font-family` del sistema sin jerarquía tipográfica. Los tamaños son arbitrarios (`text-xs`, `text-sm`, `text-xl`) sin escala consistente.

#### 7. Sin sombras ni elevación
Solo `shadow-2xl` en la tarjeta de login. El resto de la UI es completamente plana. Sin jerarquía visual entre elementos.

#### 8. Sin animaciones ni transiciones
No hay micro-interacciones. Los estados de carga son texto plano ("Analizando..."). Sin feedback visual para acciones del usuario.

#### 9. Sidebar no responsiva
La barra lateral de 256px siempre está visible. En tablets o móviles, el contenido principal se comprime. No hay menú hamburguesa ni colapso automático.

#### 10. Tablas sin funcionalidad básica
- Sin paginación
- Sin ordenamiento de columnas
- Sin búsqueda/filtros
- Sin sticky header
- Sin responsive (horizontal scroll en móvil)

#### 11. Sin estados de carga visuales
No hay skeletons, spinners o placeholders. Solo texto "Cargando..." o "Analizando...".

#### 12. Código muerto: App.css
El archivo `App.css` contiene estilos boilerplate de Vite (`.logo`, `.card`, `.read-the-docs`, `@keyframes logo-spin`) que no se usan en ningún componente.

#### 13. LoginPage: año hardcodeado
`© 2025 MinerIA` — el año no se actualiza dinámicamente.

#### 14. index.html: lang="en"
El atributo `lang` está en inglés para una aplicación completamente en español.

### 🟢 Medios

#### 15. Sin loading states en uploads
No hay barras de progreso para uploads de imágenes o videos. El usuario no sabe si el archivo se está subiendo o procesando.

#### 16. Sin preview de Grad-CAM
Aunque el backend devuelve `gradcamUrl`, el frontend nunca lo muestra. El análisis detallado tampoco lo incluye.

#### 17. Sin notificaciones/toasts
Los errores se muestran como alertas inline o `alert()` de JavaScript. No hay sistema de notificaciones.

#### 18. Sin error boundaries
Cualquier error en un componente rompe toda la página. Sin fallback UI.

#### 19. Sin paginación en historial
La API devuelve hasta 200 registros, pero el frontend no paginó. En producción esto sería inmanejable.

#### 20. Sin accesibilidad
- Sin atributos ARIA
- Sin `aria-label` en iconos/botones
- Sin `role` en elementos interactivos
- Sin `aria-current` en navegación activa
- Sin `tabIndex` explícito
- Contraste cuestionable en algunos textos pequeños

#### 21. Sin iconografía
Usa el emoji ⛏ en lugar de un icono vectorial profesional. Sin librería de iconos.

#### 22. Download PDF duplicado
`downloadVideoPdf()` en `analysis.ts` usa Axios con blob. `handleDownloadPdf()` en `AnalysisDetailPage.tsx` usa `fetch()` nativo. Misma lógica, dos implementaciones.

#### 23. Base URL resuelta en 4 lugares
`VITE_API_URL` se resuelve en `apiClient.ts`, `client.ts`, `DashboardPage.tsx` y `AnalysisDetailPage.tsx`.

---

## Fortalezas

A pesar de los problemas, el frontend tiene bases sólidas:

1. **TypeScript estricto** — `noUnusedLocals` y `noUnusedParameters` habilitados.
2. **React 19** — Versión moderna con soporte a futuro.
3. **Vite 7** — Build rápido, HMR eficiente.
4. **Router v7** — Routing moderno con soporte de loaders y acciones.
5. **Context API** — Suficiente para el estado actual (sin over-engineering).
6. **Separación API** — Llamadas HTTP en archivos dedicados.
7. **Interceptor JWT** — Token management centralizado en Axios.
8. **Funcionalidad completa** — Login, upload, análisis, historial, videos, batch processing.

---

## Componentes Actuales vs. Necesarios

### Existentes (3)
| Componente | Archivo | Líneas | Estado |
|-----------|---------|--------|--------|
| Sidebar | `components/layout/Sidebar.tsx` | 59 | Funcional, no responsive |
| TopBar | `components/layout/TopBar.tsx` | 17 | Funcional, título hardcodeado |
| PrivateRoute | `App.tsx` (inline) | 6 | Funcional |

### Necesarios (por crear)
| Componente | Razón |
|-----------|-------|
| `Layout` | Eliminar duplicación de estructura |
| `MetricCard` | KPIs actualmente hardcodeados |
| `UploadZone` | Drag & drop reutilizable |
| `AIResultCard` | Resultados IA con diseño profesional |
| `DataTable` | Tablas con paginación, sorting, filtros |
| `StatusBadge` | Indicadores de estado reutilizables |
| `EmptyState` | Estado vacío consistente |
| `LoadingSkeleton` | Esqueletos de carga |
| `Alert / Toast` | Notificaciones del sistema |
| `Modal` | Diálogos modales |
| `Button` | Botón con variantes, loading, iconos |
| `Input / Select` | Formularios con estados |
| `TabBar` | Tabs reutilizables |
| `Pagination` | Paginación de datos |
| `ChartCard` | Contenedor para gráficos |
| `ProgressBar` | Indicador de progreso para uploads |

---

## Problemas de UX

1. **Dashboard sin datos reales** — KPIs hardcodeados, no conectados a backend.
2. **Sin jerarquía visual** — Todo tiene el mismo nivel de importancia.
3. **Resultados IA pobres** — Texto plano sin formato, sin visualización de confianza.
4. **Upload sin feedback** — No hay drag & drop visual, no hay progreso.
5. **Historial plano** — Sin métricas, sin resúmenes, sin búsqueda.
6. **Sin onboarding** — El usuario no sabe qué hacer al entrar.
7. **Estados vacíos genéricos** — "No hay análisis registrados" sin ilustración ni call to action.
8. **Sin diferenciación de roles** — Admin y analyst ven exactamente lo mismo.
9. **Navegación limitada** — Solo 2 rutas en el sidebar.

---

## Problemas de UI

1. **Paleta de colores inconsistente** — Slate + Blue + Emerald + Amber + Rose sin sistema.
2. **Sin tipografía de marca** — Font-family del sistema.
3. **Bordes mezclados** — `rounded-lg`, `rounded-xl`, `rounded-2xl` sin criterio.
4. **Sin sombras** — Tarjetas planas sin profundidad.
5. **Icono emoji** — ⛏ no escala bien en diferentes resoluciones.
6. **TopBar hardcodeado** — "Panel de Control" y "Versión demo frontend" fijos.
7. **Login con fondo geométrico artesanal** — Patrón CSS manual en vez de diseño intencional.
8. **Sin favicon personalizado** — Usa el SVG de Vite.

---

## Problemas de Accesibilidad

| Issue | Ubicación | Severidad |
|-------|-----------|-----------|
| Sin `aria-label` en botones | Sidebar, TopBar, Dashboard | Alta |
| Sin `aria-current` en nav | Sidebar (`NavLink`) | Media |
| Contraste bajo | `text-slate-400` sobre `bg-white` (4.5:1 en algunos tamaños) | Media |
| Sin `role` en elementos clickeables | Upload zones, botones | Alta |
| Sin `htmlFor` en labels | Todos los formularios | Alta |
| Sin manejo de foco | Sidebar, modales | Media |
| Sin `lang="es"` | `index.html` | Baja |
| Sin skip navigation | Toda la app | Alta |

---

## Problemas de Responsive

| Breakpoint | Problema |
|-----------|---------|
| Mobile (< 768px) | Sidebar ocupa 256px sin opción de colapsar |
| Tablet (768-1024px) | Grid de KPIs se apila, sidebar comprime contenido |
| Desktop (> 1024px) | Funciona correctamente |
| General | Sin media queries consistentes, layout rígido |
| Tablas | Sin horizontal scroll, se rompen en mobile |

---

## Propuesta de Mejora

### Inmediatas (sin refactor mayor)
1. Eliminar `client.ts` (no usado) y `App.css` (código muerto)
2. Centralizar tipos en `types/`
3. Extraer layout a componente `DashboardLayout`
4. Cambiar `lang="en"` a `lang="es"` en `index.html`
5. Agregar `htmlFor` en labels de formularios
6. Actualizar año en LoginPage dinámicamente

### Corto Plazo (Fase 1-2 del rediseño)
1. Crear Design System con variables CSS y Tailwind extend
2. Implementar componentes base (Button, Input, Select, Badge, Card)
3. Rediseñar Layout (Sidebar + TopBar responsivos)
4. Agregar Lucide React como librería de iconos
5. Implementar sistema de notificaciones (Toast)

### Mediano Plazo (Fase 3-4)
1. Rediseñar Dashboard con KPIs reales y gráficos
2. Rediseñar Historial con DataTable completa
3. Agregar skeletons y loading states
4. Implementar Error Boundaries

### Largo Plazo (Fase 5-6)
1. Rediseñar páginas de detalle
2. Agregar preview de Grad-CAM
3. Agregar animaciones de transición
4. Accesibilidad WCAG completa
5. Pruebas responsivas exhaustivas

---

## Riesgos del Refactor

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|-----------|
| Romper rutas existentes | Baja | Alto | No modificar router, solo componentes |
| Perder funcionalidad de upload | Media | Alto | Pruebas manuales después de cada fase |
| Introducir regresión visual | Alta | Medio | Comparar screenshots antes/después |
| Dependencias nuevas (Lucide) | Baja | Bajo | Solo añadir, no migrar dependencias existentes |
| Tiempo de implementación | Alta | Medio | Entregar por fases con aprobación |
| Curva de aprendizaje del equipo | Media | Bajo | Documentar componentes en DESIGN_SYSTEM.md |
| Problemas de rendimiento | Baja | Medio | Usar React.memo y lazy loading si es necesario |

---

## Conclusión

El frontend de MinerIA tiene una base técnica sólida (TypeScript, React 19, Vite 7) pero carece de la madurez de producto necesaria para ser comercial. Los problemas principales son:

1. **Arquitectura**: Monolito Dashboard, layout duplicado, tipos dispersos
2. **UX**: Sin feedback, sin estados de carga, KPIs hardcodeados
3. **UI**: Sin sistema de diseño, colores inconsistentes, icono emoji
4. **Accesibilidad**: Múltiples violaciones WCAG
5. **Responsive**: Sidebar no colapsable, tablas sin scroll

El rediseño debe enfocarse en transformar la percepción de "proyecto académico" a "producto SaaS profesional" manteniendo toda la funcionalidad existente intacta.

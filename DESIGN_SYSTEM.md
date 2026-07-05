# MinerIA Design System

> Sistema de diseño para MinerIA — SaaS de Inteligencia Artificial para minería
> Inspirado en: Linear, Vercel, GitHub, Azure AI Studio, Supabase

---

## Filosofía Visual

MinerIA debe comunicar:

- **Tecnología e innovación** — Visual moderno, limpio, preciso
- **Confianza y solidez** — Tipografía clara, espaciado generoso, jerarquía visual
- **Profesionalismo** — Consistencia obsesiva, sin elementos fuera de lugar
- **Industria minera** — Toques sutiles de la industria sin caer en lo genérico

La interfaz debe sentirse como una herramienta de trabajo, no como un dashboard de marketing. Cada píxel debe tener un propósito.

---

## 1. Colores

### Primary (Azul — Identidad principal)
Mantener el azul como color primario. Representa tecnología, confianza y minería.

| Token | Hex | RGB | Uso |
|-------|-----|-----|-----|
| `--color-primary-50` | `#EFF6FF` | rgb(239,246,255) | Background hover, alertas suaves |
| `--color-primary-100` | `#DBEAFE` | rgb(219,234,254) | Background selección |
| `--color-primary-200` | `#BFDBFE` | rgb(191,219,254) | Bordes hover |
| `--color-primary-300` | `#93C5FD` | rgb(147,197,253) | Bordes activos |
| `--color-primary-400` | `#60A5FA` | rgb(96,165,250) | Link hover |
| `--color-primary-500` | `#3B82F6` | rgb(59,130,246) | Links, iconos |
| `--color-primary-600` | `#2563EB` | rgb(37,99,235) | Botones primarios, activos |
| `--color-primary-700` | `#1D4ED8` | rgb(29,78,216) | Botones hover |
| `--color-primary-800` | `#1E40AF` | rgb(30,64,175) | Texto primary |
| `--color-primary-900` | `#1E3A8A` | rgb(30,58,138) | Deep accent |

### Neutral (Gris — Base del sistema)

| Token | Hex | RGB | Uso |
|-------|-----|-----|-----|
| `--color-neutral-50` | `#F8FAFC` | rgb(248,250,252) | Page background |
| `--color-neutral-100` | `#F1F5F9` | rgb(241,245,249) | Card background, section bg |
| `--color-neutral-200` | `#E2E8F0` | rgb(226,232,240) | Border default |
| `--color-neutral-300` | `#CBD5E1` | rgb(203,213,225) | Border hover |
| `--color-neutral-400` | `#94A3B8` | rgb(148,163,184) | Placeholder, disabled text |
| `--color-neutral-500` | `#64748B` | rgb(100,116,139) | Secondary text |
| `--color-neutral-600` | `#475569` | rgb(71,85,105) | Body text |
| `--color-neutral-700` | `#334155` | rgb(51,65,85) | Heading text |
| `--color-neutral-800` | `#1E293B` | rgb(30,41,59) | High emphasis text |
| `--color-neutral-900` | `#0F172A` | rgb(15,23,42) | Sidebar background, dark surfaces |

### Success (Verde)

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-success-50` | `#F0FDF4` | Background |
| `--color-success-100` | `#DCFCE7` | Background hover |
| `--color-success-500` | `#22C55E` | Status dot, icon |
| `--color-success-600` | `#16A34A` | Badge, text |

### Warning (Ámbar)

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-warning-50` | `#FFFBEB` | Background |
| `--color-warning-100` | `#FEF3C7` | Background hover |
| `--color-warning-500` | `#F59E0B` | Status dot, icon |
| `--color-warning-600` | `#D97706` | Badge, text |

### Danger (Rojo)

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-danger-50` | `#FEF2F2` | Background |
| `--color-danger-100` | `#FEE2E2` | Background hover |
| `--color-danger-500` | `#EF4444` | Status dot, icon |
| `--color-danger-600` | `#DC2626` | Badge, text |

### Info (Celeste)

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-info-50` | `#ECFEFF` | Background |
| `--color-info-500` | `#06B6D4` | Status dot, icon |
| `--color-info-600` | `#0891B2` | Badge, text |

---

## 2. Tipografía

### Font Family
```css
font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

Inter es una fuente diseñada específicamente para interfaces de pantalla, con excelente legibilidad en pesos livianos y tamaños pequeños.

### Escala Tipográfica

| Token | Size | Line Height | Weight | Tracking | Uso |
|-------|------|-------------|--------|----------|-----|
| `text-heading-xl` | 30px / 1.875rem | 1.2 | 700 (bold) | -0.025em | Page titles |
| `text-heading-lg` | 24px / 1.5rem | 1.3 | 600 (semibold) | -0.02em | Section titles |
| `text-heading-md` | 20px / 1.25rem | 1.4 | 600 (semibold) | -0.015em | Card titles |
| `text-body` | 14px / 0.875rem | 1.5 | 400 (regular) | normal | Body text |
| `text-body-bold` | 14px / 0.875rem | 1.5 | 600 (semibold) | normal | Body emphasis |
| `text-small` | 13px / 0.8125rem | 1.5 | 400 (regular) | normal | Secondary text |
| `text-caption` | 12px / 0.75rem | 1.5 | 400 (regular) | normal | Labels, metadata |
| `text-caption-bold` | 12px / 0.75rem | 1.5 | 500 (medium) | normal | Badge text |
| `text-overline` | 11px / 0.6875rem | 1.5 | 500 (medium) | 0.05em | Overline, uppercase |

---

## 3. Espaciado

Escala estricta de 8px basada en potencia de 2:

| Token | Rem | Pixels | Uso |
|-------|-----|--------|-----|
| `space-1` | 0.25rem | 4px | Icon padding interno |
| `space-2` | 0.5rem | 8px | Gap entre elementos relacionados |
| `space-3` | 0.75rem | 12px | Padding input, gap secciones pequeñas |
| `space-4` | 1rem | 16px | Padding tarjetas, gap estándar |
| `space-5` | 1.25rem | 20px | Padding formularios |
| `space-6` | 1.5rem | 24px | Gap entre secciones |
| `space-8` | 2rem | 32px | Padding contenedores |
| `space-10` | 2.5rem | 40px | Gap entre páginas |
| `space-12` | 3rem | 48px | Padding página |
| `space-16` | 4rem | 64px | Gap secciones mayores |

**Regla:** Nunca usar valores fuera de esta escala.

---

## 4. Bordes

| Token | Radius | Uso |
|-------|--------|-----|
| `radius-sm` | 4px | Inputs, botones pequeños |
| `radius-md` | 6px | Badges, chips |
| `radius-lg` | 8px | Tarjetas, paneles |
| `radius-xl` | 12px | Modales, tarjetas grandes |
| `radius-2xl` | 16px | Sidebar, login card |
| `radius-full` | 9999px | Avatars, status dots |

---

## 5. Sombras

| Token | Elevación | Uso |
|-------|-----------|-----|
| `shadow-xs` | 0 1px 2px rgba(0,0,0,0.05) | Cards en estado normal |
| `shadow-sm` | 0 1px 3px rgba(0,0,0,0.08) | Cards hover, inputs focus |
| `shadow-md` | 0 4px 6px rgba(0,0,0,0.07) | Dropdowns, popovers |
| `shadow-lg` | 0 10px 15px rgba(0,0,0,0.08) | Modales, sidebars flotantes |
| `shadow-xl` | 0 20px 25px rgba(0,0,0,0.10) | Toast, notificaciones |
| `shadow-inner` | inset 0 2px 4px rgba(0,0,0,0.05) | Inputs focus, estados activos |

---

## 6. Iconografía

**Librería exclusiva:** [Lucide React](https://lucide.dev/)

Prohibido mezclar con otras librerías o usar emojis como iconos.

### Iconos requeridos
| Contexto | Icono |
|----------|-------|
| Logo MinerIA | `Pickaxe` |
| Dashboard | `LayoutDashboard` |
| History | `History` |
| Upload | `Upload`, `FileUp` |
| Image | `Image` |
| Video | `Video` |
| AI / Brain | `Brain`, `Cpu` |
| Copper | `Cable`, `Zap` |
| Check | `CheckCircle2`, `Check` |
| Alert | `AlertTriangle`, `AlertCircle` |
| Download | `Download` |
| Search | `Search` |
| Filter | `Filter` |
| Sort | `ArrowUpDown` |
| User | `UserCircle2` |
| Logout | `LogOut` |
| Settings | `Settings` |
| Chevron | `ChevronRight`, `ChevronLeft` |
| Close | `X` |
| Menu | `Menu` |
| Loading | `Loader2` (con animate-spin) |
| Empty | `Inbox` |
| Error | `AlertTriangle` |
| Success | `CheckCircle2` |
| Warning | `AlertCircle` |
| Info | `Info` |
| Risk | `ShieldAlert` |
| Confidence | `Gauge` |
| Clock | `Clock` |
| Calendar | `Calendar` |

---

## 7. Transiciones y Animaciones

Duración máxima: 250ms. Nunca animaciones exageradas.

| Token | Duración | Uso |
|-------|---------|-----|
| `duration-fast` | 150ms | Hover, active states |
| `duration-normal` | 200ms | Transiciones estándar |
| `duration-slow` | 250ms | Modales, sidebars |

Easing:
```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
```

---

## 8. Componentes Base

### Button
| Prop | Opciones |
|------|---------|
| Variant | `primary`, `secondary`, `outline`, `ghost`, `danger` |
| Size | `sm` (32px), `md` (40px), `lg` (48px) |
| States | default, hover, active, disabled, loading |
| Icon | Optional left/right icon slot |

### Input
| Prop | Opciones |
|------|---------|
| Variant | `outline`, `filled` |
| Size | `sm`, `md`, `lg` |
| States | default, hover, focus, error, disabled, success |
| Elementos | label, input, helper text, error message, icon prefix |

### Select
Mismos estados que Input, con chevron icon personalizado.

### Badge
| Prop | Opciones |
|------|---------|
| Variant | `primary`, `success`, `warning`, `danger`, `info`, `neutral` |
| Size | `sm`, `md` |
| Dot | Optional status dot |

### Card
| Prop | Opciones |
|------|---------|
| Variant | `default` (bordered), `elevated` (shadow), `flat` (no border) |
| Padding | `none`, `sm`, `md`, `lg` |
| Elements | header, body, footer |

### DataTable
| Feature | Descripción |
|---------|-------------|
| Header | Sticky, con sorting indicators |
| Rows | Hover state, striped optional |
| Pagination | Page size selector, prev/next |
| Empty | Estado vacío con icono y mensaje |
| Loading | Skeleton rows |
| Responsive | Horizontal scroll en mobile |

### Dashboard Components (src/componentes/dashboard/)

| Componente | Archivo | Descripción |
|-----------|---------|-------------|
| `KpiCard` | `TarjetaKpi.tsx` | KPI con icono, valor, label, cambio %, borde izquierdo de color |
| `ActivityChart` | `ActividadReciente.tsx` | Gráfico de barras SVG, 7 días, responsive |
| `MineralDistribution` | `DistribucionMineral.tsx` | Barras horizontales con color y porcentaje |
| `RecentAnalyses` | `UltimosAnalisis.tsx` | Lista compacta con zona, ley Cu, confianza, badge riesgo, acción ver |
| `SystemAlerts` | `AlertasSistema.tsx` | Lista de estado del sistema con iconos y StatusDot |

---

## 9. Layout

### Sidebar
| Estado | Ancho | Descripción |
|--------|-------|-------------|
| Expanded | 240px | Estado por defecto en desktop |
| Collapsed | 64px | Solo iconos, activable por toggle |
| Mobile | Overlay | Full-width overlay con backdrop |

### TopBar
Altura fija de 56px (h-14). Contenido variable según página.

### Main Content
Padding: 24px (p-6) consistente en todas las páginas.

---

## 10. Breakpoints Responsive

| Alias | Min Width | Target |
|-------|-----------|--------|
| `sm` | 640px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 1024px | Desktop |
| `xl` | 1280px | Desktop wide |
| `2xl` | 1536px | Ultra-wide |

---

## 11. Modo Claro / Oscuro

Inicialmente solo modo claro. Preparar variables CSS para modo oscuro futuro:

```css
[data-theme="dark"] {
  --color-neutral-50: #0F172A;
  --color-neutral-100: #1E293B;
  /* ... */
}
```

No implementar hasta fase 6.

---

## 12. Implementación Técnica

### TailwindCSS Extend
El Design System se implementa como extensión del `theme` en `tailwind.config.js`:

```js
theme: {
  extend: {
    colors: { ... },
    fontFamily: { ... },
    fontSize: { ... },
    spacing: { ... },
    borderRadius: { ... },
    boxShadow: { ... },
    transitionDuration: { ... },
    transitionTimingFunction: { ... },
  }
}
```

### CSS Variables
Las variables CSS se definen en `:root` dentro de `index.css` para acceso desde JavaScript si es necesario.

### Componentes React
Cada componente del Design System se implementa como un componente React puro, sin dependencias externas excepto Lucide React para iconos.

---

## 13. Ejemplos de Uso

```tsx
// Botón primario con icono
<Button variant="primary" size="md" icon={<Upload />}>
  Subir imagen
</Button>

// Badge de estado
<Badge variant="success" dot>
  Conectado
</Badge>

// Card con header
<Card padding="md">
  <Card.Header>
    <Heading size="md">Resultados IA</Heading>
  </Card.Header>
  <Card.Body>
    <p className="text-body">...</p>
  </Card.Body>
</Card>

// Input con error
<Input
  label="Ubicación"
  error="La ubicación es requerida"
  placeholder="Mina Norte - Zona A3"
/>
```

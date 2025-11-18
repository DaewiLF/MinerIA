# MinerIA

Frontend en React + TypeScript + TailwindCSS para el proyecto **MinerIA**, una plataforma para análisis de imágenes de muestras minerales mediante Inteligencia Artificial.

## Tecnologías principales

- React + TypeScript
- Vite
- TailwindCSS
- Axios
- Context API para autenticación
- Comunicación con backend FastAPI (API REST)

---

# Información técnica del template (React + TypeScript + Vite)

Esta plantilla proporciona la configuración base para trabajar con React en Vite, incluyendo HMR y reglas ESLint.

## Plugins oficiales disponibles:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc)

## React Compiler

El compilador no viene activado por defecto debido a impacto en performance.  
Guía oficial: https://react.dev/learn/react-compiler/installation

## Expandiendo ESLint (opcional)

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      tseslint.configs.recommendedTypeChecked,
      tseslint.configs.strictTypeChecked,
      tseslint.configs.stylisticTypeChecked,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
])

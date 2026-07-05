-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 18-11-2025 a las 22:01:34
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_integracion`
--
CREATE DATABASE IF NOT EXISTS `proyecto_integracion` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
USE `proyecto_integracion`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clasificaciones`
--

DROP TABLE IF EXISTS `clasificaciones`;
CREATE TABLE IF NOT EXISTS `clasificaciones` (
  `id_clasificacion` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_imagen` int UNSIGNED NOT NULL,
  `resultado` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `confianza` decimal(5,4) DEFAULT NULL,
  `es_correcto` tinyint(1) DEFAULT NULL,
  `fecha_clasificacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modelo_usado` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'CNN',
  PRIMARY KEY (`id_clasificacion`),
  KEY `idx_clasificaciones_imagen` (`id_imagen`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `clasificaciones`
--

INSERT INTO `clasificaciones` (`id_clasificacion`, `id_imagen`, `resultado`, `confianza`, `es_correcto`, `fecha_clasificacion`, `modelo_usado`) VALUES
(1, 1, 'sin_cobre', 9.9999, NULL, '2025-11-15 18:20:44', 'CNN'),
(2, 2, 'sin_cobre', 9.9999, NULL, '2025-11-15 18:23:14', 'CNN'),
(3, 3, 'con_cobre', 9.9999, NULL, '2025-11-15 18:44:37', 'CNN'),
(4, 4, 'con_cobre', 9.9999, NULL, '2025-11-15 18:45:27', 'CNN'),
(5, 5, 'sin_cobre', 9.9999, NULL, '2025-11-15 22:09:20', 'CNN'),
(6, 6, 'sin_cobre', 9.9999, NULL, '2025-11-15 22:10:30', 'CNN'),
(7, 7, 'sin_cobre', 9.9999, NULL, '2025-11-17 16:30:59', 'CNN'),
(8, 8, 'con_cobre', 9.9999, NULL, '2025-11-17 16:47:48', 'CNN'),
(9, 9, 'con_cobre', 9.9999, NULL, '2025-11-17 20:28:57', 'CNN');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `errores`
--

DROP TABLE IF EXISTS `errores`;
CREATE TABLE IF NOT EXISTS `errores` (
  `id_error` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_reporte` int UNSIGNED NOT NULL,
  `descripcion` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_reporte` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `resuelto` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_error`),
  KEY `idx_errores_reporte` (`id_reporte`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagenes`
--

DROP TABLE IF EXISTS `imagenes`;
CREATE TABLE IF NOT EXISTS `imagenes` (
  `id_imagen` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_usuario` int UNSIGNED NOT NULL,
  `ruta_archivo` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `tamano` int UNSIGNED NOT NULL,
  `formato` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_carga` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('pendiente','procesada','error') COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'pendiente',
  PRIMARY KEY (`id_imagen`),
  KEY `idx_imagenes_usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `imagenes`
--

INSERT INTO `imagenes` (`id_imagen`, `id_usuario`, `ruta_archivo`, `tamano`, `formato`, `fecha_carga`, `estado`) VALUES
(1, 2, 'uploads\\ab7a2f8648ea4818bd0983a7519f5887.png', 1716735, 'image/png', '2025-11-15 18:20:44', 'procesada'),
(2, 2, 'uploads\\4042dec2ce6f4948bc29b5a4d62f3982.jpg', 232844, 'image/jpeg', '2025-11-15 18:23:14', 'procesada'),
(3, 2, 'uploads\\2fa88ea2340e4fb9906dd4db0b0dfc7d.jpg', 529200, 'image/jpeg', '2025-11-15 18:44:37', 'procesada'),
(4, 2, 'uploads\\6295d12af3ed42dd9f084562e26154bd.jpeg', 81589, 'image/jpeg', '2025-11-15 18:45:27', 'procesada'),
(5, 2, 'uploads\\842fe1011ebe4e788edae79c83467e35.jpg', 529997, 'image/jpeg', '2025-11-15 22:09:20', 'procesada'),
(6, 2, 'uploads\\809951b67eeb42fb93fb1b00eed9de7f.jpg', 529997, 'image/jpeg', '2025-11-15 22:10:30', 'procesada'),
(7, 2, 'uploads\\6e2ea542a9c64c08b5cc9e2c44299fca.jpg', 601089, 'image/jpeg', '2025-11-17 16:30:59', 'procesada'),
(8, 2, 'uploads\\dcc56cbf92714ff992c7fc13340ee185.jpeg', 81589, 'image/jpeg', '2025-11-17 16:47:48', 'procesada'),
(9, 2, 'uploads\\71175823913048aca4b9dedf8583c123.jpeg', 81589, 'image/jpeg', '2025-11-17 20:28:57', 'procesada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
--

DROP TABLE IF EXISTS `notificaciones`;
CREATE TABLE IF NOT EXISTS `notificaciones` (
  `id_notificacion` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_imagen` int UNSIGNED NOT NULL,
  `id_clasificacion` int UNSIGNED DEFAULT NULL,
  `tipo` enum('formato_invalido','fallo_clasificacion','exito') COLLATE utf8mb4_spanish_ci NOT NULL,
  `mensaje` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_notificacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `enviada` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_notificacion`),
  KEY `idx_notificaciones_imagen` (`id_imagen`),
  KEY `idx_notificaciones_clasificacion` (`id_clasificacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `predicciones`
--

DROP TABLE IF EXISTS `predicciones`;
CREATE TABLE IF NOT EXISTS `predicciones` (
  `id_prediccion` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_clasificacion` int UNSIGNED NOT NULL,
  `resultado_en_base_datos` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_almacenamiento` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_prediccion`),
  KEY `idx_predicciones_clasificacion` (`id_clasificacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cola_analisis`
--

DROP TABLE IF EXISTS `cola_analisis`;
CREATE TABLE IF NOT EXISTS `cola_analisis` (
  `id_cola` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_usuario` int UNSIGNED NOT NULL,
  `ruta_archivo` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `tamano` int UNSIGNED NOT NULL,
  `formato` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL,
  `metadata_json` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `modelo_id` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'copper',
  `estado` enum('pendiente','procesando','completado','error') COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'pendiente',
  `error` text COLLATE utf8mb4_spanish_ci,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_procesamiento` datetime DEFAULT NULL,
  PRIMARY KEY (`id_cola`),
  KEY `idx_cola_usuario` (`id_usuario`),
  KEY `idx_cola_estado` (`estado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagenes_panorama`
--

DROP TABLE IF EXISTS `imagenes_panorama`;
CREATE TABLE IF NOT EXISTS `imagenes_panorama` (
  `id_panorama` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_usuario` int UNSIGNED NOT NULL,
  `ruta_archivo` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `ancho_original` int UNSIGNED NOT NULL,
  `alto_original` int UNSIGNED NOT NULL,
  `patch_size` int UNSIGNED NOT NULL DEFAULT '224',
  `overlap` int UNSIGNED NOT NULL DEFAULT '32',
  `total_patches` int UNSIGNED NOT NULL DEFAULT '0',
  `fecha_carga` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_panorama`),
  KEY `idx_panorama_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parches_panorama`
--

DROP TABLE IF EXISTS `parches_panorama`;
CREATE TABLE IF NOT EXISTS `parches_panorama` (
  `id_parche` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_panorama` int UNSIGNED NOT NULL,
  `ruta_parche` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `x_min` int NOT NULL,
  `y_min` int NOT NULL,
  `x_max` int NOT NULL,
  `y_max` int NOT NULL,
  `fila` int UNSIGNED NOT NULL DEFAULT '0',
  `columna` int UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_parche`),
  KEY `idx_parches_panorama` (`id_panorama`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes`
--

DROP TABLE IF EXISTS `reportes`;
CREATE TABLE IF NOT EXISTS `reportes` (
  `id_reporte` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_clasificacion` int UNSIGNED NOT NULL,
  `contenido` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_generacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `formato_reporte` enum('pdf','html','json') COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'pdf',
  PRIMARY KEY (`id_reporte`),
  UNIQUE KEY `uq_reportes_id_clasificacion` (`id_clasificacion`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `reportes`
--

INSERT INTO `reportes` (`id_reporte`, `id_clasificacion`, `contenido`, `fecha_generacion`, `formato_reporte`) VALUES
(1, 8, '{\"id\": 8, \"date\": \"2025-11-17T16:47:48\", \"zone\": \"Mina 3\", \"category\": \"Clasificación Mineral\", \"riskLevel\": \"Bajo\", \"copperGrade\": \"Presencia de cobre detectada (9975.0 % de confianza)\", \"aiSummary\": \"Se detecta PRESENCIA de vetas de cobre en la imagen con una confianza de 9975.0%. Zona: Mina 3. Nivel de riesgo declarado: Bajo. Responsable del registro: Geo. Personal involucrado: 3.\", \"recommendations\": [\"Derivar el registro al área de geología para evaluación detallada.\", \"Actualizar el modelo geológico de la zona con esta evidencia.\", \"Priorizar esta zona en el plan de explotación según los lineamientos de la faena.\"], \"metadata\": {\"category\": \"Clasificación Mineral\", \"riskLevel\": \"Bajo\", \"location\": \"Mina 3\", \"coordinates\": \"234234234234\", \"responsible\": \"Geo\", \"personnel\": 3, \"modelo\": \"CopperCNN\", \"confianza_porcentaje\": 9975.0}, \"imageUrl\": \"/uploads/dcc56cbf92714ff992c7fc13340ee185.jpeg\", \"status\": \"con_cobre\", \"pdfPath\": \"reports\\\\reporte_8.pdf\"}', '2025-11-17 16:47:48', 'pdf'),
(2, 9, '{\"id\": 9, \"date\": \"2025-11-17T20:28:57\", \"zone\": \"Mina 3\", \"category\": \"Producción Activa\", \"riskLevel\": \"Alto\", \"copperGrade\": \"Presencia de cobre detectada (9975.0 % de confianza)\", \"aiSummary\": \"Se detecta PRESENCIA de vetas de cobre en la imagen con una confianza de 9975.0%. Zona: Mina 3. Nivel de riesgo declarado: Alto. Responsable del registro: JANSOIDE. Personal involucrado: 10.\", \"recommendations\": [\"Derivar el registro al área de geología para evaluación detallada.\", \"Actualizar el modelo geológico de la zona con esta evidencia.\", \"Priorizar esta zona en el plan de explotación según los lineamientos de la faena.\"], \"metadata\": {\"category\": \"Producción Activa\", \"riskLevel\": \"Alto\", \"location\": \"Mina 3\", \"coordinates\": \"234234234234\", \"responsible\": \"JANSOIDE\", \"personnel\": 10, \"modelo\": \"CopperCNN\", \"confianza_porcentaje\": 9975.0}, \"imageUrl\": \"/uploads/71175823913048aca4b9dedf8583c123.jpeg\", \"status\": \"con_cobre\", \"pdfPath\": \"reports\\\\reporte_9.pdf\"}', '2025-11-17 20:28:57', 'pdf');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `revisiones`
--

DROP TABLE IF EXISTS `revisiones`;
CREATE TABLE IF NOT EXISTS `revisiones` (
  `id_revision` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_reporte` int UNSIGNED NOT NULL,
  `id_usuario` int UNSIGNED NOT NULL,
  `comentario` text COLLATE utf8mb4_spanish_ci,
  `aprobado` tinyint(1) DEFAULT NULL,
  `fecha_revision` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_revision`),
  KEY `idx_revisiones_reporte` (`id_reporte`),
  KEY `idx_revisiones_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `hashed_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `cargo` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_registro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `email`, `hashed_password`, `cargo`, `fecha_registro`) VALUES
(1, 'Usuario Prueba', 'prueba@example.com', '$pbkdf2-sha256$29000$5jxHCKG0VopxDkHonXMOwQ$D8gTUtqsc2K62xIX4MJ3X9k8EQwhVuskkMok6BEqODw', 'Tester', '2025-11-15 16:36:17'),
(2, 'Usuario Prueba1', 'prueba1@example.com', '$pbkdf2-sha256$29000$OOfcmxNizJkTQghhrHVOKQ$YovnRRzuomk4TevTDTgAV4vrJ07vGeygdRcOaJxpXSk', 'admin', '2025-11-15 17:35:57');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `clasificaciones`
--
ALTER TABLE `clasificaciones`
  ADD CONSTRAINT `fk_clasificaciones_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenes` (`id_imagen`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `errores`
--
ALTER TABLE `errores`
  ADD CONSTRAINT `fk_errores_reportes` FOREIGN KEY (`id_reporte`) REFERENCES `reportes` (`id_reporte`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `imagenes`
--
ALTER TABLE `imagenes`
  ADD CONSTRAINT `fk_imagenes_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD CONSTRAINT `fk_notificaciones_clasificaciones` FOREIGN KEY (`id_clasificacion`) REFERENCES `clasificaciones` (`id_clasificacion`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_notificaciones_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenes` (`id_imagen`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `predicciones`
--
ALTER TABLE `predicciones`
  ADD CONSTRAINT `fk_predicciones_clasificaciones` FOREIGN KEY (`id_clasificacion`) REFERENCES `clasificaciones` (`id_clasificacion`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `reportes`
--
ALTER TABLE `reportes`
  ADD CONSTRAINT `fk_reportes_clasificaciones` FOREIGN KEY (`id_clasificacion`) REFERENCES `clasificaciones` (`id_clasificacion`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `revisiones`
--
ALTER TABLE `revisiones`
  ADD CONSTRAINT `fk_revisiones_reportes` FOREIGN KEY (`id_reporte`) REFERENCES `reportes` (`id_reporte`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_revisiones_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `cola_analisis`
--
ALTER TABLE `cola_analisis`
  ADD CONSTRAINT `fk_cola_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `imagenes_panorama`
--
ALTER TABLE `imagenes_panorama`
  ADD CONSTRAINT `fk_panorama_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `parches_panorama`
--
ALTER TABLE `parches_panorama`
  ADD CONSTRAINT `fk_parches_panorama` FOREIGN KEY (`id_panorama`) REFERENCES `imagenes_panorama` (`id_panorama`) ON DELETE CASCADE ON UPDATE CASCADE;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `analisis_video`
--

DROP TABLE IF EXISTS `analisis_video`;
CREATE TABLE IF NOT EXISTS `analisis_video` (
  `id_video` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_usuario` int UNSIGNED NOT NULL,
  `nombre_archivo` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `ruta_video` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `duracion_segundos` int UNSIGNED NOT NULL DEFAULT '0',
  `total_frames_analizados` int UNSIGNED NOT NULL DEFAULT '0',
  `total_hallazgos` int UNSIGNED NOT NULL DEFAULT '0',
  `reporte_json` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `ruta_pdf` varchar(255) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `fecha_analisis` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_video`),
  KEY `idx_video_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Filtros para la tabla `analisis_video`
--
ALTER TABLE `analisis_video`
  ADD CONSTRAINT `fk_video_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

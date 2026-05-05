# Guía de Contribución

Gracias por tu interés en contribuir a este proyecto. Aquí se encuentran los pasos para ayudarnos a mejorar.

## Cómo contribuir

### 1. Reportar Errores (Bugs)

Antes de crear un reporte de bug, verifica que el problema no ha sido reportado antes.

**Cuando reportes un bug, incluye:**
- Una descripción clara del error
- Pasos exactos para reproducir el problema
- El comportamiento esperado vs el comportamiento actual
- Versión de Python
- Sistema operativo

### 2. Sugerir Mejoras (Enhancements)

Las sugerencias de mejoras son bienvenidas. Por favor:
- Usa un título descriptivo
- Proporciona descripciones claras
- Enumera ejemplos de casos de uso
- Describe el comportamiento actual vs el comportamiento deseado

### 3. Pull Requests

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/tu-feature`)
3. Commit tus cambios (`git commit -m 'Agrega tu feature'`)
4. Push a la rama (`git push origin feature/tu-feature`)
5. Abre un Pull Request

**Directrices para Pull Requests:**
- Sigue la estructura MVC/N-capas existente
- Agrega pruebas si es posible
- Actualiza la documentación correspondiente
- Asegúrate de que no haya errores de sintaxis

## Estándares de Código

- Sigue PEP 8
- Agrega comentarios y docstrings
- Usa nombres descriptivos para variables y funciones
- Mantén funciones pequeñas y enfocadas

## Estructura de Carpetas

Mantén la estructura existente:
```
- config/     - Configuraciones
- database/   - Conexión a BD
- models/     - Modelos de datos
- controllers/ - Lógica de negocio
- views/      - Interfaz gráfica
- utils/      - Funciones utilitarias
```

## Testing

Antes de enviar un PR:
1. Prueba manualmente la nueva funcionalidad
2. Verifica que no rompe funcionalidad existente
3. Prueba con diferentes configuraciones si es posible

## Preguntas

Si tienes preguntas, puedes:
- Crear un issue (asegúrate de usar etiquetas apropiadas)
- Revisar la documentación en el README.md

¡Gracias por contribuir!

# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Sistema de Reconocimiento Facial! 🎉

## 📋 Cómo Contribuir

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub, luego:
git clone https://github.com/TU_USUARIO/TU_FORK.git
cd TU_FORK
```

### 2. Crear Rama

```bash
git checkout -b feature/nombre-funcionalidad
# o
git checkout -b fix/descripcion-bug
```

**Convenciones de nombres:**
- `feature/` - Nuevas funcionalidades
- `fix/` - Corrección de bugs
- `docs/` - Documentación
- `refactor/` - Refactorización de código
- `test/` - Tests

### 3. Configurar Entorno

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
python manage.py migrate
```

### 4. Hacer Cambios

- Sigue las convenciones de código (PEP 8 para Python)
- Agrega comentarios descriptivos
- Actualiza documentación si es necesario

### 5. Probar Cambios

```bash
# Ejecutar el servidor
python manage.py runserver

# Probar manualmente todas las funcionalidades afectadas
```

### 6. Commit

```bash
git add .
git commit -m "Add: descripción clara del cambio"
```

**Convenciones de commits:**
- `Add:` - Nueva funcionalidad
- `Fix:` - Corrección de bug
- `Update:` - Actualización de código existente
- `Docs:` - Cambios en documentación
- `Refactor:` - Refactorización sin cambio de funcionalidad
- `Test:` - Agregar o modificar tests

### 7. Push y Pull Request

```bash
git push origin feature/nombre-funcionalidad
```

Luego en GitHub:
1. Abre un Pull Request
2. Describe claramente los cambios
3. Referencia issues relacionados (#123)
4. Espera revisión

## 🎯 Áreas de Contribución

### 🚀 Prioridad Alta
- Detección de vivacidad (anti-spoofing)
- Tests unitarios y de integración
- Optimización de velocidad de reconocimiento
- Documentación de API

### 🔧 Prioridad Media
- Dashboard con gráficas avanzadas
- Exportar reportes PDF
- Multi-idioma (i18n)
- Modo oscuro

### 💡 Ideas Bienvenidas
- Reconocimiento con máscaras
- App móvil
- Integración con hardware (control de acceso)
- Machine learning mejorado

## 📝 Estándares de Código

### Python (PEP 8)
```python
# ✅ Bien
def recognize_face(image_data):
    """Reconoce un rostro en la imagen."""
    frame = decode_image(image_data)
    return process_frame(frame)

# ❌ Mal
def recognizeFace(imageData):
    frame=decode_image(imageData)
    return process_frame(frame)
```

### JavaScript (ES6+)
```javascript
// ✅ Bien
async function captureFrame() {
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    return await processImage(imageData);
}

// ❌ Mal
function captureFrame() {
    var imageData = canvas.toDataURL('image/jpeg', 0.8);
    return processImage(imageData);
}
```

### HTML/CSS
- Indentación: 4 espacios
- Nombres de clases: kebab-case (`video-container`)
- IDs: camelCase (`captureButton`)

## 🐛 Reportar Bugs

Usa el template de GitHub Issues e incluye:

1. **Descripción clara** del problema
2. **Pasos para reproducir:**
   - Paso 1: ...
   - Paso 2: ...
   - Resultado esperado vs obtenido
3. **Entorno:**
   - Sistema operativo
   - Python version
   - Navegador (para problemas frontend)
4. **Logs/Screenshots** si aplica

## 💬 Código de Conducta

- Sé respetuoso y profesional
- Acepta críticas constructivas
- Enfócate en el código, no en las personas
- Ayuda a otros contribuidores

## 📧 Contacto

- **Issues:** GitHub Issues
- **Email:** tu-email@example.com
- **Discusiones:** GitHub Discussions

---

¡Gracias por contribuir! 🙌

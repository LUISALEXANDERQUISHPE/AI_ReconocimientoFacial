# 📁 Estructura del Proyecto

## 🌳 Árbol de Archivos

```
claudeApe/
│
├── 📄 manage.py                          # CLI de Django
├── 📄 settings.py                        # Configuración principal
├── 📄 urls.py                            # Rutas principales
├── 📄 wsgi.py                            # Deploy WSGI
├── 📄 asgi.py                            # Deploy ASGI
│
├── 📚 README.md                          # Documentación completa (LEER PRIMERO)
├── 📚 QUICK_START.md                     # Inicio rápido (3 pasos)
├── 📚 INSTALL.md                         # Instalación detallada
├── 📚 CONTRIBUTING.md                    # Guía de contribución
├── 📚 PROJECT_STRUCTURE.md               # Este archivo
│
├── 📦 requirements.txt                   # Dependencias Python
├── 🔧 check_installation.py              # Script de verificación
├── 📝 LICENSE                            # Licencia MIT
│
├── 🔒 .gitignore                         # Archivos ignorados por Git
├── 🔒 .env.example                       # Template de configuración
│
├── 💾 db.sqlite3                         # Base de datos Django (local)
│
├── 📁 venv/                              # Entorno virtual Python
│   └── ...                               # (NO se sube a Git)
│
├── 📁 media/                             # Archivos generados
│   ├── 📁 models/                        # Modelos entrenados
│   │   ├── .gitkeep                      # Mantiene directorio en Git
│   │   ├── modelo_*.h5                   # Modelo neuronal (NO en Git)
│   │   └── clases_*.npy                  # Clases (NO en Git)
│   │
│   └── 📁 samples/                       # Muestras visuales
│       ├── .gitkeep                      # Mantiene directorio en Git
│       └── NOMBRE_PERSONA/               # (NO en Git - privacidad)
│           ├── sample_1.jpg
│           ├── sample_2.jpg
│           ├── sample_3.jpg
│           ├── sample_4.jpg
│           ├── sample_5.jpg
│           └── sample_6.jpg
│
└── 📁 face_recognition_app/              # Aplicación principal
    │
    ├── 📄 __init__.py                    # Paquete Python
    ├── 📄 models.py                      # Documentación MongoDB
    ├── 📄 views.py                       # Lógica de negocio + APIs
    ├── 📄 utils.py                       # FaceRecognitionUtils + ModelTrainer
    ├── 📄 urls.py                        # Rutas de la app
    │
    └── 📁 templates/                     # Plantillas HTML
        └── 📁 face_recognition/
            ├── login.html                # Login facial
            ├── register.html             # Registro (3 pasos, 300 encodings)
            ├── dashboard.html            # Dashboard principal
            ├── train_model.html          # Entrenar modelo
            └── recognition.html          # Reconocimiento en tiempo real
```

---

## 📋 Descripción de Archivos Clave

### 🎯 Archivos de Documentación (IMPORTANTE)

| Archivo | Descripción | Cuándo Leer |
|---------|-------------|-------------|
| **README.md** | Documentación completa del sistema | Primero - información general |
| **QUICK_START.md** | Inicio rápido (3 comandos) | Cuando quieras empezar YA |
| **INSTALL.md** | Instalación paso a paso | Cuando necesites ayuda instalando |
| **CONTRIBUTING.md** | Cómo contribuir al proyecto | Antes de hacer Pull Request |
| **PROJECT_STRUCTURE.md** | Este archivo - estructura del proyecto | Para entender la organización |

### ⚙️ Archivos de Configuración

| Archivo | Propósito | ¿Se sube a Git? |
|---------|-----------|-----------------|
| `settings.py` | Configuración Django + MongoDB | ✅ Sí (sin secrets) |
| `.env.example` | Template de configuración | ✅ Sí |
| `.env` | Configuración real con secrets | ❌ NO (en .gitignore) |
| `requirements.txt` | Lista de dependencias Python | ✅ Sí |
| `.gitignore` | Archivos a ignorar en Git | ✅ Sí |
| `db.sqlite3` | Base de datos local Django | ❌ NO (se genera con migrate) |

### 🧠 Código Principal

| Archivo | Función | Líneas Clave |
|---------|---------|--------------|
| **views.py** | Lógica de negocio + APIs | ~550 líneas |
| **utils.py** | Reconocimiento facial + ML | ~300 líneas |
| **urls.py** | Rutas del sistema | ~20 líneas |
| **models.py** | Documentación MongoDB | ~50 líneas (solo comentarios) |

### 🎨 Templates HTML

| Template | Función | Características |
|----------|---------|-----------------|
| `login.html` | Login facial | Cámara en vivo + reconocimiento |
| `register.html` | Registro de usuarios | 3 pasos + captura 300 frames |
| `dashboard.html` | Panel principal | Estadísticas + gestión |
| `train_model.html` | Entrenar modelo | Auto-limpieza + progreso |
| `recognition.html` | Reconocimiento en vivo | Detección múltiple + estadísticas |

---

## 🗂️ Estructura de MongoDB

### Base de datos: `face_recognition_system`

| Collection | Documentos | Tamaño Aprox. |
|------------|------------|---------------|
| `face_encodings` | 1 por persona | ~50 KB cada uno (300 encodings × 128 dim) |
| `persons` | 1 por persona | ~1 KB cada uno |
| `model_trainings` | 1-5 histórico | ~500 bytes cada uno |
| `recognition_logs` | Ilimitado | ~200 bytes cada uno |

**Total estimado:** ~50-100 MB con 10 personas registradas

---

## 📦 Dependencias (requirements.txt)

| Paquete | Versión | Tamaño | Propósito |
|---------|---------|--------|-----------|
| Django | 5.2.8 | ~10 MB | Framework web |
| pymongo | 4.6.0 | ~500 KB | Driver MongoDB |
| opencv-python | 4.8.1.78 | ~80 MB | Visión por computadora |
| tensorflow | 2.14.0 | ~1.2 GB | Machine learning |
| numpy | 1.24.3 | ~15 MB | Operaciones numéricas |
| scikit-learn | 1.3.2 | ~30 MB | Preprocessing ML |
| Pillow | 10.1.0 | ~5 MB | Procesamiento imágenes |

**Total instalado:** ~1.5 GB

---

## 🚫 Archivos NO Subidos a Git (.gitignore)

### Categoría: Entorno Virtual
```
venv/
env/
.venv/
```
**Razón:** Cada usuario debe crear su propio entorno virtual

### Categoría: Cache Python
```
__pycache__/
*.pyc
*.pyo
```
**Razón:** Archivos compilados temporales

### Categoría: Base de Datos
```
db.sqlite3
*.db
```
**Razón:** Se genera automáticamente con `migrate`

### Categoría: Modelos Entrenados
```
media/models/*.h5
media/models/*.npy
```
**Razón:** Muy pesados (5-10 MB) y se generan al entrenar

### Categoría: Muestras Faciales
```
media/samples/
```
**Razón:** Privacidad - datos biométricos sensibles

### Categoría: Configuración Sensible
```
.env
settings_local.py
secrets.json
```
**Razón:** Contienen credenciales y SECRET_KEY

---

## 🔄 Flujo de Trabajo Git

### 1. Clonar Repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 2. Configurar Entorno
```bash
# Crear venv (NO se sube a Git)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Copiar configuración
cp .env.example .env
# Editar .env con tu MongoDB URI
```

### 3. Inicializar Base de Datos
```bash
# Crear db.sqlite3 (NO se sube a Git)
python manage.py migrate
```

### 4. Primera Ejecución
```bash
python manage.py runserver
```

### 5. Uso Normal
```bash
# Registrar 2+ personas → media/samples/ (NO Git)
# Entrenar modelo → media/models/ (NO Git)
# Login facial
```

---

## 📊 Tamaños de Archivos

| Categoría | Incluido en Git | Tamaño |
|-----------|-----------------|--------|
| Código fuente (.py, .html) | ✅ Sí | ~150 KB |
| Documentación (.md) | ✅ Sí | ~80 KB |
| Dependencias (venv/) | ❌ NO | ~1.5 GB |
| Base de datos (db.sqlite3) | ❌ NO | ~100 KB |
| Modelos (.h5, .npy) | ❌ NO | ~5-10 MB |
| Muestras faciales | ❌ NO | ~2 MB por persona |
| **Total en Git** | - | **~230 KB** |
| **Total local completo** | - | **~1.5-2 GB** |

---

## 🎯 Para Tu Compañero

### Después de clonar el repo:

1. ✅ **Leer primero:** `README.md` (documentación completa)
2. ✅ **Inicio rápido:** `QUICK_START.md` (3 comandos)
3. ✅ **Verificar instalación:**
   ```bash
   python check_installation.py
   ```
4. ✅ **Configurar MongoDB:** Editar `settings.py` línea 140
5. ✅ **Ejecutar:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Archivos que DEBE crear localmente:
- `venv/` - Entorno virtual
- `db.sqlite3` - Base de datos Django
- `.env` - Configuración personal
- `media/models/` - Modelos entrenados (al entrenar)
- `media/samples/` - Muestras faciales (al registrar)

---

## 🆘 Ayuda

- **Problemas de instalación:** Ver `INSTALL.md`
- **Errores comunes:** Ver `README.md` sección "Solución de Problemas"
- **Contribuir:** Ver `CONTRIBUTING.md`
- **Verificación:** Ejecutar `python check_installation.py`

---

**Fecha de actualización:** Noviembre 2025  
**Versión:** 1.0.0

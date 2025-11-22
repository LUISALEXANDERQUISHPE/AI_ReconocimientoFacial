# 🔐 Sistema de Reconocimiento Facial - Django + MongoDB + TensorFlow

Sistema profesional de reconocimiento facial en tiempo real usando Django, MongoDB, OpenCV y TensorFlow con captura rápida de 300 encodings faciales.

## 🎯 Características Principales

✅ **Login por Reconocimiento Facial** (90% confianza mínima)  
✅ **Registro Rápido** con captura de 300 encodings en ~20 segundos  
✅ **6 Muestras Visuales** para auditoría y trazabilidad  
✅ **Dashboard Administrativo** con estadísticas en tiempo real  
✅ **Entrenamiento de Modelo** con auto-limpieza de modelos antiguos  
✅ **Reconocimiento en Tiempo Real** con cámara web  
✅ **Arquitectura Híbrida**: SQLite (Django) + MongoDB (Datos faciales)  
✅ **Sistema Batch**: 1 sola operación de BD para 300 encodings

---

## 📋 Requisitos Previos

- **Python 3.10+**
- **MongoDB Atlas** (cuenta gratuita) o MongoDB local
- **Cámara web** funcional
- **Navegador moderno** (Chrome, Firefox, Edge)
- **Sistema operativo**: Windows, Linux o macOS

---

## 🚀 Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 2. Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install django==5.2.8 pymongo opencv-python tensorflow numpy scikit-learn pillow
```

**Lista completa de paquetes:**
- `django==5.2.8` - Framework web
- `pymongo` - Conector MongoDB
- `opencv-python==4.8.1.78` - Visión por computadora
- `tensorflow==2.14.0` - Machine Learning
- `numpy` - Operaciones numéricas
- `scikit-learn` - Preprocesamiento ML
- `pillow` - Procesamiento de imágenes

### 4. Configurar MongoDB

#### Opción A: MongoDB Atlas (Recomendado - Gratis)

1. Crea una cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Crea un cluster gratuito (M0)
3. Configura usuario y contraseña
4. Agrega tu IP a la whitelist (0.0.0.0/0 para desarrollo)
5. Obtén tu connection string

#### Opción B: MongoDB Local

```bash
# Instalar MongoDB Community Edition
# Windows: https://www.mongodb.com/try/download/community
# Linux: sudo apt install mongodb
# macOS: brew install mongodb-community
```

**Editar `settings.py`** (línea ~140):

```python
MONGODB_SETTINGS = {
    'URI': 'mongodb+srv://USUARIO:PASSWORD@cluster.mongodb.net/',  # MongoDB Atlas
    # O para local:
    # 'URI': 'mongodb://localhost:27017/',
    'DB_NAME': 'face_recognition_system'
}
```

### 5. Ejecutar Migraciones Django

```bash
python manage.py migrate
```

Esto crea 18 tablas en SQLite para el sistema interno de Django (sesiones, admin, etc).

### 6. Crear Directorio de Muestras

```bash
# Windows
New-Item -ItemType Directory -Force -Path media\samples

# Linux/macOS
mkdir -p media/samples
```

### 7. Iniciar el Servidor

```bash
python manage.py runserver
```

Accede a: **http://127.0.0.1:8000**

---

## 📖 Guía de Uso Completa

### 🎬 PASO 1: Registrar Primera Persona

1. En la página de login, haz clic en **"Registrarse"**
2. **Paso 1 - Datos Personales:**
   - Nombre completo
   - Email (opcional)
   - Departamento/Empresa
3. **Paso 2 - Captura Facial (20 segundos):**
   - ⚡ Captura automática de **300 frames a 15 fps**
   - 🖼️ Guarda **6 muestras visuales** (cada 50 frames)
   - 💡 **Recomendaciones:**
     - Buena iluminación frontal
     - Mueve tu cabeza lentamente (izquierda/derecha, arriba/abajo)
     - Cambia expresiones gradualmente (neutral, sonrisa)
     - No uses lentes oscuros
     - Evita sombras fuertes
4. **Paso 3 - Confirmación:**
   - Verifica: 300 encodings + 6 muestras
   - Finaliza registro

**Resultado:** Persona registrada en MongoDB con estructura optimizada (1 documento con 300 encodings).

---

### 🧠 PASO 2: Entrenar el Modelo

**⚠️ IMPORTANTE:** Necesitas **mínimo 2 personas** registradas para entrenar.

1. Accede al dashboard temporalmente (sin login facial)
2. Ve a **"Entrenar Modelo"** en el menú
3. Haz clic en **"Iniciar Entrenamiento"**
4. El sistema automáticamente:
   - 🗑️ Elimina modelos antiguos (auto-limpieza)
   - 📊 Carga 300 encodings por persona desde MongoDB
   - 🧠 Entrena red neuronal Dense(256→128→64→clases)
   - 💾 Guarda modelo `.h5` y clases `.npy` en `media/models/`
   - ✅ Marca modelo como activo en BD
   - 🔄 Recarga modelo en memoria automáticamente
5. **Tiempo estimado:** 10-60 segundos (depende de personas/hardware)
6. **Resultado:** Precisión ~95-100% con 2-3 personas

**Métricas mostradas:**
- ✅ Precisión final
- 📊 Total de muestras
- 👥 Número de clases
- ⏱️ Tiempo de entrenamiento

---

### 🔐 PASO 3: Login por Reconocimiento Facial

1. Ve a la página principal: **http://127.0.0.1:8000**
2. Permite acceso a la cámara (aparecerá popup del navegador)
3. Mira directamente a la cámara
4. **Resultados automáticos:**
   - 🟢 **Confianza > 90%** → Acceso al dashboard inmediato
   - 🟡 **Confianza 70-90%** → "Confianza insuficiente" (muestra %)
   - 🔴 **Confianza < 70%** → "Desconocido" o "Sin modelo"

**Tips para mejor reconocimiento:**
- Iluminación similar a la del registro
- Posición frontal a la cámara
- Sin obstáculos (manos, objetos)
- Cámara a la altura de los ojos

---

### 📊 PASO 4: Dashboard y Gestión

**Dashboard muestra:**
- 👥 Total de personas registradas
- 🔢 Total de encodings en BD
- 📈 Estadísticas de reconocimiento
- 📋 Listado de personas con opciones:
  - ✏️ Ver detalles
  - 🗑️ Eliminar persona

**Reconocimiento en Tiempo Real:**
- Ve a `/recognition/`
- Visualiza detección en vivo con:
  - 🟢 Cuadros verdes: Confianza >90%
  - 🟡 Cuadros amarillos: Confianza 70-90%
  - 🔴 Cuadros rojos: Desconocido
- Estadísticas en tiempo real (rostros detectados, reconocimientos, confianza promedio)

---

## 🗂️ Estructura del Proyecto

```
claudeApe/
├── face_recognition_app/
│   ├── templates/face_recognition/
│   │   ├── login.html              # Login facial
│   │   ├── register.html           # Registro 3 pasos (300 encodings)
│   │   ├── dashboard.html          # Dashboard principal
│   │   ├── train_model.html        # Entrenar modelo
│   │   └── recognition.html        # Reconocimiento en vivo
│   ├── views.py                    # Lógica de negocio y APIs
│   ├── utils.py                    # FaceRecognitionUtils + ModelTrainer
│   ├── models.py                   # Documentación MongoDB (vacío)
│   └── urls.py                     # Rutas del sistema
├── media/
│   ├── models/                     # Modelos entrenados (.h5 + .npy)
│   └── samples/                    # 6 muestras visuales por persona
│       └── NOMBRE_PERSONA/
│           ├── sample_1.jpg
│           ├── sample_2.jpg
│           ├── sample_3.jpg
│           ├── sample_4.jpg
│           ├── sample_5.jpg
│           └── sample_6.jpg
├── db.sqlite3                      # Base de datos Django (sesiones)
├── settings.py                     # Configuración general
├── urls.py                         # Rutas principales
├── manage.py                       # CLI Django
├── requirements.txt                # Dependencias
├── .gitignore                      # Archivos ignorados por Git
└── README.md                       # Este archivo
```

---

## 🗄️ Estructura de MongoDB

### Base de datos: `face_recognition_system`

#### Collection: `face_encodings` (Estructura Unificada)
```javascript
{
    _id: ObjectId,
    person_name: "Luis Alexander",
    email: "luis@example.com",
    empresa: "Sistemas",
    face_encodings: [                      // Array de 300 encodings
        [0.123, -0.456, 0.789, ...],       // Encoding 1 (128 dim)
        [0.234, -0.567, 0.890, ...],       // Encoding 2 (128 dim)
        ...                                 // 300 encodings totales
    ],
    sample_images: [                        // 6 muestras visuales
        "samples/Luis_Alexander/sample_1.jpg",
        "samples/Luis_Alexander/sample_2.jpg",
        ...
    ],
    timestamp: 1732234567.123,
    registration_date: ISODate("2025-11-21T18:30:00Z"),
    total_encodings: 300,
    total_samples: 6,
    encoding_dimension: 128,
    extraction_method: "opencv_custom_features",
    status: "registered",
    capture_date: ISODate("2025-11-21T18:30:00Z")
}
```

#### Collection: `persons` (Índice rápido)
```javascript
{
    _id: ObjectId,
    name: "Luis Alexander",
    email: "luis@example.com",
    department: "Sistemas",
    is_active: true,
    created_at: ISODate("2025-11-21T18:30:00Z"),
    total_encodings: 300,
    total_samples: 6
}
```

#### Collection: `model_trainings`
```javascript
{
    _id: ObjectId,
    training_date: ISODate("2025-11-21T19:00:00Z"),
    model_file: "modelo_20251121_190045.h5",
    classes_file: "clases_20251121_190045.npy",
    total_samples: 600,                    // 300 × 2 personas
    num_classes: 2,
    final_accuracy: 100.0,                 // Porcentaje
    final_val_accuracy: 98.5,
    training_time_seconds: 45.23,
    is_active: true                        // Solo 1 modelo activo
}
```

#### Collection: `recognition_logs`
```javascript
{
    _id: ObjectId,
    person_id: "507f1f77bcf86cd799439011",
    person_name: "Luis Alexander",
    confidence: 0.952,                     // 95.2%
    timestamp: ISODate("2025-11-21T20:15:30Z"),
    event_type: "login",                   // login | recognition
    ip_address: "192.168.1.100"
}
```

---

## ⚙️ Configuración Avanzada

### Cambiar Cantidad de Encodings

**Archivo:** `face_recognition_app/templates/face_recognition/register.html`

```javascript
// Línea ~438
const TARGET_ENCODINGS = 300;  // Cambiar a 200, 400, etc.
const SAMPLE_INTERVAL = 50;    // Guardar muestra cada N frames
```

### Ajustar Umbral de Confianza

**Archivo:** `face_recognition_app/views.py`

```python
# Línea ~125 (api_recognize_login)
if name is not None and confidence > 0.90:  # Cambiar 0.90 a 0.85, 0.95, etc.
```

### Cambiar Velocidad de Captura

**Archivo:** `face_recognition_app/templates/face_recognition/register.html`

```javascript
// Línea ~532
captureInterval = setInterval(captureFrame, 65);  // 65ms = ~15fps, cambiar a 50 para 20fps
```

### Arquitectura del Modelo

**Archivo:** `face_recognition_app/utils.py` (línea ~205)

```python
def build_model(self, num_classes):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation='relu', input_dim=128),  # Cambiar 256
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(128, activation='relu'),                 # Cambiar 128
        # ...
    ])
```

---

## 🎯 Umbrales de Reconocimiento

| Confianza | Estado | Color | Acción |
|-----------|--------|-------|--------|
| **> 90%** | ✅ Confirmado | 🟢 Verde | Acceso al dashboard |
| **70-90%** | ⚠️ Insuficiente | 🟡 Amarillo | Mostrar % (no acceso) |
| **< 70%** | ❌ Desconocido | 🔴 Rojo | Rechazar |

---

## 🔧 Solución de Problemas

### ❌ Error: "No se pudo acceder a la cámara"

**Causas:**
- Navegador sin permisos de cámara
- Otra app usando la cámara
- HTTPS requerido (excepto localhost)

**Soluciones:**
- Chrome: `chrome://settings/content/camera`
- Cierra Zoom, Teams, Skype
- Usa `http://127.0.0.1:8000` o `http://localhost:8000`

---

### ❌ Error: "Sin modelo entrenado"

**Mensaje en pantalla:** `⚠️ Sin modelo entrenado - Ve a entrenar modelo`

**Causas:**
- Modelo no entrenado
- Archivo de modelo eliminado
- Error al cargar modelo

**Soluciones:**
1. Ve a `/train/`
2. Haz clic en "Iniciar Entrenamiento"
3. Espera hasta ver "✅ Modelo entrenado exitosamente"
4. Verifica que existe `media/models/modelo_*.h5`

---

### ❌ Error: "No hay datos para entrenar"

**Causas:**
- Menos de 2 personas registradas
- MongoDB sin datos

**Soluciones:**
1. Registra al menos 2 personas diferentes
2. Verifica conexión a MongoDB:
```python
# En Python shell
from pymongo import MongoClient
client = MongoClient('TU_URI')
db = client['face_recognition_system']
print(db.face_encodings.count_documents({}))  # Debe ser > 0
```

---

### ❌ Error: "MongoDB connection failed"

**Mensaje:** `✅ MongoDB conectado exitosamente` NO aparece al iniciar

**Causas:**
- URI incorrecta en `settings.py`
- IP no whitelisted en MongoDB Atlas
- MongoDB local no iniciado

**Soluciones:**
1. Verifica URI en `settings.py`:
```python
MONGODB_SETTINGS = {
    'URI': 'mongodb+srv://USER:PASS@cluster.mongodb.net/',  # ← Aquí
    'DB_NAME': 'face_recognition_system'
}
```
2. MongoDB Atlas: Settings → Network Access → Add IP (0.0.0.0/0 para desarrollo)
3. MongoDB local:
```bash
# Windows
net start MongoDB

# Linux
sudo systemctl start mongod

# macOS
brew services start mongodb-community
```

---

### ❌ Reconocimiento con baja confianza (<70%)

**Causas:**
- Iluminación diferente al registro
- Ángulo o distancia incorrectos
- Pocos encodings (menos de 200)
- Cambio de apariencia (barba, lentes, etc.)

**Soluciones:**
1. Re-registrarte con 300 encodings
2. Captura con variedad de ángulos y expresiones
3. Usa iluminación consistente
4. Entrena nuevamente el modelo
5. Considera bajar umbral a 85% en `views.py`

---

## 📊 API Endpoints

### 🔓 Públicos (sin autenticación)

```
GET  /                              - Página de login facial
GET  /register/                     - Registro de nueva persona
POST /api/recognize-login/          - Reconocer rostro para login
POST /api/process-frame/            - Procesar frame (extrae encoding)
POST /api/register-complete/        - Guardar registro completo (300 encodings + 6 muestras)
```

### 🔒 Protegidos (requieren sesión)

```
GET  /dashboard/                    - Dashboard principal
GET  /train/                        - Página entrenar modelo
POST /train/                        - Ejecutar entrenamiento
GET  /recognition/                  - Reconocimiento en tiempo real
GET  /logout/                       - Cerrar sesión

GET  /api/dashboard-stats/          - Estadísticas (JSON)
GET  /api/persons-list/             - Listado personas (JSON)
POST /api/delete-person/            - Eliminar persona
POST /api/recognize-realtime/       - Reconocer en vivo (sin autenticar)
```

---

## 🧪 Arquitectura Técnica

### 📸 Extracción de Características (128 dimensiones)

**Proceso completo:**

1. **Preprocesamiento:**
   ```
   Imagen → Resize(64×64) → Grayscale → EqualizeHist → GaussianBlur(3×3)
   ```

2. **División en Regiones:**
   ```
   64×64 píxeles → Grid 8×8 = 64 regiones de 8×8 píxeles cada una
   ```

3. **Estadísticas por Región:**
   ```
   Cada región → [media, desviación_estándar] → 2 valores × 64 regiones = 128 características
   ```

4. **Normalización L2:**
   ```
   Vector[128] → Normalizar(L2) → Encoding final de 128 dimensiones
   ```

**Ejemplo de encoding:**
```python
[0.123, -0.456, 0.789, 0.234, ..., -0.123]  # 128 valores entre -1 y 1
```

---

### 🧠 Red Neuronal (Arquitectura)

```
Input Layer
    ↓ (128 neuronas)
Dense(256) + ReLU
    ↓
BatchNormalization
    ↓
Dropout(0.3)
    ↓
Dense(128) + ReLU
    ↓
BatchNormalization
    ↓
Dropout(0.3)
    ↓
Dense(64) + ReLU
    ↓
Dropout(0.2)
    ↓
Dense(num_classes) + Softmax
    ↓
Output (probabilidades por clase)
```

**Hiperparámetros:**
- Optimizer: Adam (learning_rate=0.001)
- Loss: Categorical Crossentropy
- Metrics: Accuracy
- Epochs: Dinámico (min 20, max 1000, o 2× muestras)
- Batch Size: Dinámico (min 4, max 32, o muestras÷4)

**Callbacks:**
- **EarlyStopping:** Para entrenamiento al mejorar después de 10 epochs
- **ReduceLROnPlateau:** Reduce learning rate al estancarse (patience=5, factor=0.5)

---

### ⚡ Sistema de Captura Rápida (Opción B Profesional)

**Flujo optimizado:**

```
Usuario inicia captura
    ↓
Captura frame cada 65ms (~15 fps)
    ↓
Procesa encoding en servidor (POST)
    ↓
Acumula en memoria JavaScript (no BD)
    ↓
Cada 50 frames → Guarda muestra visual
    ↓
Al llegar a 300 frames → STOP
    ↓
1 SOLO POST con:
    - 300 encodings
    - 6 muestras base64
    ↓
Backend: insert_one() en MongoDB
    ↓
Guarda muestras en media/samples/
    ↓
¡Registro completo en <30 segundos!
```

**Ventajas vs captura tradicional:**
| Aspecto | Tradicional | Sistema Actual |
|---------|-------------|----------------|
| Encodings | 50-100 | 300 |
| Tiempo | 60-90s | ~20s |
| Operaciones BD | 50-100 inserts | 1 insert |
| Velocidad | ~2-3 fps | ~15 fps |
| Muestras visuales | Todas (pesado) | 6 estratégicas |
| Experiencia UX | Lenta | Rápida ⚡ |

---

## 🆚 Comparación con Scripts Originales

| Característica | Scripts CLI | Sistema Django Web |
|----------------|-------------|-------------------|
| **Interfaz** | Terminal/CLI | Web profesional responsive |
| **Captura** | Manual ~40s | Automática ~20s (300 frames) |
| **Encodings** | 100-200 | 300 optimizados |
| **Muestras** | Todas guardadas | 6 estratégicas (balance) |
| **Entrenamiento** | Script separado | Botón en dashboard |
| **Reconocimiento** | Terminal | Tiempo real web con UI |
| **Sesiones** | No | Sí (simple con Django) |
| **Multi-usuario** | No | Sí (ilimitado) |
| **Base de datos** | Archivos locales | MongoDB Atlas (nube) |
| **Logs** | Terminal | MongoDB + visualización web |
| **Escalabilidad** | Limitada | Alta (MongoDB + Django) |
| **Acceso remoto** | No | Sí (deploy en servidor) |

---

## ✅ Checklist de Producción

### 🔒 Seguridad
- [ ] Cambiar `SECRET_KEY` en `settings.py`
- [ ] `DEBUG = False` en producción
- [ ] Configurar `ALLOWED_HOSTS`
- [ ] HTTPS obligatorio (certbot/Let's Encrypt)
- [ ] Firewall configurado (solo puertos 80/443)
- [ ] Whitelist de IPs en MongoDB Atlas
- [ ] Implementar rate limiting (django-ratelimit)
- [ ] CSP headers configurados
- [ ] Sanitizar inputs de usuario

### 🚀 Rendimiento
- [ ] Usar Gunicorn/uWSGI en lugar de runserver
- [ ] Nginx como reverse proxy
- [ ] Caché con Redis (django-redis)
- [ ] Comprimir assets estáticos (gzip)
- [ ] CDN para archivos media
- [ ] Índices en MongoDB (campos frecuentes)
- [ ] Monitoreo con Sentry

### 📊 Monitoreo
- [ ] Logs centralizados (ELK Stack)
- [ ] Métricas de reconocimiento (precisión, latencia)
- [ ] Alertas automáticas (fallos de modelo)
- [ ] Backups automáticos MongoDB (Atlas)
- [ ] Health checks cada 5 min

---

## 📚 Dependencias Detalladas

```txt
# requirements.txt
Django==5.2.8              # Framework web
pymongo==4.6.0             # Driver MongoDB
opencv-python==4.8.1.78    # Computer vision
tensorflow==2.14.0         # Machine learning
numpy==1.24.3              # Operaciones numéricas
scikit-learn==1.3.2        # Preprocessing ML
Pillow==10.1.0             # Procesamiento imágenes
```

**Tamaño total instalado:** ~1.5 GB (principalmente TensorFlow)

---

## 🔮 Roadmap (Futuras Mejoras)

### Corto Plazo (1-2 meses)
- [ ] Detección de vivacidad (anti-spoofing con parpadeo)
- [ ] Modo oscuro en interfaz
- [ ] Exportar reportes PDF
- [ ] Multi-idioma (i18n)
- [ ] Notificaciones por email

### Mediano Plazo (3-6 meses)
- [ ] Reconocimiento con máscaras faciales
- [ ] App móvil (React Native)
- [ ] Dashboard avanzado con Chart.js
- [ ] API REST completa con DRF
- [ ] Autenticación 2FA adicional

### Largo Plazo (6-12 meses)
- [ ] Integración con sistemas de RRHH
- [ ] Control de acceso a puertas (hardware)
- [ ] Machine learning en tiempo real (sin reentrenar)
- [ ] Clustering automático de rostros
- [ ] Análisis de emociones

---

## 🆘 Soporte y Contribuciones

### Reportar Issues
Si encuentras bugs o tienes sugerencias:
1. Crea un issue en GitHub con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Logs relevantes
   - Sistema operativo y versiones

### Contribuir al Proyecto
1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Add: nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

### Contacto
- **GitHub Issues:** [Link al repo]
- **Email:** tu-email@example.com
- **LinkedIn:** [Tu perfil]

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 🙏 Agradecimientos

- **OpenCV Community** - Algoritmos de visión por computadora
- **TensorFlow Team** - Framework de machine learning
- **MongoDB** - Base de datos NoSQL flexible
- **Django Software Foundation** - Framework web robusto

---

## 📸 Screenshots

*(Añade aquí screenshots de tu aplicación)*

- Login facial con cámara en vivo
- Proceso de registro (3 pasos)
- Dashboard con estadísticas
- Página de entrenamiento
- Reconocimiento en tiempo real

---

**Desarrollado con ❤️ usando:**
- Django 5.2.8
- MongoDB Atlas
- TensorFlow 2.14.0
- OpenCV 4.8.1
- Python 3.10+

**Versión:** 1.0.0  
**Última actualización:** Noviembre 2025

## 📋 Flujo del Sistema

```
📸 CAPTURA → 🔧 PROCESAMIENTO → 🧠 ENTRENAMIENTO → 🎯 RECONOCIMIENTO
     │              │                │                 │
     ▼              ▼                ▼                 ▼
   Crudo         Normalizado      Modelo H5        Tiempo Real
```

## 🚀 Inicio Rápido

### 1. Activar entorno virtual e instalar dependencias

```powershell
.\venv\Scripts\Activate.ps1
pip install django pymongo opencv-python tensorflow numpy scikit-learn pillow
```

### 2. Ejecutar migraciones (solo para Django interno)

```powershell
python manage.py migrate
```

### 3. Iniciar el servidor

```powershell
python manage.py runserver
```

### 4. Acceder al sistema

Abre tu navegador en: http://localhost:8000

## 📖 Guía de Uso

### PASO 1: Registrar Primera Persona

1. En la página de login, haz clic en **"Registrarse"**
2. Completa tus datos personales (Nombre, Email, Departamento)
3. **Captura Facial Automática:**
   - La cámara capturará 50 huellas faciales automáticamente
   - Mueve tu cabeza lentamente (izquierda/derecha, arriba/abajo)
   - Cambia expresiones faciales gradualmente
   - Mantén buena iluminación
4. Confirma y finaliza el registro

### PASO 2: Entrenar el Modelo

**Importante:** Después de registrar personas, debes entrenar el modelo.

1. Accede al dashboard (temporalmente sin reconocimiento)
2. Haz clic en **"Entrenar Modelo"**
3. El sistema:
   - Cargará todas las huellas faciales desde MongoDB
   - Entrenará la red neuronal
   - Guardará el modelo en `media/models/`
4. Espera a que termine (puede tomar 1-5 minutos)

### PASO 3: Login por Reconocimiento Facial

1. Ve a la página principal: http://localhost:8000
2. La cámara se activará automáticamente
3. Mira directamente a la cámara
4. **Si tu confianza > 90%** → Acceso automático al dashboard
5. **Si confianza < 90%** → "Confianza insuficiente" o "Desconocido"

## 🗂️ Estructura del Proyecto

```
claudeApe/
├── face_recognition_app/
│   ├── templates/face_recognition/
│   │   ├── login.html           # Login facial
│   │   ├── register.html        # Registro 3 pasos
│   │   ├── dashboard.html       # Dashboard principal
│   │   ├── train_model.html     # Entrenar modelo
│   │   └── recognition.html     # Reconocimiento en vivo
│   ├── views.py                 # Lógica de negocio
│   ├── utils.py                 # Reconocimiento facial
│   ├── models.py                # Vacío (solo documentación MongoDB)
│   └── urls.py                  # Rutas
├── media/models/                # Modelos entrenados (.h5)
├── settings.py                  # Configuración
└── manage.py                    # Comando Django
```

## 🗄️ Estructura de MongoDB

### Base de datos: `face_recognition_system`

#### Collection: `persons`
```javascript
{
    _id: ObjectId,
    name: "Juan Pérez",
    email: "juan@example.com",
    department: "Sistemas",
    is_active: true,
    created_at: ISODate,
    total_encodings: 50
}
```

#### Collection: `face_encodings`
```javascript
{
    _id: ObjectId,
    person_id: "507f1f77bcf86cd799439011",
    person_name: "Juan Pérez",
    encoding: [0.123, -0.456, ...],  // Array de 128 características
    quality_score: 245.67,
    confidence: 0.85,
    capture_date: ISODate
}
```

#### Collection: `model_trainings`
```javascript
{
    _id: ObjectId,
    training_date: ISODate,
    model_file: "models/modelo_20241121_143022.h5",
    classes_file: "models/clases_20241121_143022.npy",
    total_samples: 150,
    num_classes: 3,
    final_accuracy: 0.98,
    final_val_accuracy: 0.96,
    training_time_seconds: 45.23,
    is_active: true
}
```

#### Collection: `recognition_logs`
```javascript
{
    _id: ObjectId,
    person_id: "507f1f77bcf86cd799439011",
    person_name: "Juan Pérez",
    confidence: 0.95,
    timestamp: ISODate,
    event_type: "login",
    ip_address: "192.168.1.100"
}
```

## ⚙️ Configuración

### Cambiar URI de MongoDB

Edita `settings.py`:

```python
MONGODB_SETTINGS = {
    'URI': 'tu-uri-de-mongodb',
    'DB_NAME': 'face_recognition_system'
}
```

### Ajustar Umbral de Confianza

En `views.py`, línea ~65:

```python
if name is not None and confidence > 0.90:  # Cambia 0.90 al valor deseado
```

## 🎯 Umbrales de Reconocimiento

- **> 90%** → ✅ Acceso confirmado (verde)
- **70% - 90%** → ⚠️ Confianza insuficiente (amarillo)
- **< 70%** → ❌ Desconocido (rojo)

## 🔧 Solución de Problemas

### Error: "No se pudo acceder a la cámara"
- Verifica que tu navegador tenga permisos de cámara
- Usa HTTPS o localhost
- Cierra otras aplicaciones que usen la cámara

### Error: "Modelo no cargado"
- Ve a `/train/` y entrena el modelo
- Asegúrate de tener al menos 2 personas registradas

### Error: "No hay datos para entrenar"
- Registra al menos 2 personas primero
- Verifica conexión a MongoDB

### Error de conexión a MongoDB
- Verifica tu URI en `settings.py`
- Asegúrate de tener conexión a internet
- Revisa que tu IP esté en la whitelist de MongoDB Atlas

## 📊 API Endpoints

```
GET  /                          - Login facial
GET  /register/                 - Registro de persona
GET  /dashboard/                - Dashboard principal
GET  /train/                    - Entrenar modelo
GET  /recognition/              - Reconocimiento en vivo
GET  /logout/                   - Cerrar sesión

POST /api/recognize-login/      - Reconocer rostro para login
POST /api/process-frame/        - Procesar frame y extraer encodings
POST /api/register-complete/    - Completar registro de persona
GET  /api/dashboard-stats/      - Estadísticas del dashboard
GET  /api/persons-list/         - Listar personas registradas
POST /api/delete-person/        - Eliminar persona
```

## 🧪 Arquitectura Técnica

### Extracción de Características (128 dimensiones)

1. Redimensionar imagen a 64x64
2. Convertir a escala de grises
3. Ecualización de histograma
4. Suavizado Gaussiano
5. División en regiones 8x8
6. Cálculo de media y desviación estándar por región
7. Normalización L2

### Red Neuronal

```
Input (128) 
    ↓
Dense(256) + ReLU + BatchNorm + Dropout(0.3)
    ↓
Dense(128) + ReLU + BatchNorm + Dropout(0.3)
    ↓
Dense(64) + ReLU + Dropout(0.2)
    ↓
Dense(num_classes) + Softmax
```

### Optimización
- Optimizer: Adam (lr=0.001)
- Loss: Categorical Crossentropy
- Early Stopping (patience=10)
- ReduceLROnPlateau (patience=5)

## 📝 Diferencias con Scripts Originales

| Aspecto | Scripts Originales | Sistema Django |
|---------|-------------------|----------------|
| Interfaz | Terminal/CLI | Web Profesional |
| Captura | Manual 40s | Automática inteligente |
| Entrenamiento | Script separado | Botón en dashboard |
| Reconocimiento | Terminal | Tiempo real web |
| Sesiones | No | Sí (simple) |
| Multi-usuario | No | Sí |
| Logs | Terminal | MongoDB |

## ✅ Sistema Listo Para

- ✅ Producción local
- ✅ Control de acceso por reconocimiento facial
- ✅ Múltiples usuarios
- ✅ Escalabilidad horizontal (MongoDB)
- ✅ Entrenamiento bajo demanda
- ✅ Logs completos

## 🔒 Seguridad

- Solo sesiones simples (sin autenticación compleja)
- Umbral de confianza alto (90%)
- Logs de todos los intentos de acceso
- Datos sensibles en MongoDB encriptado

## 📚 Próximas Mejoras (Opcionales)

- [ ] Detección de vivacidad (anti-spoofing)
- [ ] Reconocimiento con máscaras
- [ ] Múltiples cámaras
- [ ] Notificaciones por email
- [ ] Dashboard con gráficas avanzadas
- [ ] Export de reportes PDF
- [ ] API REST completa

## 🆘 Soporte

Si tienes problemas:
1. Revisa esta documentación
2. Verifica los logs en terminal
3. Prueba con diferentes iluminaciones
4. Asegúrate de tener buena calidad de cámara

---

**Desarrollado con:** Django 5.2 + MongoDB + TensorFlow 2.14 + OpenCV 4.8

# 🚀 Guía de Instalación Rápida

## ⚡ Instalación en 5 Minutos

### 1️⃣ Clonar y Entrar

```bash
git clone https://github.com/TU_USUARIO/face-recognition-django.git
cd face-recognition-django
```

### 2️⃣ Crear Entorno Virtual

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

**⏱️ Tiempo:** ~5-10 minutos (descarga ~1.5 GB)

### 4️⃣ Configurar MongoDB

#### Opción A: MongoDB Atlas (Recomendado - Gratis)

1. Ve a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Crea cuenta y cluster gratuito (M0)
3. Crea usuario de base de datos
4. Whitelist IP: `0.0.0.0/0` (desarrollo)
5. Copia tu connection string

#### Opción B: MongoDB Local

**Windows:**
```powershell
# Descargar: https://www.mongodb.com/try/download/community
# Instalar y ejecutar:
net start MongoDB
```

**Linux:**
```bash
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb
```

**macOS:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

### 5️⃣ Configurar settings.py

Edita `settings.py` (línea ~140):

```python
MONGODB_SETTINGS = {
    # MongoDB Atlas:
    'URI': 'mongodb+srv://USER:PASS@cluster.mongodb.net/',
    
    # O MongoDB Local:
    # 'URI': 'mongodb://localhost:27017/',
    
    'DB_NAME': 'face_recognition_system'
}
```

### 6️⃣ Migrar y Ejecutar

```bash
python manage.py migrate
python manage.py runserver
```

### 7️⃣ Acceder

Abre en tu navegador: **http://127.0.0.1:8000**

---

## ✅ Verificar Instalación

Al iniciar el servidor deberías ver:

```
✅ MongoDB conectado exitosamente
✅ Modelo cargado: modelo_XXXXXX.h5 con N clases

System check identified no issues (0 silenced).
Django version 5.2.8, using settings 'settings'
Starting development server at http://127.0.0.1:8000/
```

---

## 🎯 Primeros Pasos

### 1. Registrar Usuarios (mínimo 2)

- Ve a: http://127.0.0.1:8000/register/
- Completa datos
- Captura 300 frames (~20 segundos)
- Repite para 2+ personas

### 2. Entrenar Modelo

- Ve a: http://127.0.0.1:8000/train/
- Clic en "Iniciar Entrenamiento"
- Espera ~30-60 segundos

### 3. Probar Login Facial

- Ve a: http://127.0.0.1:8000
- Permite acceso a cámara
- Mira a la cámara
- ¡Acceso automático si confianza > 90%!

---

## 🔧 Solución Rápida de Problemas

### Error: "pip no reconocido"
```bash
python -m pip install -r requirements.txt
```

### Error: "MongoDB connection failed"
- Verifica URI en `settings.py`
- Whitelist IP en MongoDB Atlas
- Inicia MongoDB local

### Error: "No module named 'django'"
```bash
# Asegúrate de activar venv:
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/macOS
```

### Error: "Cámara no funciona"
- Usa Chrome/Firefox/Edge
- Permite permisos de cámara
- Cierra otras apps usando cámara

---

## 📚 Documentación Completa

Ver: [README.md](README.md)

---

## 🆘 Ayuda

- **Issues:** [GitHub Issues](https://github.com/TU_USUARIO/TU_REPO/issues)
- **Email:** tu-email@example.com

---

**¡Listo para empezar!** 🎉

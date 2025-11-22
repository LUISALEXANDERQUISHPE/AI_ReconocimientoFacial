# ⚡ Quick Start - 3 Comandos

Para poner el sistema en marcha rápidamente:

## 1️⃣ Instalar

```bash
pip install -r requirements.txt
```

## 2️⃣ Configurar

Edita `settings.py` línea 140 con tu MongoDB URI:

```python
MONGODB_SETTINGS = {
    'URI': 'mongodb+srv://USER:PASS@cluster.mongodb.net/',
    'DB_NAME': 'face_recognition_system'
}
```

## 3️⃣ Ejecutar

```bash
python manage.py migrate
python manage.py runserver
```

## ✅ Listo!

Accede a: **http://127.0.0.1:8000**

---

## 🎯 Flujo de Uso

1. **Registrar 2+ personas** → `/register/`
2. **Entrenar modelo** → `/train/`
3. **Login facial** → `/` (página principal)

---

## 📚 Documentación Completa

- **Instalación detallada:** [INSTALL.md](INSTALL.md)
- **Manual completo:** [README.md](README.md)
- **Contribuir:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

**¿Problemas?** Ejecuta:

```bash
python check_installation.py
```

Este script verifica que todo esté correctamente instalado.

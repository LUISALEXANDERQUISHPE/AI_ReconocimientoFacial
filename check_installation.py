"""
Script de verificación de instalación
Ejecutar después de instalar dependencias para validar que todo funciona
"""

import sys
import os

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python_version():
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.10+")
        return False

def check_dependencies():
    print("\n📦 Verificando dependencias...")
    dependencies = [
        ('django', 'Django'),
        ('pymongo', 'PyMongo'),
        ('cv2', 'OpenCV'),
        ('tensorflow', 'TensorFlow'),
        ('numpy', 'NumPy'),
        ('sklearn', 'Scikit-learn'),
        ('PIL', 'Pillow')
    ]
    
    all_ok = True
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"   ✅ {display_name} - Instalado")
        except ImportError:
            print(f"   ❌ {display_name} - NO instalado")
            all_ok = False
    
    return all_ok

def check_directories():
    print("\n📁 Verificando estructura de directorios...")
    directories = [
        'face_recognition_app',
        'face_recognition_app/templates',
        'face_recognition_app/templates/face_recognition',
        'media',
        'media/models',
        'media/samples'
    ]
    
    all_ok = True
    for directory in directories:
        if os.path.exists(directory):
            print(f"   ✅ {directory}/ - Existe")
        else:
            print(f"   ❌ {directory}/ - NO existe")
            all_ok = False
    
    return all_ok

def check_required_files():
    print("\n📄 Verificando archivos requeridos...")
    files = [
        'manage.py',
        'settings.py',
        'face_recognition_app/views.py',
        'face_recognition_app/utils.py',
        'face_recognition_app/urls.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            print(f"   ✅ {file} - Existe")
        else:
            print(f"   ❌ {file} - NO existe")
            all_ok = False
    
    return all_ok

def check_mongodb_config():
    print("\n🗄️  Verificando configuración de MongoDB...")
    try:
        with open('settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'MONGODB_SETTINGS' in content:
                print("   ✅ MONGODB_SETTINGS encontrado en settings.py")
                if 'mongodb+srv://' in content or 'mongodb://localhost' in content:
                    print("   ⚠️  Recuerda configurar tu URI de MongoDB real")
                    return True
            else:
                print("   ❌ MONGODB_SETTINGS NO encontrado en settings.py")
                return False
    except Exception as e:
        print(f"   ❌ Error leyendo settings.py: {e}")
        return False

def main():
    print_header("🔍 VERIFICACIÓN DE INSTALACIÓN")
    print("Sistema de Reconocimiento Facial - Django + MongoDB")
    
    results = []
    
    # Ejecutar verificaciones
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencias", check_dependencies()))
    results.append(("Directorios", check_directories()))
    results.append(("Archivos", check_required_files()))
    results.append(("MongoDB Config", check_mongodb_config()))
    
    # Resumen
    print_header("📊 RESUMEN")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}  {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("\n🎉 ¡TODO CORRECTO! El sistema está listo para ejecutarse.")
        print("\n📝 Próximos pasos:")
        print("   1. Configura tu URI de MongoDB en settings.py")
        print("   2. Ejecuta: python manage.py migrate")
        print("   3. Ejecuta: python manage.py runserver")
        print("   4. Accede a: http://127.0.0.1:8000")
    else:
        print("\n⚠️  HAY PROBLEMAS. Por favor revisa los errores arriba.")
        print("\n📝 Soluciones comunes:")
        print("   - Instala dependencias: pip install -r requirements.txt")
        print("   - Verifica que estás en el directorio correcto")
        print("   - Activa el entorno virtual (venv)")
    
    print("\n" + "="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

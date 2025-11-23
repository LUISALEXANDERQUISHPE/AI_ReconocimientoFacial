# face_recognition_app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import json
import time
import os
import shutil
from datetime import datetime, timedelta
from pymongo import MongoClient
from .utils import FaceRecognitionUtils, ModelTrainer
from django.conf import settings

# Configuración MongoDB
MONGO_URI = getattr(settings, 'MONGODB_SETTINGS', {}).get('URI', 
    'mongodb+srv://lithubprogramadores_db_user:NlejQAZ9OuLJnv55@ai.xr4bewc.mongodb.net/?appName=Ai')
DB_NAME = getattr(settings, 'MONGODB_SETTINGS', {}).get('DB_NAME', 'face_recognition_system')

try:
    mongo_client = MongoClient(MONGO_URI)
    mongo_db = mongo_client[DB_NAME]
    persons_collection = mongo_db['persons']
    encodings_collection = mongo_db['face_encodings']
    trainings_collection = mongo_db['model_trainings']
    logs_collection = mongo_db['recognition_logs']
    recognition_logs_collection = mongo_db['recognition_logs']  # Alias para consistencia
    mongo_client.admin.command('ping')
    print(" MongoDB conectado exitosamente")
except Exception as e:
    print(f" Error conectando a MongoDB: {e}")
    mongo_client = None

# Instancia global de utilidades
face_utils = FaceRecognitionUtils()

def login_view(request):
    """Página de login facial"""
    return render(request, 'face_recognition/login.html')

def register_page(request):
    """Página de registro con 3 pasos"""
    return render(request, 'face_recognition/register.html')

def dashboard(request):
    """Dashboard principal con tabla de personas"""
    # Obtener info del usuario desde session (simple)
    user_name = request.session.get('user_name', 'Administrador')
    user_department = request.session.get('user_department', 'Sistema')
    
    # VERIFICACIÓN DESHABILITADA TEMPORALMENTE PARA PRIMER ENTRENAMIENTO
    # Permitir acceso directo si no hay modelo entrenado
    from pymongo import MongoClient
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        trainings = db['model_trainings']
        model_exists = trainings.find_one({'is_active': True}) is not None
        
        # Si no hay modelo entrenado, permitir acceso directo
        if not model_exists:
            messages.info(request, ' Modo administrador: No hay modelo entrenado. Por favor entrena el modelo primero.')
            request.session['authenticated'] = True
            request.session['user_name'] = 'Administrador'
            request.session['user_department'] = 'Sistema'
    except:
        pass
    
    # Verificar si hay usuario reconocido (solo si ya hay modelo)
    if not request.session.get('authenticated'):
        messages.warning(request, 'Debes autenticarte con reconocimiento facial')
        return redirect('login')
    
    context = {
        'user_name': user_name,
        'user_department': user_department
    }
    return render(request, 'face_recognition/dashboard.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def api_recognize_login(request):
    """API para reconocer rostro en el login"""
    try:
        data = json.loads(request.body)
        image_data = data.get('image')
        
        if not image_data:
            return JsonResponse({'success': False, 'error': 'No image data'}, status=400)
        
        # Decodificar imagen
        frame = face_utils.decode_base64_image(image_data)
        if frame is None:
            return JsonResponse({'success': False, 'error': 'Invalid image'}, status=400)
        
        # Detectar rostros
        faces = face_utils.detect_faces(frame)
        
        if len(faces) == 0:
            return JsonResponse({
                'success': True,
                'authenticated': False,
                'faces': []
            })
        
        # Tomar el primer rostro
        x, y, w, h = faces[0]
        face_roi = frame[y:y+h, x:x+w]
        
        # Reconocer
        name, confidence = face_utils.recognize_face(face_roi)
        
        # Si no hay modelo entrenado
        if name is None:
            return JsonResponse({
                'success': True,
                'authenticated': False,
                'message': ' No hay modelo entrenado. Ve a /train/ para entrenar.',
                'faces': [{
                    'bbox': {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)},
                    'name': 'Desconocido',
                    'label': 'Sin modelo entrenado',
                    'confidence': 0.0,
                    'status': 'no_model'
                }]
            })
        
        if name is not None and confidence > 0.97:  # Umbral del 95%
            # Buscar persona en MongoDB
            person = persons_collection.find_one({'name': name})
            
            if person:
                # Crear sesión simple
                request.session['user_id'] = str(person['_id'])
                request.session['user_name'] = person['name']
                request.session['user_department'] = person.get('department', 'Usuario')
                request.session['authenticated'] = True
                
                # Log de acceso
                logs_collection.insert_one({
                    'person_id': str(person['_id']),
                    'person_name': name,
                    'confidence': float(confidence),
                    'timestamp': datetime.now(),
                    'event_type': 'login',
                    'ip_address': request.META.get('REMOTE_ADDR')
                })
                
                return JsonResponse({
                    'success': True,
                    'authenticated': True,
                    'name': name,
                    'confidence': float(confidence),
                    'redirect_url': '/dashboard/'
                })
        
        # Responder con detección pero sin autenticación
        face_info = []
        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            name, confidence = face_utils.recognize_face(face_roi)
            
            if name:
                confidence_pct = f"{confidence * 100:.1f}%"
                if confidence > 0.97:
                    status = 'confirmed'
                    label = f'{name} ({confidence_pct})'
                    message = f' Reconocido: {name} - Confianza: {confidence_pct}'
                elif confidence > 0.90:
                    status = 'insufficient'
                    label = f'{name} - Insuficiente ({confidence_pct})'
                    message = f' Confianza insuficiente: {confidence_pct} (se requiere >95%)'
                else:
                    status = 'unknown'
                    label = f'Desconocido ({confidence_pct})'
                    message = f' No reconocido - Confianza muy baja: {confidence_pct}'
                
                face_info.append({
                    'bbox': {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)},
                    'name': name if confidence > 0.70 else 'Desconocido',
                    'label': label,
                    'confidence': float(confidence),
                    'status': status,
                    'message': message
                })
            else:
                face_info.append({
                    'bbox': {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)},
                    'name': 'Sin modelo',
                    'label': 'Entrenar modelo',
                    'confidence': 0.0,
                    'status': 'no_model',
                    'message': ' Entrena el modelo primero'
                })
        
        return JsonResponse({
            'success': True,
            'authenticated': False,
            'faces': face_info,
            'message': face_info[0].get('message', '') if face_info else ''
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_register_complete(request):
    """API para guardar registro completo con encodings por lotes + muestras visuales"""
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        department = data.get('department')
        encodings_data = data.get('encodings', [])
        sample_images = data.get('sample_images', [])  # Muestras visuales (6 imágenes)
        
        if not name or not encodings_data:
            return JsonResponse({'success': False, 'error': 'Faltan datos'}, status=400)
        
        # Verificar si ya existe
        existing = encodings_collection.find_one({'person_name': name})
        if existing:
            return JsonResponse({'success': False, 'error': 'Esta persona ya está registrada'}, status=400)
        
        # Extraer solo los arrays de encodings
        face_encodings_list = [enc['encoding'] for enc in encodings_data]
        
        # Guardar imágenes de muestra (6 frames estratégicos) para trazabilidad
        sample_paths = []
        if sample_images:
            import os
            import base64
            from django.conf import settings
            
            person_dir = os.path.join(settings.MEDIA_ROOT, 'samples', name.replace(' ', '_'))
            os.makedirs(person_dir, exist_ok=True)
            
            for idx, img_data in enumerate(sample_images):
                try:
                    # Decodificar imagen base64
                    img_bytes = base64.b64decode(img_data.split(',')[1] if ',' in img_data else img_data)
                    img_path = os.path.join(person_dir, f'sample_{idx+1}.jpg')
                    
                    with open(img_path, 'wb') as f:
                        f.write(img_bytes)
                    
                    sample_paths.append(f'samples/{name.replace(" ", "_")}/sample_{idx+1}.jpg')
                except Exception as e:
                    print(f" Error guardando muestra {idx+1}: {e}")
        
        # Guardar UN SOLO documento con TODOS los encodings de la persona
        person_doc = {
            'person_name': name,
            'email': email,
            'empresa': department,
            'face_encodings': face_encodings_list,  # Lista de listas (cada encoding es lista de 128 valores)
            'sample_images': sample_paths,  # Rutas a las 6 muestras visuales
            'timestamp': datetime.now().timestamp(),
            'registration_date': datetime.now(),
            'total_encodings': len(face_encodings_list),
            'total_samples': len(sample_paths),
            'encoding_dimension': 128,
            'extraction_method': 'opencv_custom_features',
            'status': 'registered',
            'capture_date': datetime.now()
        }
        encoding_result = encodings_collection.insert_one(person_doc)
        
        # Guardar también en persons (opcional, para stats)
        person_simple = {
            'name': name,
            'email': email,
            'department': department,
            'is_active': True,
            'created_at': datetime.now(),
            'total_encodings': len(face_encodings_list),
            'total_samples': len(sample_paths)
        }
        persons_collection.insert_one(person_simple)
        
        return JsonResponse({
            'success': True,
            'message': f'Persona registrada con {len(face_encodings_list)} encodings + {len(sample_paths)} muestras',
            'encoding_id': str(encoding_result.inserted_id),
            'total_encodings': len(face_encodings_list),
            'total_samples': len(sample_paths)
        })
        
    except Exception as e:
        import traceback
        print(f" Error en register_complete: {traceback.format_exc()}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def process_frame(request):
    """API para procesar frame y extraer encodings"""
    try:
        data = json.loads(request.body)
        image_data = data.get('image')
        person_name = data.get('person_name', 'temp') 
        
        if not image_data:
            return JsonResponse({'success': False, 'error': 'No image data'}, status=400)
        
        frame = face_utils.decode_base64_image(image_data)
        if frame is None:
            return JsonResponse({'success': False, 'error': 'Invalid image'}, status=400)
        
        faces = face_utils.detect_faces(frame)
        
        results = []
        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            encoding = face_utils.extract_face_encoding(face_roi)
            
            if encoding is not None:
                import cv2
                blur_score = cv2.Laplacian(cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
                
                results.append({
                    'bbox': {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)},
                    'encoding': encoding.tolist(),
                    'quality_score': float(blur_score),
                    'confidence': 0.8
                })
        
        return JsonResponse({
            'success': True,
            'faces_detected': len(results),
            'faces': results
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def api_dashboard_stats(request):
    """API para estadísticas del dashboard"""
    try:
        total_persons = persons_collection.count_documents({'is_active': True})
        
        # Reconocimientos de hoy
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_recognitions = logs_collection.count_documents({
            'timestamp': {'$gte': today_start}
        })
        
        # Estado del modelo
        latest_training = trainings_collection.find_one(
            {'is_active': True},
            sort=[('training_date', -1)]
        )
        
        if latest_training:
            model_status = f" Entrenado ({latest_training['final_accuracy']:.0%})"
        else:
            model_status = " Sin entrenar"
        
        return JsonResponse({
            'success': True,
            'total_persons': total_persons,
            'today_recognitions': today_recognitions,
            'model_status': model_status
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def api_persons_list(request):
    """API para listar personas desde MongoDB"""
    try:
        persons = list(persons_collection.find({}).sort('created_at', -1))
        
        persons_data = []
        for person in persons:
            persons_data.append({
                'id': str(person['_id']),
                'name': person['name'],
                'email': person.get('email', ''),
                'department': person.get('department', ''),
                'is_active': person.get('is_active', True),
                'created_at': person['created_at'].isoformat(),
                'total_encodings': person.get('total_encodings', 0)
            })
        
        return JsonResponse({
            'success': True,
            'persons': persons_data
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_delete_person(request):
    """API para eliminar persona completamente"""
    try:
        data = json.loads(request.body)
        person_id = data.get('person_id')
        
        if not person_id:
            return JsonResponse({'success': False, 'error': 'No person_id'}, status=400)
        
        from bson import ObjectId
        import shutil
        
        # 1. Obtener información de la persona antes de eliminar
        person = persons_collection.find_one({'_id': ObjectId(person_id)})
        
        if not person:
            return JsonResponse({'success': False, 'error': 'Persona no encontrada'}, status=404)
        
        person_name = person.get('name')
        
        # 2. Eliminar encodings de MongoDB (usar person_name que es el campo correcto)
        result_encodings = encodings_collection.delete_many({'person_name': person_name})
        print(f" Eliminados {result_encodings.deleted_count} encodings de {person_name}")
        
        # 3. Eliminar carpeta de muestras en media/samples/NOMBRE_PERSONA/
        samples_path = os.path.join(settings.MEDIA_ROOT, 'samples', person_name)
        if os.path.exists(samples_path):
            try:
                shutil.rmtree(samples_path)
                print(f" Carpeta eliminada: {samples_path}")
            except Exception as e:
                print(f" Error eliminando carpeta {samples_path}: {e}")
        
        # 4. Eliminar logs de reconocimiento (opcional, para limpiar historial)
        try:
            result_logs = recognition_logs_collection.delete_many({'person_name': person_name})
            print(f" Eliminados {result_logs.deleted_count} logs de reconocimiento")
        except Exception as e:
            print(f" Error eliminando logs: {e}")
        
        # 5. Eliminar persona de MongoDB
        persons_collection.delete_one({'_id': ObjectId(person_id)})
        print(f" Persona {person_name} eliminada completamente")
        
        # Verificar si la carpeta fue eliminada
        folder_deleted = not os.path.exists(samples_path)
        
        return JsonResponse({
            'success': True,
            'message': f'Persona {person_name} eliminada completamente',
            'deleted': {
                'encodings': result_encodings.deleted_count,
                'samples_folder': folder_deleted
            }
        })
        
    except Exception as e:
        print(f" Error en api_delete_person: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def train_model_view(request):
    """Vista para entrenar modelo"""
    if request.method == 'POST':
        try:
            trainer = ModelTrainer()
            result = trainer.train()  # Usar método train() que ya existe
            
            if result['success']:
                # Guardar en MongoDB
                training_doc = {
                    'training_date': datetime.now(),
                    'model_file': result.get('model_filename', 'modelo_rostros.h5'),
                    'classes_file': result.get('classes_filename', 'clases.npy'),
                    'total_samples': result['total_samples'],
                    'num_classes': result['num_classes'],
                    'final_accuracy': result['accuracy'],  # Guardar como decimal (0.0 a 1.0)
                    'final_val_accuracy': result.get('val_accuracy') if result.get('val_accuracy') else None,
                    'training_time_seconds': result['training_time'],
                    'is_active': True
                }
                
                # Desactivar modelos anteriores
                trainings_collection.update_many({}, {'$set': {'is_active': False}})
                trainings_collection.insert_one(training_doc)
                
                # Recargar el modelo en memoria
                face_utils.load_model()
                
                messages.success(request, f" ¡Modelo entrenado exitosamente! Precisión: {result['accuracy']:.1%} | Muestras: {result['total_samples']} | Clases: {result['num_classes']}")
            else:
                messages.error(request, f" Error al entrenar: {result.get('error', 'Error desconocido')}")
        except Exception as e:
            messages.error(request, f" Error durante el entrenamiento: {str(e)}")
        
        return redirect('train_model')
    
    # GET: Mostrar página
    persons = list(persons_collection.find({}))
    total_encodings = encodings_collection.count_documents({})
    latest_training = trainings_collection.find_one({'is_active': True}, sort=[('training_date', -1)])
    
    context = {
        'persons': persons,
        'total_encodings': total_encodings,
        'latest_training': latest_training
    }
    
    return render(request, 'face_recognition/train_model.html', context)

def recognition_view(request):
    """Vista de reconocimiento en tiempo real"""
    context = {
        'model_loaded': face_utils.model is not None,
        'available_classes': list(face_utils.classes) if face_utils.classes is not None else []
    }
    return render(request, 'face_recognition/recognition.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def api_recognize_realtime(request):
    """API para reconocimiento facial en tiempo real (solo muestra info, no autentica)"""
    try:
        data = json.loads(request.body)
        image_data = data.get('image')
        
        if not image_data:
            return JsonResponse({'success': False, 'error': 'No image data'}, status=400)
        
        # Decodificar imagen
        frame = face_utils.decode_base64_image(image_data)
        if frame is None:
            return JsonResponse({'success': False, 'error': 'Invalid image'}, status=400)
        
        # Detectar rostros
        faces = face_utils.detect_faces(frame)
        
        if len(faces) == 0:
            return JsonResponse({
                'success': True,
                'faces_detected': 0,
                'faces': []
            })
        
        # Reconocer cada rostro detectado
        faces_info = []
        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            name, confidence = face_utils.recognize_face(face_roi)
            
            if name and confidence > 0.90:  # Umbral más bajo para mostrar info
                confidence_pct = f"{confidence * 100:.1f}%"
                status = 'confirmed' if confidence > 0.97 else 'low_confidence'
                
                faces_info.append({
                    'name': name,
                    'confidence': float(confidence),
                    'confidence_pct': confidence_pct,
                    'status': status,
                    'bbox': {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)}
                })
            else:
                faces_info.append({
                    'name': 'Desconocido',
                    'confidence': float(confidence) if confidence else 0.0,
                    'confidence_pct': f"{confidence * 100:.1f}%" if confidence else "0%",
                    'status': 'unknown',
                    'bbox': {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)}
                })
        
        return JsonResponse({
            'success': True,
            'faces_detected': len(faces_info),
            'faces': faces_info
        })
        
    except Exception as e:
        import traceback
        print(f" Error en reconocimiento: {traceback.format_exc()}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def logout_view(request):
    """Cerrar sesión"""
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')
# face_recognition_app/utils.py
import cv2
import numpy as np
import tensorflow as tf
import os
import base64
from pathlib import Path
from django.conf import settings

class FaceRecognitionUtils:
    """Utilidades para reconocimiento facial"""
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.model = None
        self.classes = None
        self.load_model()
    
    def load_model(self):
        """Carga el modelo entrenado más reciente desde MongoDB"""
        try:
            from pymongo import MongoClient
            
            MONGO_URI = getattr(settings, 'MONGODB_SETTINGS', {}).get('URI', '')
            DB_NAME = getattr(settings, 'MONGODB_SETTINGS', {}).get('DB_NAME', 'face_recognition_system')
            
            client = MongoClient(MONGO_URI)
            db = client[DB_NAME]
            trainings_collection = db['model_trainings']
            
            # Obtener el modelo activo más reciente
            latest_training = trainings_collection.find_one(
                {'is_active': True},
                sort=[('training_date', -1)]
            )
            
            if latest_training:
                model_path = os.path.join(settings.MEDIA_ROOT, 'models', latest_training['model_file'])
                classes_path = os.path.join(settings.MEDIA_ROOT, 'models', latest_training['classes_file'])
                
                if os.path.exists(model_path) and os.path.exists(classes_path):
                    self.model = tf.keras.models.load_model(model_path)
                    self.classes = np.load(classes_path, allow_pickle=True)
                    print(f"✅ Modelo cargado: {latest_training['model_file']} con {len(self.classes)} clases")
                    return True
                else:
                    print(f"❌ Archivos no encontrados: {model_path} o {classes_path}")
            
            return False
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            return False
    
    def extract_face_encoding(self, face_image):
        """Extrae características faciales (encoding)"""
        try:
            face_resized = cv2.resize(face_image, (64, 64))
            
            if len(face_resized.shape) == 3:
                gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
            else:
                gray = face_resized
            
            gray = gray.astype(np.uint8)
            gray = cv2.equalizeHist(gray)
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            
            h, w = gray.shape
            caracteristicas = []
            
            # Dividir en 8x8 regiones
            for i in range(0, h, 8):
                for j in range(0, w, 8):
                    region = gray[i:i+8, j:j+8]
                    if region.size > 0:
                        caracteristicas.append(np.mean(region))
                        caracteristicas.append(np.std(region))
            
            caracteristicas.append(np.mean(gray))
            caracteristicas.append(np.std(gray))
            caracteristicas.append(np.median(gray))
            
            while len(caracteristicas) < 128:
                caracteristicas.append(0.0)
            
            caracteristicas = caracteristicas[:128]
            caracteristicas = np.array(caracteristicas, dtype=np.float32)
            
            if np.linalg.norm(caracteristicas) > 0:
                caracteristicas = caracteristicas / np.linalg.norm(caracteristicas)
            
            return caracteristicas
            
        except Exception as e:
            print(f"Error extrayendo características: {e}")
            return None
    
    def detect_faces(self, frame):
        """Detecta rostros en un frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(80, 80)
        )
        return faces
    
    def recognize_face(self, face_image):
        """Reconoce un rostro usando el modelo entrenado"""
        if self.model is None or self.classes is None:
            return None, 0.0
        
        features = self.extract_face_encoding(face_image)
        if features is None:
            return None, 0.0
        
        features_batch = features.reshape(1, -1)
        prediction = self.model.predict(features_batch, verbose=0)[0]
        
        idx_max = np.argmax(prediction)
        confidence = prediction[idx_max]
        nombre_detectado = self.classes[idx_max]
        
        return nombre_detectado, confidence
    
    def decode_base64_image(self, base64_string):
        """Decodifica imagen base64 a numpy array"""
        try:
            # Remover prefijo data:image si existe
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            img_data = base64.b64decode(base64_string)
            nparr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img
        except Exception as e:
            print(f"Error decodificando imagen: {e}")
            return None
    
    def encode_image_to_base64(self, image):
        """Codifica imagen numpy array a base64"""
        try:
            _, buffer = cv2.imencode('.jpg', image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            return f"data:image/jpeg;base64,{img_base64}"
        except Exception as e:
            print(f"Error codificando imagen: {e}")
            return None

class ModelTrainer:
    """Clase para entrenar el modelo con datos de MongoDB"""
    
    def __init__(self):
        self.model_dir = os.path.join(settings.MEDIA_ROOT, 'models')
        Path(self.model_dir).mkdir(parents=True, exist_ok=True)
    
    def load_encodings_from_mongodb(self):
        """Carga todas las huellas faciales desde MongoDB"""
        from pymongo import MongoClient
        
        MONGO_URI = getattr(settings, 'MONGODB_SETTINGS', {}).get('URI', 
            'mongodb+srv://lithubprogramadores_db_user:NlejQAZ9OuLJnv55@ai.xr4bewc.mongodb.net/?appName=Ai')
        DB_NAME = getattr(settings, 'MONGODB_SETTINGS', {}).get('DB_NAME', 'face_recognition_system')
        
        try:
            client = MongoClient(MONGO_URI)
            db = client[DB_NAME]
            encodings_collection = db['face_encodings']
            
            # Obtener todos los documentos (1 doc = 1 persona con lista de encodings)
            encodings_cursor = encodings_collection.find({})
            
            X = []
            y = []
            
            for doc in encodings_cursor:
                try:
                    person_name = doc.get('person_name')
                    face_encodings = doc.get('face_encodings', [])
                    
                    if not person_name or not face_encodings:
                        continue
                    
                    # Expandir todos los encodings de esta persona
                    for encoding in face_encodings:
                        encoding_array = np.array(encoding, dtype=np.float32)
                        X.append(encoding_array)
                        y.append(person_name)
                    
                except Exception as e:
                    print(f"Error procesando doc {doc.get('_id')}: {e}")
                    continue
            
            if len(X) == 0:
                print("⚠️ No se encontraron encodings en MongoDB")
                return np.array([]), np.array([])
            
            print(f"✅ Cargados {len(X)} encodings de MongoDB")
            return np.array(X, dtype=np.float32), np.array(y)
            
        except Exception as e:
            print(f"Error cargando desde MongoDB: {e}")
            return np.array([]), np.array([])
    
    def load_encodings_from_db(self):
        """Alias para compatibilidad - usa MongoDB"""
        return self.load_encodings_from_mongodb()
    
    def train_from_mongodb(self):
        """Alias para compatibilidad - redirige a train()"""
        return self.train()
    
    def build_model(self, num_classes):
        """Construye el modelo de red neuronal"""
        model = tf.keras.models.Sequential([
            tf.keras.layers.Input(shape=(128,)),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(num_classes, activation="softmax")
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        
        return model
    
    def train(self):
        """Entrena el modelo con los datos de la base de datos"""
        import time
        from sklearn.preprocessing import LabelEncoder
        
        X, y = self.load_encodings_from_db()
        
        if len(X) == 0:
            return {'success': False, 'error': 'No hay datos para entrenar'}
        
        # Codificar etiquetas
        le = LabelEncoder()
        y_int = le.fit_transform(y)
        classes = le.classes_
        num_classes = len(classes)
        
        if num_classes < 2:
            return {'success': False, 'error': 'Se necesitan al menos 2 personas'}
        
        y_cat = tf.keras.utils.to_categorical(y_int, num_classes=num_classes)
        
        # Construir modelo
        model = self.build_model(num_classes)
        
        # Entrenar
        epochs = min(1000, max(20, len(X) * 2))
        batch_size = max(4, min(32, len(X) // 4))
        
        start_time = time.time()
        
        history = model.fit(
            X, y_cat,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.1,
            verbose=0,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
                tf.keras.callbacks.ReduceLROnPlateau(patience=5, factor=0.5)
            ]
        )
        
        training_time = time.time() - start_time
        
        # Eliminar modelos antiguos
        if os.path.exists(self.model_dir):
            for file in os.listdir(self.model_dir):
                if file.endswith('.h5') or file.endswith('.npy'):
                    old_file_path = os.path.join(self.model_dir, file)
                    try:
                        os.remove(old_file_path)
                        print(f"🗑️ Eliminado: {file}")
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar {file}: {e}")
        
        # Guardar nuevo modelo
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        model_filename = f'modelo_{timestamp}.h5'
        classes_filename = f'clases_{timestamp}.npy'
        
        model_path = os.path.join(self.model_dir, model_filename)
        classes_path = os.path.join(self.model_dir, classes_filename)
        
        model.save(model_path)
        np.save(classes_path, classes)
        print(f"✅ Nuevo modelo guardado: {model_filename}")
        
        # Preparar resultado
        final_acc = history.history['accuracy'][-1]
        val_acc = history.history.get('val_accuracy', [None])[-1]
        
        return {
            'success': True,
            'model_filename': model_filename,
            'classes_filename': classes_filename,
            'accuracy': final_acc,
            'val_accuracy': val_acc,
            'training_time': training_time,
            'total_samples': len(X),
            'num_classes': num_classes,
            'classes': list(classes)
        }
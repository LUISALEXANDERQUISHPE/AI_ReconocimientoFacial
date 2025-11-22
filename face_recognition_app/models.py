# face_recognition_app/models.py
# Archivo vacío - Todo se maneja en MongoDB
# Django requiere este archivo pero no lo usamos

# Los modelos comentados están aquí solo como referencia
# de la estructura en MongoDB, pero NO SE USAN

"""
MongoDB Collections Structure:

persons:
{
    _id: ObjectId,
    name: String,
    email: String,
    department: String,
    is_active: Boolean,
    created_at: DateTime,
    total_encodings: Integer
}

face_encodings:
{
    _id: ObjectId,
    person_id: String,
    person_name: String,
    encoding: Array[128],
    quality_score: Float,
    confidence: Float,
    capture_date: DateTime
}

model_trainings:
{
    _id: ObjectId,
    training_date: DateTime,
    model_file: String,
    classes_file: String,
    total_samples: Integer,
    num_classes: Integer,
    final_accuracy: Float,
    final_val_accuracy: Float,
    training_time_seconds: Float,
    is_active: Boolean
}

recognition_logs:
{
    _id: ObjectId,
    person_id: String,
    person_name: String,
    confidence: Float,
    timestamp: DateTime,
    event_type: String,
    ip_address: String
}
"""

# routes/predict.py - VERSIÓN CORREGIDA

from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from models.cnn_model import copper_model  # ← CAMBIADO: usar copper_model en lugar de predict_copper
import uuid
from datetime import datetime

predict_bp = Blueprint('predict', __name__)

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@predict_bp.route('/predict', methods=['GET'])
def predict_page():
    return render_template('predict.html')

@predict_bp.route('/api/predict', methods=['POST'])
def predict_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Generar nombre único para el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Realizar predicción - CAMBIADO: usar copper_model.predict()
            prediction, confidence = copper_model.predict(filepath)
            
            if prediction is None:
                return jsonify({'error': 'Error en la predicción'}), 500
            
            # Guardar resultado en base de datos si es necesario
            result_data = {
                'filename': unique_filename,
                'original_name': filename,
                'prediction': prediction,
                'confidence': confidence,  # Ya viene en porcentaje
                'timestamp': datetime.now().isoformat(),
                'file_path': filepath
            }
            
            return jsonify({
                'success': True,
                'prediction': prediction,
                'confidence': confidence,
                'filename': unique_filename,
                'result_id': str(uuid.uuid4())
            })
        
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400
        
    except Exception as e:
        return jsonify({'error': f'Error del servidor: {str(e)}'}), 500
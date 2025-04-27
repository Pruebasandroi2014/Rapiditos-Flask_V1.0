from flask import Flask, render_template, request, jsonify, url_for
import requests
import time
import config
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    if 'logo' not in request.files:
        return jsonify({'success': False, 'mensaje': 'No se seleccionó ningún archivo'})
    
    file = request.files['logo']
    if file.filename == '':
        return jsonify({'success': False, 'mensaje': 'No se seleccionó ningún archivo'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename('logo.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': True, 'mensaje': 'Logo subido correctamente'})
    
    return jsonify({'success': False, 'mensaje': 'Tipo de archivo no permitido'})

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/config', methods=['GET', 'POST'])
def admin_config():
    if request.method == 'POST':
        data = request.get_json()
        config.COSTO_POR_KM = float(data['costo_km'])
        return jsonify({
            'success': True,
            'mensaje': 'Configuración actualizada correctamente'
        })
    return jsonify({'costo_km': config.COSTO_POR_KM})

def obtener_coordenadas(direccion):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={direccion}&format=json"
        headers = {'User-Agent': 'Replit Distance Calculator'}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()

        if data and len(data) > 0:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon
        return None
    except Exception as e:
        print(f"Error al obtener coordenadas para {direccion}: {str(e)}")
        return None

def calcular_distancia(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2

    R = 6371  # Radio de la Tierra en kilómetros

    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distancia = R * c

    return round(distancia, 2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        inicio = request.form['inicio'].split(',')
        destino = request.form['destino'].split(',')

        lat1, lon1 = float(inicio[0]), float(inicio[1])
        lat2, lon2 = float(destino[0]), float(destino[1])

        distancia = calcular_distancia(lat1, lon1, lat2, lon2)
        if distancia:
            costo = distancia * config.COSTO_POR_KM
            return jsonify({
                "success": True,
                "distancia": distancia,
                "costo": costo,
                "mensaje": f"La distancia es: {distancia} km y el costo es: ${costo:.2f}"
            })
        return jsonify({
            "success": False,
            "mensaje": "No se pudo calcular la distancia entre los puntos seleccionados"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "mensaje": f"Error al calcular la distancia: {str(e)}"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
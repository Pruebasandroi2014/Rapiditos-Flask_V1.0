
from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

def obtener_coordenadas(direccion):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={direccion}&format=json"
        headers = {'User-Agent': 'Replit Distance Calculator'}
        response = requests.get(url, headers=headers)
        data = response.json()

        if data and len(data) > 0:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            time.sleep(1)  # Respetar límites de uso
            return lat, lon
        return None
    except Exception as e:
        print(f"Error al obtener coordenadas para {direccion}: {str(e)}")
        return None

def calcular_distancia(lat1, lon1, lat2, lon2):
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
    response = requests.get(url)
    data = response.json()

    if "routes" in data and data["routes"]:
        distancia_km = data["routes"][0]["distance"] / 1000
        return round(distancia_km, 2)
    return None

import os

@app.route('/')
def home():
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY', '')
    return render_template('index.html', api_key=api_key)

@app.route('/calcular', methods=['POST'])
def calcular():
    direccion_inicio = request.form['inicio']
    direccion_destino = request.form['destino']
    
    coordenadas_inicio = obtener_coordenadas(direccion_inicio)
    coordenadas_destino = obtener_coordenadas(direccion_destino)
    
    if coordenadas_inicio and coordenadas_destino:
        distancia = calcular_distancia(*coordenadas_inicio, *coordenadas_destino)
        return jsonify({
            "success": True,
            "distancia": distancia,
            "mensaje": f"Distancia entre {direccion_inicio} y {direccion_destino}: {distancia} km"
        })
    return jsonify({
        "success": False,
        "mensaje": "No se pudo calcular la distancia. Por favor, asegúrate de escribir direcciones válidas y específicas, incluyendo la ciudad y el país. Por ejemplo: 'Caracas, Venezuela' o 'Maracaibo, Venezuela'"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

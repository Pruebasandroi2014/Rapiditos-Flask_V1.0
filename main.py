
from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

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
    try:
        url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "Ok" and "routes" in data:
                return round(data["routes"][0]["distance"] / 1000, 2)
        return None
            
        data = response.json()
        
        if data.get("code") != "Ok":
            print(f"Error en la respuesta: {data.get('message', 'Error desconocido')}")
            return None
            
        if "routes" in data and data["routes"]:
            distancia_km = data["routes"][0]["distance"] / 1000
            return round(distancia_km, 2)
            
        return None
    except Exception as e:
        print(f"Error al calcular distancia: {str(e)}")
        return None

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
            return jsonify({
                "success": True,
                "distancia": distancia,
                "mensaje": f"La distancia es: {distancia} km"
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

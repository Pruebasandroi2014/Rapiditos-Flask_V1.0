
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
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Radio de la Tierra en kilómetros
    
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distancia = R * c
    
    return round(distancia, 2)
        
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

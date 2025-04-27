import requests

# Clave de API de Google Maps (sustituye 'YOUR_API_KEY' por tu clave real)
API_KEY = "YOUR_API_KEY"

# Función para obtener coordenadas a partir de una dirección
def obtener_coordenadas(direccion):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        lat = data["results"][0]["geometry"]["location"]["lat"]
        lng = data["results"][0]["geometry"]["location"]["lng"]
        return lat, lng
    else:
        return None

# Función para calcular la distancia entre dos coordenadas usando OSRM
def calcular_distancia(lat1, lon1, lat2, lon2):
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
    response = requests.get(url)
    data = response.json()

    if "routes" in data and data["routes"]:
        distancia_km = data["routes"][0]["distance"] / 1000
        return round(distancia_km, 2)
    else:
        return None

# 📍 Ejemplo de uso
direccion_inicio = "Caracas, Venezuela"
direccion_destino = "Maracaibo, Venezuela"

coordenadas_inicio = obtener_coordenadas(direccion_inicio)
coordenadas_destino = obtener_coordenadas(direccion_destino)

if coordenadas_inicio and coordenadas_destino:
    distancia = calcular_distancia(*coordenadas_inicio, *coordenadas_destino)
    print(f"Distancia entre {direccion_inicio} y {direccion_destino}: {distancia} km")
else:
    print("Error al obtener coordenadas.")
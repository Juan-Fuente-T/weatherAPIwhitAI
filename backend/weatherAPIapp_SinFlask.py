
from flask import Flask, request, jsonify
from weather_utils import is_postal_code, geocode_location, geocode_postal_code, get_weather#, consulta_openAI, get_timezone
from flask_cors import CORS
import logging


# Crea una instancia de la aplicación Flask
#app = Flask(__name__)

def consulta_tiempo(input_value):
    if not input_value:
        return {"error": "Debes proporcionar una ubicación o código postal"}, 400
    
    if is_postal_code(input_value):
        postal_code = input_value
        location = None
    else:
        location = input_value
        postal_code = None

    if location:
        latitude, longitude, timezone = geocode_location(location)
        print("Datos location, lat, log y tmz:", latitude, longitude, timezone)
    elif postal_code:
        latitude, longitude, timezone = geocode_postal_code(postal_code)
    else:
        return {"error": "Ubicación o código postal no válidos"}, 400

    if latitude is not None and longitude is not None and timezone is not None:
        weather= get_weather(latitude, longitude, timezone)
        print("Weather:", weather)
        return f'Los datos meteorológicos son: {weather}'
    else:
        return {"error": "No se pudieron obtener coordenadas o zona horaria para la ubicación."}, 400

# Ejemplo de uso
input_value = 'Madrid'  # Reemplaza con la ubicación o código postal que desees consultar
result = consulta_tiempo(input_value)
print("Resultado:",result)
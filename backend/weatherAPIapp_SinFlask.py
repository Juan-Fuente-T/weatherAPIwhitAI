
from flask import Flask, request, jsonify
from weather_utils import is_postal_code, geocode_location, geocode_postal_code, get_weather, consulta_openAI#, get_timezone
from flask_cors import CORS
import json


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
        respuesta_openAI = "¡Hola! En Vigo el tiempo ahora mismo es soleado y caluroso, ¡así que prepárate para sudar! Para los próximos días se espera que el sol siga brillando y las temperaturas continúen altas. No se esperan cambios importantes en el clima, así que podrás seguir disfrutando del buen tiempo. ¡Aprovecha para tomar el sol y disfrutar de la ciudad!"
        #respuesta_openAI = consulta_openAI(location)
        #print("Respuesta AI Location:", respuesta_openAI)
        

    if location:
        latitude, longitude, timezone = geocode_location(location)
        print("Datos location, lat, log y tmz:", latitude, longitude, timezone)
    elif postal_code:
        latitude, longitude, timezone = geocode_postal_code(postal_code)
    else:
        return {"error": "Ubicación o código postal no válidos"}, 400

    if latitude is not None and longitude is not None and timezone is not None:
        weather= get_weather(latitude, longitude, timezone)
        #print("Weather:", weather)
        #return jsonify({"respuesta_openAI": respuesta_openAI, "datos_meteorologicos": weather})
        respuesta_openAI = "¡Hola! En Madrid el tiempo ahora mismo es soleado y caluroso, ¡así que prepárate para sudar! Para los próximos días se espera que el sol siga brillando y las temperaturas continúen altas."
        response_data = {"respuesta_openAI": respuesta_openAI, "datos_meteorologicos": weather}
        response_json = json.dumps(response_data, indent=4)  # Convierte los datos a formato JSON con formato
        print("response_json",response_json)
        
    else:
        return {"error": "No se pudieron obtener coordenadas o zona horaria para la ubicación."}, 400

# Ejemplo de uso

input_value = '15930'  # Reemplaza con la ubicación o código postal que desees consultar
result = consulta_tiempo(input_value)
print("Resultado:",result)
#print("Respuesta OpenAI:", result.get("respuesta_openAI"))
print("Datos Meteorológicos:", result.get("datos_meteorologicos"))
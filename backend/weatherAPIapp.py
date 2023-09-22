
from flask import Flask, request, jsonify
from weather_utils import is_postal_code, geocode_location, geocode_postal_code, get_weather#, consulta_openAI#, get_timezone
from flask_cors import CORS
import logging


# Crea una instancia de la aplicación Flask

from flask import Flask, request, jsonify
from weather_utils import is_postal_code, geocode_location, geocode_postal_code, get_weather#, consulta_openAI, get_timezone
from flask_cors import CORS
import logging


# Crea una instancia de la aplicación Flask
app = Flask(__name__)
CORS(app) 
CORS(app, resources={r"/consulta": {"origins": "http://localhost:3000/"}})

app.logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.debug = True  # Habilitar el modo de depuración

# Tu código existente de funciones y configuraciones

# Define una ruta y una función de vista
@app.route('/')
def index():
    app.logger.info("Mensaje de depuración")
    return '¡Hola, esta es tu aplicación de pronóstico del tiempo!'

@app.route('/consulta', methods=['POST'])
def consulta_tiempo():
    app.logger.debug("Input_value")
    data = request.get_json()
    input_value = data.get('input_value')
    
    app.logger.debug("Recibida solicitud POST en consulta_tiempo con input_value: %s", input_value)
    
    if not input_value:
        app.logger.debug("No se proporcionó una ubicación o código postal")
        return jsonify({"error": "Debes proporcionar una ubicación o código postal"}), 400
    
    if is_postal_code(input_value):
        postal_code = input_value
        location = None
    else:
        app.logger.debug("Else de location")
        location = input_value
        postal_code = None

    if location:
        #tiempo = consulta_openAI(location)
        app.logger.debug("Llamada a location")
        latitude, longitude, timezone = geocode_location(location)
        #print("Lat, long y timezone location:", latitude, longitude, timezone)
    elif postal_code:
        #tiempo = consulta_openAI(postal_code)
        latitude, longitude, timezone = geocode_postal_code(postal_code)
        #print("Lat, long y timezone postal code:", latitude, longitude, timezone)
    else:
        return jsonify({"error": "Ubicación o código postal no válidos"}), 400

    if latitude is not None and longitude is not None and timezone is not None:
        # Llamar a get_weather con los valores obtenidos
        weather= get_weather(latitude, longitude, timezone)
        #return jsonify({"tiempo": tiempo, "datos_meteorologicos": weather_data})
        print("Datos meteorologicos:", weather)
        app.logger.debug("El return deberia funcionar")
        #return f'Los datos meteorológicos son: {weather}'
        return jsonify({"datos_meteorologicos": weather})
    else:
        return jsonify({"error": "No se pudieron obtener coordenadas o zona horaria para la ubicación."}), 400

if __name__ == '__main__':
    app.run()
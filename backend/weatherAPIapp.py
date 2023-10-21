
from flask import Flask, request, jsonify
from weather_utils import is_postal_code, geocode_location, geocode_postal_code, get_weather, consulta_openAI, is_location#, get_timezone
from flask_cors import CORS
import logging
from decouple import config


# Se crea una instancia de la aplicación Flask
app = Flask(__name__)
#Se habilita CORS para la ruta especificada con ese origen permitido
#_ORIGIN = config('_ORIGIN')
_ORIGIN = "http://localhost:5000/"
CORS(app) 
CORS(app, resources={r"/consulta": {"origins": _ORIGIN}})

#Se establece la configuracion para los registros de depuracion
app.logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.debug = True  # Se habilita el modo de depuración


# Se define la ruta raíz del servidor web.
@app.route('/')
def index():
    app.logger.info("Mensaje de depuración")
    # Se devuelve un mensaje de bienvenida.
    return '¡Hola, esta es tu aplicación de pronóstico del tiempo!'

# Define la ruta '/consulta', que permite a los usuarios consultar y recibir los datos, con el método 'POST'.
@app.route('/consulta', methods=['POST'])
def consulta_tiempo():
    #app.logger.debug("Input_value")
    #Se consulta el tiempo en una ubicación determinada usando el input_value que se recibe del fronted. Devuelve Los datos meteorológicos para esa ubicación.
    
    #Se obtienen los datos JSON de la solicitud HTTP.
    data = request.get_json()
    #Se obtiene el valor de la clave 'input_value' de los datos JSON.
    input_value = data.get('input_value')
    
    #app.logger.debug("Recibida solicitud POST en consulta_tiempo con input_value: %s", input_value)
    
    if not input_value:
        app.logger.debug("No se proporcionó una ubicación o código postal")
        return jsonify({"error": "Debes proporcionar una ubicación o código postal"}), 400 #notification en caso de error, co un message y el codigo 400
    
    #Se inicializan las variables
    postal_code = None
    location = None
    
    #se evalua el tipo d evalor ecibido y se asigna
    if is_postal_code(input_value):
        postal_code = input_value
    elif is_location(input_value):
        location = input_value
    else:
        return jsonify({"error": "Ubicación o código postal no válidos"}), 400 #notificacion en caso de error
  
    #se ejecuta en caso de recibir un valor location
    if location:
        latitude, longitude, timezone = geocode_location(location)
    #se ejecuta en caso de recibir un valor postal_code 
    elif postal_code:
        latitude, longitude, timezone = geocode_postal_code(postal_code)
    #se no se recibe ni un postal_code o location válido se devuelve error
    else:
        return jsonify({"error": "No se pudieron obtener coordenadas o zona horaria para la ubicación."}), 400
    
    #se ejecuta la función para obtener los datos meteorologicos
    weather = get_weather(latitude, longitude, timezone)

    #se ejecuta la función para obtener respuesta de openAI
    respuesta_openAI = consulta_openAI(postal_code, weather) if postal_code else consulta_openAI(location, weather)

    #Si hay respuesta valida de ambas apis se unen los datos para enviar al frontend
    if weather and respuesta_openAI:
        data = {
            "respuesta_openAI": respuesta_openAI,
            "datos_meteorologicos": weather
        }
        #se devuelven los datos en formato json
        return jsonify({"respuesta_openAI": respuesta_openAI, "datos_meteorologicos": weather})
    else:
        #se devuelven error si falla
        return jsonify({"error": "No se pudieron obtener coordenadas o zona horaria para la ubicación."}), 400


#Ejecuta la aplicación Flask.
if __name__ == '__main__':
    app.run()
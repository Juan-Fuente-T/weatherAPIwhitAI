
from flask import Flask, request, jsonify
from weather_utils import is_postal_code, geocode_location, geocode_postal_code, get_weather, consulta_openAI#, get_timezone
from flask_cors import CORS
import logging
from decouple import config


# Crea una instancia de la aplicación Flask
app = Flask(__name__)
#_ORIGIN = config('_ORIGIN')
_ORIGIN = "http://localhost:5000/"
CORS(app) 
CORS(app, resources={r"/consulta": {"origins": _ORIGIN}})

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
        respuesta_openAI = consulta_openAI(postal_code)
        #respuesta_openAI = "¡Hola! En Madrid el tiempo ahora mismo es soleado y caluroso, ¡así que prepárate para sudar! Para los próximos días se espera que el sol siga brillando y las temperaturas continúen altas. No se esperan cambios importantes en el clima, así que podrás seguir disfrutando del buen tiempo. ¡Aprovecha para tomar el sol y disfrutar de la ciudad!"
        #respuesta_openAI = "¡Hola! En Luarca, el tiempo actual es soleado y agradable. Para los próximos días, la previsión indica cielos despejados y temperaturas suaves. No se esperan cambios importantes en el clima, así que puedes disfrutar del buen tiempo sin preocupaciones. ¡Aprovecha para salir y disfrutar del día!"
        
    else:
        app.logger.debug("Else de location")
        location = input_value
        postal_code = None
        respuesta_openAI = consulta_openAI(location)
        #respuesta_openAI = "¡Hola! En Madrid el tiempo ahora mismo es soleado y caluroso, ¡así que prepárate para sudar! Para los próximos días se espera que el sol siga brillando y las temperaturas continúen altas. No se esperan cambios importantes en el clima, así que podrás seguir disfrutando del buen tiempo. ¡Aprovecha para tomar el sol y disfrutar gggg"
        print("Respuesta AI Location:", respuesta_openAI)
        app.logger.debug(respuesta_openAI)
        

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
        weather= get_weather(latitude, longitude, timezone, location)
        #return jsonify({"tiempo": tiempo, "datos_meteorologicos": weather_data})
        print("Datos meteorologicos:", weather)
        app.logger.debug("El return deberia funcionar")
        #return f'Los datos meteorológicos son: {weather}'
            # Genera o recupera los datos que deseas enviar
        data = {
            "respuesta_openAI": respuesta_openAI,
            "datos_meteorologicos": weather
        }
        app.logger.debug(data)
        # Imprime los datos en la terminal del servidor
        print("Datos que se enviarán al cliente:", data)


        return jsonify({"respuesta_openAI": respuesta_openAI, "datos_meteorologicos": weather})
    else:
        return jsonify({"error": "No se pudieron obtener coordenadas o zona horaria para la ubicación."}), 400

if __name__ == '__main__':
    app.run()
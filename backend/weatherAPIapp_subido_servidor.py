
from flask import Flask, request, jsonify
from weather_utils import is_postal_code, geocode_location, geocode_postal_code, get_weather, consulta_openAI#, get_timezone
from flask_cors import CORS
import logging
from decouple import config


# Crea una instancia de la aplicación Flask
app = Flask(__name__)
#_ORIGIN = config('_ORIGIN')
_ORIGIN = "http://localhost:3000/"
CORS(app)
CORS(app, resources={r"/consulta": {"origins": _ORIGIN}})

#Se habilita un registro de eventos para depuracion
app.logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.debug = True  # Habilitar el modo de depuración



# Se define una ruta y una función de vista
@app.route('/')
def index():
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
        #respuesta de openAI para pruebas
        #respuesta_openAI = "¡Hola! En Luarca, el tiempo actual es soleado y agradable. Para los próximos días, la previsión indica cielos despejados y temperaturas suaves. No se esperan cambios importantes en el clima, así que puedes disfrutar del buen tiempo sin preocupaciones. ¡Aprovecha para salir y disfrutar del día!"

    else:
        location = input_value
        postal_code = None
        respuesta_openAI = consulta_openAI(location)
        #respuesta de openAI para pruebas
        #respuesta_openAI = "¡Hola! En Madrid el tiempo ahora mismo es soleado y caluroso, ¡así que prepárate para sudar! Para los próximos días se espera que el sol siga brillando y las temperaturas continúen altas. No se esperan cambios importantes en el clima, así que podrás seguir disfrutando del buen tiempo. ¡Aprovecha para tomar el sol y disfrutar gggg"

    if location:
        latitude, longitude, timezone = geocode_location(location)

    elif postal_code:
        latitude, longitude, timezone = geocode_postal_code(postal_code)

    else:
        return jsonify({"error": "Ubicación o código postal no válidos"}), 400

    if latitude is not None and longitude is not None and timezone is not None:
        # Llamar a get_weather con los valores obtenidos
        weather= get_weather(latitude, longitude, timezone)
        print("Datos meteorologicos:", weather)

        data = {
            "respuesta_openAI": respuesta_openAI,
            "datos_meteorologicos": weather
        }

        print("Datos que se enviarán al cliente:", data)


        return jsonify({"respuesta_openAI": respuesta_openAI, "datos_meteorologicos": weather})
    else:
        return jsonify({"error": "No se pudieron obtener coordenadas o zona horaria para la ubicación."}), 400

#En el servidor la tiene su propio if __name__ 0 __main__:
"""if __name__ == '__main__':
    app.run()
"""
#Llamada de pruebas para ejecutar en local (necesario comentar el ultimo  __name__ == '__main__
"""
if __name__ == '__main__':
    # Llamar a la función consulta_tiempo con una ubicación o código postal
    location = "Albacete"
    #response = consulta_tiempo()
    respuesta_openAI = consulta_openAI(location)

    print("FFFRespuestaAI:", respuesta_openAI)"""


if __name__ == '__main__':
    app.run(host='0.0.0.0')

from flask import Flask, request, jsonify
from weather_utils import is_postal_code, geocode_location, geocode_postal_code, get_weather, consulta_openAI#, get_timezone
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
    
    if is_postal_code(input_value):
        #se ejecuta en caso de recibir un valor de postal code
        postal_code = input_value
        location = None #Se da valor nulo a la otra opción
        respuesta_openAI = consulta_openAI(postal_code)
        #Respuesta de prueba para no gstar llamadas a la API
        #respuesta_openAI = "¡Hola! En Madrid el tiempo ahora mismo es soleado y caluroso, ¡así que prepárate para sudar! Para los próximos días se espera que el sol siga brillando y las temperaturas continúen altas. No se esperan cambios importantes en el clima, así que podrás seguir disfrutando del buen tiempo. ¡Aprovecha para tomar el sol y disfrutar de la ciudad!"
        #respuesta_openAI = "¡Hola! En Luarca, el tiempo actual es soleado y agradable. Para los próximos días, la previsión indica cielos despejados y temperaturas suaves. No se esperan cambios importantes en el clima, así que puedes disfrutar del buen tiempo sin preocupaciones. ¡Aprovecha para salir y disfrutar del día!"
        
    else:
        #se ejecuta en caso de recibir un valor de location
        location = input_value
        postal_code = None #Se da valor nulo a la otra opcion
        respuesta_openAI = consulta_openAI(location)
        #respuesta_openAI = "¡Hola! En Madrid el tiempo ahora mismo es soleado y caluroso, ¡así que prepárate para sudar! Para los próximos días se espera que el sol siga brillando y las temperaturas continúen altas. No se esperan cambios importantes en el clima, así que podrás seguir disfrutando del buen tiempo. ¡Aprovecha para tomar el sol y disfrutar gggg"
        

    if location:
        #se ejecuta en caso de recibir un valor de location
        latitude, longitude, timezone = geocode_location(location)#la funcion evalua que sea una location valida y devuelve los datos necesarios
        
        
    elif postal_code:
        #tiempo = consulta_openAI(postal_code)
        latitude, longitude, timezone = geocode_postal_code(postal_code)
        #la funcion evalua que sea un postal code valido y devuelve los datos necesarios
        
    else:
        return jsonify({"error": "Ubicación o código postal no válidos"}), 400 ##notification en caso de error, co un message y el codigo 400

    if latitude is not None and longitude is not None and timezone is not None:
        # Llamar a get_weather con los valores obtenidos
        weather= get_weather(latitude, longitude, timezone, location)
        #Se unen las dos repuestas de las API en data
        data = {
            "respuesta_openAI": respuesta_openAI,
            "datos_meteorologicos": weather
        }

        print("Datos", weather)
        return jsonify({"respuesta_openAI": respuesta_openAI, "datos_meteorologicos": weather})#se devuelven de las dos APIS en formato json
    else:
        return jsonify({"error": "No se pudieron obtener coordenadas o zona horaria para la ubicación."}), 400 #notification en caso de error, co un message y el codigo 400
    
#Ejecuta la aplicación Flask.
if __name__ == '__main__':
    app.run()
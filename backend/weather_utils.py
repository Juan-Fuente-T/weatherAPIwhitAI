
import requests 
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import pgeocode
from timezonefinder import TimezoneFinder
import re
import json
from decouple import config
from weathercodesList import weatherCodes

#funcion que comprueba que la location introducida sea correcta 
def is_location(input_value):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(input_value)
    return location is not None

#funcion que comprueba que el codigo postal introducido sea un formato válido, devuelve true o false  
def is_postal_code(input_value):
# Expresión regular para verificar si el input es un código postal (formato numérico de 5 dígitos)
    postal_code_pattern = r'^\d{5}$'

    # Verificar si el input coincide con el patrón de código postal
    if re.match(postal_code_pattern, input_value):
        return True  # Es un código postal válido
    else:
        return False  # No es un código postal válido (asumimos que es una ciudad)    
    
       
#funcion que comprueba que el codigo postal sea valido en cuyo caso devuelve la longitud y latitud

def geocode_postal_code(postal_code):
    geocoder = pgeocode.Nominatim('es') #solo es válido con codigos postales españoles
    location_data = geocoder.query_postal_code(postal_code) #se comprueba el codigo postal
    latitude = location_data.latitude if not location_data.empty else None #se obtiene la latitud si el dato es bueno
    longitude = location_data.longitude if not location_data.empty else None #se obtiene la longitud si el dato es bueno
    
    if latitude is not None and longitude is not None: #se evalua que tengamos latitud y longitud
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lng=longitude, lat=latitude) #se obtiene el timezone a partir de la latitud y longitud
        return latitude, longitude, timezone 
    else:
        return None, None, None
    

#funcion que comprueba la localizacion de una location y devuelve la latitud, longitud y el timezone

def geocode_location(location):
    geolocator = Nominatim(user_agent="myWeatherApp")
    #print(f"Geocodificando la ubicación: {location}") #impresion de control
    location_data = geolocator.geocode(location) 
    try:
        location_data = geolocator.geocode(location, timeout=10)
        if location_data:#si la respuesta es buena se obtienen latitud y longitud
            latitude = location_data.latitude #se va valor a latitud
            longitude = location_data.longitude #se da valor a longitud
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=longitude, lat=latitude)#se obtiene el timezone a partir de la latitud y longitud
            #print(f"Ubicación encontrada. Latitud: {latitude}, Longitud: {longitude}") #impresion de control
            return latitude, longitude,timezone
        else:
            print("No se pudo encontrar la ubicación.") #impresiones de error
            return None, None, None, None
    except GeocoderTimedOut:
        print("Tiempo de espera agotado al buscar la ubicación.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al buscar la ubicación: {e}")
        return None

   


#funcion que devuelve el timezone para location o postal_code ¿¿Es necesaria??
"""
def get_timezone(location):
    coordinates = geocode_location(location)
    if coordinates:
        latitude, longitude = coordinates
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        if debugging:
            print("Timezone location:", timezone)
        return timezone
    else:
        coordinates = geocode_postal_code(postal_code)
        if coordinates:
            latitude, longitude = coordinates
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=longitude, lat=latitude)
            if debugging:
                print("Timezone postal _code:", timezone)
            return timezone
        else:
            return None
"""


#funcion que consulta el prediccion meteorologica

def get_weather(latitude, longitude, timezone):

    url_base = "https://api.open-meteo.com/v1/forecast"

    # Parámetros de la solicitud de datos de datos meteorologicos a la API
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "daily": "apparent_temperature_max,apparent_temperature_min,precipitation_probability_mean,weathercode,sunrise,sunset",
        "current_weather": "true",
        "forecast_days": 7
    }
    #api_OpenMeteo = config("API_OpenMeteo")
    weather_response = requests.get(url_base, params=params) #se hace la llamada a la API
    #weather_response = requests.get(api_OpenMeteo) #se hace la llamada a la API
    
    weather = weather_response.json() #transforma la respuesta en un objeto manipulable

    return weather


# Se importa la clave de la API desde el archivo .env
openai_api_key = config("api_key")

# Se configura la URL de la API de OpenAI
URL = "https://api.openai.com/v1/chat/completions"
# Se configuran los encabezados de la solicitud
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}


#funcion que realiza una consulta a openAI(ANTIGUA)
"""
def consulta_openAI (location_or_postal_code):
    payload = { #se establecen los parametros de la llamada
        "model": "gpt-3.5-turbo",
        "messages" : [
            {"role": "system", "content": f"Eres un asistente que proporciona información meteorologica relevante en un tono coloquial y simpatico pero muy conciso y dando los datos principales con gracia.La longitd máxima de la respuesta es de 330 caracteres, y evita nombrar el postal_code."},
            {"role": "user", "content": f"¿Que tiempo hace ahora en {location_or_postal_code}?, ¿Cuál es la previsión para los próximos días?, ¿Se esperan cambios importantes en el clima de para los próximos días? ¿Cuáles?"}
        ]
    }

    response = requests.post(URL, headers=headers, json=payload) #se hace la llamada a la API de openAI, con los parametros que ya se han definido antes

    response = response.json() #transforma la respuesta en un objto manipulable

    # Verifica si la respuesta incluye el campo 'choices'
    if 'choices' in response:
        return response['choices'][0]['message']['content']
    else:
        # Si no, devuelve un mensaje de error
        return "Error: La respuesta de la API no incluye el campo 'choices'."
"""     
#funcion que realiza una consulta a openAI(OPTIMIZADA)
def consulta_openAI (location_or_postal_code, weather):
    
    # Extraer datos relevantes del tiempo actual para current_weather
    current_weather = weather['current_weather']
    # Extraer los datos relevantes del tiempo actual dentro de current_weather
    temperature = current_weather['temperature']
    windspeed = current_weather['windspeed']
    weathercode_today = current_weather['weathercode']
    #Evaluar que el valor weathercode este en el diccionario de codigos de condiciones meteorologicas y si esta cambiar el nuevo valor por el numero incicial
    if weathercode_today in weatherCodes:
        weatherCode = weatherCodes[weathercode_today]
    else:
        weatherCode = 'No disponible'#notificacion de error


    # Extraer datos de la previsión para siete dias
    daily_data = weather.get ('daily', {})
    # Extraer los datos de dentro de la previsión para siete dias
    max_temperatures = daily_data.get('apparent_temperature_max', 'No disponible') 
    min_temperatures = daily_data.get('apparent_temperature_min', 'No disponible')
    rain_probabilities = daily_data.get('precipitation_probability_mean', 'No disponible')
    weathercodes = daily_data.get('weathercode', 'No disponible')
    #Cambiar los valores de condiciones meteorologicas por el numero incicial
    daily_weatherCodes = [weatherCodes.get(code, "Desconocido") for code in weathercodes]
    
    # Crear el contenido del mensaje del usuario
    user_message = f"Dime qué tiempo hace ahora en {location_or_postal_code} y cuál es la previsión y posibilidad de lluvia para los próximos días, sabiendo que el día es {weatherCode}, la temperatura es de {temperature}°C y la velocidad del viento es {windspeed}km/h. Para los próximos días, y por ese orden, estas son las temperaturas esperadas {', '.join(map(str, max_temperatures))}°C,estas las mínimas {', '.join(map(str, min_temperatures))}°C, estas las previsiones {', '.join(map(str, rain_probabilities))}% de lluvia y estas las previsiones del dia {', '.join(map(str, daily_weatherCodes))}."

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Eres un presentador meteorológico cercano y simpático. La longitud máxima de la respuesta es de 330 caracteres, y evita nombrar el postal_code."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(URL, headers=headers, json=payload) #se hace la llamada a la API de openAI, con los parametros que ya se han definido antes

    response = response.json() #transforma la respuesta en un objto manipulable

    # Verifica si la respuesta incluye el campo 'choices'
    if 'choices' in response:
        return response['choices'][0]['message']['content']
        #'return' de depuracion en probarAPI.py
        #return weatherCode, daily_weatherCodes
    else:
        # Si no, devuelve un mensaje de error
        return "Error: La respuesta de la API no incluye el campo 'choices'."
      


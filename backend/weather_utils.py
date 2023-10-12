
import requests 
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import pgeocode
from timezonefinder import TimezoneFinder
import re
from decouple import config


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

    #url_base = config("API_OpenMeteo")
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

    weather_response = requests.get(url_base, params=params) #se hace la llamada a la API
    
    weather = weather_response.json() #transforma la respuesta en un objeto manipulable
    return weather
"""    
latitude = 40.4167047
longitude = -3.7035825
timezone = "Europe/Madrid"
url_base = config("API_OpenMeteo")
    
print("LAtit,longi, timez:",latitude,longitude, timezone)
weather_data = get_weather(latitude, longitude, timezone)
print("URL completa:", url_base)  # Agregar esta línea para verificar la URL
weather_response = requests.get(url_base)   
print("Datos meteorológicos:", weather_data)
"""

# Se importa la clave de la API desde el archivo .env
openai_api_key = config("api_key")

# Se configura la URL de la API de OpenAI
URL = "https://api.openai.com/v1/chat/completions"
# Se configuran los encabezados de la solicitud
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}


#funcion que realiza una consulta a openAI
 
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
      


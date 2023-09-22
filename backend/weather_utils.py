
import requests #se necesita requests instalado con pip para hacer llamada a la API de conversion

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
    geocoder = pgeocode.Nominatim('es')
    location_data = geocoder.query_postal_code(postal_code)
    latitude = location_data.latitude if not location_data.empty else None
    longitude = location_data.longitude if not location_data.empty else None
    
    if latitude is not None and longitude is not None:
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        return latitude, longitude, timezone
    else:
        return None, None, None
    

#funcion que comprueba la localizacion de una location y devuelve la latitud, longitud y el timezone

def geocode_location(location):
    print("Comprobando entrada datos Location Nominating:", location)
    geolocator = Nominatim(user_agent="myWeatherApp")
    print(f"Geocodificando la ubicación: {location}")
    location_data = geolocator.geocode(location)
    print("location_data", location)
    try:
        location_data = geolocator.geocode(location, timeout=10)
        if location_data:
            latitude = location_data.latitude
            longitude = location_data.longitude
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=longitude, lat=latitude)
            print(f"Ubicación encontrada. Latitud: {latitude}, Longitud: {longitude}")
            return latitude, longitude,timezone
        else:
            print("No se pudo encontrar la ubicación.")
            return None, None, None
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


    # Parámetros de la solicitud
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "daily": "apparent_temperature_max,apparent_temperature_min,precipitation_probability_mean,weathercode,sunrise,sunset",
        "current_weather": "true",
        "forecast_days": 7
    }

    print("URLBase", url_base)
    weather_response = requests.get(url_base, params=params)
   
    
    print("Respuesta directa:", weather_response)
    weather = weather_response.json()
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

#funcion que realiza una consulta a openAI
    
"""def consulta_openAI (location_or_postal_code):
    payload = {
        "model": "gpt-3.5-turbo",
        "messages" : [
            {"role": "system", "content": f"Eres un asistente que proporciona información meteorologica relevante en un tono coloquial y simpatico pero muy conciso y dando los datos principales con gracia. Evitar nombrar {postal_code} en la respuesta."},
            {"role": "user", "content": f"¿Que tiempo hace ahora en {location_or_postal_code}?, ¿Cuál es la previsión para los próximos días?, ¿Se esperan cambios importantes en el clima de para los próximos días? ¿Cuáles?"}
        ]
    }

    response = requests.post(URL, headers=headers, json=payload)

    response = response.json()
    
    #print(response)

    # Verifica si la respuesta incluye el campo 'choices'
    if 'choices' in response:
        return response['choices'][0]['message']['content']
    else:
        # Si no, devuelve un mensaje de error
        return "Error: La respuesta de la API no incluye el campo 'choices'."
        """


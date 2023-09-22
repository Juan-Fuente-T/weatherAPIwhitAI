import React from 'react';
import { Box, Heading, Text, Stack, Divider } from '@chakra-ui/react';


// Diccionario de códigos de clima y sus significados
const weatherCodeMeanings = {
  0: 'Cielo Despejado',
  1: 'Cielo Mayormente Despejado',
  3: 'Cielo Parcialmente Nublado',
  // Agregar más códigos y significados aquí según corresponda
};

function WeatherDisplay({ datosMeteorologicos }) {
  const currentWeather = datosMeteorologicos ? datosMeteorologicos.current_weather : null;
  const dailyForecast = datosMeteorologicos ? datosMeteorologicos.daily : null;
  
  // Función para formatear la fecha en formato legible
  /*const formatFecha = (fecha) => {
    const date = new Date(fecha);
    return date.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };*/

  return (
    <Box p={4}>
      <Heading size="lg">Información Meteorológica</Heading>
      <Divider my={4} />
      
      <Box mt={4}>
        <Heading size="md">Tiempo Actual</Heading>
        <Text>Previsión: {weatherCodeMeanings[currentWeather.weathercode]}</Text>
        <Text>Temperatura: {currentWeather.temperature}°C</Text>
        {/* Otros detalles del tiempo actual */}
      </Box>

      <Divider my={4} />

      <Box mt={4}>
        <Heading size="md">Previsión para el Día Siguiente</Heading>
        <Text>Previsión: {weatherCodeMeanings[dailyForecast.weathercode[1]]}</Text>
        <Text>Temperatura Máxima: {dailyForecast.apparent_temperature_max[1]}°C</Text>
        <Text>Temperatura Mínima: {dailyForecast.apparent_temperature_min[1]}°C</Text>
        <Text>Probabilidad de Lluvia: {dailyForecast.precipitation_probability_mean[1]}%</Text>
        {/* Otros detalles de la previsión del día siguiente */}
      </Box>

      <Divider my={4} />

      <Box mt={4}>
        <Heading size="md">Respuesta de OpenAI</Heading>
        <Text>Aquí se mostrará la respuesta de OpenAI.</Text>
      </Box>
    </Box>
  );




  /*return (
    <div className="weather-display">
      <h2>Información Meteorológica</h2>
      
      <div className="current-weather">
        <h3>Tiempo Actual</h3>
        <p>Previsión: {weatherCodeMeanings[currentWeather.weathercode]}</p>
        <p>Temperatura: {currentWeather.temperature}°C</p>
      </div>

      <div className="next-day-forecast">
        <h3>Previsión para el Día Siguiente</h3>
        <p>Previsión: {weatherCodeMeanings[dailyForecast.weathercode[1]]}</p>
        <p>Temperatura Máxima: {dailyForecast.apparent_temperature_max[1]}°C</p>
        <p>Temperatura Mínima: {dailyForecast.apparent_temperature_min[1]}°C</p>
        <p>Probabilidad de Lluvia: {dailyForecast.precipitation_probability_mean[1]}%</p>
      </div>

      <div className="openai-response">
        <h3>Respuesta de OpenAI</h3>
        <p>Aquí se mostrará la respuesta de OpenAI.</p>
      </div>
    </div>
  );*/
}

export default WeatherDisplay;
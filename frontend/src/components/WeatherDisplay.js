import React, { useState, useEffect } from 'react';
import { Box, Heading, Divider } from '@chakra-ui/react';
import InfoWindow from './InfoWindow';
import weatherCodes from './weathercodesList.js'

const weatherCodeMeanings = {
  0: 'Cielo Despejado',
  1: 'Cielo Mayormente Despejado',
  3: 'Cielo Parcialmente Nublado',
  // Agregar más códigos y significados aquí según corresponda
};

function WeatherDisplay({ datosMeteorologicos }) {
  const initialCurrentWeather = datosMeteorologicos && datosMeteorologicos.current_weather ? datosMeteorologicos.current_weather : {};
  const initialDailyForecast = datosMeteorologicos && datosMeteorologicos.daily ? datosMeteorologicos.daily : {};
  console.log("Datos meteorologicos", datosMeteorologicos);
  console.log("Initial current Weather", initialCurrentWeather);
  console.log("Initail daily Forecast", initialDailyForecast);
  console.log("Temp-max-antes:",initialDailyForecast.apparent_temperature_max)


  const [currentWeather, setCurrentWeather] = useState(initialCurrentWeather);
  const [dailyForecast, setDailyForecast] = useState(initialDailyForecast);

  useEffect(() => {
    // Esto se ejecuta cuando cambian los datos iniciales
    // Asegurémonos de que los estados se actualicen correctamente
    setCurrentWeather(initialCurrentWeather);
    setDailyForecast(initialDailyForecast);
  }, [initialCurrentWeather, initialDailyForecast]); // Esto escucha cambios en los datos iniciales


  console.log("Datos meteorologicos después", datosMeteorologicos);
  console.log("Current Weather", initialCurrentWeather);
  console.log("Daily Forecast", initialDailyForecast);
  console.log("Temp-max:",dailyForecast.apparent_temperature_max)
  
  const handleCurrentWeatherChange = (key, newValue) => {
    console.log(`Cambio en ${key}: ${newValue}`);
    setCurrentWeather((prevWeather) => ({
      ...currentWeather,
      [key]: newValue,
    }));
  };

  const handleDailyForecastChange = (key, newValue) => {
    setDailyForecast((prevWeather) => ({
      ...dailyForecast,
      [key]: newValue,
    }));
  };

  if (!datosMeteorologicos) {
    // Datos meteorológicos no disponibles, puedes mostrar un mensaje o componente de carga aquí
    return null;
  }

  return (
    <Box p={4}>
      <Heading size="lg">Información Meteorológica</Heading>
      <Divider my={4} />

      <Box mt={4}>
        <Heading size="md">Tiempo Actual</Heading>
        <InfoWindow
          label="Previsión"
          //value={weatherCodes[currentWeather.weathercode] || 'No disponible'}
          value={weatherCodes.hasOwnProperty(currentWeather.weathercode) ? weatherCodes[currentWeather.weathercode] : 'No disponible'}
          onChange={(value) => handleCurrentWeatherChange('weathercode', value)}
        />
        <InfoWindow
          label="Temperatura"
          value={currentWeather.temperature || 'No disponible'}
          onChange={(value) => handleCurrentWeatherChange('temperature', value)}
        />
        {/* Otros detalles del tiempo actual */}
      </Box>

      <Divider my={4} />

      <Box mt={4}>
        <Heading size="md">Previsión para el Día Siguiente</Heading>
        <InfoWindow
          label="Previsión para mañana"
          //value={weatherCodes[dailyForecast.weathercode] || 'No disponible'}
          value={weatherCodes.hasOwnProperty(dailyForecast.weathercode[1]) ? weatherCodes[dailyForecast.weathercode[1]] : 'No disponible'}
          onChange={(value) => handleCurrentWeatherChange('weathercode', value)}
        />
        <InfoWindow
          label="Temperatura Máxima"
          value={dailyForecast.apparent_temperature_max ? `${dailyForecast.apparent_temperature_max[1]}°C` : 'No disponible'}
          onChange={(value) => handleDailyForecastChange('apparent_temperature_max', value)}
        />
        <InfoWindow
          label="Temperatura Mínima"
          value={dailyForecast.apparent_temperature_min ? `${dailyForecast.apparent_temperature_min[1]}°C` : 'No disponible'}
          onChange={(value) => handleDailyForecastChange('apparent_temperature_min', value)}
        />
        <InfoWindow
          label="Probabilidad de Lluvia"
          value={dailyForecast.precipitation_probability_mean ? `${dailyForecast.precipitation_probability_mean[1]}%` : 'No disponible'}
          onChange={(value) => handleDailyForecastChange('precipitation_probability_mean', value)}
        />
        {/* Otros detalles de la previsión del día siguiente */}
      </Box>
              

      <Divider my={4} />

      <Box mt={4}>
        <Heading size="md">Respuesta de OpenAI</Heading>
        <InfoWindow
          label="Respuesta de OpenAI"
          value="Aquí se mostrará la respuesta de OpenAI."
          onChange={(value) => handleCurrentWeatherChange('respuesta_openai', value)}
        />
      </Box>
    </Box>
  );
}

export default WeatherDisplay;
import React from 'react';
import { Box, Heading, Input, Stack, Divider } from '@chakra-ui/react';

const weatherCodeMeanings = {
  0: 'Cielo Despejado',
  1: 'Cielo Mayormente Despejado',
  3: 'Cielo Parcialmente Nublado',
  // Agregar más códigos y significados aquí según corresponda
};

function WeatherDisplay({ datosMeteorologicos }) {
  const currentWeather = datosMeteorologicos ? datosMeteorologicos.current_weather : null;
  const dailyForecast = datosMeteorologicos ? datosMeteorologicos.daily : null;

  return (
    <Box p={4}>
      <Heading size="lg">Información Meteorológica</Heading>
      <Divider my={4} />
      
      <Box mt={4}>
        <Heading size="md">Tiempo Actual</Heading>
        <Box>
          <label>Previsión:</label>
          <Input value={currentWeather ? weatherCodeMeanings[currentWeather.weathercode] : 'No disponible'} isReadOnly />
        </Box>
        <Box>
          <label>Temperatura:</label>
          <Input value={currentWeather ? `${currentWeather.temperature}°C` : 'No disponible'} isReadOnly />
        </Box>
        {/* Otros detalles del tiempo actual */}
      </Box>

      <Divider my={4} />

      <Box mt={4}>
        <Heading size="md">Previsión para el Día Siguiente</Heading>
        <Box>
          <label>Previsión:</label>
          <Input value={dailyForecast ? weatherCodeMeanings[dailyForecast.weathercode[1]] : 'No disponible'} isReadOnly />
        </Box>
        <Box>
          <label>Temperatura Máxima:</label>
          <Input value={dailyForecast ? `${dailyForecast.apparent_temperature_max[1]}°C` : 'No disponible'} isReadOnly />
        </Box>
        <Box>
          <label>Temperatura Mínima:</label>
          <Input value={dailyForecast ? `${dailyForecast.apparent_temperature_min[1]}°C` : 'No disponible'} isReadOnly />
        </Box>
        <Box>
          <label>Probabilidad de Lluvia:</label>
          <Input value={dailyForecast ? `${dailyForecast.precipitation_probability_mean[1]}%` : 'No disponible'} isReadOnly />
        </Box>
        {/* Otros detalles de la previsión del día siguiente */}
      </Box>

      <Divider my={4} />

      <Box mt={4}>
        <Heading size="md">Respuesta de OpenAI</Heading>
        <Input value="Aquí se mostrará la respuesta de OpenAI." isReadOnly />
      </Box>
    </Box>
  );
}

export default WeatherDisplay;
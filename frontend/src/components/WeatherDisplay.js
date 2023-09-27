import React, { useState, useEffect } from 'react';
import { Box, Heading, Divider, Flex,ChakraProvider, extendTheme } from '@chakra-ui/react';
import InfoWindow from './InfoWindow';
import weatherCodes from './weathercodesList.js'


function WeatherDisplay({ datosMeteorologicos }) {

  const initialCurrentWeather = datosMeteorologicos?.datos_meteorologicos?.current_weather || {};
  const initialDailyForecast = datosMeteorologicos?.datos_meteorologicos?.daily || {};

  const initialRespuestaOpenAI = datosMeteorologicos?.respuesta_openAI || 'No disponible';

  const [currentWeather, setCurrentWeather] = useState(initialCurrentWeather);
  const [dailyForecast, setDailyForecast] = useState(initialDailyForecast);
  const [respuestaOpenAI, setRespuestaOpenAI] = useState(initialRespuestaOpenAI);
  const temperaturaActual = datosMeteorologicos?.respuesta_openAI;
  console.log("Temp. actual", temperaturaActual);
 
  console.log("Datos meteorologicos", datosMeteorologicos);
  console.log("Initial current Weather", initialCurrentWeather);
  console.log("Initial daily Forecast", initialDailyForecast);
  console.log("Temp-max-antes:",dailyForecast.apparent_temperature_max);
  console.log("Initial AI",initialRespuestaOpenAI);
  
  
  /*const [currentWeather, setCurrentWeather] = useState(initialCurrentWeather);
  const [dailyForecast, setDailyForecast] = useState(initialDailyForecast);
  const [respuestaOpenAI, setRespuestaOpenAI] = useState(initialRespuestaOpenAI);*/
  //const [consultaOpenAI, setConsultaOpenAI] = useState(initialConsultaOpenAI);
/*const [respuestaOpenAI, setRespuestaOpenAI] = useState(
    datosMeteorologicos && datosMeteorologicos.respuesta_openAI
      ? datosMeteorologicos.respuesta_openAI
      : 'No disponible'
  );*/

  // Función para actualizar los estados cuando cambian los datos
 

  useEffect(() => {
    // Actualizamos los estados con los datos de datosMeteorologicos
    setCurrentWeather(datosMeteorologicos?.datos_meteorologicos?.current_weather || {});
    setDailyForecast(datosMeteorologicos?.datos_meteorologicos?.daily || {});
    setRespuestaOpenAI(datosMeteorologicos?.respuesta_openAI || 'No disponible');
  }, [datosMeteorologicos]); // Esto escucha cambios en los datos iniciales

  console.log("Datos meteorologicos después", datosMeteorologicos);
  console.log("Current Weather", currentWeather);
  console.log("Daily Forecast", dailyForecast);
  console.log("Temp-max:",dailyForecast.apparent_temperature_max)
  console.log("Respuesta AI:", respuestaOpenAI)
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
  const handleRespuestaOpenAiChange = (key, newValue) =>{
    setRespuestaOpenAI((prevRespuestaOpenAI) => ({
      ...respuestaOpenAI,
      [key]: newValue,
 }));
};

return (
  <ChakraProvider>
    <Box p={4}>
      <Box 
        size = {'sm'}
        textColor={'darkAlfa.900'}
        fontSize="1.9xl"
        fontWeight="bold"
        backgroundColor={'teal.800'} 
        borderRadius={'10px'} 
        p={'2%'}
        alignItems={'center'}
          >
        <Box mt={4} width={'100%'} padding={'2%'} backgroundColor={'teal.500'} borderRadius={'10px'} size={'sm'}>
          <InfoWindow
            label="Información Meteorológica"
            value={respuestaOpenAI ? respuestaOpenAI : 'No disponible'}
            onChange={(value) => handleRespuestaOpenAiChange('respuesta_openAI', value)}
            />
        </Box>
      </Box>

      <Divider my={4} />

      <Heading size="lg" color={'teal.800'}>
        Información Detallada
      </Heading>

      <Divider my={4} />

      <Flex
        p={4}
        flexDirection="row"
        justifyContent="space-between"
        alignItems={'normal'}
        backgroundColor={'teal.800'}
        borderRadius="10px"
      >
        {/* Sección Izquierda */}
        <Flex
        text
          textColor={'darkAlfa.900'}
          fontSize="1.9xl"
          fontWeight="bold"
          flexDirection="column"
          justifyContent="space-around"
          alignItems="center"
          padding="20px"
          margin="10px"
          backgroundColor={'teal.500'}
          flex={1}
          borderRadius="10px"
        >
          <Heading size="md" mb={'-9%'}>Tiempo Actual</Heading>
          <InfoWindow
            label="Previsión"
            value={
              currentWeather && weatherCodes.hasOwnProperty(currentWeather.weathercode)
                ? weatherCodes[currentWeather.weathercode]
                : 'No disponible'
            }
            onChange={(value) => handleCurrentWeatherChange('weathercode', value)}
          />
          <InfoWindow
            label="Temperatura"
            value={currentWeather.temperature || 'No disponible'}
            onChange={(value) => handleCurrentWeatherChange('temperature', value)}
          />
        </Flex>

        {/* Sección Derecha */}
        <Flex
          textColor={'darkAlfa.900'}
          fontSize="1.9xl"
          fontWeight="bold"
          flexDirection="column"
          justifyContent={'space-around'}
          alignItems="normal"
          padding="20px"
          margin="10px"
          backgroundColor={'teal.500'}
          flex={2}
          borderRadius="10px"
        >
          <Heading size="md" pt={'3%'}>Previsión para mañana</Heading>
          <Flex flexDirection="row" justifyContent="space-between" alignItems="center" padding="20px">
            <InfoWindow
              label="Previsión para mañana"
              value={currentWeather && weatherCodes.hasOwnProperty(currentWeather.weathercode) ? weatherCodes[currentWeather.weathercode] : 'No disponible'}
              onChange={(value) => handleCurrentWeatherChange('weathercode', value)}
            />
            <InfoWindow
              label="Probabilidad de Lluvia"
              value={dailyForecast.precipitation_probability_mean ? `${dailyForecast.precipitation_probability_mean[1]}%` : 'No disponible'}
              onChange={(value) => handleDailyForecastChange('precipitation_probability_mean', value)}
            />
          </Flex>
          <Flex flexDirection="row" justifyContent="space-between" alignItems="center" padding="20px">
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
          </Flex>
        </Flex>
      </Flex>
    </Box>
  </ChakraProvider>
);
}
export default WeatherDisplay;
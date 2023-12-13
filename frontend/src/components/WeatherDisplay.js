import React, { useState, useEffect, useRef } from 'react';
import { Box, Heading, Divider, Flex, ChakraProvider, Text, useBreakpointValue, extendTheme } from '@chakra-ui/react';
import InfoWindow from './InfoWindow';
import weatherCodes from './weathercodesList.js'
import InfoExtraWindow from './InfoExtraWindow';


// Define el componente WeatherDisplay
function WeatherDisplay({ datosMeteorologicos }) {
  // Se extraen los datos iniciales de datosMeteorologicos
  const initialCurrentWeather = datosMeteorologicos?.datos_meteorologicos?.current_weather || {};
  const initialDailyForecast = datosMeteorologicos?.datos_meteorologicos?.daily || {};
  const initialRespuestaOpenAI = datosMeteorologicos?.respuesta_openAI || 'No disponible';

  // Se nicializan los estados con los datos iniciales
  const [currentWeather, setCurrentWeather] = useState(initialCurrentWeather);
  const [dailyForecast, setDailyForecast] = useState(initialDailyForecast);
  const [respuestaOpenAI, setRespuestaOpenAI] = useState(initialRespuestaOpenAI);

  const containerRef = useRef(null);
  const contentRef = useRef(null);

  // Llamada a datos e impresiones para depuración en la consola
  /*const temperaturaActual = datosMeteorologicos?.respuesta_openAI;
  console.log("Temp. actual", temperaturaActual);
  console.log("Datos meteorológicos", datosMeteorologicos);
  console.log("Initial current Weather", initialCurrentWeather);
  console.log("Initial daily Forecast", initialDailyForecast);
  console.log("Temp-max-antes:",dailyForecast.apparent_temperature_max);
  console.log("Initial AI",initialRespuestaOpenAI);*/

  // Se actualizan los estados cuando cambian los datos
  useEffect(() => {
    const container = containerRef.current;
    const content = contentRef.current;

    if (container & content) {

      const scrollSpeed = 30; // Ajusta la velocidad de desplazamiento según tus preferencias
      const contentWidth = content.clientWidth;
      const containerWidth = container.clientWidth;

      //Funcion que desplaza el texto en la ventana principal
      function scrollText() {
        if (contentWidth > containerWidth) {
          content.style.transform = `translateX(${containerWidth}px)`; // Inicializa la posición del texto
          const animationDuration = (contentWidth / scrollSpeed) * 1000;

          content.style.transition = `transform ${animationDuration}ms linear`;
          content.style.transform = `translateX(-${contentWidth}px)`; // Desplaza el texto
        }
      }

      scrollText();

      // Reinicia el desplazamiento cuando termine la animación
      content.addEventListener('transitionend', () => {
        content.style.transition = 'none';
        content.style.transform = `translateX(${containerWidth}px)`;
        setTimeout(scrollText, 500); // Pausa antes de reiniciar
      });
    }


    // Actualizamos los estados con los datos de datosMeteorologicos
    setCurrentWeather(datosMeteorologicos?.datos_meteorologicos?.current_weather || {});
    setDailyForecast(datosMeteorologicos?.datos_meteorologicos?.daily || {});
    setRespuestaOpenAI(datosMeteorologicos?.respuesta_openAI || 'No disponible');
  }, [datosMeteorologicos, respuestaOpenAI]); // Esto escucha cambios en los datos iniciales


  // Función para manejar cambios en el clima actual
  const handleCurrentWeatherChange = (key, newValue) => {
    console.log(`Cambio en ${key}: ${newValue}`);
    setCurrentWeather((prevWeather) => ({
      ...currentWeather,
      [key]: newValue,
    }));
  };

  // Función para manejar cambios en el pronóstico diario
  const handleDailyForecastChange = (key, newValue) => {
    setDailyForecast((prevWeather) => ({
      ...dailyForecast,
      [key]: newValue,
    }));
  };
  console.log("RespuestaAI:", respuestaOpenAI)
  // Función para manejar cambios en la respuesta de OpenAI
  const handleRespuestaOpenAiChange = (key, newValue) => {
    setRespuestaOpenAI((prevRespuestaOpenAI) => ({
      ...respuestaOpenAI,
      [key]: newValue,
    }));
  };

  // Se renderiza el componente que muestra las respuestas, WeatherDisplay
  return (
    //Se envuelve todo en Chakra provider para acceder a sus componentes
    <ChakraProvider>
      <Box p={4} >
        <Box
          margin={'0 auto'}
          size={'sm'}
          textColor={'darkAlfa.900'}
          fontSize="1.9xl"
          fontWeight="bold"
          backgroundColor={'teal.800'}
          borderRadius={'10px'}
          p={'2%'}
          alignItems={'center'}
          justifyContent={'center'} >

          <Box mt={4} maxW={'100%'} padding={'2%'} backgroundColor={'teal.500'} borderRadius={'10px'} size={'sm'} overflowX="auto" justifyContent={'center'} alignItems={'center'} >
            <Box ref={contentRef} className='scroll-content' maxW={'100%'} m={'10px'} alignItems={'center'}>
              <InfoExtraWindow
                label="Información Meteorológica"
                value={respuestaOpenAI ? respuestaOpenAI : 'No disponible'} //se evalua si existen los datos antes de asignarlos o se devuelve No disponible
                onChange={(value) => handleRespuestaOpenAiChange('respuesta_openAI', value)} //Se asignan los valores correspondientes

                customClassName='scroll-slow' // Se asigna una clase CSS específica para controlar la velocidad de desplazamiento
              />
            </Box>
          </Box>
        </Box>

        <Divider my={4} />

        <Heading size="lg" color={'teal.800'}>
          Información Detallada
        </Heading>

        <Divider my={4} />

        <Flex

          p={4}
          maxW={'100%'}
          flexDirection={useBreakpointValue({ base: "column", md: "row", lg: "row" })}
          alignContent={['center', 'center', 'space-baround']}  //flexDirection responsive especifica segun el tamaño de la pantalla
          alignItems={['center', 'center', 'stretch']}
          backgroundColor={'teal.800'}
          borderRadius="10px"
          flexWrap={'wrap'}
        >

          {/* Sección Izquierda */}
          <Flex
            width={['100%', '100%', '45%']}
            textColor={'darkAlfa.900'}
            fontSize="1.9xl"
            fontWeight="bold"
            flexDirection="column"
            justifyContent={'center'}
            alignItems={['center', 'center', 'stretch']}
            padding="20px"
            margin={['5px', '5px', '5px']} // 
            backgroundColor={'teal.500'}
            flex={1}
            borderRadius="10px"
            overflowX="auto"
          //height={'360px'}
          >
            <Heading size="md" mb={'1%'}>Tiempo Actual</Heading>
            <Box mt={useBreakpointValue({ base: 0, md: 4, lg: 4 })}></Box>
            <InfoWindow
              label="Tiempo"
              value={
                currentWeather && weatherCodes.hasOwnProperty(currentWeather.weathercode)
                  ? weatherCodes[currentWeather.weathercode]
                  : 'No disponible' //se evalua si existen los datos antes de asignarlos o se devuelve No disponible
              }
              onChange={(value) => handleCurrentWeatherChange('weathercode', value)}//Se asignan los valores correspondientes
              customClassName='scroll-fast' // Se asigna una clase CSS específica para controlar la velocidad de desplazamiento
            />
            <Box mt={useBreakpointValue({ base: 0, md: 10, lg: 12 })}></Box> {/* Ajusta el espacio vertical según el tamaño de pantalla */}
            <InfoWindow
              label="Temperatura"
              value={currentWeather.temperature || 'No disponible'} //Se cogen el valor si esta dispponible
              onChange={(value) => handleCurrentWeatherChange('temperature', value)}//Se asignan el valor correspondientes
            />

          </Flex>

          {/* Sección Derecha */}
          <Flex
            width={['100%', '100%', '45%']}
            textColor={'darkAlfa.900'}
            fontSize="1.9xl"
            fontWeight="bold"
            flexDirection="column"
            justifyContent={'center'}
            alignItems={['center', 'center', 'stretch']}
            padding="3%"
            margin={['5px', '5px', '5px']} // 
            backgroundColor={'teal.500'}
            flex={2}
            borderRadius="10px">

            <Heading size="md" pt={'3%'}>Previsión para mañana</Heading>
            <Flex flexDirection={useBreakpointValue({ base: "column", md: "row", lg: "row" })} justifyContent="space-between" alignItems="center" padding="20px">
              <InfoWindow
                label="Previsión para mañana"
                value={currentWeather && weatherCodes.hasOwnProperty(currentWeather.weathercode) ? weatherCodes[currentWeather.weathercode] : 'No disponible'} //se evalua si existen los datos antes de asignarlos o se devuelve No disponible
                onChange={(value) => handleCurrentWeatherChange('weathercode', value)}
                customClassName='scroll-fast' // Se asigna una clase CSS específica para controlar la velocidad de desplazamiento
              />
              <InfoWindow
                label="Probabilidad de Lluvia"
                value={dailyForecast.precipitation_probability_mean ? `${dailyForecast.precipitation_probability_mean[1]}%` : 'No disponible'}//se evalua si existen los datos antes de asignarlos o se devuelve No disponible
                onChange={(value) => handleDailyForecastChange('precipitation_probability_mean', value)}//Se asignan los valores correspondientes
              />
            </Flex>
            <Flex flexDirection={useBreakpointValue({ base: "column", md: "row", lg: "row" })} justifyContent="space-between" alignItems="center" padding="20px">
              <InfoWindow
                label="Temperatura Máxima"
                value={dailyForecast.apparent_temperature_max ? `${dailyForecast.apparent_temperature_max[1]}°C` : 'No disponible'} //se evalua si existen los datos antes de asignarlos o se devuelve No disponible
                onChange={(value) => handleDailyForecastChange('apparent_temperature_max', value)}//Se asignan los valores correspondientes
              />
              <InfoWindow
                label="Temperatura Mínima"
                value={dailyForecast.apparent_temperature_min ? `${dailyForecast.apparent_temperature_min[1]}°C` : 'No disponible'} //se evalua si existen los datos antes de asignarlos o se devuelve No disponible
                onChange={(value) => handleDailyForecastChange('apparent_temperature_min', value)} //Se asignan los valores correspondientes
              />
            </Flex>
          </Flex>
        </Flex>
      </Box>
    </ChakraProvider>
  );
}
export default WeatherDisplay;
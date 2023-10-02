//import logo from './logo.svg';
//import './App.css';
import React, { useState } from 'react';
import InputForm from './components/InputForm';
import WeatherDisplay from './components/WeatherDisplay';
import { ChakraProvider, Box, Heading } from '@chakra-ui/react'; 


function App() {
  const [datosMeteorologicos, setDatosMeteorologicos] = useState(null);

  const consultarTiempo = (inputValue) => {
    // Realizar una solicitud a tu API de Flask con el inputValue
    fetch('http://localhost:5000/consulta', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000/'
      },
      body: JSON.stringify({ input_value: inputValue }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Datos recibidos del servidor:", data);
        setDatosMeteorologicos({
          datos_meteorologicos: data.datos_meteorologicos,
          respuesta_openAI: data.respuesta_openAI,
      });
    })
      .catch((error) => {
        console.error('Error al consultar el tiempo:', error);
      });
  };


  return (
    <ChakraProvider> {/* Envuelve tu aplicación con ChakraProvider */}
      <Box textAlign="center" p={4}>
        <Heading as="h1" size="2xl" color={'teal.800'} >
          Pronóstico del Tiempo con AI
        </Heading>
        <InputForm consultarTiempo={consultarTiempo} font color={'teal.800'}/>
        <WeatherDisplay datosMeteorologicos={datosMeteorologicos || {}} />
      </Box>
    </ChakraProvider>
  );
}
export default App;

/*
  return (
    <div className="App">
      <h1>Aplicación de Pronóstico del Tiempo</h1>
      <InputForm consultarTiempo={consultarTiempo} />
      {datosMeteorologicos && (
        <WeatherDisplay datosMeteorologicos={datosMeteorologicos} />
      )}
    </div>
  );
}
*/

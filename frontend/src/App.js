//import logo from './logo.svg';
//import './App.css';
import React, { useState } from 'react';
import InputForm from './components/InputForm';
import WeatherDisplay from './components/WeatherDisplay';
import { ChakraProvider, Box, Heading } from '@chakra-ui/react'; 


function App() {
  // Definimos un estado inicial para los datos meteorológicos
  const [datosMeteorologicos, setDatosMeteorologicos] = useState(null);

  
  // Función para consultar el tiempo al servidor (parte de la APP en Python/Flask)
  const consultarTiempo = (inputValue) => {
    // Realizar una solicitud a la API de Flask con el inputValue del usuario
    //Se configura como POST
    console.log("Procces",process.env.REACT_APP_ORIGIN);
    fetch('http://juanfuente.pythonanywhere.com/consulta', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        //'Origin': process.env.REACT_APP_ORIGIN 
        'Origin': process.env.REACT_APP_ORIGIN 
      },
      //se construye la solicitud con el valor del input del usuario, segun el valor enviado se espera una respuesta u otra
      body: JSON.stringify({ input_value: inputValue }), 
    })
      .then((response) => response.json())//si Flask responde se lee la respuesta como un json
      .then((data) => {
        console.log("Datos recibidos del servidor:", data);//impresion de depuracion
        // Actualizamos los estados con los datos recibidos de Flask
        setDatosMeteorologicos({
          datos_meteorologicos: data.datos_meteorologicos,
          respuesta_openAI: data.respuesta_openAI,
      });
    })
      .catch((error) => {
        console.error('Error al consultar el tiempo:', error); //impresion en caso de fallo
      });
  };


  return (
    <ChakraProvider> {/* Se nvuelve la app con ChakraProvider para usar sus componentes UI*/}
      <Box textAlign="center" p={4}>
        <Heading as="h1" size="2xl" color={'teal.800'} >
          Pronóstico del Tiempo con AI
        </Heading>
        {/*Se renderiza el componente InputForm y se pasa la función consultarTiempo como prop */}
        <InputForm consultarTiempo={consultarTiempo} font color={'teal.800'}/>
        {/* Se renderiza el componente WeatherDisplay y se pasan los datos meteorológicos como prop */}
        <WeatherDisplay datosMeteorologicos={datosMeteorologicos || {}} />
      </Box>
    </ChakraProvider>
  );
}
export default App; // Se exporta el componente App para su uso 



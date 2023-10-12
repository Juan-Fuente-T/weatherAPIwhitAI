import React from 'react';
import { Box, Flex, Input, chakra } from '@chakra-ui/react';
import '../stylesheets/keyframes.css'

//se define el elemento con las props(propiedades) que va a utilizar
function InfoExtraWindow({ label, value, onChange, customClassName}) {
  // Se intenta renderizar el componente InfoWindow
  try {
    // Se devuelve un componente de caja que contiene una etiqueta y un cuadro de entrada
    return (
      <Flex textColor="darkAlfa.900" fontSize="1.9xl" fontWeight="bold" flexDirection={'column'} justifyContent={'center'} pr={'2%'}>
        <Box pb="5%">
          {/* Etiqueta que muestra el nombre del campo */}
          <label>{label}:</label>
        </Box>
        {/* Contenedor que establece el estilo de borde, margen y desplazamiento horizontal */}
        <Box borderWidth="6px" borderRadius="10px" p="2" mb="4" mx="1%" overflowX="auto" width="100%" style={{ whiteSpace: 'nowrap' }} justifyContent={'center'}> 
          {/* Cuadro de entrada de texto */}
          <Input
            width="2500px"
            textColor="darkAlfa.900"
            fontSize={["sm", "md", "lg", "xl", "2xl"]}
            fontWeight="bold"
            border="none"
            justifyContent={'center'}
            type="text"
            // Valor del cuadro de entrada que se muestra
            value={value}
            // Maneja el evento de cambio en el cuadro de entrada
            onChange={(e) => onChange(e.target.value)} //e.target.value = valor actual en el momento del evento
            // Aplica la clase CSS condicionalmente según la prop customClassName
            className={customClassName}
          />
        </Box>
      </Flex>
    );
  } catch (error) {
    // Capturamos y manejamos errores si ocurren al renderizar el componente
    console.error("Error en Infowindow: ", error);
    // Devolvemos null y un mensaje de error si se produce una excepción
    return null;
  }
}

// Exportamos el componente InfoWindow con la capacidad de usar características de Chakra UI
export default chakra(InfoExtraWindow);
import React, { useState } from 'react';
import { Box, Input, Button } from '@chakra-ui/react';

function InputForm({ consultarTiempo }) {
  // Se define el estado para el input delusuario y la funcion que lo actualiza. Se inicializa como un string vacio.
  const [inputValue, setInputValue] = useState('');

  // Función para manejar cambios en el input
  const handleInputChange = (e) => {
    setInputValue(e.target.value); //e.target.value = valor actual en el momento del evento
  };

  // Función para manejar clics en el botón de consulta
  const handleConsultaClick = () => {
    consultarTiempo(inputValue); // Llama a la función consultarTiempo con el valor actual del input asignado por el usuario como parametro
  };

  // Función para manejar pulsaciones de tecla (Enter) en el input y pedir resultados
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      consultarTiempo(inputValue); // Sellama a la función consultarTiempo cuando se presiona Enter con el inputValue asignado por el usuario como parametro
    }
  };

  return (
    <Box display={'flex'} flexDirection={'column'} alignItems={'center'} m={'10'} color={'teal.800'}>
      <Input
        type="text"
        color={'teal.800'}
        placeholder="Introduce tu Ciudad o código postal"
        _placeholder={{ color: 'teal.800' }}
        value={inputValue}
        onChange={handleInputChange} // Se asocia la función de cambio al evento onChange
        onKeyDown={handleKeyPress}   // Se asocia la función de pulsación de tecla al evento onKeyPress
        size="lg"
        width={350}
        fontSize={["sm", "md", "lg", "xl", "2xl"]}
        fontWeight="bold"
        textAlign={'center'}
        border={'2px'}
        borderColor={'teal.800'}
        _hover={{ borderColor: 'teal.500' }}
        _focus={{ borderColor: 'darkAlfa.900' }}
        focusBorderColor='darkAlfa.900'
      />
      <Button mt={2} colorScheme="teal" backgroundColor={'teal.800'} onClick={handleConsultaClick}>
        Consultar
      </Button>
    </Box>
  );
}

export default InputForm;
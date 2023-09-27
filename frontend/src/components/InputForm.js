import React, { useState } from 'react';
import { Box, Input, Button } from '@chakra-ui/react';
import { color } from 'framer-motion';

function InputForm({ consultarTiempo }) {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleConsultaClick = () => {
    consultarTiempo(inputValue);
  };

  return (
    <Box display={'flex'} flexDirection={'column'} alignItems={'center'} m={'10'}color={'teal.800'} >
      <Input
        type="text"
        color={'teal.800'}
        placeholder="Introduce tu Ciudad o código postal"
        _placeholder={{ color: 'teal.800' }}
        value={inputValue}
        onChange={handleInputChange}
        size="lg"
        width={350}
        fontSize="1.9xl"
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
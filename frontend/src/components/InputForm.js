import React, { useState } from 'react';
import { Box, Input, Button } from '@chakra-ui/react';

function InputForm({ consultarTiempo }) {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleConsultaClick = () => {
    consultarTiempo(inputValue);
  };

  return (
    <Box>
      <Input
        type="text"
        placeholder="Introduce tu Ciudad o código postal"
        value={inputValue}
        onChange={handleInputChange}
        size="lg"
      />
      <Button mt={2} colorScheme="teal" onClick={handleConsultaClick}>
        Consultar
      </Button>
    </Box>
  );
}

export default InputForm;
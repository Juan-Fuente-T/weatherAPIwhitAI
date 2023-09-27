import React from 'react';
import { Box, Input,chakra } from '@chakra-ui/react';

function InfoWindow({ label, value, onChange }) {
  try{
    return (
      <Box textColor={'darkAlfa.900'}
      fontSize="1.9xl"
      fontWeight="bold">
        <Box pb={'5%'}  >
        <label>{label}:</label>
        </Box>
        <Box
        borderWidth="6px" 
        borderRadius="10px" 
        p="2" 
        mb="4"
        mx={'1%'}
        
       
        >
        <Input
          textColor={'darkAlfa.900'}
          fontSize="1.9xl"
          fontWeight="bold"
          border="none" 
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
      </Box>
    </Box>
    );
  }catch (error){
    console.error("Error en Infowindow: ", error);
    return null; //se devuelve null con un mensaje de error
  }
}
export default chakra(InfoWindow);
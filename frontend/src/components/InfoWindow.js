import React from 'react';
import { Box, Input,chakra } from '@chakra-ui/react';

function InfoWindow({ label, value, onChange }) {
  try{
    return (
      <Box>
        <Box>
        <label>{label}:</label>
        </Box>
        <Box 
        borderWidth="11px" 
        borderRadius="md" 
        p="3" 
        mb="4"
        
       
        >
        <Input
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
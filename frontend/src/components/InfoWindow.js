import React from 'react';
import { Box } from '@chakra-ui/react';

function InfoWindow({ label, value, onChange }) {
  try{
    return (
      <Box borderWidth="11px" borderRadius="md" p="3" mb="4">
      <label>{label}:</label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </Box>
    );
  }catch (error){
    console.error("Error en Infowindow: ", error);
    return null; //se devuelve null con un mensaje de error
  }
}
export default InfoWindow;
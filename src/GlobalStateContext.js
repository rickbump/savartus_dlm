import React, { createContext, useState } from 'react';
// Create the context
const GlobalStateContext = createContext();

// Create a provider component
export const GlobalStateProvider = ({ children }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const addFiles = (files) => {
    setSelectedFiles((prevFiles) => [...prevFiles, ...files]);
  };

  const clearFiles = () => {
    setSelectedFiles([]);
  };

  return (
    <GlobalStateContext.Provider value={{ selectedFiles, addFiles, clearFiles }}>
      {children}
    </GlobalStateContext.Provider>
  );
};

export default GlobalStateContext;
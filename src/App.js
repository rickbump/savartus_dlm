import React, { useState } from 'react';
import { GlobalStateProvider } from './GlobalStateContext';
import IngestionTab from './components/IngestionTab';
import AccessShareTab from './components/AccessShareTab';
import { Tab, Tabs } from '@mui/material';
import TabPanel from './components/TabPanel';
import './App.css'; // Import the CSS file

function App() {
  const [value, setValue] = useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <GlobalStateProvider>
      <div className="App">
        {/* Fixed header section */}
        <div className="App-header">
          <h1>Data Lifecycle Management by SAVARTUS</h1>
          <Tabs value={value} onChange={handleChange} aria-label="DLM Tabs">
            <Tab label="Ingestion" />
            <Tab label="Contextualize" />
            <Tab label="Access/Share" />
            <Tab label="Store" />
            <Tab label="Destroy" />
            <Tab label="Analytics" />
            <Tab label="Configurations" />
            <Tab label="Settings" />
          </Tabs>
        </div>

        {/* Main content section */}
        <div className="App-content">
          <TabPanel value={value} index={0}>
            <IngestionTab />
          </TabPanel>
          <TabPanel value={value} index={1}>
            <h2>Contextualize</h2>
            <p>Contextualize your data...</p>
          </TabPanel>
          <TabPanel value={value} index={2}>
            <AccessShareTab />
          </TabPanel>
          <TabPanel value={value} index={3}>
            <h2>Store</h2>
            <p>Store your data securely...</p>
          </TabPanel>
          <TabPanel value={value} index={4}>
            <h2>Destroy</h2>
            <p>Manage data destruction...</p>
          </TabPanel>
          <TabPanel value={value} index={5}>
            <h2>Analytics</h2>
            <p>Run analytics on your data...</p>
          </TabPanel>
          <TabPanel value={value} index={6}>
            <h2>Configurations</h2>
            <p>Configure settings for your data lifecycle management...</p>
          </TabPanel>
          <TabPanel value={value} index={7}>
            <h2>Settings</h2>
            <p>General settings and preferences...</p>
          </TabPanel>
        </div>
      </div>
    </GlobalStateProvider>
  );
}

export default App;
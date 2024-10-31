import React, { useState, useContext, useCallback } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Grid,
  Typography,
  Paper,
  TextField
} from '@mui/material';
import { styled } from '@mui/system';
import { LocalizationProvider, DatePicker, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import GlobalStateContext from '../GlobalStateContext';

const API_URL = 'http://10.0.0.5:5000/upload';

const DragDropArea = styled(Paper)(({ theme }) => ({
  border: '2px dashed #aaa',
  padding: theme.spacing(2),
  textAlign: 'center',
  cursor: 'pointer',
  backgroundColor: '#f9f9f9',
  minHeight: '100px',
}));

const SelectedFilesBox = styled(Paper)(({ theme }) => ({
  border: '1px solid #ddd',
  padding: theme.spacing(2),
  marginTop: theme.spacing(2),
}));

const IngestionTab = () => {
  const [timing, setTiming] = useState('processNow');
  const [scheduleDate, setScheduleDate] = useState(null);
  const [scheduleTime, setScheduleTime] = useState(null);
  const { selectedFiles, addFiles, clearFiles } = useContext(GlobalStateContext);

  // State to store selected file
  const [uploadMessage, setUploadMessage] = useState('');

  const handleTimingChange = useCallback((event) => setTiming(event.target.value), []);
  const handleFileSelect = useCallback((event) => addFiles(Array.from(event.target.files)), [addFiles]);
  const handleDragDrop = useCallback((event) => {
    event.preventDefault();
    addFiles(Array.from(event.dataTransfer.files));
  }, [addFiles]);

  const handleCancel = useCallback(clearFiles, [clearFiles]);

  const handleOk = useCallback(async () => {
    console.log("OK button clicked");
    console.log("Selected files:", selectedFiles);

    const formData = new FormData();
    selectedFiles.forEach((file, index) => formData.append(`file${index}`, file));

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Success:', data);
      alert(`Processing Output:\n${data.message}`);
      clearFiles();
    } catch (error) {
      console.error('Error:', error);
      setUploadMessage(`Error uploading file: ${error.message}`);
    }
  }, [selectedFiles, clearFiles]);

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={6}>
        <Box>
          <FormControl component="fieldset">
            <FormLabel component="legend">Timing</FormLabel>
            <RadioGroup value={timing} onChange={handleTimingChange}>
              <FormControlLabel value="processNow" control={<Radio />} label="Process Now" />
              <FormControlLabel value="scheduled" control={<Radio />} label="Schedule Processing" />
            </RadioGroup>

            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <Box display="flex" alignItems="center" mt={2}>
                <DatePicker
                  label="Select Date"
                  value={scheduleDate}
                  onChange={(newValue) => setScheduleDate(newValue)}
                  disabled={timing !== 'scheduled'}
                  slotProps={{ textField: { style: { marginRight: '20px' } } }}
                />
                <TimePicker
                  label="Select Time"
                  value={scheduleTime}
                  onChange={(newValue) => setScheduleTime(newValue)}
                  disabled={timing !== 'scheduled'}
                  slotProps={{ textField: {} }}
                />
              </Box>
            </LocalizationProvider>
          </FormControl>

          <Box mt={2}>
            <DragDropArea onDrop={handleDragDrop} onDragOver={(e) => e.preventDefault()}>
              <Typography component="div" variant="h6">Drag and drop files here</Typography>
            </DragDropArea>
          </Box>

          <Box mt={2}>
            <Button variant="contained" component="label">
              Select Files
              <input type="file" hidden multiple onChange={handleFileSelect} />
            </Button>
          </Box>

          <SelectedFilesBox>
            <Typography component="div" variant="h6">Selected Files/Folders:</Typography>
            <Box component="ul">
              {selectedFiles.map((file, index) => (
                <li key={index}>{file.name}</li>
              ))}
            </Box>
          </SelectedFilesBox>

          <Box mt={2} display="flex" justifyContent="space-between">
            <Button variant="outlined" onClick={handleCancel}>Cancel</Button>
            <Button variant="contained" color="primary" onClick={handleOk}>OK</Button>
          </Box>
          {uploadMessage && (
            <Box mt={2}>
              <Typography component="div" variant="body1" color="error">
                {uploadMessage}
              </Typography>
            </Box>
          )}
        </Box>
      </Grid>

      <Grid item xs={12} md={6}>
        <Box>
          <Typography component="div" variant="h5" gutterBottom>
            Ingestion Settings
          </Typography>
        </Box>
      </Grid>
    </Grid>
  );
};

export default IngestionTab;
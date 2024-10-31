import React, { useState } from 'react';
import {
  TextField, Button, Box, Typography, Paper, Table, TableBody, TableCell,
  TableHead, TableRow, Grid, Divider
} from '@mui/material';

const AccessShareTab = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');

  // Handle search query
  const handleSearch = () => {
    fetch(`http://10.0.0.5:5000/search_processed_files?query=${searchQuery}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setSearchResults(data);
        setError('');  // Clear any previous errors
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setError('Error fetching data. Please try again later.');
      });
  };

  // Handle selection of a file to show details on the right side
  const handleFileSelect = (file) => {
    setSelectedFile(file);
  };

  return (
    <Box p={3}>
      <Typography variant="h5" gutterBottom>
        Access and Share Files
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Box mb={2}>
            <TextField
              label="Search Files"
              variant="outlined"
              fullWidth
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleSearch}
              style={{ marginTop: '10px' }}
            >
              Search
            </Button>
          </Box>

          {error && (
            <Typography color="error" variant="body2">
              {error}
            </Typography>
          )}

          {/* Search Results */}
          <Paper variant="outlined" style={{ maxHeight: '400px', overflowY: 'auto' }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>File Name</TableCell>
                  <TableCell>File Size</TableCell>
                  <TableCell>File Type</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {searchResults.map((result, index) => (
                  <TableRow
                    key={index}
                    onClick={() => handleFileSelect(result)}
                    style={{ cursor: 'pointer' }}
                  >
                    <TableCell>{result.id}</TableCell>
                    <TableCell>{result.file_name}</TableCell>
                    <TableCell>{result.file_size}</TableCell>
                    <TableCell>{result.file_type}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          {selectedFile ? (
            <Box p={2} border="1px solid #ddd">
              <Typography variant="h6" gutterBottom>
                File Details
              </Typography>
              <Divider />
              <Typography><strong>ID:</strong> {selectedFile.id}</Typography>
              <Typography><strong>File Name:</strong> {selectedFile.file_name}</Typography>
              <Typography><strong>File Size:</strong> {selectedFile.file_size}</Typography>
              <Typography><strong>File Type:</strong> {selectedFile.file_type}</Typography>
              <Typography><strong>Process Date:</strong> {selectedFile.process_date}</Typography>
              <Typography><strong>Additional Data:</strong> {selectedFile.additional_data}</Typography>
            </Box>
          ) : (
            <Box p={2} border="1px solid #ddd" display="flex" alignItems="center" justifyContent="center" minHeight="400px">
              <Typography>Select a file to view details</Typography>
            </Box>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default AccessShareTab;
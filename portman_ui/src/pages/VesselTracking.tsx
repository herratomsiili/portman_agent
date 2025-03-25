import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Chip,
  CircularProgress,
  Alert
} from '@mui/material';
import { api } from '../services/api';
import { mockPortCalls, mockTrackedVessels } from '../data/mockData';

const VesselTracking: React.FC = () => {
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterPort, setFilterPort] = useState('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [portCalls, setPortCalls] = useState<any[]>([]);

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        // In a production environment, this would be an actual API call
        // For now, we'll use our mock data with a simulated delay

        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Use mock data
        setPortCalls(mockPortCalls);

        // In a real implementation, we would use:
        // const response = await api.getPortCalls();
        // setPortCalls(response);
      } catch (err) {
        console.error('Error fetching vessel tracking data:', err);
        setError('Failed to load vessel tracking data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleStatusChange = (event: SelectChangeEvent) => {
    setFilterStatus(event.target.value);
  };

  const handlePortChange = (event: SelectChangeEvent) => {
    setFilterPort(event.target.value);
  };

  // Get unique ports for filter
  const uniquePorts = Array.from(new Set(portCalls.map(call => call.port.name)));

  // Filter vessels based on selected filters
  const filteredVessels = portCalls.filter(call => {
    if (filterStatus !== 'all' && call.portCallStatus !== filterStatus) {
      return false;
    }
    if (filterPort !== 'all' && call.port.name !== filterPort) {
      return false;
    }
    return true;
  });

  if (loading) {
    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress />
        </Box>
    );
  }

  return (
      <Box sx={{ flexGrow: 1 }}>
        <Typography variant="h4" gutterBottom component="div">
          Vessel Tracking
        </Typography>

        {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
        )}

        {/* Filters */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel id="status-filter-label">Status</InputLabel>
              <Select
                  labelId="status-filter-label"
                  id="status-filter"
                  value={filterStatus}
                  label="Status"
                  onChange={handleStatusChange}
              >
                <MenuItem value="all">All Statuses</MenuItem>
                <MenuItem value="ACTIVE">Active</MenuItem>
                <MenuItem value="SCHEDULED">Scheduled</MenuItem>
                <MenuItem value="COMPLETED">Completed</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel id="port-filter-label">Port</InputLabel>
              <Select
                  labelId="port-filter-label"
                  id="port-filter"
                  value={filterPort}
                  label="Port"
                  onChange={handlePortChange}
              >
                <MenuItem value="all">All Ports</MenuItem>
                {uniquePorts.map(port => (
                    <MenuItem key={port} value={port}>{port}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>

        {/* Map Visualization */}
        <Paper
            sx={{
              height: 500,
              width: '100%',
              backgroundColor: '#e6f2ff',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              position: 'relative',
              overflow: 'hidden'
            }}
        >
          <Typography variant="h5" color="primary" gutterBottom>
            Interactive Map Visualization
          </Typography>
          <Typography variant="body1" align="center" sx={{ maxWidth: '80%', mb: 2 }}>
            This would be an interactive map showing vessel locations and port calls.
            In a production implementation, this would use Leaflet or Google Maps API.
          </Typography>

          {/* Simulate map markers for vessels */}
          {filteredVessels.map((call, index) => {
            // Generate random positions for demo purposes
            const left = 10 + (index * 15) % 80;
            const top = 20 + (index * 20) % 60;

            return (
                <Box
                    key={call.portCallId}
                    sx={{
                      position: 'absolute',
                      left: `${left}%`,
                      top: `${top}%`,
                      transform: 'translate(-50%, -50%)',
                      zIndex: 10,
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center'
                    }}
                >
                  <Box
                      sx={{
                        width: 20,
                        height: 20,
                        borderRadius: '50%',
                        backgroundColor: call.portCallStatus === 'ACTIVE' ? 'green' : 'blue',
                        border: '2px solid white',
                        boxShadow: '0 0 5px rgba(0,0,0,0.3)',
                        cursor: 'pointer',
                        '&:hover': {
                          transform: 'scale(1.2)',
                          boxShadow: '0 0 8px rgba(0,0,0,0.5)',
                        }
                      }}
                  />
                  <Typography
                      variant="caption"
                      sx={{
                        mt: 0.5,
                        backgroundColor: 'rgba(255,255,255,0.7)',
                        px: 1,
                        borderRadius: 1,
                        fontWeight: 'bold'
                      }}
                  >
                    {call.vessel.vesselName}
                  </Typography>
                </Box>
            );
          })}

          {/* Simulate port locations */}
          {Array.from(new Set(portCalls.map(call => call.port.name))).map((portName, index) => {
            // Generate random positions for demo purposes
            const left = 15 + (index * 25) % 70;
            const top = 30 + (index * 15) % 50;

            return (
                <Box
                    key={portName}
                    sx={{
                      position: 'absolute',
                      left: `${left}%`,
                      top: `${top}%`,
                      transform: 'translate(-50%, -50%)',
                      zIndex: 5,
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center'
                    }}
                >
                  <Box
                      sx={{
                        width: 15,
                        height: 15,
                        backgroundColor: 'red',
                        border: '2px solid white',
                        boxShadow: '0 0 5px rgba(0,0,0,0.3)',
                        cursor: 'pointer',
                        '&:hover': {
                          transform: 'scale(1.2)',
                          boxShadow: '0 0 8px rgba(0,0,0,0.5)',
                        }
                      }}
                  />
                  <Typography
                      variant="caption"
                      sx={{
                        mt: 0.5,
                        backgroundColor: 'rgba(255,255,255,0.7)',
                        px: 1,
                        borderRadius: 1
                      }}
                  >
                    {portName}
                  </Typography>
                </Box>
            );
          })}
        </Paper>

        {/* Vessel List */}
        <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
          Tracked Vessels
        </Typography>

        <Grid container spacing={2}>
          {filteredVessels.map(call => (
              <Grid item xs={12} sm={6} md={4} key={call.portCallId}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <Typography variant="h6" component="div">
                        {call.vessel.vesselName}
                      </Typography>
                      <Chip
                          label={call.portCallStatus}
                          color={
                            call.portCallStatus === 'ACTIVE'
                                ? 'success'
                                : call.portCallStatus === 'SCHEDULED'
                                    ? 'primary'
                                    : 'default'
                          }
                          size="small"
                      />
                    </Box>
                    <Typography color="text.secondary" gutterBottom>
                      IMO: {call.vessel.imoLloyds}
                    </Typography>
                    <Typography variant="body2" sx={{ mb: 1.5 }}>
                      {call.port.name} - {call.berth.berthName}
                    </Typography>
                    <Grid container spacing={1}>
                      <Grid item xs={6}>
                        <Typography variant="caption" display="block">
                          ETA: {call.eta ? new Date(call.eta).toLocaleString() : 'N/A'}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" display="block">
                          ETD: {call.etd ? new Date(call.etd).toLocaleString() : 'N/A'}
                        </Typography>
                      </Grid>
                      {call.ata && (
                          <Grid item xs={6}>
                            <Typography variant="caption" display="block">
                              ATA: {new Date(call.ata).toLocaleString()}
                            </Typography>
                          </Grid>
                      )}
                      {call.atd && (
                          <Grid item xs={6}>
                            <Typography variant="caption" display="block">
                              ATD: {new Date(call.atd).toLocaleString()}
                            </Typography>
                          </Grid>
                      )}
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
          ))}
          {filteredVessels.length === 0 && (
              <Grid item xs={12}>
                <Paper sx={{ p: 3, textAlign: 'center' }}>
                  <Typography>No vessels match the selected filters</Typography>
                </Paper>
              </Grid>
          )}
        </Grid>
      </Box>
  );
};

export default VesselTracking;

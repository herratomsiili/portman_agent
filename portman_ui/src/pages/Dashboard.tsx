import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider,
  CircularProgress,
  Alert
} from '@mui/material';
import { api } from '../services/api';
import { PortCall } from '../types';

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [portCalls, setPortCalls] = useState<PortCall[]>([]);
  const [trackedVessels, setTrackedVessels] = useState<number[]>([]);

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        // In a production environment, these would be actual API calls
        // For now, we'll use our mock data with a simulated delay

        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Use mock data
        // setPortCalls(mockPortCalls);
        // setTrackedVessels(mockTrackedVessels);

        // In a real implementation, we would use:
        const portCallsResponse = await api.getPortCalls();
        setPortCalls(portCallsResponse);
        const mockTrackedVessels = [9902419, 9902420, 9234567, 9456789, 9567890];


        // const vesselsResponse = await api.getTrackedVessels();
        setTrackedVessels(mockTrackedVessels);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Calculate statistics
  const activeVessels = portCalls.filter(call => call.ata !== undefined).length;
  const scheduledVessels = portCalls.filter(call => call.ata === undefined).length;
  const totalPassengers = portCalls.reduce((sum, call) => sum + (call.passengersonarrival || 0), 0);

  // Get upcoming arrivals (sorted by ETA)
  const upcomingArrivals = [...portCalls]
      .filter(call => call.ata === undefined)
      .sort((a, b) => new Date(a.eta).getTime() - new Date(b.eta).getTime())
      .slice(0, 5);

  if (loading) {
    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress data-cy="dashboard-loading" />
        </Box>
    );
  }

  return (
      <Box sx={{ flexGrow: 1 }} data-cy="dashboard-container">
        <Typography variant="h4" gutterBottom component="div" data-cy="dashboard-title">
          Vessel Tracking Dashboard
        </Typography>

        {error && (
            <Alert severity="error" sx={{ mb: 3 }} data-cy="dashboard-error">
              {error}
            </Alert>
        )}

        {/* Summary Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }} data-cy="summary-cards">
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={3} sx={{ height: '100%' }} data-cy="card-tracked-vessels">
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h6" color="primary">Tracked Vessels</Typography>
                <Typography variant="h3" data-cy="tracked-vessels-count">{trackedVessels.length}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={3} sx={{ height: '100%' }} data-cy="card-active-calls">
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h6" color="primary">Active Port Calls</Typography>
                <Typography variant="h3" data-cy="active-calls-count">{activeVessels}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={3} sx={{ height: '100%' }} data-cy="card-scheduled-arrivals">
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h6" color="primary">Scheduled Arrivals</Typography>
                <Typography variant="h3" data-cy="scheduled-arrivals-count">{scheduledVessels}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={3} sx={{ height: '100%' }} data-cy="card-passengers">
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h6" color="primary">Total Passengers</Typography>
                <Typography variant="h3" data-cy="passengers-count">{totalPassengers}</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Main Content */}
        <Grid container spacing={3} data-cy="dashboard-content">
          {/* Upcoming Arrivals */}
          <Grid item xs={12} md={6}>
            <Card data-cy="upcoming-arrivals-card">
              <CardContent>
                <Typography variant="h6" gutterBottom data-cy="upcoming-arrivals-title">
                  Upcoming Arrivals
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <List data-cy="upcoming-arrivals-list">
                  {upcomingArrivals.map((call) => (
                      <React.Fragment key={call.portcallid}>
                        <ListItem data-cy={`arrival-item-${call.portcallid}`}>
                          <ListItemText
                              primary={call.vesselname}
                              secondary={
                                <>
                                  <Typography component="span" variant="body2" color="text.primary">
                                    {call.portareaname} - {call.berthname}
                                  </Typography>
                                  {` — ETA: ${new Date(call.eta).toLocaleString()}`}
                                </>
                              }
                          />
                        </ListItem>
                        <Divider />
                      </React.Fragment>
                  ))}
                  {upcomingArrivals.length === 0 && (
                      <ListItem data-cy="no-upcoming-arrivals">
                        <ListItemText primary="No upcoming arrivals" />
                      </ListItem>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Active Vessels */}
          <Grid item xs={12} md={6}>
            <Card data-cy="active-vessels-card">
              <CardContent>
                <Typography variant="h6" gutterBottom data-cy="active-vessels-title">
                  Active Vessels
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <List data-cy="active-vessels-list">
                  {portCalls
                      .filter(call => call.ata !== undefined)
                      .map((call) => (
                          <React.Fragment key={call.portcallid}>
                            <ListItem data-cy={`vessel-item-${call.portcallid}`}>
                              <ListItemText
                                  primary={call.vesselname}
                                  secondary={
                                    <>
                                      <Typography component="span" variant="body2" color="text.primary">
                                        {call.portareaname} - {call.berthname}
                                      </Typography>
                                      {` — ATA: ${call.ata ? new Date(call.ata).toLocaleString() : 'N/A'}`}
                                    </>
                                  }
                              />
                            </ListItem>
                            <Divider />
                          </React.Fragment>
                      ))}
                  {portCalls.filter(call => call.ata !== undefined).length === 0 && (
                      <ListItem data-cy="no-active-vessels">
                        <ListItemText primary="No active vessels" />
                      </ListItem>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
  );
};

export default Dashboard;

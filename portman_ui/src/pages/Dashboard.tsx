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
import { mockPortCalls, mockTrackedVessels } from '../data/mockData';
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
        setPortCalls(mockPortCalls);
        setTrackedVessels(mockTrackedVessels);

        // In a real implementation, we would use:
        // const portCallsResponse = await api.getPortCalls();
        // setPortCalls(portCallsResponse);
        // 
        // const vesselsResponse = await api.getTrackedVessels();
        // setTrackedVessels(vesselsResponse);
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
  const activeVessels = portCalls.filter(call => call.portCallStatus === 'ACTIVE').length;
  const scheduledVessels = portCalls.filter(call => call.portCallStatus === 'SCHEDULED').length;
  const totalPassengers = portCalls.reduce((sum, call) => sum + (call.passengerCount || 0), 0);

  // Get upcoming arrivals (sorted by ETA)
  const upcomingArrivals = [...portCalls]
      .filter(call => call.portCallStatus === 'SCHEDULED')
      .sort((a, b) => new Date(a.eta).getTime() - new Date(b.eta).getTime())
      .slice(0, 5);

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
          Vessel Tracking Dashboard
        </Typography>

        {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
        )}

        {/* Summary Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={3} sx={{ height: '100%' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h6" color="primary">Tracked Vessels</Typography>
                <Typography variant="h3">{trackedVessels.length}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={3} sx={{ height: '100%' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h6" color="primary">Active Port Calls</Typography>
                <Typography variant="h3">{activeVessels}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={3} sx={{ height: '100%' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h6" color="primary">Scheduled Arrivals</Typography>
                <Typography variant="h3">{scheduledVessels}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={3} sx={{ height: '100%' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h6" color="primary">Total Passengers</Typography>
                <Typography variant="h3">{totalPassengers}</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Main Content */}
        <Grid container spacing={3}>
          {/* Upcoming Arrivals */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Upcoming Arrivals
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <List>
                  {upcomingArrivals.map((call) => (
                      <React.Fragment key={call.portCallId}>
                        <ListItem>
                          <ListItemText
                              primary={call.vessel.vesselName}
                              secondary={
                                <>
                                  <Typography component="span" variant="body2" color="text.primary">
                                    {call.port.name} - {call.berth.berthName}
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
                      <ListItem>
                        <ListItemText primary="No upcoming arrivals" />
                      </ListItem>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Active Vessels */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Active Vessels
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <List>
                  {portCalls
                      .filter(call => call.portCallStatus === 'ACTIVE')
                      .map((call) => (
                          <React.Fragment key={call.portCallId}>
                            <ListItem>
                              <ListItemText
                                  primary={call.vessel.vesselName}
                                  secondary={
                                    <>
                                      <Typography component="span" variant="body2" color="text.primary">
                                        {call.port.name} - {call.berth.berthName}
                                      </Typography>
                                      {` — ATA: ${call.ata ? new Date(call.ata).toLocaleString() : 'N/A'}`}
                                    </>
                                  }
                              />
                            </ListItem>
                            <Divider />
                          </React.Fragment>
                      ))}
                  {portCalls.filter(call => call.portCallStatus === 'ACTIVE').length === 0 && (
                      <ListItem>
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

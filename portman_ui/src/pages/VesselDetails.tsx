import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Divider,
  List,
  ListItem,
  ListItemText,
  Paper,
  Chip,
  CircularProgress,
  Alert
} from '@mui/material';
import { api } from '../services/api';
import { mockPortCalls, mockArrivalUpdates } from '../data/mockData';
import { PortCall } from '../types';

const VesselDetails: React.FC = () => {
  const { imoNumber } = useParams<{ imoNumber: string }>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [vesselPortCalls, setVesselPortCalls] = useState<PortCall[]>([]);
  const [vesselArrivalUpdates, setVesselArrivalUpdates] = useState<any[]>([]);

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      if (!imoNumber) return;

      setLoading(true);
      setError(null);

      try {
        // In a production environment, these would be actual API calls
        // For now, we'll use our mock data with a simulated delay

        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Filter mock data for this vessel
        const filteredPortCalls = mockPortCalls.filter(
            call => call.vessel.imoLloyds.toString() === imoNumber
        );

        const filteredArrivalUpdates = mockArrivalUpdates.filter(
            update => {
              const portCall = mockPortCalls.find(call => call.portCallId === update.portCallId);
              return portCall?.vessel.imoLloyds.toString() === imoNumber;
            }
        );

        setVesselPortCalls(filteredPortCalls);
        setVesselArrivalUpdates(filteredArrivalUpdates);

        // In a real implementation, we would use:
        // const portCallsResponse = await api.getPortCalls({ imo: imoNumber });
        // setVesselPortCalls(portCallsResponse);
        // 
        // const updatesResponse = await api.getArrivalUpdates({ imo: imoNumber });
        // setVesselArrivalUpdates(updatesResponse);
      } catch (err) {
        console.error('Error fetching vessel details:', err);
        setError('Failed to load vessel details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [imoNumber]);

  // Get the vessel details from the first port call
  const vessel = vesselPortCalls.length > 0 ? vesselPortCalls[0].vessel : null;

  const formatDateTime = (dateString: string | null) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress />
        </Box>
    );
  }

  if (!vessel) {
    return (
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h4" gutterBottom component="div">
            Vessel Not Found
          </Typography>
          <Typography variant="body1">
            No vessel found with IMO number {imoNumber}.
          </Typography>
        </Box>
    );
  }

  return (
      <Box sx={{ flexGrow: 1 }}>
        <Typography variant="h4" gutterBottom component="div">
          Vessel Details: {vessel.vesselName}
        </Typography>

        {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
        )}

        {/* Vessel Information */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Vessel Information
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <Typography variant="subtitle2">Vessel Name</Typography>
                  </Grid>
                  <Grid item xs={8}>
                    <Typography variant="body1">{vessel.vesselName}</Typography>
                  </Grid>

                  <Grid item xs={4}>
                    <Typography variant="subtitle2">IMO Number</Typography>
                  </Grid>
                  <Grid item xs={8}>
                    <Typography variant="body1">{vessel.imoLloyds}</Typography>
                  </Grid>

                  <Grid item xs={4}>
                    <Typography variant="subtitle2">Vessel Type</Typography>
                  </Grid>
                  <Grid item xs={8}>
                    <Typography variant="body1">{vessel.vesselTypeCode}</Typography>
                  </Grid>

                  {vessel.mmsi && (
                      <>
                        <Grid item xs={4}>
                          <Typography variant="subtitle2">MMSI</Typography>
                        </Grid>
                        <Grid item xs={8}>
                          <Typography variant="body1">{vessel.mmsi}</Typography>
                        </Grid>
                      </>
                  )}
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Current Status
                </Typography>
                <Divider sx={{ mb: 2 }} />
                {vesselPortCalls.filter(call => call.portCallStatus === 'ACTIVE').length > 0 ? (
                    vesselPortCalls
                        .filter(call => call.portCallStatus === 'ACTIVE')
                        .map((call: PortCall) => (
                            <Grid container spacing={2} key={call.portCallId}>
                              <Grid item xs={4}>
                                <Typography variant="subtitle2">Current Port</Typography>
                              </Grid>
                              <Grid item xs={8}>
                                <Typography variant="body1">{call.port.name}</Typography>
                              </Grid>

                              <Grid item xs={4}>
                                <Typography variant="subtitle2">Berth</Typography>
                              </Grid>
                              <Grid item xs={8}>
                                <Typography variant="body1">{call.berth.berthName}</Typography>
                              </Grid>

                              <Grid item xs={4}>
                                <Typography variant="subtitle2">Arrival Time</Typography>
                              </Grid>
                              <Grid item xs={8}>
                                {/*<Typography variant="body1">{formatDateTime(call.ata)}</Typography>*/}
                              </Grid>

                              <Grid item xs={4}>
                                <Typography variant="subtitle2">Expected Departure</Typography>
                              </Grid>
                              <Grid item xs={8}>
                                <Typography variant="body1">{formatDateTime(call.etd)}</Typography>
                              </Grid>

                              <Grid item xs={4}>
                                <Typography variant="subtitle2">Status</Typography>
                              </Grid>
                              <Grid item xs={8}>
                                <Chip label={call.portCallStatus} color="success" size="small" />
                              </Grid>
                            </Grid>
                        ))
                ) : (
                    <Typography variant="body1">
                      No active port calls for this vessel.
                    </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Port Call History */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Port Call History
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <List>
                {vesselPortCalls.map((call: PortCall) => (
                    <React.Fragment key={call.portCallId}>
                      <ListItem>
                        <ListItemText
                            primary={`${call.port.name} - ${call.berth.berthName}`}
                            secondary={
                              <>
                                <Typography component="span" variant="body2" color="text.primary">
                                  {formatDateTime(call.eta)} - {formatDateTime(call.etd)}
                                </Typography>
                                <br />
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
                                    sx={{ mt: 1 }}
                                />
                              </>
                            }
                        />
                      </ListItem>
                      <Divider />
                    </React.Fragment>
                ))}
                {vesselPortCalls.length === 0 && (
                    <ListItem>
                      <ListItemText primary="No port call history available" />
                    </ListItem>
                )}
              </List>
            </Paper>
          </Grid>

          {/* Arrival Updates */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Arrival Time Updates
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <List>
                {vesselArrivalUpdates.map((update) => (
                    <React.Fragment key={update.id}>
                      <ListItem>
                        <ListItemText
                            primary={`${update.portAreaName} - ${update.berthName}`}
                            secondary={
                              <>
                                <Typography component="span" variant="body2" color="text.primary">
                                  ETA changed from {formatDateTime(update.oldEta)} to {formatDateTime(update.eta)}
                                </Typography>
                                <br />
                                <Typography variant="caption">
                                  Updated on {formatDateTime(update.created)}
                                </Typography>
                              </>
                            }
                        />
                      </ListItem>
                      <Divider />
                    </React.Fragment>
                ))}
                {vesselArrivalUpdates.length === 0 && (
                    <ListItem>
                      <ListItemText primary="No arrival updates available" />
                    </ListItem>
                )}
              </List>
            </Paper>
          </Grid>
        </Grid>
      </Box>
  );
};

export default VesselDetails;

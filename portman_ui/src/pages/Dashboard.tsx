import React, { useState, useEffect } from 'react';
import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';
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
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Checkbox,
  FormControlLabel
} from '@mui/material';
import { api } from '../services/api';
import { mockPortCalls, mockTrackedVessels } from '../data/mockData';
import { PortCall } from '../types';
import { group } from 'console';

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

  // Popup button
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [selectedToAdd, setSelectedToAdd] = useState<string[]>([]);

  // Calculate statistics
  const activeVessels = portCalls.filter(call => call.portCallStatus === 'ACTIVE').length;
  const scheduledVessels = portCalls.filter(call => call.portCallStatus === 'SCHEDULED').length;
  const totalPassengers = portCalls.reduce((sum, call) => sum + (call.passengerCount || 0), 0);

  // Dynamic Card state
  const availableCardTypes = [
    { type: 'Tracked Vessels', getValue: () => trackedVessels.length, group: 'stats' },
    { type: 'Active Port Calls', getValue: () => activeVessels, group: 'stats' },
    { type: 'Scheduled Arrivals', getValue: () => scheduledVessels, group: 'stats' },
    { type: 'Total Passengers', getValue: () => totalPassengers, group: 'stats' },
    {
      type: 'Upcoming Arrivals',
      getValue: () => [...portCalls]
        .filter(call => call.portCallStatus === 'SCHEDULED')
        .sort((a, b) => new Date(a.eta).getTime() - new Date(b.eta).getTime())
        .slice(0, 5),
      group: 'views'
    },
    {
      type: 'Active Vessels',
      getValue: () => portCalls.filter(call => call.portCallStatus === 'ACTIVE'),
      group: 'views'
    }
  ];

  type StatCard = {
    id: string;
    type: string;
    value: number | PortCall[];
  };

  const addCard = (type: string) => {
    const cardType = availableCardTypes.find(c => c.type === type);
    if (!cardType) return;

    setStatistics(prev => [
      ...prev,
      {
        id: crypto.randomUUID(),
        type: cardType.type,
        value: cardType.getValue()
      }
    ]);
  };


  const removeCard = (id: string) => {
    setStatistics(prev => prev.filter(card => card.id !== id));
  };

  const [statistics, setStatistics] = useState<StatCard[]>([]);
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

      <Button
        variant="outlined"
        onClick={() => setAddDialogOpen(true)}
        sx={{ mb: 2 }}
      >
        Add Card
      </Button>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {statistics.map(card => (
          <Grid key={card.id} item xs={12} sm={6} md={typeof card.value === 'number' ? 3 : 6}>
            <Card
              elevation={3}
              sx={{
                height: '100%',
                position: 'relative',
                '&:hover .close-button': { opacity: 1 }
              }}
            >
              <IconButton
                className="close-button"
                size="small"
                onClick={() => removeCard(card.id)}
                sx={{
                  position: 'absolute',
                  top: 8,
                  right: 8,
                  opacity: 0,
                  transition: 'opacity 0.2s ease-in-out'
                }}
              >
                <CloseIcon fontSize="small" />
              </IconButton>

              <CardContent>
                {/* NUMEROT */}
                {typeof card.value === 'number' && (
                  <>
                    <Typography variant="h6" color="primary" sx={{ textAlign: 'center' }}>
                      {card.type}
                    </Typography>
                    <Typography variant="h3" sx={{ textAlign: 'center' }}>
                      {card.value}
                    </Typography>
                  </>
                )}

                {/* LISTAT: Upcoming Arrivals */}
                {card.type === 'Upcoming Arrivals' && Array.isArray(card.value) && (
                  <>
                    <Typography variant="h6" gutterBottom>Upcoming Arrivals</Typography>
                    <Divider sx={{ mb: 2 }} />
                    <List>
                      {card.value.map((call: PortCall) => (
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
                    </List>
                  </>
                )}

                {/* LISTAT: Active Vessels */}
                {card.type === 'Active Vessels' && Array.isArray(card.value) && (
                  <>
                    <Typography variant="h6" gutterBottom>Active Vessels</Typography>
                    <Divider sx={{ mb: 2 }} />
                    <List>
                      {card.value.map((call: PortCall) => (
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
                    </List>
                  </>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>


      {/* Main Content */}
      <Grid container spacing={3}>


        <Dialog open={addDialogOpen} onClose={() => setAddDialogOpen(false)}>
          <DialogContent>
            {/* Stats Group */}
            <Typography variant="subtitle2" sx={{ mt: 1, mb: 1 }}>
              Stat Cards
            </Typography>
            {availableCardTypes
              .filter(card => card.group === 'stats')
              .map(card => (
                <Button
                  key={card.type}
                  fullWidth
                  sx={{ mb: 1 }}
                  onClick={() => addCard(card.type)}
                  variant="outlined"
                >
                  + {card.type}
                </Button>
              ))}

            {/* Views Group */}
            <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
              List Views
            </Typography>
            {availableCardTypes
              .filter(card => card.group === 'views')
              .map(card => (
                <Button
                  key={card.type}
                  fullWidth
                  sx={{ mb: 1 }}
                  onClick={() => addCard(card.type)}
                  variant="outlined"
                >
                  + {card.type}
                </Button>
              ))}
          </DialogContent>

          <DialogActions>
            <Button onClick={() => setAddDialogOpen(false)}>Close</Button>
          </DialogActions>
        </Dialog>
      </Grid>
    </Box>
  );
};

export default Dashboard;
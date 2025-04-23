import React, { useState, useEffect } from 'react';
import { Box, Typography, Grid } from '@mui/material';
import { api } from '../services/api';
import { PortCall } from '../types';
import SummaryCards from '../components/dashboard/SummaryCards';
import UpcomingArrivals from '../components/dashboard/UpcomingArrivals';
import ActiveVessels from '../components/dashboard/ActiveVessels';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorAlert from '../components/common/ErrorAlert';

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [portCalls, setPortCalls] = useState<PortCall[]>([]);
  const [trackedVessels, setTrackedVessels] = useState<number[]>([]);
  const [activeVesselsPage, setActiveVesselsPage] = useState(0);
  const [activeVesselsRowsPerPage, setActiveVesselsRowsPerPage] = useState(5);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const portCallsResponse = await api.getPortCalls();
        setPortCalls(portCallsResponse || []);
        const mockTrackedVessels = [9902419, 9902420, 9234567, 9456789, 9567890];
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
  const activeVessels = portCalls?.filter(call => call?.ata !== undefined).length || 0;
  const scheduledVessels = portCalls?.filter(call => call?.ata === undefined).length || 0;
  const totalPassengers = portCalls?.reduce((sum, call) => sum + (call?.passengersonarrival || 0), 0) || 0;

  // Get upcoming arrivals (sorted by ETA)
  const upcomingArrivals = [...(portCalls || [])]
    .filter(call => call?.ata === undefined)
    .sort((a, b) => new Date(a?.eta || 0).getTime() - new Date(b?.eta || 0).getTime())
    .slice(0, 5);

  // Get active vessels (sorted by ATA)
  const activeVesselsList = [...(portCalls || [])]
    .filter(call => call?.ata !== undefined)
    .sort((a, b) => {
      const dateA = a?.ata ? new Date(a.ata).getTime() : 0;
      const dateB = b?.ata ? new Date(b.ata).getTime() : 0;
      return dateB - dateA;
    });

  // Paginate active vessels
  const paginatedActiveVessels = activeVesselsList.slice(
    activeVesselsPage * activeVesselsRowsPerPage,
    activeVesselsPage * activeVesselsRowsPerPage + activeVesselsRowsPerPage
  );

  const handleActiveVesselsPageChange = (event: unknown, newPage: number) => {
    setActiveVesselsPage(newPage);
  };

  const handleActiveVesselsRowsPerPageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setActiveVesselsRowsPerPage(parseInt(event.target.value, 10));
    setActiveVesselsPage(0);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <Box sx={{ flexGrow: 1, p: 3 }} data-cy="dashboard-container">
      <Typography variant="h4" gutterBottom component="div" data-cy="dashboard-title">
        Dashboard
      </Typography>

      {error && <ErrorAlert message={error} />}

      <SummaryCards
        trackedVesselsCount={trackedVessels.length}
        activeVesselsCount={activeVessels}
        scheduledVesselsCount={scheduledVessels}
        totalPassengers={totalPassengers}
      />

      <Grid container spacing={3} data-cy="dashboard-content">
        <Grid item xs={12} md={6}>
          <UpcomingArrivals arrivals={upcomingArrivals} />
        </Grid>
        <Grid item xs={12} md={6}>
          <ActiveVessels
            vessels={paginatedActiveVessels}
            page={activeVesselsPage}
            rowsPerPage={activeVesselsRowsPerPage}
            onPageChange={handleActiveVesselsPageChange}
            onRowsPerPageChange={handleActiveVesselsRowsPerPageChange}
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;

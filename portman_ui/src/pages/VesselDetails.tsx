import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination
} from '@mui/material';
import { api } from '../services/api';
import { mockPortCalls } from '../data/mockData';
import { PortCall } from '../types';

const VesselDetails: React.FC = () => {
  const { imo } = useParams<{ imo: string }>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [vesselData, setVesselData] = useState<PortCall | null>(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  useEffect(() => {
    const fetchVesselData = async () => {
      setLoading(true);
      setError(null);

      try {
        // In a production environment, this would be an actual API call
        // For now, we'll use our mock data with a simulated delay

        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Find vessel in mock data
        const vessel = mockPortCalls.find(call => call.imolloyds.toString() === imo);
        if (!vessel) {
          throw new Error('Vessel not found');
        }

        setVesselData(vessel);

        // In a real implementation, we would use:
        // const response = await api.getVesselDetails(imo);
        // setVesselData(response);
      } catch (err) {
        console.error('Error fetching vessel details:', err);
        setError('Failed to load vessel details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    if (imo) {
      fetchVesselData();
    }
  }, [imo]);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  if (loading) {
    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress />
        </Box>
    );
  }

  if (error || !vesselData) {
    return (
        <Box sx={{ p: 3 }}>
          <Alert severity="error">
            {error || 'Vessel not found'}
          </Alert>
        </Box>
    );
  }

  return (
      <Box sx={{ flexGrow: 1 }}>
        <Typography variant="h4" gutterBottom component="div">
          Vessel Details
        </Typography>

        {/* Vessel Information Card */}
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h5" gutterBottom>
                  {vesselData.vesselname}
                </Typography>
                <Typography color="text.secondary" gutterBottom>
                  IMO: {vesselData.imolloyds}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Chip
                      label={vesselData.ata !== undefined ? 'Active' : 'Scheduled'}
                      color={vesselData.ata !== undefined ? 'success' : 'primary'}
                      sx={{ mr: 1 }}
                  />
                  <Chip
                      label={`Port: ${vesselData.portareaname}`}
                      variant="outlined"
                      sx={{ mr: 1 }}
                  />
                  <Chip
                      label={`Berth: ${vesselData.berthname}`}
                      variant="outlined"
                  />
                </Box>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>
                  Schedule
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      ETA
                    </Typography>
                    <Typography variant="body1">
                      {vesselData.eta ? new Date(vesselData.eta).toLocaleString() : 'N/A'}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      ETD
                    </Typography>
                    <Typography variant="body1">
                      {vesselData.etd ? new Date(vesselData.etd).toLocaleString() : 'N/A'}
                    </Typography>
                  </Grid>
                  {vesselData.ata && (
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          ATA
                        </Typography>
                        <Typography variant="body1">
                          {new Date(vesselData.ata).toLocaleString()}
                        </Typography>
                      </Grid>
                  )}
                  {vesselData.atd && (
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          ATD
                        </Typography>
                        <Typography variant="body1">
                          {new Date(vesselData.atd).toLocaleString()}
                        </Typography>
                      </Grid>
                  )}
                </Grid>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Additional Information */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Additional Information
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Agent Name
                </Typography>
                <Typography variant="body1" gutterBottom>
                  {vesselData.agentname || 'N/A'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Shipping Company
                </Typography>
                <Typography variant="body1">
                  {vesselData.shippingcompany || 'N/A'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
  );
};

export default VesselDetails;

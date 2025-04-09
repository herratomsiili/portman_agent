import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent
} from '@mui/material';
import { api } from '../services/api';
import { mockPortCalls } from '../data/mockData';
import { PortCall } from '../types';

const Reports: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [portCalls, setPortCalls] = useState<PortCall[]>([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterPort, setFilterPort] = useState('all');

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
        console.error('Error fetching port calls:', err);
        setError('Failed to load port calls. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleStatusChange = (event: SelectChangeEvent) => {
    setFilterStatus(event.target.value);
    setPage(0);
  };

  const handlePortChange = (event: SelectChangeEvent) => {
    setFilterPort(event.target.value);
    setPage(0);
  };

  // Get unique ports for filter
  const uniquePorts = Array.from(new Set(portCalls.map(call => call.portareaname)));

  // Filter port calls based on selected filters
  const filteredPortCalls = portCalls.filter(call => {
    if (filterStatus !== 'all') {
      const isActive = call.ata !== undefined;
      if (filterStatus === 'ACTIVE' && !isActive) return false;
      if (filterStatus === 'SCHEDULED' && isActive) return false;
    }
    if (filterPort !== 'all' && call.portareaname !== filterPort) {
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
          Port Call Reports
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

        {/* Port Calls Table */}
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Vessel Name</TableCell>
                <TableCell>IMO</TableCell>
                <TableCell>Port</TableCell>
                <TableCell>Berth</TableCell>
                <TableCell>ETA</TableCell>
                <TableCell>ETD</TableCell>
                <TableCell>ATA</TableCell>
                <TableCell>ATD</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredPortCalls
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((call) => (
                      <TableRow key={call.portcallid}>
                        <TableCell>{call.vesselname}</TableCell>
                        <TableCell>{call.imolloyds}</TableCell>
                        <TableCell>{call.portareaname}</TableCell>
                        <TableCell>{call.berthname}</TableCell>
                        <TableCell>{call.eta ? new Date(call.eta).toLocaleString() : 'N/A'}</TableCell>
                        <TableCell>{call.etd ? new Date(call.etd).toLocaleString() : 'N/A'}</TableCell>
                        <TableCell>{call.ata ? new Date(call.ata).toLocaleString() : 'N/A'}</TableCell>
                        <TableCell>{call.atd ? new Date(call.atd).toLocaleString() : 'N/A'}</TableCell>
                        <TableCell>
                          {call.ata !== undefined ? 'Active' : 'Scheduled'}
                        </TableCell>
                      </TableRow>
                  ))}
            </TableBody>
          </Table>
          <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              component="div"
              count={filteredPortCalls.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </TableContainer>
      </Box>
  );
};

export default Reports;

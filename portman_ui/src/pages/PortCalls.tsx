import React, { useState, useEffect } from 'react';
import {
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  TextField,
  InputAdornment,
  IconButton,
  Paper,
  CircularProgress,
  Alert
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { api } from '../services/api';
import { mockPortCalls } from '../data/mockData';
import { PortCall } from '../types';

const PortCalls: React.FC = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [portCalls, setPortCalls] = useState<PortCall[]>([]);

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
        console.error('Error fetching port calls:', err);
        setError('Failed to load port calls. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Filter port calls based on search term
  const filteredPortCalls = portCalls.filter(call =>
      call.vessel.vesselName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      call.vessel.imoLloyds.toString().includes(searchTerm) ||
      call.port.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return 'success';
      case 'SCHEDULED':
        return 'primary';
      case 'COMPLETED':
        return 'default';
      default:
        return 'default';
    }
  };

  const formatDateTime = (dateString: string | undefined) => {
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

  return (
      <Box sx={{ flexGrow: 1 }}>
        <Typography variant="h4" gutterBottom component="div">
          Port Calls
        </Typography>

        {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
        )}

        {/* Search */}
        <Box sx={{ mb: 3 }}>
          <TextField
              fullWidth
              variant="outlined"
              placeholder="Search by vessel name, IMO number, or port"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                ),
                endAdornment: searchTerm && (
                    <InputAdornment position="end">
                      <IconButton onClick={() => setSearchTerm('')} edge="end">
                        &times;
                      </IconButton>
                    </InputAdornment>
                )
              }}
          />
        </Box>

        {/* Port Calls Table */}
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
          <TableContainer sx={{ maxHeight: 'calc(100vh - 300px)' }}>
            <Table stickyHeader aria-label="port calls table">
              <TableHead>
                <TableRow>
                  <TableCell>Vessel Name</TableCell>
                  <TableCell>IMO</TableCell>
                  <TableCell>Port</TableCell>
                  <TableCell>Berth</TableCell>
                  <TableCell>ETA</TableCell>
                  <TableCell>ATA</TableCell>
                  <TableCell>ETD</TableCell>
                  <TableCell>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredPortCalls
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((call: PortCall) => (
                        <TableRow hover key={call.portCallId}>
                          <TableCell>{call.vessel.vesselName}</TableCell>
                          <TableCell>{call.vessel.imoLloyds}</TableCell>
                          <TableCell>{call.port.name}</TableCell>
                          <TableCell>{call.berth.berthName}</TableCell>
                          <TableCell>{formatDateTime(call.eta)}</TableCell>
                          <TableCell>{formatDateTime(call.ata)}</TableCell>
                          <TableCell>{formatDateTime(call.etd)}</TableCell>
                          <TableCell>{'002202020'}</TableCell>
                          <TableCell>{formatDateTime(call.etd)}</TableCell>
                          <TableCell>
                            <Chip
                                label={call.portCallStatus}
                                color={getStatusColor(call.portCallStatus) as any}
                                size="small"
                            />
                          </TableCell>
                        </TableRow>
                    ))}
                {filteredPortCalls.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={8} align="center">
                        No port calls found
                      </TableCell>
                    </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              component="div"
              count={filteredPortCalls.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
      </Box>
  );
};

export default PortCalls;

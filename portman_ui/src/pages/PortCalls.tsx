import React, { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Chip,
  CircularProgress,
  IconButton,
  InputAdornment,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TablePagination,
  TableRow,
  TextField,
  Typography,
  Tooltip
} from '@mui/material';
import { Search as SearchIcon, Info as InfoIcon } from '@mui/icons-material';
import { PortCall } from '../types';
import api from "../services/api";

const PortCalls: React.FC = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [portCalls, setPortCalls] = useState<PortCall[]>([]);
  const [totalPortCalls, setTotalPortCalls] = useState<number>(0);
  const [nextPageUrl, setNextPageUrl] = useState<string | null>(null);
  const [loadingAllData, setLoadingAllData] = useState(false);

  // Initial data load
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.getPortCallsPaginated();
        const data = response?.data?.value || [];
        setPortCalls(data);
        setTotalPortCalls(data.length);
        
        // Store the next page URL if available
        if (response?.data?.nextLink) {
          setNextPageUrl(response.data.nextLink);
          // Automatically start loading all data
          loadAllData(response.data.nextLink, data);
        }
      } catch (err) {
        console.error('Error fetching port calls:', err);
        setError('Failed to load port calls. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Function to load all data recursively
  const loadAllData = async (url: string, currentData: PortCall[]) => {
    if (!url) return;
    
    setLoadingAllData(true);
    setLoadingMore(true);
    
    try {
      const urlObj = new URL(url);
      const params = new URLSearchParams(urlObj.search);
      const afterParam = params.get('$after');
      
      if (afterParam) {
        const response = await api.getPortCallsPaginated(afterParam);
        const newData = response?.data?.value || [];
        
        const combinedData = [...currentData, ...newData];
        setPortCalls(combinedData);
        setTotalPortCalls(combinedData.length);
        
        // If there's more data, continue loading
        if (response?.data?.nextLink) {
          // Short delay to prevent overloading the server
          setTimeout(() => {
            loadAllData(response.data.nextLink, combinedData);
          }, 300);
        } else {
          setNextPageUrl(null);
          setLoadingAllData(false);
          setLoadingMore(false);
        }
      }
    } catch (err) {
      console.error('Error loading more port calls:', err);
      setError('Failed to load all port calls. Some data might be missing.');
      setLoadingAllData(false);
      setLoadingMore(false);
    }
  };

  // Filter port calls based on search term
  const filteredPortCalls = (portCalls || []).filter((call: PortCall) =>
    call?.vesselname?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    call?.imolloyds?.toString().includes(searchTerm) ||
    call?.portareaname?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const formatDateTime = (dateString: string | null | undefined) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
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

  if (loading && portCalls.length === 0) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress data-cy="portcalls-loading" />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }} data-cy="portcalls-container">
      <Box sx={{ 
        display: 'flex', 
        flexDirection: { xs: 'column', md: 'row' },
        justifyContent: 'space-between',
        alignItems: { xs: 'stretch', md: 'center' },
        mb: 3,
        gap: 2
      }}>
        <Typography variant="h4" component="h1" data-cy="portcalls-title">
          Port Calls
        </Typography>
        <Box sx={{ width: { xs: '100%', md: 'auto' } }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Search vessels..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            size="small"
            data-cy="portcalls-search"
          />
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} data-cy="portcalls-error">
          {error}
        </Alert>
      )}

      {/* Statistics Summary */}
      <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 2, boxShadow: 1 }}>
        <Typography variant="h6" gutterBottom>Summary</Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography>
            Total Port Calls: <strong>{totalPortCalls}</strong>
            {loadingAllData && ' (loading more...)'}
          </Typography>
          {loadingAllData && <CircularProgress size={20} />}
        </Box>
      </Box>

      <Paper sx={{ 
        width: '100%', 
        overflow: 'hidden',
        borderRadius: 2,
        boxShadow: 2,
        mb: 3
      }} data-cy="portcalls-table-container">
        <Box sx={{ overflowX: 'auto' }}>
          <Table data-cy="portcalls-table">
            <TableHead>
              <TableRow sx={{ bgcolor: 'primary.main' }}>
                <TableCell sx={{ fontWeight: 'bold', color: 'white' }} data-cy="table-header-vessel">Vessel</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', width: 110 }} data-cy="table-header-status">Status</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white' }} data-cy="table-header-port">Port</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-eta">ETA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-ata">ATA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-etd">ETD</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', width: 100, textAlign: 'center' }} data-cy="table-header-actions">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody data-cy="portcalls-table-body">
              {filteredPortCalls
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((call: PortCall) => (
                  <TableRow 
                    hover 
                    key={call?.portcallid}
                    sx={{ 
                      '&:nth-of-type(odd)': { backgroundColor: 'rgba(0, 0, 0, 0.03)' },
                      transition: 'all 0.2s ease-in-out',
                      '&:hover': { backgroundColor: 'rgba(0, 0, 0, 0.06)' }
                    }}
                    data-cy={`portcall-row-${call?.portcallid}`}
                  >
                    <TableCell>
                      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                        <Typography variant="body1" sx={{ fontWeight: 500 }} data-cy="vessel-name">
                          {call?.vesselname || 'N/A'}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" data-cy="vessel-imo">
                          IMO: {call?.imolloyds || 'N/A'}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                          label={call?.ata ? 'Arrived' : 'Expected'}
                          color={call?.ata ? 'success' : 'primary'}
                          size="small"
                          data-cy="status-chip"
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                        <Typography variant="body1" data-cy="port-area">
                          {call?.portareaname || 'N/A'}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" data-cy="berth-name">
                          {call?.berthname || 'N/A'}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell sx={{ display: { xs: 'none', md: 'table-cell' } }} data-cy="eta-value">
                      {formatDateTime(call?.eta)}
                    </TableCell>
                    <TableCell sx={{ display: { xs: 'none', md: 'table-cell' } }} data-cy="ata-value">
                      {call?.ata ? formatDateTime(call.ata) : '-'}
                    </TableCell>
                    <TableCell sx={{ display: { xs: 'none', md: 'table-cell' } }} data-cy="etd-value">
                      {formatDateTime(call?.etd)}
                    </TableCell>
                    <TableCell sx={{ textAlign: 'center' }}>
                      <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center' }}>
                        <Tooltip title="View Details">
                          <IconButton 
                            color="info" 
                            size="small"
                            onClick={() => window.location.href = `/port-call/${call?.portcallid}`}
                          >
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              {filteredPortCalls.length === 0 && (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    No port calls found
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </Box>
        {loadingMore && (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
            <CircularProgress size={24} />
          </Box>
        )}
        <TablePagination
          component="div"
          count={filteredPortCalls.length}
          page={page}
          onPageChange={handleChangePage}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          rowsPerPageOptions={[5, 10, 25, 50, 100, 150, 200, 300, 500]}
        />
      </Paper>
    </Box>
  );
};

export default PortCalls;

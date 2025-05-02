import React, {useEffect, useState} from 'react';
import {
  Alert,
  Box,
  Button,
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
  Tooltip,
  Typography,
  Chip
} from '@mui/material';
import {
  Search as SearchIcon, 
  Visibility as VisibilityIcon, 
  Info as InfoIcon,
  ExpandMore as ExpandMoreIcon
} from '@mui/icons-material';
import {Arrival} from '../types';
import api from "../services/api";

const Arrivals: React.FC = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [arrivals, setArrivals] = useState<Arrival[]>([]);
  const [totalArrivals, setTotalArrivals] = useState<number>(0);
  const [nextPageUrl, setNextPageUrl] = useState<string | null>(null);
  const [loadingAllData, setLoadingAllData] = useState(false);

  // Initial data load
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.getArrivals();
        const data = response?.data?.value || [];
        setArrivals(data);
        setTotalArrivals(data.length);
        
        // Store the next page URL if available
        if (response?.data?.nextLink) {
          setNextPageUrl(response.data.nextLink);
          // Automatically start loading all data
          loadAllData(response.data.nextLink, data);
        }
      } catch (err) {
        console.error('Error fetching arrivals:', err);
        setError('Failed to load arrivals. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Function to load all data recursively
  const loadAllData = async (url: string, currentData: Arrival[]) => {
    if (!url) return;
    
    setLoadingAllData(true);
    setLoadingMore(true);
    
    try {
      const urlObj = new URL(url);
      const params = new URLSearchParams(urlObj.search);
      const afterParam = params.get('$after');
      
      if (afterParam) {
        const response = await api.getArrivals(afterParam);
        const newData = response?.data?.value || [];
        
        const combinedData = [...currentData, ...newData];
        setArrivals(combinedData);
        setTotalArrivals(combinedData.length);
        
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
      console.error('Error loading more arrivals:', err);
      setError('Failed to load all arrivals. Some data might be missing.');
      setLoadingAllData(false);
      setLoadingMore(false);
    }
  };

  // Filter arrivals based on search term
  const filteredArrivals = (arrivals || []).filter((arrival: Arrival) =>
    arrival?.vesselname?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    arrival?.portcallid?.toString().includes(searchTerm) ||
    arrival?.portareaname?.toLowerCase().includes(searchTerm.toLowerCase())
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

  const handleViewXML = (url: string) => {
    window.open(url, '_blank');
  };

  if (loading && arrivals.length === 0) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress data-cy="arrivals-loading" />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }} data-cy="arrivals-container">
      <Box sx={{ 
        display: 'flex', 
        flexDirection: { xs: 'column', md: 'row' },
        justifyContent: 'space-between',
        alignItems: { xs: 'stretch', md: 'center' },
        mb: 3,
        gap: 2
      }}>
        <Typography variant="h4" component="h1" data-cy="arrivals-title">
          Arrivals
        </Typography>
        <Box sx={{ width: { xs: '100%', md: 'auto' } }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Search arrivals..."
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
            data-cy="arrivals-search"
          />
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} data-cy="arrivals-error">
          {error}
        </Alert>
      )}

      {/* Statistics Summary */}
      <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 2, boxShadow: 1 }}>
        <Typography variant="h6" gutterBottom>Summary</Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography>
            Total Arrivals: <strong>{totalArrivals}</strong>
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
      }} data-cy="arrivals-table-container">
        <Box sx={{ overflowX: 'auto' }}>
          <Table data-cy="arrivals-table">
            <TableHead>
              <TableRow sx={{ bgcolor: 'primary.main' }}>
                <TableCell sx={{ fontWeight: 'bold', color: 'white' }} data-cy="table-header-vessel">Vessel</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', width: 110 }} data-cy="table-header-status">Status</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white' }} data-cy="table-header-port">Port</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-eta">ETA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-old-ata">Previous ATA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white' }} data-cy="table-header-ata">ATA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-timestamp">Timestamp</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', width: 100, textAlign: 'center' }} data-cy="table-header-actions">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody data-cy="arrivals-table-body">
              {filteredArrivals
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((arrival: Arrival) => (
                  <TableRow 
                    hover 
                    key={arrival.id}
                    sx={{ 
                      '&:nth-of-type(odd)': { backgroundColor: 'rgba(0, 0, 0, 0.03)' },
                      transition: 'all 0.2s ease-in-out',
                      '&:hover': { backgroundColor: 'rgba(0, 0, 0, 0.06)' }
                    }}
                    data-cy={`arrival-row-${arrival.id}`}
                  >
                    <TableCell>
                      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                        <Typography variant="body1" sx={{ fontWeight: 500 }} data-cy="vessel-name">
                          {arrival.vesselname || 'N/A'}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" data-cy="vessel-port-call-id">
                          ID: {arrival.portcallid || 'N/A'}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={arrival.old_ata ? "Updated" : "New Arrival"}
                        color={arrival.old_ata ? "warning" : "success"}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                        <Typography variant="body1" data-cy="port-area">
                          {arrival.portareaname || 'N/A'}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" data-cy="berth-name">
                          {arrival.berthname || 'N/A'}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell sx={{ display: { xs: 'none', md: 'table-cell' } }} data-cy="eta-value">
                      {formatDateTime(arrival.eta)}
                    </TableCell>
                    <TableCell sx={{ display: { xs: 'none', md: 'table-cell' } }} data-cy="old-ata-value">
                      {arrival.old_ata ? formatDateTime(arrival.old_ata) : '-'}
                    </TableCell>
                    <TableCell data-cy="ata-value">
                      {formatDateTime(arrival.ata)}
                    </TableCell>
                    <TableCell sx={{ display: { xs: 'none', md: 'table-cell' } }} data-cy="timestamp-value">
                      {formatDateTime(arrival.created)}
                    </TableCell>
                    <TableCell sx={{ textAlign: 'center' }}>
                      <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center' }}>
                        {arrival.ata_xml_url && (
                          <Tooltip title="View ATA XML">
                            <IconButton 
                              color="primary" 
                              size="small"
                              onClick={() => handleViewXML(arrival.ata_xml_url || '')}
                            >
                              <VisibilityIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )}
                        <Tooltip title="Vessel Details">
                          <IconButton 
                            color="info" 
                            size="small"
                            onClick={() => window.location.href = `/vessel/${arrival.portcallid}`}
                          >
                            <InfoIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              {filteredArrivals.length === 0 && (
                <TableRow>
                  <TableCell colSpan={8} align="center">
                    No arrivals found
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
          count={filteredArrivals.length}
          page={page}
          onPageChange={handleChangePage}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          rowsPerPageOptions={[5, 10, 25, 50, 100]}
        />
      </Paper>
    </Box>
  );
};

export default Arrivals; 
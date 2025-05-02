import React, {useEffect, useState} from 'react';
import {
  Alert,
  Box,
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
  Info as InfoIcon
} from '@mui/icons-material';
import {Arrival} from '../types';
import api from "../services/api";

const Arrivals: React.FC = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [arrivals, setArrivals] = useState<Arrival[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.getArrivalUpdates();
        setArrivals(response || []);
      } catch (err) {
        console.error('Error fetching arrivals:', err);
        setError('Failed to load arrivals. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

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

  if (loading) {
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

      {/* TODO: Add later maybe? */}
      {/* Statistics Summary */}
      {/*<Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 2, boxShadow: 1 }}>*/}
      {/*  <Typography variant="h6" gutterBottom>Summary</Typography>*/}
      {/*  <Typography>*/}
      {/*    Total Arrivals: <strong>{arrivals.length}</strong>*/}
      {/*  </Typography>*/}
      {/*</Box>*/}

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
                <TableCell sx={{ fontWeight: 'bold', color: 'white' }} data-cy="table-header-port">Port</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-eta">ETA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-old-ata">Previous ATA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white' }} data-cy="table-header-ata">ATA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-timestamp">Timestamp</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'white' }} data-cy="table-header-actions">Actions</TableCell>
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
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Typography variant="body1" sx={{ fontWeight: 500 }} data-cy="vessel-name">
                            {arrival.vesselname || 'N/A'}
                          </Typography>
                          <Chip 
                            label={arrival.old_ata ? "Updated" : "New Arrival"}
                            color={arrival.old_ata ? "warning" : "success"}
                            size="small"
                            sx={{ ml: 1 }}
                          />
                        </Box>
                        <Typography variant="body2" color="text.secondary" data-cy="vessel-port-call-id">
                          ID: {arrival.portcallid || 'N/A'}
                        </Typography>
                      </Box>
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
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 1 }}>
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
                  <TableCell colSpan={7} align="center">
                    No arrivals found
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </Box>
        <TablePagination
          component="div"
          count={filteredArrivals.length}
          page={page}
          onPageChange={handleChangePage}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          rowsPerPageOptions={[5, 10, 25]}
        />
      </Paper>
    </Box>
  );
};

export default Arrivals; 
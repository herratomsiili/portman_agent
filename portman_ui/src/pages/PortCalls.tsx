import React, { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Chip,
  CircularProgress,
  InputAdornment,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TextField,
  Typography,
  Collapse,
  Grid2,
  IconButton
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { PortCall } from '../types';
import api from "../services/api";
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';

import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';


const PortCalls: React.FC = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [portCalls, setPortCalls] = useState<PortCall[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.getPortCalls();
        setPortCalls(response || []);
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

  interface GridItemProps {
    title: string;
    value: any;
  }

  const GridItem: React.FC<GridItemProps> = ({ title, value }) => {
    return (
      <Box sx={{ width: "20%", paddingLeft: "3px" }}>
        <Typography variant="body1" sx={{
          textDecoration: "underline",
          textDecorationColor: '9e9e9e',
          textDecorationStyle: 'dotted',
        }}>
          {title}
        </Typography>
        <Typography variant="body2">
          {value}
        </Typography>
      </Box>
    );
  }


  interface RowProps {
    call: PortCall;
  }

  const Row: React.FC<RowProps> = ({ call }) => {
    const [open, setOpen] = useState(false);

    return (
      <React.Fragment>
        <TableRow
          hover
          key={call?.portcallid}
          sx={{ '&:hover .action-buttons': { opacity: 1 } }}
          data-cy={`portcall-row-${call?.portcallid}`}
        >
          <TableCell>
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
              <IconButton
                aria-label="expand row"
                size="small"
                onClick={() => setOpen(!open)}
              >
                {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
              </IconButton>
            </Box>
          </TableCell>

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
          <TableCell>
            <Chip
              label={call?.ata ? 'Arrived' : 'Expected'}
              color={call?.ata ? 'success' : 'primary'}
              size="small"
              data-cy="status-chip"
            />
          </TableCell>
        </TableRow>

        <TableRow sx={{ backgroundColor: "#eeeeee" }}>
          <TableCell style={{ padding: 0 }} colSpan={8} >
            <Collapse in={open} timeout="auto" unmountOnExit>
              <Box sx={{ paddingLeft: '50px', display: 'flex', flexDirection: 'column' }}>
                <Grid2 container spacing={0} sx={{
                  '--Grid-borderWidth': '1px',
                  borderColor: 'divider',
                  '& > div': {
                    borderLeft: 'var(--Grid-borderWidth) solid',
                    borderColor: 'grey',
                  },
                  paddingLeft: "1px",
                  justifyContent: "flex-start"
                }}>
                  <GridItem title="Port Call ID" value={call.portcallid} />
                  <GridItem title="Vessel Type Code" value={call.vesseltypecode} />

                  <GridItem title="Port to Visit" value={call.porttovisit} />
                  <GridItem title="Berth Code" value={call.berthcode} />
                  <GridItem title="Previous Port" value={call.prevport} />
                  <GridItem title="Next Port" value={call.nextport} />

                  <GridItem title="ATD" value={formatDateTime(call.atd)} />

                  <GridItem title="Crew on Arrival" value={call.crewonarrival} />
                  <GridItem title="Crew on Departure" value={call.crewondeparture} />
                  <GridItem title="Passengers on Arrival" value={call.passengersonarrival} />
                  <GridItem title="Passengers on Departure" value={call.passengersondeparture} />

                  <GridItem title="Agent Name" value={call.agentname} />
                  <GridItem title="Shipping Company" value={call.shippingcompany} />

                  <GridItem title="Created" value={formatDateTime(call.created)} />
                  <GridItem title="Modified" value={formatDateTime(call.modified)} />
                </Grid2>
              </Box>
            </Collapse>
          </TableCell>
        </TableRow>
      </React.Fragment>
    );
  }

  if (loading) {
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

      <Paper sx={{
        width: '100%',
        overflow: 'hidden',
        borderRadius: 2,
        boxShadow: 2
      }} data-cy="portcalls-table-container">
        <Box sx={{ overflowX: 'auto' }}>
          <Table data-cy="portcalls-table" sx={{ tableLayout: 'fixed' }}>
            <TableHead>
              <TableRow>
                <TableCell width="50px" />
                <TableCell sx={{ fontWeight: 'bold', width: '20%' }} data-cy="table-header-vessel">Vessel</TableCell>
                <TableCell sx={{ fontWeight: 'bold', width: '20%' }} data-cy="table-header-port">Port</TableCell>
                <TableCell sx={{ fontWeight: 'bold', width: '15%', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-eta">ETA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', width: '15%', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-ata">ATA</TableCell>
                <TableCell sx={{ fontWeight: 'bold', width: '15%', display: { xs: 'none', md: 'table-cell' } }} data-cy="table-header-etd">ETD</TableCell>
                <TableCell sx={{ fontWeight: 'bold', width: '15%' }} data-cy="table-header-status">Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody data-cy="portcalls-table-body">
              {filteredPortCalls
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((call: PortCall) => (
                  <Row call={call} />
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
        </Box>
        <TablePagination
          component="div"
          count={filteredPortCalls.length}
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

export default PortCalls;

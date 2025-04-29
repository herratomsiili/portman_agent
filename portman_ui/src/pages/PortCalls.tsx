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
  IconButton,
  Collapse,
  Grid2
} from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { Search as SearchIcon } from '@mui/icons-material';
import { api } from '../services/api';
import { mockPortCalls } from '../data/mockData';
import { PortCall2 } from '../types';
import axios from 'axios';

const PortCalls: React.FC = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [portCalls, setPortCalls] = useState<PortCall2[]>([]);
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      // TODO: Fetch data from API
      // TODO: Parse api data if necessary
      // TODO: set fetched data to portCalls state
      try {
        // In a production environment, this would be an actual API call
        // For now, we'll use our mock data with a simulated delay

        // Simulate API call delay
        // await new Promise(resolve => setTimeout(resolve, 1000));

        // Use mock data
        // setPortCalls(mockPortCalls);

        // In a real implementation, we would use:
        const response = await api.getPortCalls();
        setPortCalls(response);
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
    call.vesselname.toLowerCase().includes(searchTerm.toLowerCase()) ||
    call.imolloyds.toString().includes(searchTerm) ||
    call.portareacode.toLowerCase().includes(searchTerm.toLowerCase())
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

  if (loading) {
    return (
      <>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress />
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress />
        </Box>
      </>
    );
  }

  function createPortCallData(
    agentname: string,
    ata: string,
    atd: string,
    berthcode: string,
    berthname: string,
    created: string,
    crewonarrival: string,
    crewondeparture: number,
    eta: string,
    etd: string,
    imolloyds: number,
    modified: string,
    nextport: string,
    passengersonarrival: number,
    passengersondeparture: number,
    portareacode: string,
    portareaname: string,
    portcallid: number,
    porttovisit: string,
    prevport: number,
    shippingcompany: string,
    vesselname: string,
    vesseltypecode: string,
  ) {
    return {
      agentname,
      ata,
      atd,
      berthcode,
      berthname,
      created,
      crewonarrival,
      crewondeparture,
      eta,
      etd,
      imolloyds,
      modified,
      nextport,
      passengersonarrival,
      passengersondeparture,
      portareacode,
      portareaname,
      portcallid,
      porttovisit,
      prevport,
      shippingcompany,
      vesselname,
      vesseltypecode,
    };
  }

  function Row(props: { row: ReturnType<typeof createPortCallData> }) {
    const { row } = props;
    const [open, setOpen] = useState(false);

    return (
      <React.Fragment>
        <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
          <TableCell>
            <IconButton
              aria-label="expand row"
              size="small"
              onClick={() => setOpen(!open)}
            >
              {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
            </IconButton>
          </TableCell>
          <TableCell align="left" component="th" scope="row">
            {row.vesselname}
          </TableCell>
          <TableCell align="center">{row.imolloyds}</TableCell>
          <TableCell align="center">{row.portareaname}</TableCell>
          <TableCell align="right">
            <Chip
              //label={row.portCallStatus}
              //color={getStatusColor(call.portCallStatus) as any}
              label="TBD"
              size="small"
            />
          </TableCell>
        </TableRow>
        <TableRow sx={{ backgroundColor: "#eeeeee" }}>
          <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={5} >
            <Collapse in={open} timeout="auto" unmountOnExit>
              <Box sx={{ margin: 1 }}>
                <Grid2 container spacing={1} sx={{
                  '--Grid-borderWidth': '1px',
                  borderColor: 'divider',
                  '& > div': {
                    borderLeft: 'var(--Grid-borderWidth) solid',
                    borderColor: 'grey',
                  },
                  //mb: 4,
                  paddingLeft: "50px",
                  justifyContent: "flex-start"
                }}>
                  <GridItem title="Port Call ID" value={row.portcallid} />

                  <GridItem title="ETA" value={formatDateTime(row.eta)} />
                  <GridItem title="ATA" value={formatDateTime(row.ata)} />
                  <GridItem title="ETD" value={formatDateTime(row.etd)} />
                  <GridItem title="ATD" value={formatDateTime(row.atd)} />

                  <GridItem title="Agent Name" value={row.agentname} />
                  <GridItem title="Shipping Company" value={row.shippingcompany} />

                  <GridItem title="Created" value={formatDateTime(row.created)} />
                  <GridItem title="Modified" value={formatDateTime(row.modified)} />

                  <GridItem title="Berth Name" value={row.berthname} />
                  <GridItem title="Berth Code" value={row.berthcode} />

                  <GridItem title="Port to Visit" value={row.porttovisit} />
                  <GridItem title="Previous Port" value={row.prevport} />
                  <GridItem title="Next Port" value={row.nextport} />

                  <GridItem title="Vessel Type Code" value={row.vesseltypecode} />

                  <GridItem title="Crew on Arrival" value={row.crewonarrival} />
                  <GridItem title="Crew on Departure" value={row.crewondeparture} />

                  <GridItem title="Passengers on Arrival" value={row.passengersonarrival} />
                  <GridItem title="Passengers on Departure" value={row.passengersondeparture} />
                </Grid2>
              </Box>
            </Collapse>
          </TableCell>
        </TableRow>
      </React.Fragment>
    );
  }

  interface GridItemProps {
    title: string;
    value: string | number;
  }

  const GridItem: React.FC<GridItemProps> = ({ title, value }) => {
    return (
      <Box sx={{ width: "23%", paddingLeft: "3px" }}>
        <Typography sx={{
          textDecoration: "underline",
          textDecorationColor: '9e9e9e',
          textDecorationStyle: 'dotted',
        }}>
          {title}
        </Typography>
        <Typography>
          {value}
        </Typography>
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
        <TableContainer component={Paper}>
          <Table aria-label="collapsible table" >
            <TableHead>
              <TableRow>
                <TableCell />
                <TableCell align="left"> Vessel Name </ TableCell >
                <TableCell align="center" > IMO </ TableCell >
                <TableCell align="center" > Port Name </ TableCell >
                <TableCell align="right" > Status </ TableCell >
              </ TableRow >
            </ TableHead >
            < TableBody >
              {
                filteredPortCalls
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row, index) => (
                    < Row key={index}
                      row={row} />
                  ))}
            </ TableBody >
          </ Table >
        </ TableContainer >
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
    </Box >

  );
};

export default PortCalls;
import React from 'react';
import {
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import { mockPortCalls } from '../data/mockData';

// Register ChartJS components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement
);

const Reports: React.FC = () => {
  const [timeRange, setTimeRange] = React.useState('week');

  const handleTimeRangeChange = (event: SelectChangeEvent) => {
    setTimeRange(event.target.value);
  };

  // Calculate port statistics
  const portStats = mockPortCalls.reduce((acc, call) => {
    const portName = call.port.name;
    if (!acc[portName]) {
      acc[portName] = 0;
    }
    acc[portName]++;
    return acc;
  }, {} as Record<string, number>);

  // Calculate vessel type statistics
  const vesselTypeStats = mockPortCalls.reduce((acc, call) => {
    const vesselType = call.vessel.vesselTypeCode;
    if (!acc[vesselType]) {
      acc[vesselType] = 0;
    }
    acc[vesselType]++;
    return acc;
  }, {} as Record<string, number>);

  // Calculate passenger statistics
  const passengerStats = mockPortCalls.reduce((acc, call) => {
    if (call.passengerCount && call.passengerCount > 0) {
      const portName = call.port.name;
      if (!acc[portName]) {
        acc[portName] = 0;
      }
      acc[portName] += call.passengerCount;
    }
    return acc;
  }, {} as Record<string, number>);

  // Prepare data for port calls by port chart
  const portCallsData = {
    labels: Object.keys(portStats),
    datasets: [
      {
        label: 'Number of Port Calls',
        data: Object.values(portStats),
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Prepare data for vessel types chart
  const vesselTypesData = {
    labels: Object.keys(vesselTypeStats),
    datasets: [
      {
        label: 'Vessel Types',
        data: Object.values(vesselTypeStats),
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  // Prepare data for passenger statistics chart
  const passengerData = {
    labels: Object.keys(passengerStats),
    datasets: [
      {
        label: 'Number of Passengers',
        data: Object.values(passengerStats),
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        tension: 0.1
      },
    ],
  };

  // Chart options
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Port Call Statistics',
      },
    },
  };

  return (
      <Box sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="div">
            Reports & Analytics
          </Typography>

          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel id="time-range-label">Time Range</InputLabel>
            <Select
                labelId="time-range-label"
                id="time-range-select"
                value={timeRange}
                label="Time Range"
                onChange={handleTimeRangeChange}
            >
              <MenuItem value="day">Last 24 Hours</MenuItem>
              <MenuItem value="week">Last Week</MenuItem>
              <MenuItem value="month">Last Month</MenuItem>
              <MenuItem value="year">Last Year</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Grid container spacing={3}>
          {/* Port Calls by Port */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2, height: 400 }}>
              <Typography variant="h6" gutterBottom>
                Port Calls by Port
              </Typography>
              <Box sx={{ height: 320 }}>
                <Bar options={chartOptions} data={portCallsData} />
              </Box>
            </Paper>
          </Grid>

          {/* Vessel Types Distribution */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2, height: 400 }}>
              <Typography variant="h6" gutterBottom>
                Vessel Types Distribution
              </Typography>
              <Box sx={{ height: 320, display: 'flex', justifyContent: 'center' }}>
                <Pie
                    data={vesselTypesData}
                    options={{
                      ...chartOptions,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          ...chartOptions.plugins.title,
                          text: 'Vessel Types Distribution',
                        },
                      },
                    }}
                />
              </Box>
            </Paper>
          </Grid>

          {/* Passenger Statistics */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2, height: 400 }}>
              <Typography variant="h6" gutterBottom>
                Passenger Statistics by Port
              </Typography>
              <Box sx={{ height: 320 }}>
                <Line
                    options={{
                      ...chartOptions,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          ...chartOptions.plugins.title,
                          text: 'Passenger Statistics by Port',
                        },
                      },
                    }}
                    data={passengerData}
                />
              </Box>
            </Paper>
          </Grid>

          {/* Summary Cards */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Summary Statistics
                </Typography>
                <Grid container spacing={3}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="subtitle1" color="text.secondary">
                        Total Port Calls
                      </Typography>
                      <Typography variant="h4">
                        {mockPortCalls.length}
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="subtitle1" color="text.secondary">
                        Total Passengers
                      </Typography>
                      <Typography variant="h4">
                        {mockPortCalls.reduce((sum, call) => sum + (call.passengerCount || 0), 0)}
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="subtitle1" color="text.secondary">
                        Total Crew
                      </Typography>
                      <Typography variant="h4">
                        {mockPortCalls.reduce((sum, call) => sum + (call.crewCount || 0), 0)}
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="subtitle1" color="text.secondary">
                        Unique Vessels
                      </Typography>
                      <Typography variant="h4">
                        {new Set(mockPortCalls.map(call => call.vessel.imoLloyds)).size}
                      </Typography>
                    </Paper>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
  );
};

export default Reports;

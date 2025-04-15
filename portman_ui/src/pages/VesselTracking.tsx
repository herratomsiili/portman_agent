import React, {useEffect, useRef, useState} from 'react';
import {
  Alert,
  Box,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  Typography
} from '@mui/material';
import api from '../services/api';
import {AISFeature, PortCall} from '../types';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import {MapContainer, Marker, Popup, TileLayer} from "react-leaflet";

// Fix Leaflet marker icons
const icon = L.icon({
  iconUrl: '/images/marker-icon.png',
  iconRetinaUrl: '/images/marker-icon-2x.png',
  shadowUrl: '/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = icon;

const VesselTracking: React.FC = () => {
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterPort, setFilterPort] = useState('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [portCalls, setPortCalls] = useState<PortCall[]>([]);
  const [vesselLocations, setVesselLocations] = useState<AISFeature[]>([]);
  const mapRef = useRef<L.Map | null>(null);
  const markersRef = useRef<{[key: string]: L.Marker}>({});

  // Initialize map
  useEffect(() => {
    const initMap = () => {
      const mapElement = document.getElementById('map');
      console.log('Map element:', mapElement);
      
      if (mapElement && !mapRef.current) {
        try {
          mapRef.current = L.map(mapElement).setView([60.1699, 24.9384], 7);
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
          }).addTo(mapRef.current);
          console.log('Map initialized successfully');
        } catch (err) {
          console.error('Error initializing map:', err);
        }
      }
    };

    // Try to initialize map immediately
    initMap();

    // If map element is not found, try again after a short delay
    if (!document.getElementById('map')) {
      const timer = setTimeout(initMap, 1000);
      return () => clearTimeout(timer);
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [portCallsResponse, locationsResponse] = await Promise.all([
          api.getPortCalls(),
          api.getVesselLocations()
        ]);

        setPortCalls(portCallsResponse);
        setVesselLocations(locationsResponse.features);

        // Update markers on the map
        if (mapRef.current) {
          // Clear old markers
          Object.values(markersRef.current).forEach(marker => marker.remove());
          markersRef.current = {};

          // Add new markers
          locationsResponse.features.forEach(feature => {
            const [lng, lat] = feature.geometry.coordinates;
            const marker = L.marker([lat, lng], {
              title: `MMSI: ${feature.mmsi}\nSOG: ${feature.properties.sog} knots\nCOG: ${feature.properties.cog}°`
            }).addTo(mapRef.current!);
            
            markersRef.current[feature.mmsi] = marker;
          });
        }
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Set up polling for vessel locations
    const intervalId = setInterval(async () => {
      try {
        const locationsResponse = await api.getVesselLocations();
        setVesselLocations(locationsResponse.features);

        // Update marker positions
        if (mapRef.current) {
          locationsResponse.features.forEach(feature => {
            const [lng, lat] = feature.geometry.coordinates;
            if (markersRef.current[feature.mmsi]) {
              markersRef.current[feature.mmsi].setLatLng([lat, lng]);
            } else {
              markersRef.current[feature.mmsi] = L.marker([lat, lng], {
                title: `MMSI: ${feature.mmsi}\nSOG: ${feature.properties.sog} knots\nCOG: ${feature.properties.cog}°`
              }).addTo(mapRef.current!);
            }
          });
        }
      } catch (err) {
        console.error('Error updating vessel locations:', err);
      }
    }, 60000); // Update every minute

    return () => clearInterval(intervalId);
  }, []);

  const handleStatusChange = (event: SelectChangeEvent) => {
    setFilterStatus(event.target.value);
  };

  const handlePortChange = (event: SelectChangeEvent) => {
    setFilterPort(event.target.value);
  };

  // Get unique ports for filter
  const uniquePorts = Array.from(new Set(portCalls.map(call => call.portareaname)));

  // Filter vessels based on selected filters
  const filteredVessels = portCalls.filter(call => {
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

  const position: [number, number] = [51.505, -0.09]; // Default position for the map

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom component="div">
        Vessel Tracking
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

      {/* Map */}
      {/*<Paper*/}
      {/*  id="map"*/}
      {/*  sx={{*/}
      {/*    height: 500,*/}
      {/*    width: '100%',*/}
      {/*    mb: 3,*/}
      {/*    '& .leaflet-container': {*/}
      {/*      height: '100%',*/}
      {/*      width: '100%'*/}
      {/*    }*/}
      {/*  }}*/}
      {/*/>*/}

      <MapContainer
          center={position}
          zoom={13}
          scrollWheelZoom={true}
          style={{ minHeight: '100vh', minWidth: '100vw' }}
      >
        <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
      </MapContainer>


      {/* Vessel List */}
      <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
        Tracked Vessels ({vesselLocations.length} active)
      </Typography>

      <Grid container spacing={2}>
        {vesselLocations.map(vessel => (
          <Grid item xs={12} sm={6} md={4} key={vessel.mmsi}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Typography variant="h6" component="div">
                    MMSI: {vessel.mmsi}
                  </Typography>
                  <Chip
                    label={`SOG: ${vessel.properties.sog} knots`}
                    color="primary"
                    size="small"
                  />
                </Box>
                <Typography color="text.secondary" gutterBottom>
                  Position: {vessel.geometry.coordinates[1].toFixed(6)}, {vessel.geometry.coordinates[0].toFixed(6)}
                </Typography>
                <Typography variant="body2">
                  Course: {vessel.properties.cog}°
                </Typography>
                <Typography variant="body2">
                  Heading: {vessel.properties.heading}°
                </Typography>
                <Typography variant="body2">
                  Last Update: {new Date(vessel.properties.timestampExternal).toLocaleString()}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default VesselTracking;

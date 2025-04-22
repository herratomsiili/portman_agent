import React from 'react';
import { Grid, Paper, Typography } from '@mui/material';

interface SummaryCardsProps {
  trackedVesselsCount: number;
  activeVesselsCount: number;
  scheduledVesselsCount: number;
  totalPassengers: number;
}

const SummaryCards: React.FC<SummaryCardsProps> = ({
  trackedVesselsCount,
  activeVesselsCount,
  scheduledVesselsCount,
  totalPassengers
}) => {
  return (
    <Grid container spacing={3} sx={{ mb: 4 }} data-cy="summary-cards">
      <Grid item xs={12} sm={6} md={3} data-cy="card-tracked-vessels">
        <Paper elevation={3} sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="h6" color="primary">Tracked Vessels</Typography>
          <Typography variant="h3">{trackedVesselsCount}</Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} sm={6} md={3} data-cy="card-active-calls">
        <Paper elevation={3} sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="h6" color="primary">Active Port Calls</Typography>
          <Typography variant="h3">{activeVesselsCount}</Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} sm={6} md={3} data-cy="card-scheduled-arrivals">
        <Paper elevation={3} sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="h6" color="primary">Scheduled Arrivals</Typography>
          <Typography variant="h3">{scheduledVesselsCount}</Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} sm={6} md={3} data-cy="card-passengers">
        <Paper elevation={3} sx={{ p: 2, textAlign: 'center' }}>
          <Typography variant="h6" color="primary">Total Passengers</Typography>
          <Typography variant="h3">{totalPassengers}</Typography>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default SummaryCards; 
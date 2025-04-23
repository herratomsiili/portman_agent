import React from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';
import { PortCall } from '../../types';

interface UpcomingArrivalsProps {
  arrivals: PortCall[];
}

const UpcomingArrivals: React.FC<UpcomingArrivalsProps> = ({ arrivals }) => {
  return (
    <Card elevation={3} data-cy="upcoming-arrivals-card">
      <CardContent>
        <Typography variant="h6" gutterBottom data-cy="upcoming-arrivals-title">
          Upcoming Arrivals
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <List data-cy="upcoming-arrivals-list">
          {arrivals.map((call) => (
            <React.Fragment key={call.portcallid}>
              <ListItem data-cy={`arrival-item-${call.portcallid}`}>
                <ListItemText
                  primary={call.vesselname}
                  secondary={
                    <>
                      <Typography component="span" variant="body2" color="text.primary">
                        {call.portareaname} - {call.berthname}
                      </Typography>
                      {` — ETA: ${new Date(call.eta).toLocaleString()}`}
                    </>
                  }
                />
              </ListItem>
              <Divider />
            </React.Fragment>
          ))}
          {arrivals.length === 0 && (
            <ListItem data-cy="no-upcoming-arrivals">
              <ListItemText primary="No upcoming arrivals" />
            </ListItem>
          )}
        </List>
      </CardContent>
    </Card>
  );
};

export default UpcomingArrivals; 
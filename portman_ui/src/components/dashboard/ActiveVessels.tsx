import React from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, Divider, TablePagination } from '@mui/material';
import { PortCall } from '../../types';

interface ActiveVesselsProps {
  vessels: PortCall[];
  page: number;
  rowsPerPage: number;
  onPageChange: (event: unknown, newPage: number) => void;
  onRowsPerPageChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const ActiveVessels: React.FC<ActiveVesselsProps> = ({
  vessels,
  page,
  rowsPerPage,
  onPageChange,
  onRowsPerPageChange
}) => {
  return (
    <Card elevation={3} data-cy="active-vessels-card">
      <CardContent>
        <Typography variant="h6" gutterBottom data-cy="active-vessels-title">
          Active Vessels
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <List data-cy="active-vessels-list">
          {vessels.map((call) => (
            <React.Fragment key={call.portcallid}>
              <ListItem data-cy={`vessel-item-${call.portcallid}`}>
                <ListItemText
                  primary={call.vesselname}
                  secondary={
                    <>
                      <Typography component="span" variant="body2" color="text.primary">
                        {call.portareaname} - {call.berthname}
                      </Typography>
                      {` — ATA: ${call.ata ? new Date(call.ata).toLocaleString() : 'N/A'}`}
                    </>
                  }
                />
              </ListItem>
              <Divider />
            </React.Fragment>
          ))}
          {vessels.length === 0 && (
            <ListItem data-cy="no-active-vessels">
              <ListItemText primary="No active vessels" />
            </ListItem>
          )}
        </List>
        <TablePagination
          component="div"
          count={vessels.length}
          page={page}
          onPageChange={onPageChange}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={onRowsPerPageChange}
          rowsPerPageOptions={[5, 10, 25]}
          data-cy="table-pagination-for-active-vessels"
        />
      </CardContent>
    </Card>
  );
};

export default ActiveVessels; 
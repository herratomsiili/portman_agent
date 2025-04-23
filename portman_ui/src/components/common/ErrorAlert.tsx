import React from 'react';
import { Alert } from '@mui/material';

interface ErrorAlertProps {
  message: string;
}

const ErrorAlert: React.FC<ErrorAlertProps> = ({ message }) => {
  return (
    <Alert severity="error" sx={{ mb: 3 }} data-cy="error-alert">
      {message}
    </Alert>
  );
};

export default ErrorAlert; 
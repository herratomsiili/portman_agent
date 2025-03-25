import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Avatar,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Alert
} from '@mui/material';
import { LockOutlined as LockOutlinedIcon } from '@mui/icons-material';

const Authentication: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('user');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Reset messages
    setError('');
    setSuccess('');

    // Validate form
    if (!email || !password) {
      setError('Email and password are required');
      return;
    }

    if (!isLogin && password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // In a real application, this would call an authentication API
    // For now, we'll just show a success message
    if (isLogin) {
      setSuccess('Login successful! Redirecting...');
    } else {
      setSuccess('Account created successfully! You can now log in.');
      // Reset form after registration
      setEmail('');
      setPassword('');
      setConfirmPassword('');
      setName('');
      setRole('user');
      // Switch to login view
      setTimeout(() => setIsLogin(true), 2000);
    }
  };

  return (
      <Box sx={{ flexGrow: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
        <Card sx={{ maxWidth: 500, width: '100%', p: 3 }}>
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
              <Avatar sx={{ m: 1, bgcolor: 'primary.main' }}>
                <LockOutlinedIcon />
              </Avatar>
              <Typography component="h1" variant="h5">
                {isLogin ? 'Sign In' : 'Create Account'}
              </Typography>
            </Box>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
            )}

            {success && (
                <Alert severity="success" sx={{ mb: 2 }}>
                  {success}
                </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit} noValidate>
              {!isLogin && (
                  <TextField
                      margin="normal"
                      required
                      fullWidth
                      id="name"
                      label="Full Name"
                      name="name"
                      autoComplete="name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      autoFocus={!isLogin}
                  />
              )}

              <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoFocus={isLogin}
              />

              <TextField
                  margin="normal"
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete={isLogin ? 'current-password' : 'new-password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
              />

              {!isLogin && (
                  <>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="confirmPassword"
                        label="Confirm Password"
                        type="password"
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                    />

                    <FormControl fullWidth margin="normal">
                      <InputLabel id="role-label">Role</InputLabel>
                      <Select
                          labelId="role-label"
                          id="role"
                          value={role}
                          label="Role"
                          onChange={(e) => setRole(e.target.value)}
                      >
                        <MenuItem value="admin">Administrator</MenuItem>
                        <MenuItem value="user">Standard User</MenuItem>
                        <MenuItem value="viewer">Viewer (Read-only)</MenuItem>
                      </Select>
                    </FormControl>
                  </>
              )}

              <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
              >
                {isLogin ? 'Sign In' : 'Create Account'}
              </Button>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ textAlign: 'center' }}>
                <Button
                    onClick={() => setIsLogin(!isLogin)}
                    variant="text"
                >
                  {isLogin ? 'Need an account? Sign Up' : 'Already have an account? Sign In'}
                </Button>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>
  );
};

export default Authentication;

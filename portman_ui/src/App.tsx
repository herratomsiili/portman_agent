import React from 'react';
import { BrowserRouter as Router, Navigate, Route, Routes } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Dashboard from './pages/Dashboard';
import PortCalls from './pages/PortCalls';
import VesselDetails from './pages/VesselDetails';
import Reports from './pages/Reports';
import Settings from './pages/Settings';
import VesselTracking from './pages/VesselTracking';
import PortCallManagement from './pages/PortCallManagement';
import Authentication from './pages/Authentication';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import Arrivals from './pages/Arrivals';

// Create a theme instance
const theme = createTheme({
    palette: {
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
        background: {
            default: '#f5f5f5',
        },
    },
    typography: {
        fontFamily: [
            '-apple-system',
            'BlinkMacSystemFont',
            '"Segoe UI"',
            'Roboto',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif',
        ].join(','),
    },
});

function AppRoutes() {
    return (
        <Routes>
            {/* Public routes */}
            <Route path="/" element={
                <Layout>
                    <PortCalls />
                </Layout>
            } />
            <Route path="/login" element={<Authentication />} />
            <Route path="/port-calls" element={
                <Layout>
                    <PortCalls />
                </Layout>
            } />
            
            <Route path="/vessel-tracking" element={
                <Layout>
                    <VesselTracking />
                </Layout>
            } />
            
            <Route path="/arrivals" element={
                <Layout>
                    <Arrivals />
                </Layout>
            } />
            
            {/* Protected routes */}
            <Route path="/vessel-tracking" element={
                <Layout>
                    <VesselTracking />
                </Layout>
            } />
            
            <Route element={<ProtectedRoute />}>
                <Route path="/dashboard" element={
                    <Layout>
                        <Dashboard />
                    </Layout>
                } />
                <Route path="/vessel/:imo" element={
                    <Layout>
                        <VesselDetails />
                    </Layout>
                } />
                <Route path="/reports" element={
                    <Layout>
                        <Reports />
                    </Layout>
                } />
            </Route>
            
            {/* Admin routes */}
            <Route element={<ProtectedRoute requiredRole="admin" />}>
                <Route path="/port-call-management" element={
                    <Layout>
                        <PortCallManagement />
                    </Layout>
                } />
                <Route path="/settings" element={
                    <Layout>
                        <Settings />
                    </Layout>
                } />
            </Route>
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/port-calls" replace />} />
        </Routes>
    );
}

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AuthProvider>
                <Router>
                    <AppRoutes />
                </Router>
            </AuthProvider>
        </ThemeProvider>
    );
}

export default App;

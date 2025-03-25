import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Dashboard from './pages/Dashboard';
import PortCalls from './pages/PortCalls';
import VesselDetails from './pages/VesselDetails';
import Reports from './pages/Reports';
import Settings from './pages/Settings';
import VesselTracking from './pages/VesselTracking';
import PortCallManagement from './pages/PortCallManagement';
import Layout from './components/Layout';
import { AuthProvider } from './context/AuthContext';

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
            <Route path="/" element={
                <Layout>
                    <Dashboard />
                </Layout>
            } />
            <Route path="/port-calls" element={
                <Layout>
                    <PortCalls />
                </Layout>
            } />
            <Route path="/vessel/:imoNumber" element={
                <Layout>
                    <VesselDetails />
                </Layout>
            } />
            <Route path="/vessel-tracking" element={
                <Layout>
                    <VesselTracking />
                </Layout>
            } />
            <Route path="/port-call-management" element={
                <Layout>
                    <PortCallManagement />
                </Layout>
            } />
            <Route path="/reports" element={
                <Layout>
                    <Reports />
                </Layout>
            } />
            <Route path="/settings" element={
                <Layout>
                    <Settings />
                </Layout>
            } />
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

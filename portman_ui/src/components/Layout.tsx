import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
    AppBar,
    Box,
    Button,
    CssBaseline,
    Divider,
    Drawer,
    IconButton,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Toolbar,
    Typography
} from '@mui/material';
import {
    DirectionsBoat as VesselIcon,
    Assessment as ReportIcon,
    // Settings as SettingsIcon,
    // Menu as MenuIcon,
    Dashboard as DashboardIcon,
    Assessment as AssessmentIcon,
    DirectionsBoat as DirectionsBoatIcon,
    DirectionsBoatFilledOutlined as PortCallManagementIcon,
    LocationOn as LocationOnIcon,
    Login as LoginIcon,
    Menu as MenuIcon,
    Settings as SettingsIcon,
    Map as MapIcon,
    EventNote as PortCallIcon,
    ExitToApp as LogoutIcon,
    AccountCircle,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import Dashboard from "../pages/Dashboard";

const drawerWidth = 240;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { text: 'Dashboard', path: '/dashboard', icon: <DashboardIcon /> },
    { text: 'Port Calls', path: '/port-calls', icon: <DirectionsBoatIcon /> },
    { text: 'Vessel Tracking', path: '/vessel-tracking', icon: <LocationOnIcon /> },
    { text: 'Reports', path: '/reports', icon: <AssessmentIcon /> },
  ];

  const adminMenuItems = [
    { text: 'Port Call Management', path: '/port-call-management', icon: <PortCallManagementIcon /> },
    { text: 'Settings', path: '/settings', icon: <SettingsIcon /> },
  ];

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          Portman
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem
            key={item.text}
            onClick={() => navigate(item.path)}
            sx={{ 
              cursor: 'pointer',
              bgcolor: location.pathname === item.path ? 'action.selected' : 'inherit'
            }}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
      {isAuthenticated && user?.role === 'admin' && (
        <>
          <Divider />
          <List>
            <ListItem>
              <ListItemText primary="Admin Tools" />
            </ListItem>
            {adminMenuItems.map((item) => (
              <ListItem
                key={item.text}
                onClick={() => navigate(item.path)}
                sx={{ 
                  cursor: 'pointer',
                  bgcolor: location.pathname === item.path ? 'action.selected' : 'inherit'
                }}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
        </>
      )}
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: { sm: isAuthenticated ? `calc(100% - ${drawerWidth}px)` : '100%' },
          ml: { sm: isAuthenticated ? `${drawerWidth}px` : 0 },
        }}
      >
        <Toolbar>
          {isAuthenticated && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { sm: 'none' } }}
            >
              <MenuIcon />
            </IconButton>
          )}
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            {menuItems.find(item => item.path === location.pathname)?.text || 'Portman'}
          </Typography>
          {!isAuthenticated ? (
            <Button
              color="inherit"
              startIcon={<LoginIcon />}
              onClick={() => navigate('/login')}
            >
              Login
            </Button>
          ) : (
            <Button color="inherit" onClick={handleLogout}>
              Logout
            </Button>
          )}
        </Toolbar>
      </AppBar>
      {isAuthenticated && (
        <Box
          component="nav"
          sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        >
          <Drawer
            variant="temporary"
            open={mobileOpen}
            onClose={handleDrawerToggle}
            ModalProps={{
              keepMounted: true,
            }}
            sx={{
              display: { xs: 'block', sm: 'none' },
              '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
            }}
          >
            {drawer}
          </Drawer>
          <Drawer
            variant="permanent"
            sx={{
              display: { xs: 'none', sm: 'block' },
              '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
            }}
            open
          >
            {drawer}
          </Drawer>
        </Box>
      )}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: { xs: 1, sm: 1 },
          width: isAuthenticated ? `calc(100% - ${drawerWidth}px)` : '100%',
          marginLeft: isAuthenticated ? 0 : 0,
          maxWidth: '100%',
          overflow: 'hidden'
        }}
      >
        <Toolbar sx={{ minHeight: { xs: 56, sm: 64 } }} />
        {children}
      </Box>
    </Box>
  );
};

export default Layout;

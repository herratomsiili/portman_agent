import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText,
  Divider,
  Tooltip
} from '@mui/material';
import { 
  Dashboard as DashboardIcon,
  DirectionsBoat as VesselIcon,
  ShoppingCart as PortCallIcon,
  LocationOn as TrackingIcon,
  Description as ReportIcon,
  Settings as SettingsIcon,
  AccessTime as TimelineIcon,
  Anchor as AnchorIcon,
  AssignmentTurnedIn as ArrivalsIcon
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

const Navigation: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const isAdmin = user?.role === 'admin';

  const navItems = [
    { 
      title: 'Dashboard', 
      path: '/dashboard', 
      icon: <DashboardIcon />,
      requires: 'user'
    },
    { 
      title: 'Port Calls', 
      path: '/port-calls', 
      icon: <PortCallIcon />,
      requires: 'none'
    },
    { 
      title: 'Vessel Tracking', 
      path: '/vessel-tracking', 
      icon: <TrackingIcon />,
      requires: 'none'
    },
    { 
      title: 'Arrivals', 
      path: '/arrivals', 
      icon: <ArrivalsIcon />,
      requires: 'none'
    },
    { 
      title: 'Port Call Management', 
      path: '/port-call-management', 
      icon: <AnchorIcon />,
      requires: 'admin'
    },
    { 
      title: 'Reports', 
      path: '/reports', 
      icon: <ReportIcon />,
      requires: 'user'
    },
    { 
      title: 'Settings', 
      path: '/settings', 
      icon: <SettingsIcon />,
      requires: 'admin'
    }
  ];

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  return (
    <List component="nav" sx={{ width: '100%' }} data-cy="navigation-list">
      {navItems.map((item) => {
        // Don't show admin items for non-admin users
        if (item.requires === 'admin' && !isAdmin) return null;
        
        // Don't show user items for unauthenticated users
        if (item.requires === 'user' && !user) return null;
        
        const isActive = location.pathname === item.path;
        
        return (
          <ListItem key={item.path} disablePadding data-cy={`nav-item-${item.title.toLowerCase().replace(' ', '-')}`}>
            <Tooltip title={item.title} placement="right">
              <ListItemButton
                selected={isActive}
                onClick={() => handleNavigation(item.path)}
                sx={{
                  py: 1.5,
                  borderLeft: isActive ? '4px solid' : '4px solid transparent',
                  borderColor: isActive ? 'primary.main' : 'transparent',
                  '&.Mui-selected': {
                    bgcolor: 'action.selected',
                  },
                  '&.Mui-selected:hover': {
                    bgcolor: 'action.hover',
                  }
                }}
              >
                <ListItemIcon sx={{ 
                  minWidth: 40,
                  color: isActive ? 'primary.main' : 'inherit'
                }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.title} />
              </ListItemButton>
            </Tooltip>
          </ListItem>
        );
      })}
    </List>
  );
};

export default Navigation; 
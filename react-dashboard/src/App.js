import React, { useState, useEffect } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Box,
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Container,
  Paper,
  IconButton,
  Badge,
  Avatar,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  ShoppingCart as OrdersIcon,
  LocalOffer as PromotionsIcon,
  Store as OutletsIcon,
  BarChart as ReportsIcon,
  Chat as ChatIcon,
  Menu as MenuIcon,
  Notifications,
  AccountCircle,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

// Import pages
import Dashboard from './pages/Dashboard';
import Orders from './pages/Orders';
import Promotions from './pages/Promotions';
import Outlets from './pages/Outlets';
import Reports from './pages/Reports';
import Chat from './pages/Chat';

// Pepsi theme colors
const pepsiTheme = createTheme({
  palette: {
    primary: {
      main: '#005CBF', // Pepsi Blue
      light: '#4A90E2',
      dark: '#003B8C',
    },
    secondary: {
      main: '#E32934', // Pepsi Red
      light: '#FF6B6B',
      dark: '#B71C1C',
    },
    background: {
      default: '#F5F7FA',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#2E3A59',
      secondary: '#6B7280',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
      color: '#005CBF',
    },
    h5: {
      fontWeight: 500,
      color: '#2E3A59',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 20px rgba(0, 92, 191, 0.1)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          margin: '4px 8px',
          '&.Mui-selected': {
            backgroundColor: '#005CBF',
            color: 'white',
            '&:hover': {
              backgroundColor: '#003B8C',
            },
            '& .MuiListItemIcon-root': {
              color: 'white',
            },
          },
          '&:hover': {
            backgroundColor: 'rgba(0, 92, 191, 0.08)',
          },
        },
      },
    },
  },
});

const drawerWidth = 280;

const navigationItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, component: 'dashboard' },
  { text: 'Orders', icon: <OrdersIcon />, component: 'orders' },
  { text: 'Promotions', icon: <PromotionsIcon />, component: 'promotions' },
  { text: 'Outlets', icon: <OutletsIcon />, component: 'outlets' },
  { text: 'Reports', icon: <ReportsIcon />, component: 'reports' },
  { text: 'AI Chat', icon: <ChatIcon />, component: 'chat' },
];

function App() {
  const [selectedPage, setSelectedPage] = useState('dashboard');
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const renderPage = () => {
    const pageComponents = {
      dashboard: <Dashboard />,
      orders: <Orders />,
      promotions: <Promotions />,
      outlets: <Outlets />,
      reports: <Reports />,
      chat: <Chat />,
    };

    return (
      <AnimatePresence mode="wait">
        <motion.div
          key={selectedPage}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {pageComponents[selectedPage]}
        </motion.div>
      </AnimatePresence>
    );
  };

  const drawer = (
    <Box sx={{ height: '100%', background: 'linear-gradient(180deg, #005CBF 0%, #003B8C 100%)' }}>
      {/* Logo Section */}
      <Box sx={{ p: 3, textAlign: 'center', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <Typography variant="h5" sx={{ color: 'white', fontWeight: 'bold', mb: 1 }}>
          🥤 Sukkur Beverages
        </Typography>
        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
          Secondary Sales Dashboard
        </Typography>
      </Box>

      {/* Navigation */}
      <List sx={{ px: 1, py: 2 }}>
        {navigationItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={selectedPage === item.component}
              onClick={() => setSelectedPage(item.component)}
              sx={{
                color: 'white',
                '& .MuiListItemIcon-root': {
                  color: selectedPage === item.component ? 'white' : 'rgba(255,255,255,0.8)',
                },
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText 
                primary={item.text}
                primaryTypographyProps={{
                  fontWeight: selectedPage === item.component ? 600 : 400,
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>

      {/* Status Section */}
      <Box sx={{ position: 'absolute', bottom: 0, left: 0, right: 0, p: 2 }}>
        <Paper sx={{ p: 2, background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(10px)' }}>
          <Typography variant="body2" sx={{ color: 'white', textAlign: 'center' }}>
            🟢 System Online
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.8)', display: 'block', textAlign: 'center' }}>
            Last updated: {new Date().toLocaleTimeString()}
          </Typography>
        </Paper>
      </Box>
    </Box>
  );

  return (
    <ThemeProvider theme={pepsiTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        {/* App Bar */}
        <AppBar
          position="fixed"
          sx={{
            width: { sm: `calc(100% - ${drawerWidth}px)` },
            ml: { sm: `${drawerWidth}px` },
            background: 'linear-gradient(90deg, #005CBF 0%, #E32934 100%)',
            boxShadow: '0 4px 20px rgba(0, 92, 191, 0.3)',
          }}
        >
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { sm: 'none' } }}
            >
              <MenuIcon />
            </IconButton>
            
            <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
              {navigationItems.find(item => item.component === selectedPage)?.text || 'Dashboard'}
            </Typography>

            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <IconButton color="inherit">
                <Badge badgeContent={4} color="secondary">
                  <Notifications />
                </Badge>
              </IconButton>
              
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                  <AccountCircle />
                </Avatar>
                <Box sx={{ display: { xs: 'none', md: 'block' } }}>
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>
                    Sales Rep
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.8 }}>
                    Online
                  </Typography>
                </Box>
              </Box>
            </Box>
          </Toolbar>
        </AppBar>

        {/* Sidebar */}
        <Box
          component="nav"
          sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        >
          <Drawer
            variant="temporary"
            open={mobileOpen}
            onClose={handleDrawerToggle}
            ModalProps={{ keepMounted: true }}
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

        {/* Main Content */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            width: { sm: `calc(100% - ${drawerWidth}px)` },
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #F5F7FA 0%, #E8F4FD 100%)',
          }}
        >
          <Toolbar /> {/* Spacer for fixed app bar */}
          <Container maxWidth="xl" sx={{ py: 3 }}>
            {renderPage()}
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;

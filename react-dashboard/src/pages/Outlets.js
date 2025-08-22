import React, { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Chip,
  TextField,
  InputAdornment,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Avatar,
  LinearProgress,
} from '@mui/material';
import {
  Search as SearchIcon,
  Store as StoreIcon,
  TrendingUp,
  TrendingDown,
  LocationOn,
  Phone,
  Email,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const outletsData = [
  {
    id: 1,
    name: 'Super Mart Downtown',
    address: '123 Main Street, Downtown',
    phone: '+92-300-1234567',
    email: 'supermart@email.com',
    manager: 'Ahmed Khan',
    sales: 45000,
    growth: 12.5,
    status: 'Active',
    performance: 85,
    lastOrder: '2025-08-22',
  },
  {
    id: 2,
    name: 'City Mall Store',
    address: '456 Mall Road, City Center',
    phone: '+92-300-2345678',
    email: 'citymall@email.com',
    manager: 'Sara Ahmed',
    sales: 38000,
    growth: 8.3,
    status: 'Active',
    performance: 78,
    lastOrder: '2025-08-21',
  },
  {
    id: 3,
    name: 'Corner Shop Plaza',
    address: '789 Plaza Street, Corner',
    phone: '+92-300-3456789',
    email: 'cornerplaza@email.com',
    manager: 'Hassan Ali',
    sales: 32000,
    growth: -2.1,
    status: 'Inactive',
    performance: 65,
    lastOrder: '2025-08-18',
  },
  {
    id: 4,
    name: 'Express Market',
    address: '321 Express Lane, Market',
    phone: '+92-300-4567890',
    email: 'express@email.com',
    manager: 'Fatima Sheikh',
    sales: 28000,
    growth: 15.7,
    status: 'Active',
    performance: 92,
    lastOrder: '2025-08-22',
  },
];

const getStatusColor = (status) => {
  switch (status) {
    case 'Active':
      return 'success';
    case 'Inactive':
      return 'error';
    default:
      return 'default';
  }
};

const getPerformanceColor = (performance) => {
  if (performance >= 80) return '#4CAF50';
  if (performance >= 60) return '#FF9800';
  return '#f44336';
};

const Outlets = () => {
  const [outlets, setOutlets] = useState(outletsData);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredOutlets = outlets.filter(outlet =>
    outlet.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    outlet.manager.toLowerCase().includes(searchTerm.toLowerCase()) ||
    outlet.address.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalSales = outlets.reduce((sum, outlet) => sum + outlet.sales, 0);
  const activeOutlets = outlets.filter(outlet => outlet.status === 'Active').length;
  const averagePerformance = outlets.reduce((sum, outlet) => sum + outlet.performance, 0) / outlets.length;

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#005CBF' }}>
            Outlet Management
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Monitor and manage all outlet locations
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<StoreIcon />}
          sx={{
            background: 'linear-gradient(45deg, #005CBF 30%, #E32934 90%)',
            borderRadius: 3,
            px: 3,
          }}
        >
          Add Outlet
        </Button>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card sx={{ background: 'linear-gradient(135deg, #005CBF10 0%, #005CBF05 100%)' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      Total Sales
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#005CBF' }}>
                      ₹{totalSales.toLocaleString()}
                    </Typography>
                  </Box>
                  <Avatar sx={{ bgcolor: '#005CBF', width: 56, height: 56 }}>
                    <TrendingUp />
                  </Avatar>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <Card sx={{ background: 'linear-gradient(135deg, #E3293410 0%, #E3293405 100%)' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      Active Outlets
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#E32934' }}>
                      {activeOutlets}
                    </Typography>
                  </Box>
                  <Avatar sx={{ bgcolor: '#E32934', width: 56, height: 56 }}>
                    <StoreIcon />
                  </Avatar>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card sx={{ background: 'linear-gradient(135deg, #00C85110 0%, #00C85105 100%)' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      Avg Performance
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#00C851' }}>
                      {averagePerformance.toFixed(1)}%
                    </Typography>
                  </Box>
                  <Avatar sx={{ bgcolor: '#00C851', width: 56, height: 56 }}>
                    <TrendingUp />
                  </Avatar>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>

      {/* Search */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search outlets..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon color="action" />
              </InputAdornment>
            ),
          }}
          sx={{
            '& .MuiOutlinedInput-root': {
              borderRadius: 2,
            },
          }}
        />
      </Paper>

      {/* Outlets Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <TableContainer component={Paper} sx={{ borderRadius: 3 }}>
          <Table>
            <TableHead sx={{ backgroundColor: '#F8FAFC' }}>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Outlet</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Manager</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Contact</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Sales</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Growth</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Performance</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredOutlets.map((outlet, index) => (
                <motion.tr
                  key={outlet.id}
                  component={TableRow}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  sx={{
                    '&:hover': {
                      backgroundColor: '#F8FAFC',
                      transform: 'scale(1.01)',
                      transition: 'all 0.2s ease-in-out',
                    },
                  }}
                >
                  <TableCell>
                    <Box>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {outlet.name}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mt: 0.5 }}>
                        <LocationOn sx={{ fontSize: 14, color: '#6B7280' }} />
                        <Typography variant="caption" color="textSecondary">
                          {outlet.address}
                        </Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Avatar sx={{ width: 32, height: 32, bgcolor: '#005CBF' }}>
                        {outlet.manager.charAt(0)}
                      </Avatar>
                      <Typography variant="body2">{outlet.manager}</Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 0.5 }}>
                        <Phone sx={{ fontSize: 14, color: '#6B7280' }} />
                        <Typography variant="caption">{outlet.phone}</Typography>
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <Email sx={{ fontSize: 14, color: '#6B7280' }} />
                        <Typography variant="caption">{outlet.email}</Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      ₹{outlet.sales.toLocaleString()}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      Last order: {outlet.lastOrder}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                      {outlet.growth > 0 ? (
                        <TrendingUp sx={{ color: '#4CAF50', fontSize: 16 }} />
                      ) : (
                        <TrendingDown sx={{ color: '#f44336', fontSize: 16 }} />
                      )}
                      <Typography
                        variant="body2"
                        sx={{
                          color: outlet.growth > 0 ? '#4CAF50' : '#f44336',
                          fontWeight: 500,
                        }}
                      >
                        {outlet.growth > 0 ? '+' : ''}{outlet.growth}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box>
                      <Typography variant="body2" sx={{ mb: 0.5 }}>
                        {outlet.performance}%
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={outlet.performance}
                        sx={{
                          height: 6,
                          borderRadius: 3,
                          backgroundColor: '#E5E7EB',
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: getPerformanceColor(outlet.performance),
                            borderRadius: 3,
                          },
                        }}
                      />
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={outlet.status}
                      color={getStatusColor(outlet.status)}
                      size="small"
                      sx={{ fontWeight: 500 }}
                    />
                  </TableCell>
                </motion.tr>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </motion.div>
    </Box>
  );
};

export default Outlets;

import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Avatar,
  Chip,
  LinearProgress,
  IconButton,
  Button,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  ShoppingCart,
  Store,
  LocalOffer,
  AttachMoney,
  Refresh,
} from '@mui/icons-material';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { motion } from 'framer-motion';

// Sample data
const salesData = [
  { month: 'Jan', sales: 45000, orders: 120 },
  { month: 'Feb', sales: 52000, orders: 135 },
  { month: 'Mar', sales: 48000, orders: 125 },
  { month: 'Apr', sales: 61000, orders: 150 },
  { month: 'May', sales: 55000, orders: 140 },
  { month: 'Jun', sales: 67000, orders: 165 },
];

const productData = [
  { name: 'Pepsi Cola', value: 40, color: '#005CBF' },
  { name: '7UP', value: 25, color: '#00C851' },
  { name: 'Mirinda', value: 20, color: '#FF6900' },
  { name: 'Mountain Dew', value: 15, color: '#7CB342' },
];

const topOutlets = [
  { name: 'Super Mart Downtown', sales: 15000, growth: 12.5 },
  { name: 'City Mall Store', sales: 12500, growth: 8.3 },
  { name: 'Corner Shop Plaza', sales: 11200, growth: -2.1 },
  { name: 'Express Market', sales: 9800, growth: 15.7 },
];

const StatsCard = ({ title, value, icon, trend, trendValue, color }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
  >
    <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${color}10 0%, ${color}05 100%)` }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', color: color }}>
              {value}
            </Typography>
            {trend && (
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                {trend === 'up' ? (
                  <TrendingUp sx={{ color: '#4CAF50', fontSize: 16, mr: 0.5 }} />
                ) : (
                  <TrendingDown sx={{ color: '#f44336', fontSize: 16, mr: 0.5 }} />
                )}
                <Typography
                  variant="body2"
                  sx={{ color: trend === 'up' ? '#4CAF50' : '#f44336' }}
                >
                  {trendValue}%
                </Typography>
              </Box>
            )}
          </Box>
          <Avatar sx={{ bgcolor: color, width: 56, height: 56 }}>
            {icon}
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  </motion.div>
);

const Dashboard = () => {
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const handleRefresh = () => {
    setLastUpdate(new Date());
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#005CBF' }}>
            Dashboard Overview
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Welcome back! Here's what's happening with your sales today.
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={handleRefresh}
          sx={{ borderColor: '#005CBF', color: '#005CBF' }}
        >
          Refresh Data
        </Button>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Total Sales"
            value="₹67,000"
            icon={<AttachMoney />}
            trend="up"
            trendValue="12.5"
            color="#005CBF"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Orders Today"
            value="42"
            icon={<ShoppingCart />}
            trend="up"
            trendValue="8.3"
            color="#E32934"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Active Outlets"
            value="156"
            icon={<Store />}
            trend="up"
            trendValue="5.2"
            color="#00C851"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Active Promotions"
            value="8"
            icon={<LocalOffer />}
            trend="down"
            trendValue="2.1"
            color="#FF6900"
          />
        </Grid>
      </Grid>

      {/* Charts Row */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Sales Trend */}
        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Paper sx={{ p: 3, height: 400 }}>
              <Typography variant="h6" sx={{ mb: 2, color: '#005CBF', fontWeight: 'bold' }}>
                Sales Trend (Last 6 Months)
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={salesData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E0E7FF" />
                  <XAxis dataKey="month" stroke="#6B7280" />
                  <YAxis stroke="#6B7280" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#FFF',
                      border: '1px solid #005CBF',
                      borderRadius: '8px',
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="sales"
                    stroke="#005CBF"
                    strokeWidth={3}
                    dot={{ fill: '#005CBF', strokeWidth: 2, r: 6 }}
                    activeDot={{ r: 8, fill: '#E32934' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Paper>
          </motion.div>
        </Grid>

        {/* Product Distribution */}
        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Paper sx={{ p: 3, height: 400 }}>
              <Typography variant="h6" sx={{ mb: 2, color: '#005CBF', fontWeight: 'bold' }}>
                Product Sales Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={productData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label={({ name, value }) => `${name}: ${value}%`}
                  >
                    {productData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Paper>
          </motion.div>
        </Grid>
      </Grid>

      {/* Top Outlets and Recent Activity */}
      <Grid container spacing={3}>
        {/* Top Performing Outlets */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
          >
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 2, color: '#005CBF', fontWeight: 'bold' }}>
                Top Performing Outlets
              </Typography>
              {topOutlets.map((outlet, index) => (
                <Box
                  key={outlet.name}
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    py: 2,
                    borderBottom: index < topOutlets.length - 1 ? '1px solid #E5E7EB' : 'none',
                  }}
                >
                  <Box>
                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                      {outlet.name}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      ₹{outlet.sales.toLocaleString()}
                    </Typography>
                  </Box>
                  <Chip
                    label={`${outlet.growth > 0 ? '+' : ''}${outlet.growth}%`}
                    color={outlet.growth > 0 ? 'success' : 'error'}
                    size="small"
                    sx={{ fontWeight: 'bold' }}
                  />
                </Box>
              ))}
            </Paper>
          </motion.div>
        </Grid>

        {/* System Status */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
          >
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 2, color: '#005CBF', fontWeight: 'bold' }}>
                System Status
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">API Response Time</Typography>
                  <Typography variant="body2" color="success.main">98ms</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={85}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: '#E5E7EB',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: '#4CAF50',
                      borderRadius: 4,
                    },
                  }}
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Database Load</Typography>
                  <Typography variant="body2" color="warning.main">65%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={65}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: '#E5E7EB',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: '#FF9800',
                      borderRadius: 4,
                    },
                  }}
                />
              </Box>

              <Box sx={{ mt: 3, p: 2, backgroundColor: '#F0FDF4', borderRadius: 2 }}>
                <Typography variant="body2" sx={{ color: '#15803D', fontWeight: 500 }}>
                  🟢 All systems operational
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Last updated: {lastUpdate.toLocaleTimeString()}
                </Typography>
              </Box>
            </Paper>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;

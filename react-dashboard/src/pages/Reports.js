import React, { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Card,
  CardContent,
} from '@mui/material';
import {
  Assessment as ReportIcon,
  Download as DownloadIcon,
  DateRange as DateIcon,
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
  Area,
  AreaChart,
} from 'recharts';
import { motion } from 'framer-motion';

// Sample data
const monthlyData = [
  { month: 'Jan', sales: 45000, orders: 120, outlets: 45 },
  { month: 'Feb', sales: 52000, orders: 135, outlets: 48 },
  { month: 'Mar', sales: 48000, orders: 125, outlets: 46 },
  { month: 'Apr', sales: 61000, orders: 150, outlets: 52 },
  { month: 'May', sales: 55000, orders: 140, outlets: 49 },
  { month: 'Jun', sales: 67000, orders: 165, outlets: 55 },
];

const productPerformance = [
  { product: 'Pepsi Cola', sales: 125000, percentage: 35 },
  { product: '7UP', sales: 89000, percentage: 25 },
  { product: 'Mirinda', sales: 71000, percentage: 20 },
  { product: 'Mountain Dew', sales: 53000, percentage: 15 },
  { product: 'Others', sales: 18000, percentage: 5 },
];

const dailySales = [
  { day: 'Mon', sales: 8500 },
  { day: 'Tue', sales: 9200 },
  { day: 'Wed', sales: 7800 },
  { day: 'Thu', sales: 10500 },
  { day: 'Fri', sales: 12000 },
  { day: 'Sat', sales: 14500 },
  { day: 'Sun', sales: 11200 },
];

const topPerformers = [
  { name: 'Ahmed Khan', sales: 45000, orders: 78 },
  { name: 'Sara Ahmed', sales: 38000, orders: 65 },
  { name: 'Hassan Ali', sales: 32000, orders: 58 },
  { name: 'Fatima Sheikh', sales: 28000, orders: 52 },
];

const COLORS = ['#005CBF', '#E32934', '#00C851', '#FF6900', '#6C757D'];

const Reports = () => {
  const [reportType, setReportType] = useState('monthly');
  const [dateRange, setDateRange] = useState('6months');

  const renderChart = () => {
    switch (reportType) {
      case 'monthly':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart data={monthlyData}>
              <defs>
                <linearGradient id="salesGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#005CBF" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#005CBF" stopOpacity={0}/>
                </linearGradient>
              </defs>
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
              <Area
                type="monotone"
                dataKey="sales"
                stroke="#005CBF"
                strokeWidth={3}
                fillOpacity={1}
                fill="url(#salesGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>
        );
      
      case 'daily':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={dailySales}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E0E7FF" />
              <XAxis dataKey="day" stroke="#6B7280" />
              <YAxis stroke="#6B7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#FFF',
                  border: '1px solid #005CBF',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="sales" fill="#E32934" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );
      
      case 'products':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={productPerformance}
                cx="50%"
                cy="50%"
                outerRadius={120}
                dataKey="percentage"
                label={({ product, percentage }) => `${product}: ${percentage}%`}
              >
                {productPerformance.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        );
      
      default:
        return null;
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#005CBF' }}>
            Reports & Analytics
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Comprehensive sales performance insights
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<DownloadIcon />}
          sx={{
            background: 'linear-gradient(45deg, #005CBF 30%, #E32934 90%)',
            borderRadius: 3,
            px: 3,
          }}
        >
          Export Report
        </Button>
      </Box>

      {/* Controls */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Report Type</InputLabel>
              <Select
                value={reportType}
                label="Report Type"
                onChange={(e) => setReportType(e.target.value)}
                sx={{ borderRadius: 2 }}
              >
                <MenuItem value="monthly">Monthly Trends</MenuItem>
                <MenuItem value="daily">Daily Sales</MenuItem>
                <MenuItem value="products">Product Performance</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Date Range</InputLabel>
              <Select
                value={dateRange}
                label="Date Range"
                onChange={(e) => setDateRange(e.target.value)}
                sx={{ borderRadius: 2 }}
              >
                <MenuItem value="7days">Last 7 Days</MenuItem>
                <MenuItem value="30days">Last 30 Days</MenuItem>
                <MenuItem value="6months">Last 6 Months</MenuItem>
                <MenuItem value="1year">Last Year</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<DateIcon />}
              sx={{
                borderColor: '#005CBF',
                color: '#005CBF',
                borderRadius: 2,
                py: 1.5,
              }}
            >
              Custom Range
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Main Chart */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Paper sx={{ p: 3, height: 500 }}>
              <Typography variant="h6" sx={{ mb: 2, color: '#005CBF', fontWeight: 'bold' }}>
                {reportType === 'monthly' && 'Monthly Sales Trends'}
                {reportType === 'daily' && 'Daily Sales Performance'}
                {reportType === 'products' && 'Product Sales Distribution'}
              </Typography>
              {renderChart()}
            </Paper>
          </motion.div>
        </Grid>

        {/* Top Performers */}
        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Paper sx={{ p: 3, height: 500 }}>
              <Typography variant="h6" sx={{ mb: 2, color: '#005CBF', fontWeight: 'bold' }}>
                Top Sales Representatives
              </Typography>
              {topPerformers.map((performer, index) => (
                <Card
                  key={performer.name}
                  sx={{
                    mb: 2,
                    background: index === 0 ? 'linear-gradient(45deg, #005CBF10 30%, #E3293410 90%)' : '#F8FAFC',
                  }}
                >
                  <CardContent sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Box>
                        <Typography variant="body1" sx={{ fontWeight: 500 }}>
                          {index + 1}. {performer.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {performer.orders} orders
                        </Typography>
                      </Box>
                      <Typography variant="h6" sx={{ color: '#005CBF', fontWeight: 'bold' }}>
                        ₹{performer.sales.toLocaleString()}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              ))}
            </Paper>
          </motion.div>
        </Grid>
      </Grid>

      {/* Summary Cards */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card sx={{ background: 'linear-gradient(135deg, #005CBF10 0%, #005CBF05 100%)' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#005CBF' }}>
                  ₹356K
                </Typography>
                <Typography color="textSecondary">
                  Total Revenue
                </Typography>
                <Typography variant="body2" sx={{ color: '#4CAF50', mt: 1 }}>
                  +12.5% from last month
                </Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={3}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <Card sx={{ background: 'linear-gradient(135deg, #E3293410 0%, #E3293405 100%)' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#E32934' }}>
                  847
                </Typography>
                <Typography color="textSecondary">
                  Total Orders
                </Typography>
                <Typography variant="body2" sx={{ color: '#4CAF50', mt: 1 }}>
                  +8.3% from last month
                </Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={3}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card sx={{ background: 'linear-gradient(135deg, #00C85110 0%, #00C85105 100%)' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#00C851' }}>
                  156
                </Typography>
                <Typography color="textSecondary">
                  Active Outlets
                </Typography>
                <Typography variant="body2" sx={{ color: '#4CAF50', mt: 1 }}>
                  +5.2% from last month
                </Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={3}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card sx={{ background: 'linear-gradient(135deg, #FF690010 0%, #FF690005 100%)' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#FF6900' }}>
                  ₹421
                </Typography>
                <Typography color="textSecondary">
                  Avg Order Value
                </Typography>
                <Typography variant="body2" sx={{ color: '#4CAF50', mt: 1 }}>
                  +3.7% from last month
                </Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Reports;

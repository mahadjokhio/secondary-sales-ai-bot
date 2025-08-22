import React, { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Button,
  Chip,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Avatar,
  InputAdornment,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

// Sample orders data
const ordersData = [
  {
    id: 'ORD-001',
    outlet: 'Super Mart Downtown',
    date: '2025-08-22',
    items: 15,
    total: 4500,
    status: 'Completed',
    customer: 'Ahmed Khan',
  },
  {
    id: 'ORD-002',
    outlet: 'City Mall Store',
    date: '2025-08-22',
    items: 8,
    total: 2400,
    status: 'Pending',
    customer: 'Sara Ahmed',
  },
  {
    id: 'ORD-003',
    outlet: 'Corner Shop Plaza',
    date: '2025-08-21',
    items: 22,
    total: 6600,
    status: 'Processing',
    customer: 'Hassan Ali',
  },
  {
    id: 'ORD-004',
    outlet: 'Express Market',
    date: '2025-08-21',
    items: 12,
    total: 3600,
    status: 'Completed',
    customer: 'Fatima Sheikh',
  },
  {
    id: 'ORD-005',
    outlet: 'Quick Stop Store',
    date: '2025-08-20',
    items: 18,
    total: 5400,
    status: 'Cancelled',
    customer: 'Omar Malik',
  },
];

const getStatusColor = (status) => {
  switch (status) {
    case 'Completed':
      return 'success';
    case 'Processing':
      return 'warning';
    case 'Pending':
      return 'info';
    case 'Cancelled':
      return 'error';
    default:
      return 'default';
  }
};

const Orders = () => {
  const [orders, setOrders] = useState(ordersData);
  const [openDialog, setOpenDialog] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [selectedOrder, setSelectedOrder] = useState(null);

  const filteredOrders = orders.filter(order => {
    const matchesSearch = order.outlet.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         order.customer.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         order.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'All' || order.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleNewOrder = () => {
    setSelectedOrder(null);
    setOpenDialog(true);
  };

  const handleViewOrder = (order) => {
    setSelectedOrder(order);
    setOpenDialog(true);
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#005CBF' }}>
            Order Management
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage and track all sales orders
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleNewOrder}
          sx={{
            background: 'linear-gradient(45deg, #005CBF 30%, #E32934 90%)',
            borderRadius: 3,
            px: 3,
          }}
        >
          New Order
        </Button>
      </Box>

      {/* Filters and Search */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              placeholder="Search orders..."
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
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Status Filter</InputLabel>
              <Select
                value={statusFilter}
                label="Status Filter"
                onChange={(e) => setStatusFilter(e.target.value)}
                sx={{ borderRadius: 2 }}
              >
                <MenuItem value="All">All Status</MenuItem>
                <MenuItem value="Completed">Completed</MenuItem>
                <MenuItem value="Processing">Processing</MenuItem>
                <MenuItem value="Pending">Pending</MenuItem>
                <MenuItem value="Cancelled">Cancelled</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={3}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<FilterIcon />}
              sx={{
                borderColor: '#005CBF',
                color: '#005CBF',
                borderRadius: 2,
                py: 1.5,
              }}
            >
              More Filters
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Orders Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <TableContainer component={Paper} sx={{ borderRadius: 3 }}>
          <Table>
            <TableHead sx={{ backgroundColor: '#F8FAFC' }}>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Order ID</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Customer</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Outlet</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Date</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Items</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Total</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Status</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: '#005CBF' }}>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredOrders.map((order, index) => (
                <motion.tr
                  key={order.id}
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
                    <Typography variant="body2" sx={{ fontWeight: 500, color: '#005CBF' }}>
                      {order.id}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Avatar sx={{ width: 32, height: 32, bgcolor: '#E32934' }}>
                        {order.customer.charAt(0)}
                      </Avatar>
                      <Typography variant="body2">{order.customer}</Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{order.outlet}</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{order.date}</Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={`${order.items} items`}
                      size="small"
                      sx={{
                        backgroundColor: '#E3F2FD',
                        color: '#005CBF',
                        fontWeight: 500,
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      ₹{order.total.toLocaleString()}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={order.status}
                      color={getStatusColor(order.status)}
                      size="small"
                      sx={{ fontWeight: 500 }}
                    />
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton
                        size="small"
                        onClick={() => handleViewOrder(order)}
                        sx={{ color: '#005CBF' }}
                      >
                        <ViewIcon />
                      </IconButton>
                      <IconButton size="small" sx={{ color: '#FF9800' }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton size="small" sx={{ color: '#f44336' }}>
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </TableCell>
                </motion.tr>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </motion.div>

      {/* Order Dialog */}
      <Dialog
        open={openDialog}
        onClose={() => setOpenDialog(false)}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: { borderRadius: 3 }
        }}
      >
        <DialogTitle sx={{ background: 'linear-gradient(45deg, #005CBF 30%, #E32934 90%)', color: 'white' }}>
          {selectedOrder ? `Order Details - ${selectedOrder.id}` : 'Create New Order'}
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          {selectedOrder ? (
            <Box>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">Customer</Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>{selectedOrder.customer}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">Outlet</Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>{selectedOrder.outlet}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">Date</Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>{selectedOrder.date}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">Status</Typography>
                  <Chip
                    label={selectedOrder.status}
                    color={getStatusColor(selectedOrder.status)}
                    sx={{ mb: 2 }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="textSecondary">Order Summary</Typography>
                  <Box sx={{ p: 2, backgroundColor: '#F8FAFC', borderRadius: 2, mt: 1 }}>
                    <Typography variant="body1">Items: {selectedOrder.items}</Typography>
                    <Typography variant="h6" sx={{ color: '#005CBF', fontWeight: 'bold' }}>
                      Total: ₹{selectedOrder.total.toLocaleString()}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Box>
          ) : (
            <Typography>New Order Form would go here...</Typography>
          )}
        </DialogContent>
        <DialogActions sx={{ p: 3 }}>
          <Button onClick={() => setOpenDialog(false)} color="inherit">
            Cancel
          </Button>
          <Button
            variant="contained"
            sx={{
              background: 'linear-gradient(45deg, #005CBF 30%, #E32934 90%)',
            }}
          >
            {selectedOrder ? 'Update Order' : 'Create Order'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Orders;

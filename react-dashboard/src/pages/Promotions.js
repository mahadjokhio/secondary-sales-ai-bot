import React, { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardMedia,
  Button,
  Chip,
  TextField,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Search as SearchIcon,
  LocalOffer as OfferIcon,
  Schedule as ScheduleIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const promotionsData = [
  {
    id: 1,
    title: 'Summer Cola Blast',
    description: 'Buy 2 Get 1 Free on all Pepsi Cola variants',
    discount: '33%',
    validUntil: '2025-08-31',
    status: 'Active',
    image: '/api/placeholder/300/200',
    terms: 'Valid on 250ml, 500ml, and 1.5L bottles. Cannot be combined with other offers.',
  },
  {
    id: 2,
    title: '7UP Fresh Deal',
    description: '20% off on 7UP family pack (6 bottles)',
    discount: '20%',
    validUntil: '2025-09-15',
    status: 'Active',
    image: '/api/placeholder/300/200',
    terms: 'Minimum purchase of 6 bottles required. Valid for 500ml bottles only.',
  },
  {
    id: 3,
    title: 'Mirinda Mania',
    description: 'Free Mirinda 250ml with every large pizza order',
    discount: 'Free',
    validUntil: '2025-08-25',
    status: 'Ending Soon',
    image: '/api/placeholder/300/200',
    terms: 'Valid at participating restaurants only. One free drink per pizza.',
  },
  {
    id: 4,
    title: 'Mountain Dew Energy',
    description: '15% off on Mountain Dew 500ml multi-packs',
    discount: '15%',
    validUntil: '2025-09-30',
    status: 'Active',
    image: '/api/placeholder/300/200',
    terms: 'Valid on 4-pack and 6-pack variants. While supplies last.',
  },
];

const getStatusColor = (status) => {
  switch (status) {
    case 'Active':
      return 'success';
    case 'Ending Soon':
      return 'warning';
    case 'Expired':
      return 'error';
    default:
      return 'default';
  }
};

const Promotions = () => {
  const [promotions, setPromotions] = useState(promotionsData);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPromotion, setSelectedPromotion] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);

  const filteredPromotions = promotions.filter(promotion =>
    promotion.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    promotion.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleViewPromotion = (promotion) => {
    setSelectedPromotion(promotion);
    setOpenDialog(true);
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#005CBF' }}>
            Promotions & Offers
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Current active promotions and special offers
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<OfferIcon />}
          sx={{
            background: 'linear-gradient(45deg, #005CBF 30%, #E32934 90%)',
            borderRadius: 3,
            px: 3,
          }}
        >
          Create Promotion
        </Button>
      </Box>

      {/* Search */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search promotions..."
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

      {/* Promotions Grid */}
      <Grid container spacing={3}>
        {filteredPromotions.map((promotion, index) => (
          <Grid item xs={12} sm={6} md={4} key={promotion.id}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -5, transition: { duration: 0.2 } }}
            >
              <Card
                sx={{
                  height: '100%',
                  borderRadius: 3,
                  overflow: 'hidden',
                  cursor: 'pointer',
                  '&:hover': {
                    boxShadow: '0 8px 30px rgba(0, 92, 191, 0.2)',
                  },
                }}
                onClick={() => handleViewPromotion(promotion)}
              >
                <CardMedia
                  component="div"
                  sx={{
                    height: 160,
                    background: `linear-gradient(45deg, #005CBF 30%, #E32934 90%)`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '2rem',
                    fontWeight: 'bold',
                  }}
                >
                  {promotion.discount}
                  <br />
                  OFF
                </CardMedia>
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#005CBF' }}>
                      {promotion.title}
                    </Typography>
                    <Chip
                      label={promotion.status}
                      color={getStatusColor(promotion.status)}
                      size="small"
                      sx={{ fontWeight: 500 }}
                    />
                  </Box>
                  
                  <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                    {promotion.description}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                    <ScheduleIcon sx={{ fontSize: 16, color: '#6B7280' }} />
                    <Typography variant="caption" color="textSecondary">
                      Valid until {promotion.validUntil}
                    </Typography>
                  </Box>
                  
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<ViewIcon />}
                    sx={{
                      borderColor: '#005CBF',
                      color: '#005CBF',
                      borderRadius: 2,
                      '&:hover': {
                        backgroundColor: '#005CBF',
                        color: 'white',
                      },
                    }}
                  >
                    View Details
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>

      {/* Promotion Details Dialog */}
      <Dialog
        open={openDialog}
        onClose={() => setOpenDialog(false)}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: { borderRadius: 3 }
        }}
      >
        {selectedPromotion && (
          <>
            <DialogTitle
              sx={{
                background: 'linear-gradient(45deg, #005CBF 30%, #E32934 90%)',
                color: 'white',
                textAlign: 'center',
              }}
            >
              <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                {selectedPromotion.title}
              </Typography>
              <Typography variant="h3" sx={{ fontWeight: 'bold', mt: 1 }}>
                {selectedPromotion.discount} OFF
              </Typography>
            </DialogTitle>
            <DialogContent sx={{ p: 4 }}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Typography variant="h6" sx={{ mb: 2, color: '#005CBF' }}>
                    Promotion Details
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 3 }}>
                    {selectedPromotion.description}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2, backgroundColor: '#F8FAFC' }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Status
                    </Typography>
                    <Chip
                      label={selectedPromotion.status}
                      color={getStatusColor(selectedPromotion.status)}
                      sx={{ mt: 1 }}
                    />
                  </Paper>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2, backgroundColor: '#F8FAFC' }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Valid Until
                    </Typography>
                    <Typography variant="body1" sx={{ mt: 1, fontWeight: 500 }}>
                      {selectedPromotion.validUntil}
                    </Typography>
                  </Paper>
                </Grid>
                
                <Grid item xs={12}>
                  <Typography variant="h6" sx={{ mb: 2, color: '#005CBF' }}>
                    Terms & Conditions
                  </Typography>
                  <Paper sx={{ p: 3, backgroundColor: '#FEF7F0' }}>
                    <Typography variant="body2">
                      {selectedPromotion.terms}
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </DialogContent>
            <DialogActions sx={{ p: 3 }}>
              <Button onClick={() => setOpenDialog(false)} color="inherit">
                Close
              </Button>
              <Button
                variant="contained"
                sx={{
                  background: 'linear-gradient(45deg, #005CBF 30%, #E32934 90%)',
                }}
              >
                Share Promotion
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default Promotions;

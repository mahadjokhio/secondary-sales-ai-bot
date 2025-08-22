import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Avatar,
  Chip,
  IconButton,
  InputAdornment,
} from '@mui/material';
import {
  Send as SendIcon,
  Mic as MicIcon,
  AttachFile as AttachIcon,
  SmartToy as BotIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

const initialMessages = [
  {
    id: 1,
    type: 'bot',
    message: 'Hello! I\'m your AI Sales Assistant. How can I help you today?',
    timestamp: new Date(Date.now() - 60000),
  },
  {
    id: 2,
    type: 'user',
    message: 'What are our top-selling products this month?',
    timestamp: new Date(Date.now() - 45000),
  },
  {
    id: 3,
    type: 'bot',
    message: 'Based on current data, your top-selling products this month are:\n\n1. Pepsi Cola (35% of total sales)\n2. 7UP (25% of total sales)\n3. Mirinda (20% of total sales)\n4. Mountain Dew (15% of total sales)\n\nPepsi Cola continues to lead with ₹125,000 in sales. Would you like detailed analytics for any specific product?',
    timestamp: new Date(Date.now() - 30000),
  },
  {
    id: 4,
    type: 'user',
    message: 'Show me the performance of outlets in the downtown area',
    timestamp: new Date(Date.now() - 15000),
  },
  {
    id: 5,
    type: 'bot',
    message: 'Here\'s the downtown area outlet performance:\n\n🏪 **Super Mart Downtown**\n- Sales: ₹45,000\n- Growth: +12.5%\n- Performance Score: 85%\n- Status: Active\n\n🏪 **City Center Plaza**\n- Sales: ₹38,000\n- Growth: +8.3%\n- Performance Score: 78%\n- Status: Active\n\nBoth outlets are performing well above average. Super Mart Downtown is your best performer in this area!',
    timestamp: new Date(Date.now() - 5000),
  },
];

const quickActions = [
  'Show daily sales report',
  'List active promotions',
  'Top performing outlets',
  'Inventory status',
  'Recent orders',
];

const Chat = () => {
  const [messages, setMessages] = useState(initialMessages);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const newUserMessage = {
      id: Date.now(),
      type: 'user',
      message: inputMessage,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        message: generateBotResponse(inputMessage),
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1500);
  };

  const generateBotResponse = (userMessage) => {
    const message = userMessage.toLowerCase();
    
    if (message.includes('sales') || message.includes('revenue')) {
      return 'Current sales performance shows strong growth. Total revenue for this month is ₹356,000, which is 12.5% higher than last month. Would you like a detailed breakdown by product or region?';
    }
    
    if (message.includes('order') || message.includes('orders')) {
      return 'You have 42 orders today, with a total value of ₹18,500. Recent orders include:\n\n• Super Mart Downtown - ₹4,500\n• City Mall Store - ₹2,400\n• Express Market - ₹3,600\n\nWould you like to view details for any specific order?';
    }
    
    if (message.includes('promotion') || message.includes('offer')) {
      return 'Current active promotions:\n\n🎯 Summer Cola Blast - 33% OFF\n🎯 7UP Fresh Deal - 20% OFF\n🎯 Mirinda Mania - Free drink offer\n🎯 Mountain Dew Energy - 15% OFF\n\nAll promotions are performing well. Summer Cola Blast has the highest engagement rate!';
    }
    
    if (message.includes('outlet') || message.includes('store')) {
      return 'You have 156 active outlets with an average performance score of 79.5%. Top performers:\n\n1. Express Market - 92% performance\n2. Super Mart Downtown - 85% performance\n3. City Mall Store - 78% performance\n\nWould you like detailed analytics for any specific outlet?';
    }
    
    return 'I understand your query about: "' + userMessage + '". I can help you with sales data, order management, promotions, outlet performance, and reporting. What specific information would you like to know?';
  };

  const handleQuickAction = (action) => {
    setInputMessage(action);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Box sx={{ height: 'calc(100vh - 150px)', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#005CBF' }}>
          AI Sales Assistant
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Get instant insights and assistance for your sales operations
        </Typography>
      </Box>

      {/* Quick Actions */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
          Quick Actions:
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {quickActions.map((action, index) => (
            <Chip
              key={index}
              label={action}
              onClick={() => handleQuickAction(action)}
              sx={{
                cursor: 'pointer',
                '&:hover': {
                  backgroundColor: '#005CBF',
                  color: 'white',
                },
              }}
            />
          ))}
        </Box>
      </Paper>

      {/* Chat Messages */}
      <Paper sx={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <Box sx={{ flex: 1, p: 2, overflowY: 'auto' }}>
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                    mb: 2,
                  }}
                >
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: 1,
                      maxWidth: '70%',
                      flexDirection: message.type === 'user' ? 'row-reverse' : 'row',
                    }}
                  >
                    <Avatar
                      sx={{
                        bgcolor: message.type === 'user' ? '#E32934' : '#005CBF',
                        width: 36,
                        height: 36,
                      }}
                    >
                      {message.type === 'user' ? <PersonIcon /> : <BotIcon />}
                    </Avatar>
                    
                    <Paper
                      sx={{
                        p: 2,
                        backgroundColor: message.type === 'user' ? '#005CBF' : '#F8FAFC',
                        color: message.type === 'user' ? 'white' : 'inherit',
                        borderRadius: 3,
                        borderTopLeftRadius: message.type === 'user' ? 3 : 1,
                        borderTopRightRadius: message.type === 'user' ? 1 : 3,
                      }}
                    >
                      <Typography
                        variant="body2"
                        sx={{
                          whiteSpace: 'pre-line',
                          wordBreak: 'break-word',
                        }}
                      >
                        {message.message}
                      </Typography>
                      <Typography
                        variant="caption"
                        sx={{
                          display: 'block',
                          mt: 1,
                          opacity: 0.7,
                          fontSize: '0.75rem',
                        }}
                      >
                        {message.timestamp.toLocaleTimeString()}
                      </Typography>
                    </Paper>
                  </Box>
                </Box>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing Indicator */}
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Avatar sx={{ bgcolor: '#005CBF', width: 36, height: 36 }}>
                  <BotIcon />
                </Avatar>
                <Paper
                  sx={{
                    p: 2,
                    backgroundColor: '#F8FAFC',
                    borderRadius: 3,
                    borderTopLeftRadius: 1,
                  }}
                >
                  <Box sx={{ display: 'flex', gap: 0.5 }}>
                    {[0, 1, 2].map((dot) => (
                      <motion.div
                        key={dot}
                        animate={{
                          scale: [1, 1.2, 1],
                          opacity: [0.5, 1, 0.5],
                        }}
                        transition={{
                          duration: 1,
                          repeat: Infinity,
                          delay: dot * 0.2,
                        }}
                        style={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          backgroundColor: '#005CBF',
                        }}
                      />
                    ))}
                  </Box>
                </Paper>
              </Box>
            </motion.div>
          )}
        </Box>

        {/* Input Area */}
        <Box sx={{ p: 2, borderTop: '1px solid #E5E7EB' }}>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
            <TextField
              fullWidth
              multiline
              maxRows={3}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about your sales data..."
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton size="small" sx={{ color: '#6B7280' }}>
                      <AttachIcon />
                    </IconButton>
                    <IconButton size="small" sx={{ color: '#6B7280' }}>
                      <MicIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3,
                },
              }}
            />
            <Button
              variant="contained"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim()}
              sx={{
                background: 'linear-gradient(45deg, #005CBF 30%, #E32934 90%)',
                borderRadius: 3,
                px: 3,
                py: 1.5,
                minWidth: 'auto',
              }}
            >
              <SendIcon />
            </Button>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default Chat;

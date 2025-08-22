# Sukkur Beverages - Secondary Sales Dashboard

A modern React dashboard for secondary sales management with Pepsi branding, built as a conversion from the original Streamlit application.

## 🎨 Features

### **Pepsi-Themed Design**
- Primary colors: Pepsi Blue (#005CBF) and Pepsi Red (#E32934)
- Modern Material-UI components with custom Pepsi styling
- Smooth animations and hover effects
- Responsive design for desktop and mobile

### **Dashboard Components**
- **📊 Dashboard**: Overview with KPIs, sales trends, and performance metrics
- **🛒 Orders**: Complete order management with search and filtering
- **🎁 Promotions**: Active promotions and offer management
- **🏪 Outlets**: Outlet performance monitoring and analytics
- **📈 Reports**: Advanced analytics with interactive charts
- **🤖 AI Chat**: Intelligent sales assistant with real-time responses

### **Interactive Features**
- Real-time data visualization with Recharts
- Responsive sidebar navigation
- Search and filtering capabilities
- Modal dialogs for detailed views
- Animated transitions and hover effects

## 🚀 Getting Started

### Prerequisites
- Node.js 14+ 
- npm or yarn package manager

### Installation

1. **Clone or navigate to the React dashboard directory:**
   ```bash
   cd d:\botsales\react-dashboard
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser and visit:**
   ```
   http://localhost:3000
   ```

## 📦 Technology Stack

- **React 18** - Modern React with hooks and functional components
- **Material-UI (MUI) 5** - Component library with custom theming
- **Recharts** - Interactive charts and data visualization
- **Framer Motion** - Smooth animations and transitions
- **React Router** - Client-side routing (ready for implementation)

## 🎯 Project Structure

```
src/
├── components/          # Reusable UI components
├── pages/              # Main dashboard pages
│   ├── Dashboard.js    # Overview dashboard
│   ├── Orders.js       # Order management
│   ├── Promotions.js   # Promotions & offers
│   ├── Outlets.js      # Outlet management
│   ├── Reports.js      # Analytics & reports
│   └── Chat.js         # AI chat interface
├── utils/              # Utility functions
├── App.js              # Main app component
└── index.js            # Application entry point
```

## 🎨 Design System

### **Color Palette**
- **Primary Blue**: #005CBF (Pepsi Blue)
- **Secondary Red**: #E32934 (Pepsi Red)
- **Success Green**: #4CAF50
- **Warning Orange**: #FF9800
- **Background**: #F5F7FA

### **Typography**
- **Font Family**: Roboto, Helvetica, Arial
- **Headings**: Bold, Pepsi Blue color
- **Body Text**: Regular, with good contrast

### **Components**
- **Cards**: Rounded corners (12px), subtle shadows
- **Buttons**: Gradient backgrounds, rounded (8px)
- **Navigation**: Gradient sidebar with white text
- **Charts**: Pepsi brand colors with smooth animations

## 📊 Sample Data

The dashboard includes comprehensive sample data:
- **Sales Data**: Monthly and daily sales trends
- **Products**: Pepsi, 7UP, Mirinda, Mountain Dew variants
- **Outlets**: Multiple store locations with performance metrics
- **Orders**: Complete order history with customer details
- **Promotions**: Active and upcoming promotional campaigns

## 🔧 Customization

### **Adding New Pages**
1. Create a new component in `src/pages/`
2. Add navigation item in `App.js`
3. Import and include in the routing logic

### **Modifying Colors**
Update the theme in `App.js`:
```javascript
const pepsiTheme = createTheme({
  palette: {
    primary: { main: '#005CBF' },
    secondary: { main: '#E32934' },
    // ... other colors
  },
});
```

### **Adding Charts**
Use Recharts components with Pepsi colors:
```javascript
<LineChart data={data}>
  <Line stroke="#005CBF" strokeWidth={3} />
</LineChart>
```

## 🌟 Key Features Implemented

### **Dashboard Overview**
- ✅ Sales KPI cards with trend indicators
- ✅ Interactive sales trend charts
- ✅ Product distribution pie chart
- ✅ Top performing outlets list
- ✅ System status monitoring

### **Order Management**
- ✅ Complete order listing with search
- ✅ Status-based filtering
- ✅ Order details modal
- ✅ Customer information display
- ✅ Action buttons for order operations

### **Promotions**
- ✅ Promotion cards with discount display
- ✅ Status indicators (Active, Ending Soon)
- ✅ Detailed promotion information
- ✅ Terms and conditions display

### **Outlets**
- ✅ Outlet performance metrics
- ✅ Contact information display
- ✅ Growth trend indicators
- ✅ Performance progress bars
- ✅ Summary statistics

### **Reports & Analytics**
- ✅ Multiple chart types (Line, Bar, Pie, Area)
- ✅ Customizable date ranges
- ✅ Top performers ranking
- ✅ Export functionality
- ✅ Summary metrics

### **AI Chat**
- ✅ Real-time chat interface
- ✅ Quick action buttons
- ✅ Typing indicators
- ✅ Message history
- ✅ Contextual responses

## 🚀 Deployment

### **Build for Production**
```bash
npm run build
```

### **Deploy to Web Server**
1. Upload the `build/` folder to your web server
2. Configure server to serve `index.html` for all routes
3. Ensure proper MIME types for static assets

## 🔗 Integration

### **API Integration**
Ready for backend integration:
- Replace sample data with API calls
- Add authentication system
- Implement real-time data updates
- Connect to actual database

### **Voice Features**
Ready for voice integration:
- Add Web Speech API
- Implement voice commands
- Add text-to-speech responses

## 📱 Responsive Design

- ✅ Mobile-first design approach
- ✅ Collapsible sidebar for mobile
- ✅ Responsive grid layouts
- ✅ Touch-friendly interface
- ✅ Optimized for tablets and phones

## 🎯 Performance

- ✅ Optimized bundle size
- ✅ Code splitting ready
- ✅ Lazy loading components
- ✅ Efficient re-rendering
- ✅ Smooth animations

## 📝 Next Steps

1. **Backend Integration**: Connect to real data sources
2. **Authentication**: Add user login and permissions
3. **Real-time Updates**: Implement WebSocket connections
4. **PWA Features**: Add offline capabilities
5. **Voice Integration**: Implement voice commands
6. **Advanced Analytics**: Add more chart types and filters

## 🎨 Brand Compliance

This dashboard strictly follows Pepsi brand guidelines:
- ✅ Official Pepsi blue and red colors
- ✅ Professional typography
- ✅ Clean, modern design
- ✅ Consistent spacing and layout
- ✅ High-quality visual hierarchy

---

**Built with ❤️ for Sukkur Beverages Limited**

For questions or support, please contact the development team.

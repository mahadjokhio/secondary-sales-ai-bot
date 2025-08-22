# Setup Instructions for React Dashboard

## Option 1: Install Node.js and Run React App

### Step 1: Install Node.js
1. Download Node.js from: https://nodejs.org/
2. Choose the LTS version (recommended)
3. Run the installer and follow the setup wizard
4. Restart your terminal/PowerShell

### Step 2: Install Dependencies and Run
```bash
cd d:\botsales\react-dashboard
npm install
npm start
```

The app will open at: http://localhost:3000

## Option 2: Quick Preview HTML Version

I've created a standalone HTML version that you can run immediately without installing Node.js.
Simply open the `preview.html` file in your browser to see the dashboard.

## Troubleshooting

### If npm command is not found:
1. Make sure Node.js is properly installed
2. Restart your terminal
3. Check if Node.js is in your PATH: `node --version`

### If you get permission errors:
1. Run PowerShell as Administrator
2. Or use: `npm install --no-optional`

### For immediate preview:
Open the `preview.html` file that I'll create next - it contains a working demo of the dashboard.

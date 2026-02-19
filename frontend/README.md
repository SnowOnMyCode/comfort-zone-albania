# Frontend - Beauty Products Admin

Simple HTML/CSS/JavaScript frontend for the Beauty Products API.

## Features

- 📊 Dashboard with charts
- 🛍️ Product management
- 💰 Bulk price updates
- 📦 Order tracking
- 👥 Customer management

## Setup

### Option 1: Simple HTTP Server (Recommended)
\`\`\`bash
cd frontend
python -m http.server 3000
\`\`\`
Visit: http://localhost:3000

### Option 2: Open Directly
Just double-click \`index.html\` in your file explorer.

**Note**: Some browsers may block API calls when opening files directly. Use Option 1 if you encounter CORS issues.

## Configuration

Make sure your backend is running at http://localhost:8000

If your backend runs on a different port, update \`app.js\`:
\`\`\`javascript
const API_BASE = 'http://localhost:YOUR_PORT/api';
\`\`\`

## Usage

### Dashboard
- View key metrics (orders today, revenue, products)
- See top-selling products in chart

### Products
- Search products by name/SKU/keywords
- View all products in table
- Delete products

### Bulk Price Update
1. Enter keyword (e.g., "shampoo")
2. Choose change type (percentage or fixed)
3. Enter value
4. Click "Update Prices"

### Orders
- View all orders
- See order status with color coding
- View customer and total amount

### Customers
- View all customers
- See customer types (hotel, hairdresser, pharmacy)
- View contact information

## Tech Stack

- **HTML5** - Structure
- **Tailwind CSS** (CDN) - Styling
- **Vanilla JavaScript** - Logic
- **Chart.js** (CDN) - Charts
- **Fetch API** - HTTP requests

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Future Enhancements

For a production-ready version, consider:
- React/Vue.js for better state management
- Form validation
- Loading states
- Error handling
- Toast notifications
- User authentication UI
- Mobile-responsive design improvements
- Add/Edit product forms
- Create order form
- Customer creation form

## Development Notes

This is a basic frontend to demonstrate the API functionality. For a portfolio project, you could enhance it with:

1. **Modern Framework**: Rebuild with React/Vue
2. **State Management**: Redux/Vuex
3. **UI Library**: Material-UI, Ant Design
4. **Forms**: React Hook Form, Formik
5. **Routing**: React Router
6. **Charts**: Recharts, ApexCharts

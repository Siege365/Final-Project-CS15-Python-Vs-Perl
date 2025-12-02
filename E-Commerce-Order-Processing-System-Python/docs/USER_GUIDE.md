# User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Roles](#user-roles)
3. [Customer Guide](#customer-guide)
4. [Staff/Admin Guide](#staffadmin-guide)
5. [Features](#features)
6. [Tips & Tricks](#tips--tricks)

## Getting Started

### First Time Login

1. **Start the Application**

   ```bash
   streamlit run app.py
   ```

2. **Open Browser** (auto-opens to `http://localhost:8501`)

3. **Login** with default credentials:
   - Admin: `admin` / `admin123`
   - Staff: `staff` / `staff123`
   - Customer: `customer` / `customer123`

### User Interface Overview

- **Sidebar**: Navigation menu (left side)
- **Main Area**: Content display
- **User Info**: Current user and role (sidebar top)
- **Logout**: Button to log out (sidebar bottom)

## User Roles

### Customer

- Browse product catalog
- Add products to cart
- Place orders
- View order history
- Update profile

### Staff

- All customer features
- Manage products
- Process orders
- View customers
- Access reports

### Admin

- All staff features
- Full system access
- User management
- System settings

## Customer Guide

### Browsing Products

1. **Navigate to Products**

   - Click "Products" in sidebar

2. **Search Products**

   - Use search box at top
   - Filter by category
   - Sort by price or name

3. **View Product Details**
   - Product name and description
   - SKU and category
   - Price
   - Stock availability

### Shopping Cart

1. **Add to Cart**

   - Select quantity
   - Click "Add to Cart" button
   - Success message appears

2. **View Cart**

   - Navigate to "My Orders" → "Shopping Cart"
   - See all items in cart

3. **Update Cart**
   - Change quantity using number input
   - Click trash icon to remove items

### Placing an Order

1. **Go to Shopping Cart**

2. **Review Cart Items**

   - Check products and quantities
   - View subtotal

3. **Review Order Summary**

   - Subtotal
   - Tax (8%)
   - Shipping (free over $100)
   - Total amount

4. **Enter Shipping Information**

   - Address
   - City
   - State
   - ZIP Code

5. **Select Payment Method**

   - Credit Card
   - Debit Card
   - PayPal
   - Cash on Delivery
   - Bank Transfer

6. **Add Order Notes** (optional)

7. **Click "Place Order"**
   - Order number generated
   - Cart cleared
   - Confirmation message

### Viewing Order History

1. **Navigate to "My Orders"**

2. **Click "Order History" tab**

3. **View Order Details**
   - Click on order to expand
   - See items, total, status
   - Track order status

### Updating Profile

1. **Navigate to Settings**

2. **Click "Profile" tab**

3. **Update Information**

   - Name
   - Phone
   - Address
   - City, State, ZIP

4. **Click "Update Profile"**

## Staff/Admin Guide

### Managing Products

#### View All Products

1. **Navigate to Products**

2. **View Products Table**
   - Search by name/SKU
   - Toggle inactive products

#### Add New Product

1. **Click "Add Product" tab**

2. **Fill in Product Information**

   - Name\* (required)
   - SKU\* (unique identifier)
   - Category\*
   - Price\*
   - Cost (optional)
   - Stock Quantity
   - Reorder Level
   - Description

3. **Click "Add Product"**

#### Edit Product

1. **Go to "All Products" tab**

2. **Select product** from dropdown

3. **Update information**

4. **Click "Update Product"**

#### Delete Product

1. **Select product**

2. **Click "Delete Product"**
   - Soft delete (sets inactive)

#### Low Stock Alert

1. **Click "Low Stock" tab**

2. **View products below reorder level**

3. **Take action** to restock

### Managing Orders

#### View All Orders

1. **Navigate to Orders**

2. **Use Filters**
   - Search by order number
   - Filter by status
   - Sort by date/total

#### View Order Details

1. **Click "Order Details" tab**

2. **Select Order**

3. **View Complete Information**
   - Customer details
   - Order items
   - Shipping address
   - Payment info

#### Update Order Status

1. **Select order** in details

2. **Choose new status**:

   - Pending
   - Processing
   - Shipped
   - Delivered
   - Cancelled
   - Refunded

3. **Click "Update Order Status"**

### Managing Customers

#### View All Customers

1. **Navigate to Customers**

2. **Search/Browse**
   - Search by name, phone, email

#### Add Customer

1. **Click "Add Customer" tab**

2. **Fill in information**

   - First Name\*
   - Last Name\*
   - Phone\*
   - Email
   - Address details

3. **Click "Add Customer"**

#### View Customer Details

1. **Click "Customer Details" tab**

2. **Select customer**

3. **View Statistics**

   - Total orders
   - Total spent
   - Average order value
   - Last order date

4. **View Order History**
   - See all customer orders

#### Edit Customer

1. **Select customer**

2. **Update information**

3. **Click "Update Customer"**

### Reports & Analytics

#### Sales Report

1. **Navigate to Reports**

2. **View Metrics**

   - Total revenue
   - Total orders
   - Average order value

3. **Analyze Charts**
   - Revenue trend (daily)
   - Orders by status
   - Revenue by payment method

#### Product Performance

1. **Click "Product Performance" tab**

2. **View Top Products**

   - By revenue
   - By units sold

3. **Revenue by Category**

4. **Low Stock Alert**

#### Customer Insights

1. **Click "Customer Insights" tab**

2. **View Top Customers**

   - By total spending
   - Order count

3. **Customer Statistics**
   - Total customers
   - Active customers (last 30 days)

#### Inventory Report

1. **Click "Inventory Report" tab**

2. **View Metrics**

   - Total products
   - Active products
   - Inventory value
   - Potential profit

3. **Stock Analysis**
   - By category
   - Stock level distribution

### Dashboard

Quick overview of system:

- Key metrics (revenue, orders, products, avg order)
- Orders by status
- Revenue by payment method
- Recent orders
- Low stock alerts
- Top selling products

## Features

### Search & Filter

**Products:**

- Search by name, description, SKU
- Filter by category
- Sort by name or price

**Orders:**

- Search by order number
- Search by customer name
- Filter by status
- Sort by date or total

**Customers:**

- Search by name, phone, email

### Automatic Calculations

**Shopping Cart:**

- Subtotal: Sum of all items
- Tax: 8% of subtotal
- Shipping: $10 (free over $100)
- Total: Subtotal + Tax + Shipping

**Inventory:**

- Auto-deduct stock on order
- Track inventory transactions
- Low stock alerts

### Data Export

Tables can be copied:

1. Click on table
2. Use Ctrl+C / Cmd+C
3. Paste into Excel/Sheets

### Real-time Updates

- Order status changes instantly
- Stock updates immediately
- Cart updates live
- No page refresh needed

## Tips & Tricks

### For Customers

1. **Free Shipping**: Orders over $100 get free shipping
2. **Cart Management**: Adjust quantities before checkout
3. **Order Notes**: Add special instructions
4. **Save Info**: Update profile to save shipping address

### For Staff

1. **Quick Search**: Use search boxes to find items fast
2. **Filters**: Use status filters for order management
3. **Low Stock**: Check regularly and restock
4. **Customer History**: View before processing orders

### For Admins

1. **Dashboard First**: Start day with dashboard overview
2. **Reports**: Check reports for insights
3. **Inventory**: Monitor stock levels
4. **Top Products**: Focus on best sellers
5. **Customer Analytics**: Identify VIP customers

### Keyboard Shortcuts

- Tab: Navigate between fields
- Enter: Submit forms
- Esc: Close dialogs
- Ctrl+F: Search on page

### Best Practices

1. **Regular Backups**: Backup database regularly
2. **Stock Management**: Keep reorder levels updated
3. **Order Processing**: Update status promptly
4. **Customer Service**: Check order notes
5. **Data Quality**: Keep customer info current

## Troubleshooting

### Common Issues

**Can't login?**

- Check username and password
- Use default credentials
- Contact admin

**Cart empty after login?**

- Cart is session-based
- Add items again

**Order not appearing?**

- Refresh page
- Check "Order History"
- Contact staff

**Product out of stock?**

- Check back later
- Contact staff for restock date

**Payment declined?**

- Try different method
- Check information
- Contact support

## Security

### Password Guidelines

- Minimum 6 characters
- Mix letters and numbers
- Change default passwords
- Don't share credentials

### Data Protection

- All passwords encrypted
- Session-based security
- Auto-logout on close
- Secure database

## Getting Help

### Resources

1. README.md - Project overview
2. INSTALLATION.md - Setup guide
3. ARCHITECTURE.md - System details
4. API_DOCUMENTATION.md - Technical docs

### Support

Contact your system administrator for:

- Technical issues
- Account problems
- Feature requests
- Training needs

---

**Happy Shopping/Managing! 🛒**

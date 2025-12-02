# E-Commerce Order Processing System

A comprehensive, full-featured e-commerce order processing and inventory management system built with Python and Streamlit.

## 🚀 Features

### Authentication & User Management

- **Role-Based Access Control**: Admin, Staff, and Customer roles
- **Secure Authentication**: Bcrypt password hashing
- **User Registration & Login**: Complete authentication system
- **Session Management**: Persistent user sessions

### Product Management

- **Product Catalog**: Complete product database with categories
- **Inventory Tracking**: Real-time stock management
- **SKU Management**: Unique product identification
- **Low Stock Alerts**: Automated reorder level monitoring
- **Product CRUD**: Full create, read, update, delete operations
- **Search & Filter**: Advanced product search and category filtering

### Order Processing

- **Shopping Cart**: Add to cart with quantity management
- **Checkout Process**: Complete order placement workflow
- **Order Tracking**: Real-time order status updates
- **Order History**: Customer and staff order views
- **Payment Methods**: Multiple payment options
- **Tax & Shipping**: Automated calculation
- **Order Details**: Comprehensive order information

### Customer Management

- **Customer Database**: Complete customer profiles
- **Customer Analytics**: Purchase history and statistics
- **Top Customers**: Revenue-based customer rankings
- **Customer CRUD**: Full customer management
- **Search Functionality**: Find customers quickly

### Reports & Analytics

- **Sales Reports**: Revenue trends and analytics
- **Product Performance**: Top-selling products analysis
- **Customer Insights**: Customer behavior analytics
- **Inventory Reports**: Stock levels and valuation
- **Visual Charts**: Interactive Plotly visualizations
- **Status Distribution**: Order and payment analytics

### User Interface

- **Responsive Design**: Clean, modern interface
- **No Gradients**: Solid color scheme for clarity
- **Custom Styling**: Professional CSS design
- **Intuitive Navigation**: Role-based sidebar menu
- **Data Tables**: Easy-to-read tabular data
- **Forms**: User-friendly input forms

## 📋 Requirements

```
Python 3.8+
streamlit==1.29.0
pandas==2.1.4
plotly==5.18.0
pillow==10.1.0
python-dateutil==2.8.2
bcrypt==4.1.2
```

## 🛠️ Installation

### 1. Clone or Download the Project

```bash
cd E-Commerce-Order-Processing-System-Python
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 👤 Default User Accounts

### Administrator

- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full system access

### Staff

- **Username**: `staff`
- **Password**: `staff123`
- **Access**: Product, order, and customer management

### Customer

- **Username**: `customer`
- **Password**: `customer123`
- **Access**: Shopping cart and order history

## 📁 Project Structure

```
E-Commerce-Order-Processing-System-Python/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
│
├── config/                     # Configuration files
│   ├── __init__.py
│   ├── config.py              # App configuration & constants
│   └── style.css              # Custom CSS styling
│
├── models/                     # Database models
│   ├── __init__.py
│   ├── database.py            # Database initialization
│   ├── user.py                # User model
│   ├── product.py             # Product model
│   ├── order.py               # Order model
│   └── customer.py            # Customer model
│
├── controllers/                # Business logic controllers
│   ├── __init__.py
│   └── auth.py                # Authentication controller
│
├── views/                      # UI views
│   ├── __init__.py
│   ├── dashboard.py           # Dashboard view
│   ├── products.py            # Product management view
│   ├── orders.py              # Order processing view
│   ├── customers.py           # Customer management view
│   ├── reports.py             # Reports & analytics view
│   └── settings.py            # Settings view
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── session.py             # Session management
│   └── formatters.py          # Data formatting utilities
│
├── data/                       # Database storage
│   └── ecommerce.db           # SQLite database (auto-generated)
│
└── docs/                       # Documentation
    ├── README.md
    ├── INSTALLATION.md
    ├── USER_GUIDE.md
    ├── API_DOCUMENTATION.md
    └── ARCHITECTURE.md
```

## 🎯 Quick Start Guide

### As Administrator/Staff:

1. **Login** with admin credentials
2. **Navigate to Products** to manage inventory
3. **Add Products** using the product form
4. **View Dashboard** for key metrics
5. **Check Reports** for analytics
6. **Manage Customers** in customer section
7. **Process Orders** in order management

### As Customer:

1. **Login** with customer credentials
2. **Browse Products** in the catalog
3. **Add to Cart** with desired quantities
4. **Checkout** with shipping information
5. **View Orders** in order history
6. **Update Profile** in settings

## 🔧 Configuration

Edit `config/config.py` to customize:

- Currency symbol and format
- Tax rate
- Shipping costs
- Free shipping threshold
- Order status options
- Payment methods
- Product categories
- Color scheme

## 📊 Database Schema

### Tables:

- **users**: User accounts and authentication
- **customers**: Customer profiles and information
- **products**: Product catalog and inventory
- **orders**: Order transactions
- **order_items**: Individual order line items
- **inventory_transactions**: Stock movement history

## 🎨 Customization

### Colors

Edit `config/config.py` COLORS dictionary:

- Primary: `#2E86AB`
- Secondary: `#A23B72`
- Success: `#06A77D`
- Warning: `#F18F01`
- Danger: `#C73E1D`

### Styling

Modify `config/style.css` for custom CSS

## 🐛 Troubleshooting

### Database Issues

```bash
# Delete database to reset
rm data/ecommerce.db
# Restart application to recreate
streamlit run app.py
```

### Port Already in Use

```bash
streamlit run app.py --server.port 8502
```

### Dependencies

```bash
pip install --upgrade -r requirements.txt
```

## 📝 License

This project is open-source and available for educational and commercial use.

## 🤝 Support

For issues, questions, or contributions, please contact the system administrator.

## 🔄 Version History

- **v1.0.0** - Initial release with full features

---

**Built with ❤️ using Python & Streamlit**

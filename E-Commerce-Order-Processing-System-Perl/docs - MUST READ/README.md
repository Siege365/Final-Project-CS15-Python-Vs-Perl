# E-Commerce Order Processing System (Perl)

A comprehensive, full-featured e-commerce order processing system built with Perl and the Mojolicious web framework. This system provides complete product management, order processing, customer management, and analytics capabilities.

## 🚀 Features

### Core Functionality

- **User Authentication**: Secure login/logout with bcrypt password hashing
- **Role-Based Access Control**: Three user roles (admin, staff, customer)
- **Product Management**: Complete CRUD operations with inventory tracking
- **Shopping Cart**: Session-based cart with real-time calculations
- **Order Processing**: Full checkout process with order tracking
- **Customer Management**: Customer profiles and analytics
- **Reports & Analytics**: Sales reports, customer insights, inventory reports

### Product Features

- Product catalog with categories
- Search and filter functionality
- Stock level tracking with low-stock alerts
- Product images support
- SKU management
- Category-based browsing

### Order Features

- Shopping cart functionality
- Tax and shipping calculations
- Multiple payment methods
- Order status tracking (6 statuses)
- Order history
- Inventory updates on order placement

### Customer Features

- Customer profiles
- Order history
- Customer analytics
- Top customers ranking

## 📋 Requirements

- **Perl**: 5.30 or higher
- **CPAN Modules**:
  - Mojolicious >= 9.0
  - DBI >= 1.643
  - DBD::SQLite >= 1.70
  - Crypt::Bcrypt >= 0.011
  - JSON >= 4.0
  - Time::Piece >= 1.33

## 🛠️ Installation

### 1. Install Perl

Ensure Perl is installed on your system:

```bash
perl --version
```

### 2. Install cpanm (CPAN Minus)

```bash
cpan App::cpanminus
```

### 3. Clone or Download Project

```bash
cd E-Commerce-Order-Processing-System-Perl
```

### 4. Install Dependencies

```bash
cpanm --installdeps .
```

Or install manually:

```bash
cpanm Mojolicious DBI DBD::SQLite Crypt::Bcrypt JSON Time::Piece
```

### 5. Initialize Database

The database will be automatically initialized on first run with sample data.

### 6. Run Application

```bash
perl app.pl daemon
```

Or for production with Hypnotoad:

```bash
hypnotoad app.pl
```

### 7. Access Application

Open your browser to: **http://localhost:3000**

## 🔑 Default Accounts

| Role     | Username | Password    |
| -------- | -------- | ----------- |
| Admin    | admin    | admin123    |
| Staff    | staff    | staff123    |
| Customer | customer | customer123 |

## 📁 Project Structure

```
E-Commerce-Order-Processing-System-Perl/
│
├── app.pl                          # Main application entry point
├── cpanfile                        # Perl dependencies
│
├── lib/
│   └── ECommerce/
│       ├── Config.pm               # Configuration module
│       ├── Database.pm             # Database initialization
│       │
│       ├── Models/
│       │   ├── User.pm             # User model
│       │   ├── Product.pm          # Product model
│       │   ├── Order.pm            # Order model
│       │   └── Customer.pm         # Customer model
│       │
│       └── Controllers/
│           └── Auth.pm             # Authentication controller
│
├── templates/
│   ├── layouts/
│   │   └── default.html.ep         # Main layout template
│   │
│   ├── login.html.ep               # Login page
│   ├── register.html.ep            # Registration page
│   ├── dashboard.html.ep           # Dashboard view
│   ├── products.html.ep            # Product catalog
│   ├── cart.html.ep                # Shopping cart
│   ├── orders.html.ep              # Order list
│   ├── order_detail.html.ep        # Order details
│   ├── customers.html.ep           # Customer management
│   └── reports.html.ep             # Reports & analytics
│
├── public/
│   └── css/
│       └── style.css               # Application styles (NO GRADIENTS)
│
├── data/
│   └── ecommerce.db                # SQLite database (auto-generated)
│
└── docs/
    ├── README.md                   # This file
    ├── INSTALLATION.md             # Detailed installation guide
    ├── USER_GUIDE.md               # User manual
    ├── ARCHITECTURE.md             # System architecture
    ├── API_DOCUMENTATION.md        # API reference
    ├── PROJECT_SUMMARY.md          # Project summary
    └── FILE_LISTING.md             # Complete file listing
```

## 🎨 Design Philosophy

- **No Gradients**: All colors are solid - clean, professional design
- **Responsive**: Mobile-friendly design
- **User-Friendly**: Intuitive interface for all user roles
- **Modular**: Well-organized code structure
- **Documented**: Comprehensive inline and external documentation

## 🔧 Configuration

Edit `lib/ECommerce/Config.pm` to customize:

- Database path
- Tax rate (default: 8%)
- Shipping rate (default: $5.00)
- Free shipping threshold (default: $100.00)
- Currency settings
- Items per page
- Color scheme

## 💾 Database Schema

### Tables:

1. **users** - User authentication and roles
2. **customers** - Customer information
3. **products** - Product catalog
4. **orders** - Order records
5. **order_items** - Order line items
6. **inventory_transactions** - Inventory tracking

See `docs/ARCHITECTURE.md` for detailed schema.

## 🚦 Quick Start

1. **Install dependencies**: `cpanm --installdeps .`
2. **Run application**: `perl app.pl daemon`
3. **Login**: Go to http://localhost:3000
4. **Browse products**: Navigate to Products page
5. **Add to cart**: Select products and add to cart
6. **Checkout**: Complete purchase
7. **View orders**: Check your order history

## 📊 Features by Role

### Customer

- Browse product catalog
- Search and filter products
- Add products to cart
- Place orders
- View order history
- Manage profile

### Staff

- All customer features
- View all orders
- Manage customers
- View reports and analytics

### Admin

- All staff features
- Full system access
- User management
- Complete analytics

## 🔒 Security Features

- **Password Hashing**: Bcrypt with cost factor 10
- **Session Management**: Secure session handling
- **Role-Based Access**: Enforced at controller level
- **SQL Injection Protection**: Prepared statements
- **Input Validation**: Server-side validation

## 📈 Sample Data

The system includes:

- 3 default users (admin, staff, customer)
- 5 sample customers
- 20 sample products across 10 categories
- Pre-configured settings

## 🐛 Troubleshooting

### Database Issues

```bash
# Remove database and restart
rm data/ecommerce.db
perl app.pl daemon
```

### Module Installation Issues

```bash
# Force install
cpanm --force DBD::SQLite
```

### Port Already in Use

Edit `app.pl` and change the port:

```perl
app->config(hypnotoad => {
    listen => ['http://*:3001'],  # Change to different port
    ...
});
```

## 📚 Documentation

- **Installation Guide**: `docs/INSTALLATION.md`
- **User Guide**: `docs/USER_GUIDE.md`
- **Architecture**: `docs/ARCHITECTURE.md`
- **API Reference**: `docs/API_DOCUMENTATION.md`
- **Project Summary**: `docs/PROJECT_SUMMARY.md`

## 🤝 Contributing

This is an educational project. Feel free to:

- Report bugs
- Suggest features
- Submit improvements

## 📝 License

This project is provided as-is for educational purposes.

## 👨‍💻 Technical Stack

- **Language**: Perl 5.30+
- **Web Framework**: Mojolicious
- **Database**: SQLite
- **Password Hashing**: Crypt::Bcrypt
- **Templating**: Embedded Perl (EP)
- **CSS**: Custom (no frameworks, no gradients)

## 📞 Support

For issues or questions:

1. Check the documentation in `docs/`
2. Review the troubleshooting section
3. Examine the code comments
4. Check Mojolicious documentation

## 🎯 Future Enhancements

- Product images upload
- Email notifications
- Payment gateway integration
- Advanced search
- Export functionality
- Multi-language support
- API endpoints for mobile apps

---

**Version**: 1.0.0  
**Last Updated**: December 2, 2025  
**Built with**: Perl & Mojolicious

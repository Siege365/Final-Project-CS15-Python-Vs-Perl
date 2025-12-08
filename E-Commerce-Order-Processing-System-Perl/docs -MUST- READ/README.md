# ShopPerl – E‑Commerce with a Perl‑sonality (Perl)

A compact, practical e‑commerce order processing system implemented in Perl with the Mojolicious web framework. The project includes product management, a session-based shopping cart, order checkout, customer management and basic analytics. The documentation reflects recent UX updates: the site uses a lightweight in-page toast for Add‑to‑Cart confirmations and the cart badge counts distinct products.

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
- **CPAN Modules** (example):
  - Mojolicious >= 9.0
  - DBI >= 1.643
  - DBD::SQLite >= 1.70
  - Crypt::Bcrypt >= 0.011
  - JSON
  - Time::Piece

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

The database is initialized automatically on first run. The initialization code lives in `lib/ECommerce/Database.pm` and will create `data/ecommerce.db` with sample users, customers and products when the application is started.

### 6. Run Application (Development)

From the project root run the Mojolicious development server:

```powershell
perl app.pl daemon
```

For a production-ready multi-worker server use Hypnotoad:

```powershell
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
ShopPerl/ (E-Commerce-Order-Processing-System-Perl)
│
├── app.pl                          # Main application entry point (loads helpers, sessions and routes)
├── cpanfile                        # Perl dependencies
├── routes/                         # Route files (shared_routes.pl, admin_routes.pl, customer_routes.pl)
├── lib/ECommerce/                  # Application Perl modules
│   ├── Config.pm
│   ├── Database.pm                  # DB initialization & sample data
│   ├── Models/                      # Product, User, Order, Customer models
│   └── Controllers/                 # Controller classes (Auth, Customer, Admin)
├── templates/                       # Embedded Perl templates (layouts + pages)
├── public/                          # Static assets (css, js, images)
│   ├── css/
│   ├── js/
│   └── images/                      # e.g. placeholder.svg
├── data/                            # SQLite database file `ecommerce.db` (auto-created)
└── docs/                            # Project documentation (this folder)
```

## 🎨 Design Philosophy

- **No Gradients**: Solid colors only
- **Responsive**: Mobile-friendly layout and a functional mobile hamburger menu
- **User-Friendly**: Simple, non-blocking feedback (Add-to-Cart uses in-page toast)
- **Modular**: Clear separation of routes, controllers, models and templates
- **Documented**: Comprehensive inline and external documentation

## 🔧 Configuration

Edit `lib/ECommerce/Config.pm` to customize runtime settings, for example:

- Database path
- Tax rate (default: 8%)
- Shipping rate (default: $5.00)
- Free shipping threshold (default: $100.00)
- Currency settings
- Items per page
- Color scheme

Other runtime options (session timeout, secrets) are set in `app.pl`.

## 💾 Database Schema

The application uses SQLite and creates these tables on first run (see `lib/ECommerce/Database.pm` and `docs/ARCHITECTURE.md`):

1. **users** - User authentication and roles
2. **customers** - Customer information
3. **products** - Product catalog (includes `image_url`)
4. **orders** - Order records
5. **order_items** - Order line items
6. **inventory_transactions** - Inventory tracking

Note: Product records include `image_url`; the app supplies a `public/images/placeholder.svg` when an image is missing.

## 🚦 Quick Start

1. Install dependencies: `cpanm --installdeps .`
2. Run application: `perl app.pl daemon`
3. Open `http://localhost:3000` in your browser
4. Browse products and add items to cart (Add-to-Cart uses AJAX with an in-page toast)
5. Checkout and view order history

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

- Product image upload and management UI
- Email notifications
- Payment gateway integration
- Advanced search and filters
- Export functionality and reporting
- Internationalization and localization
- API endpoints for mobile apps

---

**Version**: 1.0.0  
**Last Updated**: December 8, 2025  
**Built with**: Perl & Mojolicious

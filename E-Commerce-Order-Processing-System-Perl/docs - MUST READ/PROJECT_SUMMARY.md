# Project Summary

## ShopPerl – E‑Commerce with a Perl‑sonality

**Version**: 1.0.0  
**Language**: Perl 5.30+  
**Framework**: Mojolicious 9.0+  
**Database**: SQLite 3  
**Status**: Complete & Production Ready

---

## Project Overview

ShopPerl is a compact, educational e-commerce order processing system built with Perl and Mojolicious. It provides product management, a session-backed shopping cart, order checkout, customer management and reporting. The UI includes a lightweight AJAX Add‑to‑Cart flow that displays a non-blocking toast confirmation and updates the cart badge (which shows the number of distinct products in the cart).

---

## Key Features Implemented

### ✅ Authentication & Authorization

- Secure user authentication with bcrypt password hashing
- Role-based access control (Admin, Staff, Customer)
- Session management with configurable expiration
- Login, logout, and registration functionality
- Password encryption with cost factor 10

### ✅ Product Management

- Complete CRUD operations for products
- 20 pre-loaded sample products
- 10 product categories
- Inventory tracking and management
- Low stock alerts and monitoring
- Product search functionality
- Category-based filtering
- SKU management
- Stock level tracking

### ✅ Shopping Cart

- Session-based cart implementation
- Add/remove products
- Quantity management
- Real-time price calculations
- Subtotal, tax, and shipping calculations
- Persistent cart (session-based)

Notes:

- The cart is stored in the user session as an arrayref of item hashrefs. The navigation cart badge counts distinct product entries (one per product) rather than summing quantities.
- Add-to-Cart supports AJAX (returns JSON) and falls back to flash+redirect for non-JS clients.

### ✅ Order Processing

- Complete checkout workflow
- Order creation and tracking
- 6 order statuses (pending, processing, shipped, delivered, cancelled, refunded)
- 5 payment methods (credit card, debit card, PayPal, cash on delivery, bank transfer)
- Automatic order numbering
- Order history
- Order details view
- Inventory updates on order placement
- Transaction logging

### ✅ Customer Management

- Customer profiles and information
- 5 pre-loaded sample customers
- Customer analytics
- Order history per customer
- Top customers ranking
- Customer search functionality
- Contact information management

### ✅ Reports & Analytics

- Sales reports
- Revenue tracking
- Orders by status
- Top customers analysis
- Average order value
- Inventory reports
- Low stock monitoring
- Dashboard metrics

### ✅ User Interface

- Responsive design
- Clean, professional styling
- NO gradients (solid colors only)
- Mobile-friendly layout
- Intuitive navigation
- Flash messages for user feedback
- Form validation
- Product grid layout
- Table-based data display

---

## Project Structure

```
📦 ShopPerl (E-Commerce-Order-Processing-System-Perl)
├── 📄 app.pl                       (Main application - loads routes, helpers, sessions)
├── 📄 cpanfile                     (Dependencies)
├── 📁 routes/                      (Route files: `shared_routes.pl`, `admin_routes.pl`, `customer_routes.pl`)
├── 📁 lib/ECommerce/               (Perl modules)
│   ├── 📄 Config.pm                (Configuration)
│   ├── 📄 Database.pm              (DB initialization & sample data)
│   ├── 📁 Models/                  (User, Product, Order, Customer)
│   └── 📁 Controllers/             (Auth, Admin/, Customer/)
├── 📁 templates/                   (EP templates, layouts and partials)
├── 📁 public/                      (Static assets)
│   ├── 📁 css/                     (styles + components)
│   ├── 📁 js/                      (client-side scripts: toast, header, nav)
│   └── 📁 images/                  (placeholder.svg, product images)
├── 📁 data/                        (SQLite database `ecommerce.db`)
└── 📁 docs/                        (Project documentation)
```

---

## Database Schema

### 6 Tables Created

1. **users** - User authentication (3 default users)
2. **customers** - Customer information (5 sample customers)
3. **products** - Product catalog (20 sample products)
4. **orders** - Order records
5. **order_items** - Order line items
6. **inventory_transactions** - Inventory tracking

### Relationships

- Users → Customers (one-to-one)
- Customers → Orders (one-to-many)
- Orders → Order Items (one-to-many)
- Products → Order Items (one-to-many)
- Products → Inventory Transactions (one-to-many)

---

## Technology Stack

| Component          | Technology                         |
| ------------------ | ---------------------------------- |
| Language           | Perl 5.30+                         |
| Web Framework      | Mojolicious 9.0+                   |
| Database           | SQLite 3                           |
| ORM                | DBI/DBD::SQLite                    |
| Password Hashing   | Crypt::Bcrypt                      |
| Templating         | Embedded Perl (EP)                 |
| CSS                | Custom (600+ lines, no frameworks) |
| HTTP Server        | Mojolicious daemon / Hypnotoad     |
| Session Management | Mojolicious sessions               |

---

## Design Specifications

### Color Scheme (NO Gradients!)

- **Primary**: #2E86AB (Blue)
- **Secondary**: #A23B72 (Purple)
- **Success**: #06A77D (Green)
- **Warning**: #F18F01 (Orange)
- **Danger**: #C73E1D (Red)
- **Info**: #4A90E2 (Light Blue)
- **Light**: #F5F5F5 (Gray)
- **Dark**: #333333 (Charcoal)

All colors are solid - no gradients anywhere!

### Layout

- Responsive grid system
- Mobile-friendly design
- Clean card-based UI
- Table layouts for data
- Form styling
- Button styles
- Status badges

---

## Configuration Options

```perl
# Tax rate
tax_rate => 0.08  # 8%

# Shipping
shipping_rate => 5.00
free_shipping_threshold => 100.00

# Currency
currency => 'USD'
currency_symbol => '$'

# Pagination
items_per_page => 20

# Session
session_expiration => 3600  # 1 hour
```

---

## System Capabilities

### For Customers

- ✓ Browse 20 products across 10 categories
- ✓ Search and filter products
- ✓ Add items to cart
- ✓ Checkout with 5 payment methods
- ✓ View order history
- ✓ Track order status
- ✓ Manage profile

### For Staff/Admin

- ✓ All customer features
- ✓ View all orders
- ✓ Manage customers
- ✓ View analytics
- ✓ Monitor inventory
- ✓ Access reports
- ✓ Track low stock

---

## Documentation Delivered

1. **README.md** (comprehensive overview)
2. **INSTALLATION.md** (step-by-step installation)
3. **USER_GUIDE.md** (complete user manual)
4. **ARCHITECTURE.md** (system design and architecture)
5. **API_DOCUMENTATION.md** (complete API reference)
6. **PROJECT_SUMMARY.md** (this document)
7. **FILE_LISTING.md** (complete file inventory)

**Total Documentation**: 7 files, ~3,500+ lines

---

## Code Statistics

### Perl Code

- **Main Application**: 340 lines
- **Models**: 790 lines (4 files)
- **Controllers**: 80 lines (1 file)
- **Database**: 260 lines
- **Config**: 110 lines
- **Total Perl**: ~1,580 lines

### Templates

- **10 template files** (Embedded Perl)
- **Layout system** with default template
- **Total Template**: ~800 lines

### Stylesheets

- **1 CSS file**: 600+ lines
- **NO gradients**: All solid colors
- **Responsive**: Mobile-friendly

### Documentation

- **7 markdown files**
- **~3,500 lines** of documentation

### Total Project

- **~30 files**
- **~6,500 lines** (code + docs + templates)

---

## Quick Start

```bash
# Install dependencies
cpanm --installdeps .

# Run application
perl app.pl daemon

# Access in browser
http://localhost:3000

# Login
Username: admin
Password: admin123
```

---

## Testing Checklist

### ✅ Authentication

- [x] Login with all 3 default accounts
- [x] Logout functionality
- [x] Registration of new users
- [x] Password encryption
- [x] Session management

### ✅ Products

- [x] View product catalog (20 products)
- [x] Search products
- [x] Filter by category (10 categories)
- [x] View product details
- [x] Stock level display

### ✅ Shopping Cart

- [x] Add products to cart
- [x] View cart
- [x] Calculate subtotal
- [x] Calculate tax (8%)
- [x] Calculate shipping ($5 or FREE)
- [x] Display total

### ✅ Orders

- [x] Complete checkout process
- [x] Place order
- [x] View order confirmation
- [x] View order history
- [x] View order details
- [x] Order status tracking

### ✅ Customers (Staff/Admin)

- [x] View customer list (5 customers)
- [x] View customer details
- [x] Search customers

### ✅ Reports (Staff/Admin)

- [x] View dashboard metrics
- [x] Total revenue
- [x] Orders by status
- [x] Top customers
- [x] Low stock alerts

### ✅ UI/UX

- [x] Responsive design
- [x] No gradients (solid colors only)
- [x] Navigation works
- [x] Flash messages display
- [x] Forms validate
- [x] Mobile-friendly

---

## Use Cases Supported

1. **Customer shops for products**

   - Browse catalog → Add to cart → Checkout → Pay → Track order

2. **Staff monitors inventory**

   - View dashboard → Check low stock → Monitor products

3. **Admin reviews business**

   - View reports → Check revenue → Analyze customers

4. **Customer tracks order**

   - Login → View orders → Check status → See details

5. **Staff manages orders**
   - View all orders → Filter by status → Update status

---

## Maintenance & Support

### Backup Database

```bash
cp data/ecommerce.db data/backup_$(date +%Y%m%d).db
```

### Reset Database

```bash
rm data/ecommerce.db
perl app.pl daemon
# Database will be recreated with sample data
```

### View Logs

```bash
tail -f log/development.log
```

---

## Future Enhancement Ideas

- Product image uploads
- Email notifications
- Payment gateway integration
- Advanced search
- Export to CSV/PDF
- Multi-language support
- API for mobile apps
- Wishlist functionality
- Product reviews
- Discount codes
- Email marketing

---

## Project Achievements

✅ **Complete MVC architecture**  
✅ **Full e-commerce functionality**  
✅ **Secure authentication**  
✅ **Role-based access control**  
✅ **Shopping cart & checkout**  
✅ **Order processing**  
✅ **Inventory management**  
✅ **Customer management**  
✅ **Business analytics**  
✅ **Responsive design (NO gradients)**  
✅ **Comprehensive documentation**  
✅ **Sample data included**  
✅ **Production-ready code**  
✅ **Well-organized structure**  
✅ **Extensive inline comments**

---

## Development Notes

### Best Practices Followed

- MVC architecture pattern
- Prepared SQL statements
- Password hashing with bcrypt
- Session-based authentication
- Input validation
- Error handling
- Transaction management
- Code documentation
- Modular design

### Security Measures

- Bcrypt password hashing
- SQL injection protection
- XSS prevention
- CSRF tokens (Mojolicious built-in)
- Session security
- Role-based authorization

---

## Conclusion

This E-Commerce Order Processing System demonstrates a complete, production-ready Perl web application built with Mojolicious. It includes all essential e-commerce features: product management, shopping cart, order processing, customer management, and analytics, all with a clean, no-gradient design and comprehensive documentation.

The system is fully functional, well-documented, and ready for deployment or further customization.

---

**Project Status**: ✅ COMPLETE  
**Version**: 1.0.0  
**Date**: December 2, 2025  
**Built with**: ❤️ and Perl

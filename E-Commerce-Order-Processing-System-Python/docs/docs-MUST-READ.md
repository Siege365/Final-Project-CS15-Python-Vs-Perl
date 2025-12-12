# ShopPy - E-Commerce Order Processing System (Python/Django)

**Wrapped in code, packed with deals.**

## 📋 Overview

ShopPy is a complete e-commerce order processing system built with Python and Django. This project is a full-featured 1-to-1 port of the original Perl-based E-Commerce Order Processing System, featuring comprehensive product management, customer accounts, shopping cart functionality, and administrative order management.

### Key Features

- 🛍️ **Product Catalog**: Browse, search, and filter products with detailed product pages
- 🛒 **Shopping Cart**: Session-based cart management with real-time updates
- 👤 **Customer Accounts**: User registration, login, profile management, and order history
- 📦 **Order Management**: Complete order tracking, status updates, and delivery information
- 👨‍💼 **Admin Dashboard**: Comprehensive administrative interface for managing products, orders, customers, and reports
- 📊 **Reporting**: Sales reports, product analytics, customer insights, and revenue tracking
- 💳 **Checkout Flow**: Streamlined multi-step checkout with shipping and tax calculations
- 🔐 **Security**: Session-based authentication with bcrypt password hashing
- 📱 **Responsive Design**: Mobile-first CSS architecture with breakpoints for all devices

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- SQLite3 (included with Python)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd E-Commerce-Order-Processing-System-Python
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://localhost:8000`

## 📁 Project Structure

```
E-Commerce-Order-Processing-System-Python/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # SQLite database
├── lib/
│   └── ECommerce/              # Main Django app
│       ├── models.py           # Database models (User, Customer, Product, Order)
│       ├── views.py            # View functions
│       ├── urls.py             # URL routing
│       ├── wsgi.py             # WSGI configuration
│       ├── Auth.py             # Authentication utilities
│       ├── Database.py         # Database helpers
│       ├── Config.py           # Configuration settings
│       ├── context_processors.py
│       ├── Controllers/        # View controllers
│       │   ├── shared_routes.py
│       │   ├── admin_routes.py
│       │   └── customer_routes.py
│       └── Models/            # ORM models
│           ├── User.py
│           ├── Customer.py
│           ├── Product.py
│           └── Order.py
├── templates/                  # Django HTML templates
│   ├── layouts/               # Base layouts
│   │   ├── default.html
│   │   └── auth.html
│   ├── customer/              # Customer pages
│   │   ├── dashboard_customer.html
│   │   ├── products_customer.html
│   │   ├── cart.html
│   │   ├── orders_customer.html
│   │   ├── order_detail_customer.html
│   │   └── account.html
│   └── admin/                 # Admin pages
│       ├── dashboard_admin.html
│       ├── products_admin.html
│       ├── product_add.html
│       ├── product_edit.html
│       ├── orders_admin.html
│       ├── order_detail_admin.html
│       ├── customers.html
│       └── reports.html
├── public/                    # Static files
│   ├── css/                   # Stylesheets
│   │   ├── style.css          # Main stylesheet
│   │   ├── base/              # Base styles
│   │   │   ├── reset.css
│   │   │   ├── variables.css
│   │   │   └── typography.css
│   │   ├── layout/            # Layout components
│   │   │   ├── header.css
│   │   │   ├── footer.css
│   │   │   ├── sidebar.css
│   │   │   └── navigation.css
│   │   ├── components/        # Reusable components
│   │   │   ├── buttons.css
│   │   │   ├── cards.css
│   │   │   ├── forms.css
│   │   │   ├── tables.css
│   │   │   ├── modals.css
│   │   │   └── alerts.css
│   │   ├── pages/             # Page-specific styles
│   │   │   ├── auth.css
│   │   │   ├── dashboard.css
│   │   │   ├── products.css
│   │   │   ├── cart.css
│   │   │   ├── orders.css
│   │   │   └── reports.css
│   │   └── utilities/         # Utility classes
│   │       ├── helpers.css
│   │       ├── animations.css
│   │       └── responsive.css
│   └── images/                # SVG assets
│       ├── logo.svg
│       ├── icons.svg
│       ├── login-illustration.svg
│       ├── empty-cart.svg
│       ├── empty-orders.svg
│       └── no-products.svg
└── docs/                      # Documentation
```

## 🗄️ Database Models

### User Model

- `id`: Primary key
- `email`: Unique email address
- `password`: Hashed password (bcrypt)
- `is_admin`: Admin flag
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Customer Model

- `user`: Foreign key to User
- `first_name`: Customer's first name
- `last_name`: Customer's last name
- `phone`: Contact phone number
- `address`: Shipping/billing address
- `city`: City
- `state`: State/Province
- `zip_code`: Postal code
- `country`: Country
- `created_at`: Registration date
- `updated_at`: Last update date

### Product Model

- `id`: Primary key
- `sku`: Stock Keeping Unit (unique)
- `name`: Product name
- `description`: Product description
- `price`: Product price
- `quantity`: Available stock quantity
- `category`: Product category
- `is_active`: Availability flag
- `created_at`: Creation date
- `updated_at`: Last update date

### Order Model

- `id`: Primary key
- `customer`: Foreign key to Customer
- `order_number`: Unique order number
- `status`: Order status (pending, processing, shipped, delivered, cancelled)
- `subtotal`: Sum of item prices
- `tax`: Tax amount
- `shipping`: Shipping cost
- `total`: Final order total
- `shipping_address`: Delivery address
- `tracking_number`: Carrier tracking number
- `notes`: Order notes
- `created_at`: Order date
- `updated_at`: Last status update

### OrderItem Model

- `order`: Foreign key to Order
- `product`: Foreign key to Product
- `quantity`: Items ordered
- `unit_price`: Price per item at order time
- `total_price`: Line item total

## 🎨 CSS Architecture

The CSS system is organized into modular, reusable files with a clear hierarchy:

### Base CSS (`public/css/base/`)

- **reset.css**: Browser reset and normalization
- **variables.css**: CSS custom properties (colors, spacing, typography, shadows)
- **typography.css**: Font definitions and text styles

### Layout CSS (`public/css/layout/`)

- **header.css**: Navigation header with logo and user menu
- **footer.css**: Footer with company info and links
- **sidebar.css**: Admin sidebar navigation
- **navigation.css**: Breadcrumbs, tabs, pagination, steps

### Component CSS (`public/css/components/`)

- **buttons.css**: Button variants (primary, secondary, danger, etc.)
- **cards.css**: Card containers with consistent styling
- **forms.css**: Form inputs, labels, and validation styles
- **tables.css**: Data table styles with responsive support
- **modals.css**: Modal dialogs and overlays
- **alerts.css**: Alert messages and toast notifications

### Page CSS (`public/css/pages/`)

- **auth.css**: Login and registration page styles
- **dashboard.css**: Admin and customer dashboard layouts
- **products.css**: Product grid and detail page styles
- **cart.css**: Shopping cart and checkout flows
- **orders.css**: Order list and detail pages
- **reports.css**: Analytics and reporting pages

### Utilities CSS (`public/css/utilities/`)

- **helpers.css**: Utility classes for layout, spacing, text, colors
- **animations.css**: Keyframe animations and transitions
- **responsive.css**: Media query utilities and responsive patterns

### CSS Variables

```css
/* Colors */
--primary-color: #6366f1          /* Indigo */
--primary-light: #818cf8
--primary-lighter: #e0e7ff
--primary-dark: #4f46e5

--success-color: #10b981          /* Green */
--error-color: #ef4444            /* Red */
--warning-color: #f59e0b           /* Amber */
--info-color: #3b82f6             /* Blue */

/* Spacing (8px base unit) */
--space-1: 0.25rem (4px)
--space-2: 0.5rem (8px)
--space-3: 0.75rem (12px)
--space-4: 1rem (16px)
--space-5: 1.25rem (20px)
--space-6: 1.5rem (24px)
--space-8: 2rem (32px)

/* Typography */
--font-size-xs: 0.75rem (12px)
--font-size-sm: 0.875rem (14px)
--font-size-base: 1rem (16px)
--font-size-lg: 1.125rem (18px)
--font-size-xl: 1.25rem (20px)

--font-weight-normal: 400
--font-weight-medium: 500
--font-weight-semibold: 600
--font-weight-bold: 700

/* Layout */
--header-height: 64px
--sidebar-width: 280px
--container-xl: 1280px

/* Shadows */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05)
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1)
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1)

/* Border Radius */
--radius-sm: 0.25rem
--radius-md: 0.375rem
--radius-lg: 0.5rem
--radius-xl: 0.75rem
--radius-full: 9999px

/* Transitions */
--transition-fast: 150ms ease
--transition-normal: 300ms ease
```

## 🔒 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **Session Management**: Django session framework for authentication
- **CSRF Protection**: Built-in Django CSRF middleware
- **SQL Injection Prevention**: Django ORM parameterized queries
- **XSS Prevention**: Django template auto-escaping
- **Admin Interface**: Role-based access control (admin vs. customer)

## ⚙️ Configuration

Edit `lib/ECommerce/Config.py` to customize:

```python
# Tax calculation
TAX_RATE = 0.08  # 8% sales tax

# Shipping
SHIPPING_RATE = 5.00              # Base shipping cost
FREE_SHIPPING_THRESHOLD = 100.00  # Free shipping above $100

# Pagination
ITEMS_PER_PAGE = 20

# Currency
CURRENCY = "USD"
CURRENCY_SYMBOL = "$"
```

## 🌐 Responsive Design

The CSS system includes responsive utilities for all breakpoints:

```
Mobile-first approach:
- Mobile: < 640px (default)
- Small tablet: 640px - 767px (sm)
- Tablet: 768px - 1023px (md)
- Desktop: 1024px - 1279px (lg)
- Large desktop: 1280px+ (xl)
```

### Responsive Classes

```html
<!-- Display utilities -->
<div class="d-none md:d-block">Hidden on mobile</div>

<!-- Grid columns -->
<div class="grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  <!-- 1 col mobile, 2 cols tablet, 3 cols desktop -->
</div>

<!-- Text alignment -->
<p class="text-center md:text-left">Centered on mobile</p>

<!-- Spacing -->
<div class="p-4 md:p-6 lg:p-8">Responsive padding</div>
```

## 🎯 Features Implementation

### Customer Features

- ✅ User registration and login
- ✅ Product browsing and search
- ✅ Shopping cart management
- ✅ Checkout with address and payment info
- ✅ Order history and tracking
- ✅ Account profile management
- ✅ Order status notifications

### Admin Features

- ✅ Product management (CRUD)
- ✅ Inventory tracking
- ✅ Order management and fulfillment
- ✅ Customer management
- ✅ Sales reports and analytics
- ✅ Dashboard with key metrics
- ✅ Export capabilities

## 📊 Business Logic

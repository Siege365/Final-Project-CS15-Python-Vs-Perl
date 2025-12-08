# Complete File Listing

## E-Commerce Order Processing System - Perl

**Generated**: December 2, 2025  
**Version**: 1.0.0

---

## Directory Structure with File Details

### Root Directory

#### app.pl (340 lines)

- **Purpose**: Main application entry point
- **Type**: Perl/Mojolicious application
- **Features**:
  - Route definitions (15 routes)
  - Authentication middleware
  - Session helpers
  - Request handlers
  - Shopping cart logic
  - Order checkout process
  - Product catalog
  - Customer management
  - Reports and analytics
- **Dependencies**: All models, controllers, Config.pm

#### cpanfile (12 lines)

- **Purpose**: Perl dependency management
- **Modules**:
  - Mojolicious >= 9.0
  - DBI >= 1.643
  - DBD::SQLite >= 1.70
  - Crypt::Bcrypt >= 0.011
  - JSON >= 4.0
  - Time::Piece >= 1.33
  - File::Basename, File::Spec
  - Digest::SHA, MIME::Base64
  - Data::Dumper, List::Util

---

### lib/ECommerce/ Directory

#### Config.pm (110 lines)

- **Purpose**: Application configuration module
- **Package**: ECommerce::Config
- **Contents**:
  - BASE_DIR, DB_PATH
  - %APP_CONFIG (currency, tax, shipping, pagination)
  - @ORDER_STATUS (6 statuses)
  - @PAYMENT_METHODS (5 methods)
  - @PRODUCT_CATEGORIES (10 categories)
  - @USER_ROLES (3 roles)
  - %COLORS (8 solid colors, NO gradients)
- **Documentation**: POD format

#### Database.pm (260 lines)

- **Purpose**: Database initialization and management
- **Package**: ECommerce::Database
- **Methods**:
  - new() - Constructor
  - connect() - Database connection
  - initialize_database() - Full setup
  - create_tables() - Schema creation
  - create_sample_data() - Populate data
- **Features**:
  - Creates 6 tables
  - Loads 3 default users
  - Loads 5 sample customers
  - Loads 20 sample products
  - SQLite with foreign keys
- **Documentation**: POD format

---

### lib/ECommerce/Models/ Directory

#### User.pm (140 lines)

- **Purpose**: User authentication and management
- **Package**: ECommerce::Models::User
- **Methods**:
  - create_user() - Create new user
  - get_user_by_username() - Retrieve by username
  - get_user_by_id() - Retrieve by ID
  - verify_password() - bcrypt verification
  - update_last_login() - Update timestamp
  - get_all_users() - List all users
  - update_user_role() - Change role
  - deactivate_user() - Disable account
- **Security**: Bcrypt cost factor 10
- **Documentation**: POD format

#### Product.pm (200 lines)

- **Purpose**: Product inventory management
- **Package**: ECommerce::Models::Product
- **Methods**:
  - create_product() - Create product
  - get_all_products() - List products
  - get_product_by_id() - Retrieve by ID
  - get_product_by_sku() - Retrieve by SKU
  - update_product() - Update fields
  - delete_product() - Soft delete
  - update_stock() - Inventory management
  - get_low_stock_products() - Alert system
  - search_products() - Search functionality
  - get_products_by_category() - Filter by category
  - get_categories() - List categories
- **Features**: Full CRUD, inventory tracking
- **Documentation**: POD format

#### Order.pm (280 lines)

- **Purpose**: Order processing and management
- **Package**: ECommerce::Models::Order
- **Methods**:
  - generate_order_number() - Unique ID
  - create_order() - Create order with items
  - create_order_from_cart() - Cart checkout
  - get_all_orders() - List all orders
  - get_order_by_id() - Retrieve by ID
  - get_order_items() - Get line items
  - update_order_status() - Status updates
  - get_orders_by_customer() - Customer orders
  - get_orders_by_status() - Filter by status
  - get_recent_orders() - Recent orders
  - get_order_stats() - Analytics
  - search_orders() - Search functionality
- **Features**: Transaction management, stock updates
- **Documentation**: POD format

#### Customer.pm (170 lines)

- **Purpose**: Customer data management
- **Package**: ECommerce::Models::Customer
- **Methods**:
  - create_customer() - Create customer
  - get_all_customers() - List all
  - get_customer_by_id() - Retrieve by ID
  - get_customer_by_user_id() - Link to user
  - update_customer() - Update fields
  - delete_customer() - Remove customer
  - search_customers() - Search functionality
  - get_customer_stats() - Customer analytics
  - get_top_customers() - Top spenders
- **Features**: Full CRUD, analytics
- **Documentation**: POD format

---

### lib/ECommerce/Controllers/ Directory

#### Auth.pm (80 lines)

- **Purpose**: Authentication and authorization controller
- **Package**: ECommerce::Controllers::Auth
- **Methods**:
  - login() - User authentication
  - register() - User registration
  - is_admin() - Admin check
  - is_staff() - Staff check
  - is_customer() - Customer check
- **Features**: Password verification, role checks
- **Documentation**: POD format

---

### templates/ Directory

#### layouts/default.html.ep (60 lines)

- **Purpose**: Main layout template
- **Type**: Embedded Perl template
- **Features**:
  - HTML5 structure
  - CSS inclusion
  - Header with site title
  - Navigation bar (conditional)
  - Flash message display
  - Content placeholder
  - Responsive meta tags

#### login.html.ep (40 lines)

- **Purpose**: Login page
- **Features**:
  - Login form
  - Username/password fields
  - Link to registration
  - Default credentials display
  - Centered layout

#### register.html.ep (45 lines)

- **Purpose**: Registration page
- **Features**:
  - Registration form
  - Username, email, password fields
  - Password confirmation
  - Link to login
  - Validation (minlength)

#### dashboard.html.ep (55 lines)

- **Purpose**: Dashboard view
- **Features**:
  - Metric cards (3)
  - Recent orders table
  - Product stats
  - Low stock alerts

#### products.html.ep (75 lines)

- **Purpose**: Product catalog
- **Features**:
  - Product grid layout
  - Search box
  - Category filter
  - Product cards with details
  - Add to cart functionality
  - Stock level display

#### cart.html.ep (90 lines)

- **Purpose**: Shopping cart and checkout
- **Features**:
  - Cart items display
  - Quantity display
  - Price calculations
  - Tax and shipping
  - Checkout form
  - Payment method selection
  - Shipping address input

#### orders.html.ep (50 lines)

- **Purpose**: Order list view
- **Features**:
  - Orders table
  - Customer info (staff/admin)
  - Status badges
  - View details button
  - Role-based filtering

#### order_detail.html.ep (85 lines)

- **Purpose**: Order details view
- **Features**:
  - Order header with status
  - Customer information
  - Shipping address
  - Order items table
  - Price breakdown
  - Detailed summary

#### customers.html.ep (40 lines)

- **Purpose**: Customer management (staff/admin only)
- **Features**:
  - Customer table
  - Contact information
  - Location data
  - Join dates

#### reports.html.ep (70 lines)

- **Purpose**: Reports and analytics (staff/admin only)
- **Features**:
  - Revenue metrics
  - Order statistics
  - Orders by status table
  - Top customers table
  - Detailed analytics

---

### public/css/ Directory

#### style.css (600+ lines)

- **Purpose**: Application stylesheet
- **Type**: Pure CSS (no preprocessors)
- **Sections**:
  - Global styles (20 lines)
  - Header styles (40 lines)
  - Navigation styles (30 lines)
  - Card styles (60 lines)
  - Metric cards (40 lines)
  - Product grid (50 lines)
  - Product cards (60 lines)
  - Button styles (80 lines)
  - Form styles (70 lines)
  - Table styles (50 lines)
  - Status badges (40 lines)
  - Cart styles (60 lines)
  - Alert messages (30 lines)
  - Search/filter (20 lines)
  - Login page (40 lines)
  - Order details (30 lines)
  - Responsive design (40 lines)
  - Utility classes (30 lines)
- **Design**: NO GRADIENTS - all solid colors
- **Colors**: 8 defined colors (#2E86AB primary, etc.)
- **Responsive**: Mobile-friendly breakpoints

---

### data/ Directory

#### ecommerce.db (auto-generated)

- **Type**: SQLite database file
- **Tables**: 6 tables
- **Initial Data**:
  - 3 users (admin, staff, customer)
  - 5 customers
  - 20 products
  - 0 orders (initially)
  - 0 order_items (initially)
  - 0 inventory_transactions (initially)
- **Size**: ~100KB (empty), grows with usage
- **Auto-created**: On first application run

---

### docs/ Directory

#### README.md (350+ lines)

- **Purpose**: Main project documentation
- **Sections**:
  - Project overview
  - Features list
  - Requirements
  - Installation instructions
  - Default accounts
  - Project structure
  - Quick start guide
  - Configuration
  - Database schema
  - Design philosophy
  - Troubleshooting
  - Documentation index
- **Target**: All users

#### INSTALLATION.md (250+ lines)

- **Purpose**: Detailed installation guide
- **Sections**:
  - Prerequisites
  - Windows installation
  - macOS installation
  - Linux installation (Ubuntu, CentOS, Arch)
  - Production deployment
  - Hypnotoad configuration
  - Verification steps
  - Troubleshooting
  - Uninstallation
- **Target**: System administrators

#### USER_GUIDE.md (400+ lines)

- **Purpose**: Complete user manual
- **Sections**:
  - Getting started
  - Login/registration
  - Customer features guide
  - Staff features guide
  - Admin features guide
  - Common tasks
  - Tips and tricks
  - Troubleshooting
  - Security guidelines
- **Target**: End users

#### ARCHITECTURE.md (450+ lines)

- **Purpose**: System architecture documentation
- **Sections**:
  - Technology stack
  - Architecture layers
  - MVC pattern explanation
  - Database schema (detailed)
  - Data flow diagrams
  - Security architecture
  - Request flow
  - Component interaction
  - Design patterns
  - Performance considerations
  - Deployment architecture
  - Testing strategy
  - Maintenance guidelines
- **Target**: Developers

#### API_DOCUMENTATION.md (550+ lines)

- **Purpose**: Complete API reference
- **Sections**:
  - Models API (User, Product, Order, Customer)
  - Controllers API (Auth)
  - Configuration reference
  - Mojolicious helpers
  - Error handling
  - Usage examples
  - Method signatures
  - Return values
  - Code samples
- **Target**: Developers

#### PROJECT_SUMMARY.md (500+ lines)

- **Purpose**: Project overview and achievements
- **Sections**:
  - Project overview
  - Key features
  - Project structure
  - Database schema summary
  - Technology stack
  - Design specifications
  - Configuration options
  - System capabilities
  - Documentation delivered
  - Code statistics
  - Quick start
  - Testing checklist
  - Use cases
  - Achievements
  - Development notes
- **Target**: All stakeholders

#### FILE_LISTING.md (This file - 450+ lines)

- **Purpose**: Complete file inventory
- **Sections**:
  - Directory structure
  - File-by-file descriptions
  - Line counts
  - Purpose statements
  - Feature lists
  - Statistics summary
- **Target**: Developers, maintainers

---

## Statistics Summary

### Code Files

| Category       | Files | Lines      |
| -------------- | ----- | ---------- |
| Main App       | 1     | 340        |
| Config         | 1     | 110        |
| Database       | 1     | 260        |
| Models         | 4     | 790        |
| Controllers    | 1     | 80         |
| **Total Perl** | **8** | **~1,580** |

### Template Files

| Category            | Files  | Lines    |
| ------------------- | ------ | -------- |
| Layouts             | 1      | 60       |
| Views               | 9      | ~650     |
| **Total Templates** | **10** | **~710** |

### Stylesheet Files

| Category         | Files | Lines    |
| ---------------- | ----- | -------- |
| CSS              | 1     | 600+     |
| **Total Styles** | **1** | **600+** |

### Documentation Files

| Category       | Files | Lines      |
| -------------- | ----- | ---------- |
| README         | 1     | 350+       |
| Installation   | 1     | 250+       |
| User Guide     | 1     | 400+       |
| Architecture   | 1     | 450+       |
| API Docs       | 1     | 550+       |
| Summary        | 1     | 500+       |
| File Listing   | 1     | 450+       |
| **Total Docs** | **7** | **~3,000** |

### Overall Project

| Metric              | Count        |
| ------------------- | ------------ |
| **Total Files**     | 27+          |
| **Total Lines**     | ~6,000       |
| **Perl Code**       | ~1,580 lines |
| **Templates**       | ~710 lines   |
| **CSS**             | ~600 lines   |
| **Documentation**   | ~3,000 lines |
| **Database Tables** | 6            |
| **Routes**          | 15+          |
| **Models**          | 4            |
| **Controllers**     | 1            |

---

## Features by File

### Authentication (3 files)

- lib/ECommerce/Controllers/Auth.pm
- lib/ECommerce/Models/User.pm
- templates/login.html.ep

### Product Management (2 files)

- lib/ECommerce/Models/Product.pm
- templates/products.html.ep

### Order Processing (3 files)

- lib/ECommerce/Models/Order.pm
- templates/cart.html.ep
- templates/orders.html.ep

### Customer Management (2 files)

- lib/ECommerce/Models/Customer.pm
- templates/customers.html.ep

### Reporting (1 file)

- templates/reports.html.ep

### Infrastructure (3 files)

- lib/ECommerce/Database.pm
- lib/ECommerce/Config.pm
- app.pl

---

## File Dependencies

### app.pl depends on:

- All models (User, Product, Order, Customer)
- Auth controller
- Config module
- All templates

### Models depend on:

- Database.pm
- Config.pm
- DBI/DBD::SQLite

### Controllers depend on:

- Models
- Config

### Templates depend on:

- style.css
- Mojolicious helpers
- Session data

---

## Installation Files

- cpanfile (dependency manifest)
- README.md (includes installation)
- INSTALLATION.md (detailed guide)

---

## Configuration Files

- lib/ECommerce/Config.pm (all settings)
- app.pl (Hypnotoad config)

---

## Documentation Files

All in `docs/` directory:

1. README.md - Overview
2. INSTALLATION.md - Setup
3. USER_GUIDE.md - Usage
4. ARCHITECTURE.md - Design
5. API_DOCUMENTATION.md - API
6. PROJECT_SUMMARY.md - Summary
7. FILE_LISTING.md - Files

---

**File Listing Complete**  
**Total Project Files**: 27+  
**Total Lines of Code**: ~6,000  
**Status**: ✅ Production Ready  
**Last Updated**: December 2, 2025

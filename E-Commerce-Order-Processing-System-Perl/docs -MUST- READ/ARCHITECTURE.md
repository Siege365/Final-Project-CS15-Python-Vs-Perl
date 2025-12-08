# System Architecture

## E-Commerce Order Processing System - Perl

## Overview

This system follows the **MVC (Model-View-Controller)** architecture pattern built on the Mojolicious framework.

## Technology Stack

- **Language**: Perl 5.30+
- **Web Framework**: Mojolicious 9.0+
- **Database**: SQLite 3
- **Password Hashing**: Crypt::Bcrypt
- **Templating**: Embedded Perl (EP)
- **HTTP Server**: Mojolicious built-in / Hypnotoad

## Architecture Layers

### 1. Application Layer (app.pl)

- Entry point and routing
- Request handling
- Response generation
- Session management
- Helper methods

Note: The project loads route files from a `routes/` directory (for example `routes/shared_routes.pl`, `routes/admin_routes.pl`, `routes/customer_routes.pl`) and registers them in `app.pl`. Several application-level helpers are defined in `app.pl` (for example: `is_logged_in`, `current_user`, `get_cart`, `get_cart_count`, `add_to_cart`, `clear_cart`) and sessions are configured there (secrets and default expiration).

### 2. Controller Layer (lib/ECommerce/Controllers/)

- **Auth.pm**: Authentication and authorization
- Business logic
- Request validation
- Response formatting

Note: Controllers are organized under `lib/ECommerce/Controllers/` and may include sub-directories such as `Customer/` (for customer-facing controllers like `CartController.pm`) and `Admin/` (for admin-facing controllers). Controllers handle form submissions, JSON API responses (AJAX), and template rendering.

### 3. Model Layer (lib/ECommerce/Models/)

- **User.pm**: User authentication
- **Product.pm**: Product management
- **Order.pm**: Order processing
- **Customer.pm**: Customer management
- Database interactions
- Data validation

### 4. View Layer (templates/)

- HTML templates with Embedded Perl
- Layout system
- Reusable components
- Form handling

Notes:

- The main layout is `templates/layouts/default.html.ep`. It contains the header/navigation and includes client-side scripts and styles.
- Some templates include lightweight UI components such as an in-page Add‑to‑Cart toast. Product listing templates add `class="ajax-add-cart"` to forms so client-side JS can intercept submission and call the controller via fetch/XHR.

### 5. Configuration (lib/ECommerce/Config.pm)

- Application settings
- Constants
- Database configuration
- Business rules

### 6. Database Layer (lib/ECommerce/Database.pm)

- Connection management
- Schema initialization
- Sample data generation

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'customer',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT,
    is_active INTEGER DEFAULT 1
);
```

### Customers Table

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    country TEXT DEFAULT 'USA',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Products Table

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    sku TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    cost REAL,
    stock_quantity INTEGER DEFAULT 0,
    reorder_level INTEGER DEFAULT 10,
    image_url TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Orders Table

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',
    subtotal REAL NOT NULL,
    tax REAL DEFAULT 0,
    shipping REAL DEFAULT 0,
    total REAL NOT NULL,
    payment_method TEXT,
    payment_status TEXT DEFAULT 'pending',
    shipping_address TEXT,
    billing_address TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

### Order Items Table

```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    product_sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Inventory Transactions Table

```sql
CREATE TABLE inventory_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity_change INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    reference_id INTEGER,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## Data Flow

### Order Placement Flow

1. **Customer adds product to cart**

   - Session stores cart items
   - Quantity validated against stock

   Implementation notes:

   - Add-to-Cart is implemented to support both traditional POSTs and AJAX: when the client submits with `X-Requested-With: XMLHttpRequest` the Cart controller returns JSON (for example `{ success => 1, product_name => 'Name', cart_count => 3 }`) and does not set the server-side flash; non-AJAX submissions fall back to setting flash and redirecting.

   - The session cart is stored as an arrayref of item hashrefs. Each item may include `product_id`, `product_name`, `quantity`, `unit_price`, and `image_url`. Older cart entries are enriched with `image_url` when the cart is viewed so templates can render images with a `public/images/placeholder.svg` fallback.

2. **Customer views cart**

   - Calculate subtotal
   - Apply tax (8%)
   - Calculate shipping ($5 or FREE over $100)
   - Display total

3. **Customer checks out**

   - Validate cart items
   - Check stock availability
   - Create order record
   - Create order items
   - Update inventory
   - Record inventory transactions
   - Clear cart

4. **Order confirmation**
   - Generate order number
   - Display order details
   - Send to order history

## Security Architecture

### Authentication

- Bcrypt password hashing (cost: 10)
- Session-based authentication
- Secure session cookies
- Login/logout functionality

### Authorization

- Role-based access control (RBAC)
- Three roles: admin, staff, customer
- Route protection
- View-level permissions

### Data Protection

- Prepared SQL statements
- Input validation
- XSS prevention via templating
- CSRF protection (Mojolicious built-in)

### Session Management

- Server-side sessions
- Configurable expiration (1 hour default)
- Secure session storage
- Session invalidation on logout

## Request Flow

1. **Client Request** → Browser sends HTTP request
2. **Routing** → Mojolicious routes to handler
3. **Authentication Check** → Verify session
4. **Authorization Check** → Verify role permissions
5. **Controller** → Process business logic
6. **Model** → Database operations
7. **View** → Render template
8. **Response** → Send HTML to client

## Component Interaction

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   app.pl    │ ← Routes & Helpers
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Controllers │ ← Auth.pm
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Models    │ ← User, Product, Order, Customer
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Database   │ ← SQLite
└─────────────┘
```

## Design Patterns

### 1. MVC Pattern

- **Model**: Data and business logic
- **View**: Presentation layer
- **Controller**: Request handling

### 2. Repository Pattern

- Models act as repositories
- Encapsulate data access
- Abstract database operations

### 3. Singleton Pattern

- Database connections
- Configuration settings

### 4. Session State Pattern

- Shopping cart
- User authentication
- Temporary data storage

## Performance Considerations

### Database Optimization

- Indexed foreign keys
- Prepared statements
- Transaction management
- Connection pooling

### Caching Strategy

- Session-based cart caching
- Template compilation caching

### Scalability

- Hypnotoad multi-worker support
- Stateless request handling
- Horizontal scaling capability

## Configuration Management

### Development

```perl
perl app.pl daemon
```

### Production

```perl
hypnotoad app.pl
```

### Settings

- Tax rate: 8%
- Shipping: $5.00 (FREE over $100)
- Session timeout: 1 hour
- Workers: 4 (production)

## Error Handling

### Application Level

- Try/catch blocks
- Graceful degradation
- User-friendly error messages

### Database Level

- Transaction rollback
- Constraint validation
- Foreign key enforcement

### View Level

- Flash messages
- Inline validation
- Error alerts

## Monitoring & Logging

### Access Logs

- Request tracking
- Response times
- Error logging

### Application Logs

- Database operations
- Authentication events
- Business logic errors

## Deployment Architecture

### Single Server

```
┌──────────────────┐
│   Web Browser    │
└────────┬─────────┘
         │
    HTTP Request
         │
         ↓
┌──────────────────┐
│   Hypnotoad      │ (4 workers)
│   (Port 3000)    │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  SQLite Database │
│  (ecommerce.db)  │
└──────────────────┘

### Static assets and client behavior

- Static assets (CSS, JS, images) are served from `public/`. The project includes component CSS (for modal/toast styles) in `public/css/components/` and small client-side scripts in `public/js/` to handle the responsive hamburger menu, toast positioning, and AJAX form interception.
- Server-rendered flash messages remain in the layout for non-AJAX flows; AJAX Add-to-Cart uses the client-side toast for user feedback.
```

### Reverse Proxy (Production)

```
┌──────────────────┐
│   Web Browser    │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  Nginx/Apache    │ (Port 80/443)
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│   Hypnotoad      │ (Port 3000)
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  SQLite Database │
└──────────────────┘
```

## Testing Strategy

### Unit Testing

- Model methods
- Controller logic
- Utility functions

### Integration Testing

- Route handlers
- Database operations
- Session management

### System Testing

- End-to-end workflows
- User scenarios
- Performance testing

## Maintenance

### Database Backup

```bash
cp data/ecommerce.db data/ecommerce.db.backup
```

### Log Rotation

- Configure system log rotation
- Archive old logs
- Monitor disk space

### Updates

- Keep dependencies updated
- Test before deploying
- Backup before changes

---

**Architecture Version**: 1.0.0  
**Last Updated**: December 2, 2025

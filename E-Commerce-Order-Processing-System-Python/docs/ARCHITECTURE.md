# Architecture Documentation

## System Overview

The E-Commerce Order Processing System is a full-stack web application built using Python and Streamlit framework, following the Model-View-Controller (MVC) architectural pattern.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit Frontend                      │
│  ┌────────────┬────────────┬────────────┬────────────────┐ │
│  │ Dashboard  │  Products  │   Orders   │   Customers    │ │
│  │            │            │            │                 │ │
│  │  Reports   │  Settings  │    Auth    │   Navigation   │ │
│  └────────────┴────────────┴────────────┴────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       Controllers                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AuthController: Authentication & Authorization      │  │
│  │  - login(), logout(), register()                     │  │
│  │  - Role-based access control                         │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                         Models                               │
│  ┌────────────┬────────────┬────────────┬──────────────┐   │
│  │  UserModel │ProductModel│ OrderModel │CustomerModel │   │
│  │            │            │            │              │   │
│  │  CRUD Ops  │  CRUD Ops  │  CRUD Ops  │  CRUD Ops    │   │
│  └────────────┴────────────┴────────────┴──────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLite Database                           │
│  ┌────────┬─────────┬────────┬──────────┬──────────────┐   │
│  │ users  │products │ orders │customers │ order_items  │   │
│  │        │         │        │          │              │   │
│  │inventory_transactions                               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend

- **Streamlit 1.29.0**: Web application framework
- **HTML/CSS**: Custom styling
- **JavaScript**: Client-side interactions (via Streamlit)

### Backend

- **Python 3.8+**: Core programming language
- **SQLite3**: Embedded database
- **Bcrypt**: Password hashing and security

### Data Processing

- **Pandas 2.1.4**: Data manipulation and analysis
- **NumPy**: Numerical operations (via Pandas)

### Visualization

- **Plotly 5.18.0**: Interactive charts and graphs
- **Plotly Express**: Simplified plotting

### Additional Libraries

- **Pillow 10.1.0**: Image processing
- **python-dateutil 2.8.2**: Date/time utilities

## Design Patterns

### 1. Model-View-Controller (MVC)

**Models** (`models/`):

- Database interaction layer
- Business logic
- Data validation
- CRUD operations

**Views** (`views/`):

- User interface components
- Data presentation
- User input forms
- Visual feedback

**Controllers** (`controllers/`):

- Request handling
- Authentication logic
- Session management
- Access control

### 2. Repository Pattern

Each model acts as a repository:

```python
class ProductModel:
    def get_all_products()
    def get_product_by_id()
    def create_product()
    def update_product()
    def delete_product()
```

### 3. Singleton Pattern

Database connection management:

```python
class Database:
    _instance = None
    def connect()  # Single connection
```

### 4. Session State Pattern

Streamlit session management:

```python
st.session_state.user_id
st.session_state.cart
st.session_state.logged_in
```

## Component Architecture

### 1. Authentication System

```
┌──────────────────────────────────────┐
│         AuthController               │
├──────────────────────────────────────┤
│  + login(username, password)         │
│  + logout()                          │
│  + register(user_data)               │
│  + is_admin()                        │
│  + is_staff()                        │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│          UserModel                   │
├──────────────────────────────────────┤
│  + verify_password()                 │
│  + create_user()                     │
│  + get_user_by_username()            │
│  + update_last_login()               │
└──────────────────────────────────────┘
```

**Security Features:**

- Bcrypt password hashing
- Session-based authentication
- Role-based access control (RBAC)
- Secure password storage

### 2. Product Management

```
┌──────────────────────────────────────┐
│       ProductModel                   │
├──────────────────────────────────────┤
│  + get_all_products()                │
│  + create_product()                  │
│  + update_product()                  │
│  + update_stock()                    │
│  + get_low_stock_products()          │
│  + search_products()                 │
└──────────────────────────────────────┘
```

**Features:**

- Full CRUD operations
- Stock tracking
- Category management
- SKU-based identification
- Search and filter

### 3. Order Processing

```
┌──────────────────────────────────────┐
│         OrderModel                   │
├──────────────────────────────────────┤
│  + create_order()                    │
│  + update_order_status()             │
│  + get_order_items()                 │
│  + search_orders()                   │
│  + get_order_stats()                 │
└──────────────────────────────────────┘
```

**Workflow:**

1. Customer adds products to cart
2. Proceeds to checkout
3. Enters shipping information
4. Selects payment method
5. Order created in database
6. Stock automatically updated
7. Inventory transaction recorded

### 4. Shopping Cart

**Session-based cart management:**

```python
st.session_state.cart = [
    {
        'product_id': 1,
        'product_name': 'Laptop',
        'unit_price': 1299.99,
        'quantity': 1,
        'subtotal': 1299.99
    }
]
```

**Functions:**

- `add_to_cart()`
- `remove_from_cart()`
- `update_cart_quantity()`
- `clear_cart()`
- `get_cart_total()`

## Database Schema

### Entity-Relationship Diagram

```
┌─────────┐         ┌──────────┐
│  users  │────────<│customers │
└─────────┘         └─────┬────┘
                          │
                          │ 1:N
                          ▼
                    ┌──────────┐
                    │  orders  │
                    └─────┬────┘
                          │
                          │ 1:N
                          ▼
                    ┌──────────────┐      ┌──────────┐
                    │ order_items  │────<│ products │
                    └──────────────┘      └─────┬────┘
                                                │
                                                │ 1:N
                                                ▼
                                    ┌────────────────────────┐
                                    │inventory_transactions │
                                    └────────────────────────┘
```

### Tables

**users**

- id (PK)
- username (UNIQUE)
- email (UNIQUE)
- password_hash
- role
- created_at
- last_login

**customers**

- id (PK)
- user_id (FK → users)
- first_name
- last_name
- phone
- address
- city, state, zip_code
- created_at

**products**

- id (PK)
- name
- description
- category
- price
- cost
- sku (UNIQUE)
- stock_quantity
- reorder_level
- is_active
- created_at, updated_at

**orders**

- id (PK)
- customer_id (FK → customers)
- order_number (UNIQUE)
- order_date
- status
- payment_method
- subtotal, tax, shipping_cost, total
- shipping_address, city, state, zip
- notes
- created_by (FK → users)
- updated_at

**order_items**

- id (PK)
- order_id (FK → orders)
- product_id (FK → products)
- product_name
- quantity
- unit_price
- subtotal

**inventory_transactions**

- id (PK)
- product_id (FK → products)
- transaction_type
- quantity
- notes
- created_by (FK → users)
- created_at

## Data Flow

### Order Creation Flow

```
1. Customer View
   └─> Add to Cart
       └─> Session State Update

2. Checkout Process
   └─> Collect shipping info
       └─> Collect payment method
           └─> Calculate totals

3. Order Controller
   └─> Validate cart
       └─> Validate customer
           └─> Call OrderModel.create_order()

4. Order Model
   └─> Begin transaction
       ├─> Insert order record
       ├─> Insert order_items
       ├─> Update product stock
       ├─> Record inventory transactions
       └─> Commit transaction

5. Response
   └─> Clear cart
       └─> Show success
           └─> Redirect to order history
```

### Authentication Flow

```
1. Login Request
   └─> Username + Password

2. AuthController.login()
   └─> UserModel.verify_password()
       ├─> Bcrypt check
       └─> Return user data

3. Session Creation
   └─> st.session_state.logged_in = True
       ├─> Store user_id
       ├─> Store username
       ├─> Store role
       └─> Store email

4. Access Control
   └─> Check role for page access
       ├─> Admin: Full access
       ├─> Staff: Limited access
       └─> Customer: Customer pages only
```

## Security Architecture

### 1. Authentication Security

**Password Hashing:**

```python
import bcrypt

# Storage
password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

# Verification
bcrypt.checkpw(password, stored_hash)
```

**Session Management:**

- Server-side sessions via Streamlit
- Auto-logout on browser close
- No password storage in sessions

### 2. Authorization

**Role-Based Access Control (RBAC):**

```python
def check_access(required_role):
    user_role = st.session_state.role
    if user_role not in allowed_roles:
        st.error("Access Denied")
        return False
    return True
```

### 3. Input Validation

- SQL injection prevention (parameterized queries)
- XSS protection (Streamlit built-in)
- Data type validation
- Required field checks

### 4. Database Security

- SQLite with file permissions
- Connection pooling
- Transaction management
- Foreign key constraints

## Performance Considerations

### Database Optimization

**Indexing:**

```sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_products_sku ON products(sku);
```

**Query Optimization:**

- Use of JOINs for related data
- Pagination for large datasets
- Selective column retrieval
- Efficient WHERE clauses

### Caching Strategy

**Streamlit Caching:**

```python
@st.cache_data
def get_all_products():
    # Cached for performance
    return product_model.get_all_products()
```

### Session State Management

- Minimal data in session
- Cart stored as lightweight objects
- Lazy loading of heavy data

## Scalability

### Current Limitations

- Single-user database (SQLite)
- Session-based cart (not persistent)
- No distributed architecture

### Future Scalability Options

1. **Database Migration:**

   - PostgreSQL or MySQL
   - Connection pooling
   - Read replicas

2. **Cart Persistence:**

   - Database-backed cart
   - Redis for sessions

3. **Microservices:**

   - Separate order service
   - Separate inventory service
   - API gateway

4. **Caching Layer:**
   - Redis for product catalog
   - Memcached for sessions

## Deployment Architecture

### Development

```
Local Machine
├── Streamlit Dev Server
├── SQLite Database
└── Python Environment
```

### Production (Recommended)

```
Cloud Platform (AWS/Azure/GCP)
├── Web Server (Nginx)
├── Streamlit Application
├── PostgreSQL Database
├── Redis Cache
└── Load Balancer
```

## Monitoring & Logging

### Logging Strategy

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Log Events:**

- User authentication
- Order creation
- Inventory updates
- Errors and exceptions

### Metrics to Monitor

- Active users
- Orders per hour
- Response times
- Database queries
- Error rates

## Error Handling

### Strategy

1. **Try-Except Blocks:**

```python
try:
    order_id = create_order(...)
except Exception as e:
    st.error(f"Error: {str(e)}")
    logging.error(f"Order creation failed: {e}")
```

2. **User-Friendly Messages:**

- Technical details hidden
- Clear action steps
- Support contact info

3. **Graceful Degradation:**

- Feature availability checks
- Fallback options
- Error recovery

## Testing Strategy

### Unit Tests

Test individual components:

```python
def test_create_product():
    product_id = product_model.create_product(...)
    assert product_id is not None
```

### Integration Tests

Test component interactions:

```python
def test_order_creation_workflow():
    # Add to cart
    # Checkout
    # Verify order
    # Verify stock update
```

### End-to-End Tests

Test complete user flows:

- Browse → Add to Cart → Checkout → Order
- Login → Manage Products → Logout

## Maintenance

### Regular Tasks

1. **Database Maintenance:**

   - Vacuum SQLite database
   - Backup regularly
   - Monitor size

2. **Security Updates:**

   - Update dependencies
   - Review access logs
   - Patch vulnerabilities

3. **Performance Monitoring:**
   - Check response times
   - Optimize slow queries
   - Clean old sessions

## Documentation Standards

### Code Documentation

```python
def create_order(customer_id, items, **kwargs):
    """
    Create a new order with items.

    Args:
        customer_id (int): Customer ID
        items (list): List of order items
        **kwargs: Additional order parameters

    Returns:
        tuple: (order_id, order_number)

    Raises:
        Exception: If order creation fails
    """
```

### API Documentation

All public methods documented with:

- Purpose
- Parameters
- Return values
- Exceptions
- Examples

---

**System Architecture Version:** 1.0.0  
**Last Updated:** 2025-12-02

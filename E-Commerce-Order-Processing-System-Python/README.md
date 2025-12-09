# 🚀 ShopPy - Quick Start Guide

## Installation & Setup (5 minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Run Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

---

## 📖 Key Paths

### Customer Pages

- Homepage: `/`
- Products: `/products`
- Cart: `/cart`
- Checkout: `/checkout`
- Orders: `/orders`
- Account: `/account`

### Admin Pages

- Dashboard: `/admin/dashboard`
- Products: `/admin/products`
- Orders: `/admin/orders`
- Customers: `/admin/customers`
- Reports: `/admin/reports`

### Auth Pages

- Login: `/login`
- Register: `/register`
- Logout: `/logout`

---

## 🎨 Project Colors

```
Primary:   #6366f1 (Indigo)
Success:   #10b981 (Green)
Error:     #ef4444 (Red)
Warning:   #f59e0b (Amber)
Info:      #3b82f6 (Blue)
```

---

## 📁 Adding New Features

### Add a New Page

1. Create template: `templates/page_name.html`
2. Create view function in Controllers
3. Add URL route in `urls.py`
4. Add CSS: `public/css/pages/page_name.css`

### Add a New Component

1. Create component HTML (reusable)
2. Add CSS: `public/css/components/component_name.css`
3. Import in `style.css`

### Add Models

1. Define in `lib/ECommerce/Models/`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`

---

## 🔧 Configuration

Edit `lib/ECommerce/Config.py`:

```python
TAX_RATE = 0.08              # 8% tax
SHIPPING_RATE = 5.00         # $5 shipping
FREE_SHIPPING_THRESHOLD = 100.00  # Free over $100
```

---

## 💡 Development Tips

### Django Shell

```bash
python manage.py shell
from lib.ECommerce.Models.Product import Product
Product.objects.all()
```

### Create Admin User

```bash
python manage.py createsuperuser
```

### Database Backup

```bash
python manage.py dumpdata > backup.json
```

### Reset Database

```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🐛 Common Issues

### Port Already in Use

```bash
python manage.py runserver 8001
```

### Static Files Not Loading

```bash
python manage.py collectstatic
```

### Database Locked

```bash
rm db.sqlite3
python manage.py migrate
```

---

## 📊 File Sizes

- Models: ~2KB each
- Templates: ~3-8KB each
- CSS Files: ~5-15KB each
- Total Project: ~2MB

---

## ✅ Checklist for Deployment

- [ ] Set `DEBUG = False` in settings
- [ ] Set `SECRET_KEY` to secure value
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up environment variables
- [ ] Run `collectstatic`
- [ ] Test all user flows
- [ ] Set up backup schedule

---

## 📚 Documentation Files

- **docs-MUST-READ.md** - Complete project documentation
- **README.md** - This file
- **requirements.txt** - Python dependencies

---

## 🆘 Getting Help

1. Check `docs-MUST-READ.md` for detailed info
2. Review template examples
3. Check CSS variables in `public/css/base/variables.css`
4. Read Django documentation: https://docs.djangoproject.com

---

## 🎯 Next Steps

1. ✅ Run the server
2. ✅ Create admin account
3. ✅ Add sample products
4. ✅ Test checkout flow
5. ✅ Customize branding
6. ✅ Deploy to production

---

**Happy coding! 🐍**

ShopPy - Wrapped in code, packed with deals.

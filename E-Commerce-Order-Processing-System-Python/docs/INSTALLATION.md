# Installation Guide

## System Requirements

### Operating System

- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, Debian, Fedora, etc.)

### Software Requirements

- Python 3.8 or higher
- pip (Python package manager)
- 500 MB free disk space
- Modern web browser (Chrome, Firefox, Edge, Safari)

## Step-by-Step Installation

### Step 1: Install Python

#### Windows

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```powershell
   python --version
   ```

#### macOS

```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Verify
python3 --version
```

### Step 2: Download Project

```bash
# Navigate to project directory
cd path/to/E-Commerce-Order-Processing-System-Python
```

### Step 3: Create Virtual Environment (Recommended)

#### Windows

```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\activate
```

#### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

This will install:

- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `plotly` - Interactive charts
- `bcrypt` - Password hashing
- `pillow` - Image processing
- `python-dateutil` - Date utilities

### Step 5: Initialize Database

The database will be automatically created on first run. No manual setup required!

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will:

1. Start the Streamlit server
2. Create the database (if not exists)
3. Populate sample data
4. Open in your default browser at `http://localhost:8501`

## Verification

After installation, verify everything works:

1. **Application loads** - Browser opens to login page
2. **Login successful** - Use `admin` / `admin123`
3. **Dashboard displays** - Shows metrics and charts
4. **Navigation works** - Click through different pages

## Default Data

The system automatically creates:

### Users:

- Admin: `admin` / `admin123`
- Staff: `staff` / `staff123`
- Customer: `customer` / `customer123`

### Sample Products:

- 20 pre-loaded products
- Various categories
- Realistic pricing

### Sample Customers:

- 5 customer profiles
- Complete information

## Configuration

### Change Port

```bash
streamlit run app.py --server.port 8502
```

### Run on Network

```bash
streamlit run app.py --server.address 0.0.0.0
```

### Custom Config

Edit `.streamlit/config.toml`:

```toml
[server]
port = 8501
headless = true

[theme]
primaryColor = "#2E86AB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## Troubleshooting

### Issue: "command not found: streamlit"

**Solution:**

```bash
# Reinstall streamlit
pip install --upgrade streamlit

# Or use full path
python -m streamlit run app.py
```

### Issue: "Port 8501 already in use"

**Solution:**

```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8501
kill -9 <PID>
```

### Issue: "ModuleNotFoundError"

**Solution:**

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Check installation
pip list
```

### Issue: "Permission denied"

**Solution:**

```bash
# Windows (Run as Administrator)
# macOS/Linux
sudo pip install -r requirements.txt
```

### Issue: Database locked

**Solution:**

```bash
# Delete database and restart
rm data/ecommerce.db
streamlit run app.py
```

### Issue: Browser doesn't open

**Solution:**

```bash
# Manually open browser to:
http://localhost:8501

# Or specify browser
streamlit run app.py --browser.gatherUsageStats false
```

## Advanced Installation

### Using Docker (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:

```bash
docker build -t ecommerce-system .
docker run -p 8501:8501 ecommerce-system
```

### Using conda (Alternative)

```bash
# Create environment
conda create -n ecommerce python=3.10

# Activate
conda activate ecommerce

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate
deactivate

# Remove folder
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows
```

### Remove Dependencies

```bash
pip uninstall -r requirements.txt -y
```

### Remove Database

```bash
rm data/ecommerce.db
```

## Next Steps

After successful installation:

1. Read [USER_GUIDE.md](USER_GUIDE.md) for usage instructions
2. Check [ARCHITECTURE.md](ARCHITECTURE.md) for system overview
3. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for development

## Support

If you encounter issues not covered here:

1. Check Python version: `python --version`
2. Check pip version: `pip --version`
3. Verify all dependencies: `pip list`
4. Review error messages carefully
5. Contact system administrator

---

**Installation complete! 🎉**
Start the application with: `streamlit run app.py`

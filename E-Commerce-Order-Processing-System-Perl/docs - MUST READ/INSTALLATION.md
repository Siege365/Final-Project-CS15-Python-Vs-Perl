# Installation Guide

## ShopPerl (E-Commerce Order Processing System - Perl)

Platform-specific installation instructions and quick start steps.

## Prerequisites

- Perl 5.30 or higher
- Internet connection for installing dependencies
- Web browser

## Windows Installation

### Step 1: Install Perl

1. Download Strawberry Perl from http://strawberryperl.com/
2. Run the installer
3. Verify installation:

```cmd
perl --version
cpan --version
```

### Step 2: Install Dependencies

Open PowerShell (recommended on Windows) and run from the project root:

```powershell
cd 'C:\path\to\E-Commerce-Order-Processing-System-Perl'
cpanm --installdeps .
```

If `cpanm` is not installed, install it first:

```powershell
cpan App::cpanminus
cpanm --installdeps .
```

Or install required modules manually:

```powershell
cpanm Mojolicious DBI DBD::SQLite Crypt::Bcrypt JSON Time::Piece
```

### Step 3: Run Application (Development)

Start the development server:

```powershell
perl app.pl daemon
```

### Step 4: Access Application

Open browser to: http://localhost:3000

## macOS Installation

### Step 1: Verify Perl

macOS comes with Perl pre-installed:

```bash
perl --version
```

### Step 2: Install cpanm

```bash
curl -L https://cpanmin.us | perl - App::cpanminus
```

### Step 3: Install Dependencies

```bash
cd E-Commerce-Order-Processing-System-Perl
cpanm --installdeps .
```

### Step 4: Run Application

```bash
perl app.pl daemon
```

## Linux Installation

### Step 1: Install Perl (if needed)

#### Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install perl cpanminus
```

#### CentOS/RHEL:

```bash
sudo yum install perl cpanminus
```

#### Arch Linux:

```bash
sudo pacman -S perl cpanminus
```

### Step 2: Install Dependencies

```bash
cd E-Commerce-Order-Processing-System-Perl
cpanm --installdeps .
```

### Step 3: Run Application

```bash
perl app.pl daemon
```

## Production Deployment

### Using Hypnotoad (Recommended)

```powershell
hypnotoad app.pl
```

To stop Hypnotoad:

```powershell
hypnotoad -s app.pl
```

### Verification

1. Confirm database file was created: `data/ecommerce.db`

2. Start the app and verify the web UI at `http://localhost:3000`.

3. Test default credentials (created by sample data):

- Admin: `admin` / `admin123`
- Staff: `staff` / `staff123`
- Customer: `customer` / `customer123`

4. Test typical flows: browse products, add to cart (note: Add-to-Cart uses AJAX and displays an in-page toast), place an order and check order history.

### 2. Test Login

- URL: http://localhost:3000
- Username: admin
- Password: admin123

### 3. Test Features

- Browse products
- Add to cart
- Place test order
- View reports (admin/staff)

## Troubleshooting

### Module Installation Fails

Try reinstalling or forcing the install:

```powershell
cpanm --force DBD::SQLite
```

### Database Permission Issues

Ensure the `data/` directory is writable by the user running the application. On Windows check file permissions in Explorer.

### Port Already in Use

Find and stop the process using the port:

```powershell
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS / Linux
lsof -i :3000
kill -9 <PID>
```

### Cannot Find Modules

Make sure the `lib` directory is included in `PERL5LIB` if you run scripts from a different working directory:

```powershell
$env:PERL5LIB = 'C:\path\to\E-Commerce-Order-Processing-System-Perl\lib;' + $env:PERL5LIB
```

## Uninstallation

1. Stop application
2. Remove project directory
3. (Optional) Remove installed modules

## Support

Check documentation:

- README.md
- USER_GUIDE.md
- ARCHITECTURE.md
- API_DOCUMENTATION.md

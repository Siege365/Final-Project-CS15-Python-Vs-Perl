# Installation Guide

## E-Commerce Order Processing System - Perl

Complete installation instructions for Windows, macOS, and Linux.

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

Open Command Prompt or PowerShell:

```cmd
cd path\to\E-Commerce-Order-Processing-System-Perl
cpanm --installdeps .
```

If cpanm is not available:

```cmd
cpan App::cpanminus
cpanm --installdeps .
```

Manual installation:

```cmd
cpanm Mojolicious
cpanm DBI
cpanm DBD::SQLite
cpanm Crypt::Bcrypt
cpanm JSON
cpanm Time::Piece
```

### Step 3: Run Application

```cmd
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

```bash
hypnotoad app.pl
```

To stop:

```bash
hypnotoad -s app.pl
```

### Configuration

Edit `app.pl` for production settings:

```perl
app->config(hypnotoad => {
    listen => ['http://*:3000'],
    workers => 4,
    pid_file => 'app.pid'
});
```

## Verification

### 1. Check Database

After first run, verify database exists:

```
data/ecommerce.db
```

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

Try with --force:

```bash
cpanm --force DBD::SQLite
```

### Database Permission Issues

Ensure data/ directory is writable:

```bash
chmod 755 data/
```

### Port Already in Use

Change port in app.pl or kill existing process:

```bash
# Linux/Mac
lsof -i :3000
kill -9 <PID>

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Cannot Find Modules

Add lib path:

```bash
export PERL5LIB=/path/to/E-Commerce-Order-Processing-System-Perl/lib:$PERL5LIB
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

# Environment Setup Guide

This guide explains how to configure environment variables for both the Python and Perl e-commerce projects.

## Overview

Both projects now use environment variables to store sensitive information like secret keys and credentials. This allows you to:

- Keep secrets out of version control
- Use different configurations for development, testing, and production
- Follow industry best practices for open-source projects

## General Setup

### 1. Copy the Example File

For each project, copy the `.env.example` file to `.env`:

**Python Project:**

```bash
cd E-Commerce-Order-Processing-System-Python
cp .env.example .env
```

**Perl Project:**

```bash
cd E-Commerce-Order-Processing-System-Perl
cp .env.example .env
```

### 2. Edit the `.env` File

Open the `.env` file in your editor and update the values for your environment:

```bash
# On Windows (PowerShell)
notepad .env

# On Linux/macOS
nano .env
```

### 3. Important Security Notes

- **Never commit `.env` to git** - It's already in `.gitignore`
- **Never share your `.env` file** - It contains sensitive data
- **Generate strong secrets** - See instructions below
- **Use different secrets for each environment** - dev, staging, production

---

## Python Project Configuration

### Required Variables

| Variable            | Description                    | Example                |
| ------------------- | ------------------------------ | ---------------------- |
| `DJANGO_SECRET_KEY` | Django secret key for security | (see generation below) |
| `ADMIN_PASSWORD`    | Initial admin password         | `your-secure-password` |

### Optional Variables

| Variable         | Description                   | Default               |
| ---------------- | ----------------------------- | --------------------- |
| `DEBUG`          | Debug mode                    | `True`                |
| `ALLOWED_HOSTS`  | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `ADMIN_USERNAME` | Admin username                | `admin`               |
| `ADMIN_EMAIL`    | Admin email                   | `admin@shoppy.com`    |

### Generating a Django Secret Key

```bash
# Using Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Or using Perl (for comparison)
perl -e "use Digest::SHA qw(sha256_hex); print sha256_hex(rand() . time())"
```

### Setup Steps

1. Copy `.env.example` to `.env`
2. Generate and add `DJANGO_SECRET_KEY`
3. Set `ADMIN_PASSWORD` to your desired admin password
4. (Optional) Customize other variables

### Creating the Admin User

Once your `.env` is configured:

```bash
python create_admin.py
```

This script will:

- Read credentials from your `.env` file
- Create an admin superuser
- Print confirmation message

---

## Perl Project Configuration

### Required Variables

| Variable                 | Description            | Example                |
| ------------------------ | ---------------------- | ---------------------- |
| `MOJOLICIOUS_SECRET_KEY` | Mojolicious secret key | (see generation below) |

### Optional Variables

| Variable            | Description       | Default       |
| ------------------- | ----------------- | ------------- |
| `ADMIN_USERNAME`    | Admin username    | `admin`       |
| `ADMIN_PASSWORD`    | Admin password    | `admin123`    |
| `STAFF_USERNAME`    | Staff username    | `staff`       |
| `STAFF_PASSWORD`    | Staff password    | `staff123`    |
| `CUSTOMER_USERNAME` | Customer username | `customer`    |
| `CUSTOMER_PASSWORD` | Customer password | `customer123` |

### Generating a Mojolicious Secret Key

```bash
# Using Perl
perl -e "use Mojo::Util qw(secure_random); print secure_random(32)"

# Or using Python
python -c "import secrets; print(secrets.token_hex(16))"
```

### Setup Steps

1. Copy `.env.example` to `.env`
2. Generate and add `MOJOLICIOUS_SECRET_KEY`
3. (Optional) Customize username/password for sample users
4. Run the app - it will load from `.env` automatically

---

## Development vs Production

### Development Environment

```bash
# .env (for development)
DJANGO_SECRET_KEY=dev-key-less-secure
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*.local
```

### Production Environment

```bash
# .env (for production)
DJANGO_SECRET_KEY=very-long-secure-random-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

⚠️ **Critical Production Settings:**

- Set `DEBUG=False`
- Use a strong, random `SECRET_KEY`
- Set specific `ALLOWED_HOSTS` (not `*`)
- Use HTTPS
- Store secrets securely (use a secrets manager like AWS Secrets Manager, Vault, etc.)

---

## Docker (Optional)

If using Docker, you can pass environment variables:

```bash
# Using .env file
docker run --env-file .env -p 8000:8000 myapp

# Or individually
docker run -e DJANGO_SECRET_KEY="your-key" -e DEBUG=False myapp
```

For Kubernetes or cloud platforms, use their native secrets management.

---

## Troubleshooting

### Python: "KeyError: ADMIN_PASSWORD"

- Make sure `ADMIN_PASSWORD` is set in your `.env` file
- Reload your terminal after editing `.env`
- Verify the `.env` file is in the root of the Python project

### Perl: "Can't locate Dotenv.pm"

- Install the module: `cpan Dotenv` or `cpanm Dotenv`
- Or add to `cpanfile`: `requires 'Dotenv';`

### Changes to `.env` not taking effect

- Restart the application
- For development servers, kill and restart them
- For production, ensure your deployment tool loads `.env`

---

## Next Steps

1. Set up your `.env` files
2. Test the applications locally
3. Deploy with appropriate environment variables
4. Document your deployment process for team members

For more information, see the main README.md files in each project.

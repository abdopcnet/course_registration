# Installation Guide - Course Registration Project

Quick installation guide to set up all dependencies and libraries for the Course Registration project.

## Prerequisites

- Linux-based system (tested on Debian/Ubuntu)
- Python 3.9 or higher
- PostgreSQL 12 or higher
- sudo/root access

## Quick Installation

### Step 1: Install System Dependencies

```bash
# Update package list
sudo apt update

# Install Python 3, pip, and venv
sudo apt install -y python3 python3-pip python3-venv

# Install PostgreSQL and development headers
sudo apt install -y postgresql postgresql-contrib libpq-dev python3-dev

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 2: Create Project Directory

```bash
# Create project directory structure
sudo mkdir -p /var/www
sudo mkdir -p /var/www/course_registration

# Set ownership (replace $USER with your username if needed)
sudo chown -R $USER:$USER /var/www/course_registration

# Navigate to project directory
cd /var/www/course_registration
```

**Note:** If you're cloning from git, use this instead:
```bash
sudo mkdir -p /var/www
cd /var/www
git clone https://github.com/abdopcnet/course_registration.git course_registration
cd course_registration
sudo chown -R $USER:$USER /var/www/course_registration
```

### Step 3: Set Up Python Environment

```bash
# Make sure you're in the project directory
cd /var/www/course_registration

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install Django>=4.2,<4.3 psycopg2-binary>=2.9 python-dotenv>=0.21 gunicorn>=20.1 whitenoise>=6.5
```

**Note:** If you have a `requirements.txt` file, use: `pip install -r requirements.txt`

### Step 4: Run Automated Setup Script

The `scripts/setup.sh` script handles database setup, migrations, and admin user creation:

```bash
# Make script executable
chmod +x scripts/setup.sh

# Run setup script
sudo ./scripts/setup.sh
```

This script automatically:
- ✅ Checks virtual environment
- ✅ Verifies PostgreSQL is running
- ✅ Creates database `courseruniversty` and user `abdalla` (if not exists)
- ✅ Runs Django migrations
- ✅ Creates admin superuser (username: `admin`, password: `123123`)

### Step 5: Start the Server

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Development server
python3 manage.py runserver 0.0.0.0:8000

# Or production server (Gunicorn)
gunicorn course_registration.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

Access the application at:
- **Application:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin/
- **Admin Credentials:** username: `admin`, password: `123123`

## Manual Setup (Alternative)

If you prefer manual setup instead of using `setup.sh`:

### Create Database Manually

```bash
sudo -u postgres psql << EOF
CREATE DATABASE courseruniversty;
CREATE USER abdalla WITH PASSWORD 'mysecretpassword';
ALTER ROLE abdalla SET client_encoding TO 'utf8';
ALTER ROLE abdalla SET default_transaction_isolation TO 'read committed';
ALTER ROLE abdalla SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE courseruniversty TO abdalla;
\q
EOF
```

### Run Migrations and Create Admin

```bash
source .venv/bin/activate
python3 manage.py migrate
python3 manage.py createsuperuser  # Follow prompts
```

## Verification

Quick verification checklist:

```bash
# Check Python version
python3 --version

# Check PostgreSQL status
sudo systemctl status postgresql

# Check virtual environment
ls -la .venv

# Check Django installation
source .venv/bin/activate
python3 manage.py --version

# Test database connection
python3 manage.py dbshell
```

## Troubleshooting

### PostgreSQL Not Running

```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install Django>=4.2,<4.3 psycopg2-binary>=2.9 python-dotenv>=0.21 gunicorn>=20.1 whitenoise>=6.5
```

### Permission Issues

```bash
sudo chown -R $USER:$USER /var/www/course_registration
chmod +x scripts/setup.sh
```

## Production Notes

For production deployment:

1. **Environment Variables**: Move secrets from `settings.py` to environment variables
2. **Static Files**: Run `python3 manage.py collectstatic`
3. **Process Manager**: Use systemd, supervisor, or Docker
4. **Reverse Proxy**: Use nginx or Apache in front of Gunicorn
5. **SSL/TLS**: Configure HTTPS certificates

## Related Documentation

- `tech_stack.md` - Technology stack details
- `app_structure.md` - Project structure
- `data_flow_diagram.md` - Application flow
- `scripts/SETUP_README.md` - Setup script documentation

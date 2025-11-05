#!/bin/bash
# Course Registration Project Setup Script
# This script sets up the database and creates the admin superuser

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="courseruniversty"
DB_USER="abdalla"
DB_PASSWORD="mysecretpassword"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="123123"
ADMIN_EMAIL="admin@example.com"

PROJECT_DIR="/var/www/course_registration"
VENV_DIR="$PROJECT_DIR/.venv"

echo -e "${GREEN}=== Course Registration Project Setup ===${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}Warning: Not running as root. Some commands may require sudo.${NC}"
fi

# Step 1: Check if virtual environment exists
echo -e "${YELLOW}[1/5] Checking virtual environment...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}Error: Virtual environment not found at $VENV_DIR${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment found${NC}"

# Step 2: Activate virtual environment
echo -e "${YELLOW}[2/5] Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Step 3: Check if PostgreSQL is running
echo -e "${YELLOW}[3/5] Checking PostgreSQL service...${NC}"
if ! systemctl is-active --quiet postgresql 2>/dev/null && ! pg_isready -h localhost >/dev/null 2>&1; then
    echo -e "${RED}Error: PostgreSQL is not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓ PostgreSQL is running${NC}"

# Step 4: Create database if it doesn't exist
echo -e "${YELLOW}[4/5] Setting up database...${NC}"
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo -e "${GREEN}✓ Database '$DB_NAME' already exists${NC}"
else
    echo "Creating database '$DB_NAME'..."
    sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
EOF
    echo -e "${GREEN}✓ Database created successfully${NC}"
fi

# Step 5: Run migrations
echo -e "${YELLOW}[5/5] Running Django migrations...${NC}"
cd "$PROJECT_DIR"
python3 manage.py migrate --noinput
echo -e "${GREEN}✓ Migrations completed${NC}"

# Step 6: Create superuser
echo -e "${YELLOW}[6/6] Creating admin superuser...${NC}"
python3 << PYTHON_SCRIPT
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_registration.settings')
sys.path.insert(0, '$PROJECT_DIR')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if user already exists
if User.objects.filter(username='$ADMIN_USERNAME').exists():
    print('Admin user already exists, updating password...')
    user = User.objects.get(username='$ADMIN_USERNAME')
    user.set_password('$ADMIN_PASSWORD')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print('✓ Admin user password updated')
else:
    print('Creating new admin user...')
    User.objects.create_superuser(
        username='$ADMIN_USERNAME',
        email='$ADMIN_EMAIL',
        password='$ADMIN_PASSWORD'
    )
    print('✓ Admin user created successfully')

print(f'Username: $ADMIN_USERNAME')
print(f'Password: $ADMIN_PASSWORD')
PYTHON_SCRIPT

echo ""
echo -e "${GREEN}=== Setup Completed Successfully! ===${NC}"
echo ""
echo -e "${GREEN}Admin Credentials:${NC}"
echo -e "  Username: ${YELLOW}$ADMIN_USERNAME${NC}"
echo -e "  Password: ${YELLOW}$ADMIN_PASSWORD${NC}"
echo ""
echo -e "${GREEN}To start the server, run:${NC}"
echo -e "  ${YELLOW}cd $PROJECT_DIR${NC}"
echo -e "  ${YELLOW}source .venv/bin/activate${NC}"
echo -e "  ${YELLOW}python3 manage.py runserver 0.0.0.0:8000${NC}"
echo ""


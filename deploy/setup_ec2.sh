#!/bin/bash

# ==========================================
# AUTHOMATED SETUP SCRIPT FOR AWS EC2
# For Ubuntu 22.04 LTS or 24.04 LTS
# ==========================================

# 1. FAIL ON ERROR
set -e

echo "🚀 STAY CALM! Starting Deployment to AWS..."

# 2. CREATE SWAP FILE (CRITICAL FOR T2.MICRO/T3.MICRO 1GB RAM)
# We create 4GB swap to handle heavy boot-up imports like pandas/osmnx
if [ ! -f /swapfile ]; then
    echo "💾 Creating 4GB Swap File to prevent OOM Crashes..."
    sudo fallocate -l 4G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "✅ Swap Created."
else
    echo "✅ Swap already exists."
fi

# 3. SYSTEM UPDATES & DEPENDENCIES
echo "📦 Installing System Dependencies (Python, Nginx, Node.js)..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl git

# Install Node.js 20.x (for building Frontend)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 4. SETUP BACKEND
echo "🐍 Setting up Django Backend..."
cd house_price_prediction/core

# Create Virtual Env if not exists
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

# Install Python Req
pip install -r requirements.txt
pip install gunicorn

# Run Migrations
python manage.py migrate

# Collect Static (Backend Admin UI)
python manage.py collectstatic --noinput

# Generate Synthetic Data if empty
# python manage.py shell -c "from ingest.generate_data import generate_synthetic_data; generate_synthetic_data()"

deactivate
cd ../..

# 5. SETUP FRONTEND
echo "⚛️  Building React Frontend..."
cd nestiq-predict-main

# Install & Build
npm install
npm run build

cd ..

# 6. CONFIGURE GUNICORN (SYSTEMD)
echo "⚙️  Configuring Gunicorn Service..."
GLOBAL_PYTHON_PATH=$(readlink -f house_price_prediction/core/.venv/bin/python)
GLOBAL_GUNICORN_PATH=$(readlink -f house_price_prediction/core/.venv/bin/gunicorn)
PROJECT_DIR=$(readlink -f house_price_prediction/core)

# Generate Systemd Service File
sudo bash -c "cat > /etc/systemd/system/nestiq.service <<EOF
[Unit]
Description=gunicorn daemon for nestiq
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$GLOBAL_GUNICORN_PATH --access-logfile - --workers 3 --bind unix:/run/nestiq.sock core.wsgi:application

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl start nestiq
sudo systemctl enable nestiq
sudo systemctl restart nestiq

# 7. CONFIGURE NGINX
echo "🌐 Configuring Nginx (Reverse Proxy)..."

# Delete default
sudo rm -f /etc/nginx/sites-enabled/default

# Create Config
# Serves Frontend (Static) at /
# Proxies /api to Backend (Gunicorn)
# Proxies /admin to Backend
FRONTEND_BUILD_DIR=$(readlink -f nestiq-predict-main/dist)

sudo bash -c "cat > /etc/nginx/sites-available/nestiq <<EOF
server {
    listen 80;
    server_name _;

    # FRONTEND (Static Files)
    location / {
        root $FRONTEND_BUILD_DIR;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    # BACKEND API
    location /api/ {
        include proxy_params;
        proxy_pass http://unix:/run/nestiq.sock;
    }
    
    # BACKEND ADMIN
    location /admin/ {
        include proxy_params;
        proxy_pass http://unix:/run/nestiq.sock;
    }

    # DJANGO STATIC FILES (Admin styles)
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }
}
EOF"

sudo ln -sf /etc/nginx/sites-available/nestiq /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 8. PERMISSIONS
# Allow Nginx to read the build dir
sudo chown -R ubuntu:www-data nestiq-predict-main/dist
sudo chmod -R 755 nestiq-predict-main/dist
sudo chown -R ubuntu:www-data house_price_prediction/core
sudo chmod -R 755 house_price_prediction/core

echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo "1. Your app should be live at: http://$(curl -s ifconfig.me)"
echo "2. If it works, try setting up SSL with: sudo certbot --nginx"
echo "=========================================="

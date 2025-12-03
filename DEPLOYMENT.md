# Deployment Guide for Makola Marketplace

This guide covers deploying the Makola Marketplace Django application to production.

## Prerequisites

- Python 3.11+
- PostgreSQL database
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)
- Server (AWS, DigitalOcean, Heroku, etc.)

## Server Setup

### 1. Update Environment Variables

Create a `.env` file on your production server with the following:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=makola_marketplace
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

STRIPE_PUBLIC_KEY=pk_live_your_stripe_public_key
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

SITE_URL=https://yourdomain.com
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
gunicorn psycopg2-binary
```

### 3. Database Setup

```bash
# Create database
sudo -u postgres psql
CREATE DATABASE makola_marketplace;
CREATE USER your_db_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE makola_marketplace TO your_db_user;
\q

# Run migrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 6. Seed Products (Optional)

```bash
python manage.py seed_products
```

## Gunicorn Configuration

Create `/etc/systemd/system/makola.service`:

```ini
[Unit]
Description=Makola Marketplace Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Africanstore
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind unix:/path/to/Africanstore/makola.sock makola.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl start makola
sudo systemctl enable makola
```

## Nginx Configuration

Create `/etc/nginx/sites-available/makola`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/Africanstore;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        root /path/to/Africanstore;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/Africanstore/makola.sock;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/makola /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Stripe Webhook Setup

1. Go to Stripe Dashboard → Webhooks
2. Add endpoint: `https://yourdomain.com/orders/webhook/`
3. Select events: `payment_intent.succeeded`
4. Copy the webhook secret to your `.env` file

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY`
- [ ] `ALLOWED_HOSTS` configured
- [ ] HTTPS enabled
- [ ] Database credentials secure
- [ ] Email configured
- [ ] Stripe keys are production keys
- [ ] Static files served correctly
- [ ] Media files secured
- [ ] Regular backups configured
- [ ] Firewall configured
- [ ] Security headers set

## Monitoring

Consider setting up:
- Error tracking (Sentry)
- Log aggregation
- Performance monitoring
- Uptime monitoring
- Database backups

## Backup Strategy

### Database Backup

```bash
# Daily backup script
pg_dump -U your_db_user makola_marketplace > backup_$(date +%Y%m%d).sql
```

### Media Files Backup

```bash
# Backup media directory
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

## Updates

When updating the application:

1. Pull latest code
2. Activate virtual environment
3. Install/update dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Collect static files: `python manage.py collectstatic --noinput`
6. Restart Gunicorn: `sudo systemctl restart makola`
7. Test the application

## Troubleshooting

### Check Gunicorn Status

```bash
sudo systemctl status makola
```

### Check Nginx Logs

```bash
sudo tail -f /var/log/nginx/error.log
```

### Check Application Logs

```bash
tail -f /var/log/makola/error.log
```

## Support

For issues or questions, contact the development team.




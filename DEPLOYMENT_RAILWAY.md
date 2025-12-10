# Quick Deployment to Railway (Recommended)

Railway is the **easiest way** to deploy your Django app for showing to clients.

## Why Railway?
- ✅ Free tier available
- ✅ Automatic PostgreSQL database
- ✅ Deploys directly from GitHub
- ✅ No complex configuration needed
- ✅ Perfect for Django applications

## Deployment Steps

### Option 1: Deploy via Railway Dashboard (Easiest)

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `Makolamarketplace` repository

3. **Add PostgreSQL Database**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway automatically creates the database

4. **Configure Environment Variables**
   Railway will auto-detect Django, but add these:
   ```
   SECRET_KEY=your-secret-key-here (generate a new one)
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app,yourdomain.com
   ```
   
   Railway automatically sets:
   - `DATABASE_URL` (from PostgreSQL service)
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

5. **Deploy**
   - Railway will automatically:
     - Install dependencies from `requirements.txt`
     - Run migrations
     - Deploy your app
   - Your app will be live at `https://your-app.railway.app`

6. **Run Migrations (if needed)**
   - Go to your project → "Deployments" → Click on deployment
   - Open "Logs" tab
   - Or use Railway CLI:
     ```bash
     railway run python manage.py migrate
     ```

7. **Create Superuser**
   ```bash
   railway run python manage.py createsuperuser
   ```

### Option 2: Deploy via Railway CLI

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Add PostgreSQL
railway add postgresql

# 5. Set environment variables
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=*.railway.app

# 6. Deploy
railway up
```

## Post-Deployment

1. **Collect Static Files**
   Railway handles this automatically, but if needed:
   ```bash
   railway run python manage.py collectstatic --noinput
   ```

2. **Access Admin Panel**
   - Go to `https://your-app.railway.app/admin`
   - Login with your superuser credentials

3. **Seed Sample Data (Optional)**
   ```bash
   railway run python manage.py seed_products
   ```

## Custom Domain (Optional)

1. Go to your project → "Settings" → "Domains"
2. Click "Generate Domain" or add your custom domain
3. Update `ALLOWED_HOSTS` to include your domain

## Cost

- **Free Tier**: $5 credit/month (usually enough for small projects)
- **Hobby Plan**: $5/month (if you exceed free tier)
- **PostgreSQL**: Included in free tier

## Troubleshooting

- **Static files not loading**: Railway handles this automatically with WhiteNoise
- **Database connection errors**: Check that PostgreSQL service is running
- **Migration errors**: Run `railway run python manage.py migrate` manually

---

**This is the fastest way to get your app live for your client! 🚀**








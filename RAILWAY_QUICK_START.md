# 🚀 Quick Railway Deployment Guide

## Step-by-Step Instructions

### Step 1: Sign Up for Railway
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with your **GitHub account** (recommended)

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub if needed
4. Select your repository: **`Makolamarketplace`**

### Step 3: Add PostgreSQL Database
1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically create a PostgreSQL database
4. **Note**: Railway automatically sets `DATABASE_URL` environment variable

### Step 4: Configure Environment Variables
1. Go to your project → Click on your **service** (not the database)
2. Click on **"Variables"** tab
3. Add these environment variables:

```
SECRET_KEY=your-super-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

**To generate a SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Optional (for Stripe payments):**
```
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-webhook-secret
```

### Step 5: Deploy
Railway will automatically:
- ✅ Detect it's a Django project
- ✅ Install dependencies from `requirements.txt`
- ✅ Run the app using `Procfile`
- ✅ Deploy your application

**Your app will be live at:** `https://your-app-name.railway.app`

### Step 6: Run Migrations
1. Go to your project dashboard
2. Click on your **service**
3. Click **"Deployments"** tab
4. Click on the latest deployment
5. Click **"View Logs"** to see the deployment process

**Or use Railway CLI:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run migrations
railway run python manage.py migrate
```

### Step 7: Create Superuser
```bash
railway run python manage.py createsuperuser
```

Or use Railway dashboard:
1. Go to your service → **"Deployments"**
2. Click on deployment → **"View Logs"**
3. Use the terminal option if available

### Step 8: Collect Static Files (if needed)
Railway usually handles this, but if static files aren't loading:
```bash
railway run python manage.py collectstatic --noinput
```

### Step 9: Seed Sample Data (Optional)
```bash
railway run python manage.py seed_products
```

## 🎉 You're Done!

Your Makola Marketplace is now live at: `https://your-app.railway.app`

### Access Points:
- **Homepage**: `https://your-app.railway.app`
- **Admin Panel**: `https://your-app.railway.app/admin`
- **API**: `https://your-app.railway.app/api/`

## 🔧 Troubleshooting

### Static Files Not Loading
- Railway uses WhiteNoise (already configured)
- Make sure `whitenoise` is in `requirements.txt` ✅
- Check that `STATIC_ROOT` is set correctly ✅

### Database Connection Errors
- Railway automatically sets `DATABASE_URL`
- Make sure PostgreSQL service is running
- Check that `dj-database-url` is in `requirements.txt` ✅

### Migration Errors
- Run migrations manually: `railway run python manage.py migrate`
- Check logs in Railway dashboard

### App Not Starting
- Check logs in Railway dashboard
- Verify `Procfile` is correct ✅
- Make sure `gunicorn` is in `requirements.txt` ✅

## 💰 Pricing

- **Free Tier**: $5 credit/month (usually enough for small projects)
- **Hobby Plan**: $5/month (if you exceed free tier)
- **PostgreSQL**: Included in free tier

## 📝 Next Steps

1. **Custom Domain** (Optional):
   - Go to project → Settings → Domains
   - Add your custom domain
   - Update `ALLOWED_HOSTS` to include your domain

2. **Set up Stripe** (for payments):
   - Get API keys from https://stripe.com
   - Add to Railway environment variables

3. **Configure Email** (for password resets):
   - Use SendGrid, Mailgun, or similar
   - Add email settings to environment variables

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Check deployment logs in Railway dashboard

---

**Your app should be live in about 5-10 minutes! 🚀**




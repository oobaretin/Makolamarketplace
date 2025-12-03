# 🚀 Railway Deployment - Step by Step

## STEP 1: Sign Up for Railway

1. **Open your browser** and go to: https://railway.app
2. Click **"Start a New Project"** or **"Login"**
3. **Sign up with GitHub** (recommended - easiest way)
   - Click "Login with GitHub"
   - Authorize Railway to access your GitHub account

**✅ Checkpoint:** You should now be logged into Railway dashboard

---

## STEP 2: Create New Project from GitHub

1. In Railway dashboard, click **"+ New Project"** (top right)
2. Select **"Deploy from GitHub repo"**
3. If this is your first time, you may need to:
   - Click "Configure GitHub App" or "Add GitHub Account"
   - Select repositories to give Railway access to
   - Choose **"All repositories"** or just **"Makolamarketplace"**
4. Find and select your repository: **`Makolamarketplace`** or **`oobaretin/Makolamarketplace`**
5. Click on it to deploy

**✅ Checkpoint:** Railway should start detecting your project and begin deployment

---

## STEP 3: Add PostgreSQL Database

1. In your Railway project dashboard, you'll see your service
2. Click **"+ New"** button (top right or in the project)
3. Select **"Database"**
4. Click **"Add PostgreSQL"**
5. Railway will automatically:
   - Create a PostgreSQL database
   - Set the `DATABASE_URL` environment variable
   - Link it to your project

**✅ Checkpoint:** You should see two services now:
   - Your Django app service
   - PostgreSQL database service

---

## STEP 4: Configure Environment Variables

1. Click on your **Django app service** (not the database)
2. Click on the **"Variables"** tab
3. Click **"+ New Variable"** to add each one:

### Required Variables:

**Variable 1: SECRET_KEY**
- **Name:** `SECRET_KEY`
- **Value:** (Use the secret key generated below - copy it exactly)

**Variable 2: DEBUG**
- **Name:** `DEBUG`
- **Value:** `False`

**Variable 3: ALLOWED_HOSTS**
- **Name:** `ALLOWED_HOSTS`
- **Value:** `*.railway.app`

### Optional Variables (for later):

**Variable 4: Stripe Keys** (if you have them)
- **Name:** `STRIPE_PUBLIC_KEY`
- **Value:** `your-stripe-public-key`

- **Name:** `STRIPE_SECRET_KEY`
- **Value:** `your-stripe-secret-key`

**✅ Checkpoint:** You should have at least 3 environment variables set

---

## STEP 5: Wait for Deployment

Railway will automatically:
1. ✅ Detect it's a Django project
2. ✅ Install all dependencies from `requirements.txt`
3. ✅ Build your application
4. ✅ Deploy it

**Watch the deployment:**
- Click on your service
- Go to **"Deployments"** tab
- Click on the latest deployment
- Click **"View Logs"** to see the build process

**✅ Checkpoint:** Deployment should complete in 2-5 minutes. Look for "Build successful" or "Deployment successful"

---

## STEP 6: Get Your App URL

1. After deployment completes, go to your service
2. Click on the **"Settings"** tab
3. Scroll down to **"Domains"**
4. You'll see your app URL: `https://your-app-name.railway.app`
5. **Copy this URL** - this is your live website!

**✅ Checkpoint:** You should have a live URL like `https://makola-marketplace-production.up.railway.app`

---

## STEP 7: Run Database Migrations

### Option A: Using Railway Dashboard (Easiest)

1. Go to your service → **"Deployments"** tab
2. Click on the latest deployment
3. Look for a **"Shell"** or **"Terminal"** button
4. If available, open it and run:
   ```bash
   python manage.py migrate
   ```

### Option B: Using Railway CLI (Recommended)

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```
   (This will open your browser to authenticate)

3. **Link to your project:**
   ```bash
   railway link
   ```
   (Select your project when prompted)

4. **Run migrations:**
   ```bash
   railway run python manage.py migrate
   ```

**✅ Checkpoint:** Migrations should complete successfully

---

## STEP 8: Create Superuser (Admin Account)

Run this command (using Railway CLI or dashboard terminal):

```bash
railway run python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email (optional)
- Password (twice)

**✅ Checkpoint:** Superuser created successfully

---

## STEP 9: Test Your Live Site

1. **Visit your app URL:** `https://your-app.railway.app`
2. **Test the homepage** - should see your hero carousel
3. **Test admin panel:** `https://your-app.railway.app/admin`
   - Login with your superuser credentials
4. **Test product pages** - browse products

**✅ Checkpoint:** Your site should be fully functional!

---

## STEP 10: Seed Sample Data (Optional)

To add sample products and categories:

```bash
railway run python manage.py seed_products
```

**✅ Checkpoint:** Sample products should be added to your database

---

## 🎉 Congratulations!

Your Makola Marketplace is now live!

### Quick Links:
- **Homepage:** `https://your-app.railway.app`
- **Admin Panel:** `https://your-app.railway.app/admin`
- **Products:** `https://your-app.railway.app`

---

## 🔧 Troubleshooting

### If deployment fails:
1. Check the **"Logs"** tab in Railway
2. Look for error messages
3. Common issues:
   - Missing environment variables → Add them in Variables tab
   - Database connection → Make sure PostgreSQL is running
   - Static files → Should work automatically with WhiteNoise

### If static files don't load:
```bash
railway run python manage.py collectstatic --noinput
```

### If you need to restart:
- Go to your service → **"Deployments"** → Click **"Redeploy"**

---

## 📞 Need Help?

- Check Railway logs for errors
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

---

**Ready to start? Begin with STEP 1! 🚀**




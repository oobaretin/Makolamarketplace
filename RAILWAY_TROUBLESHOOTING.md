# Railway 500 Error - Troubleshooting

## Step 1: Check Railway Logs

1. Go to your Railway project
2. Click on your **Django service**
3. Go to **"Deployments"** tab
4. Click on the **latest deployment**
5. Click **"View Logs"** or check the **"Logs"** tab
6. Look for **red error messages** at the bottom

**Common errors you might see:**
- `relation "accounts_user" does not exist` → Need to run migrations
- `No such table` → Need to run migrations
- `Database connection error` → Database not linked properly
- `ModuleNotFoundError` → Missing dependency

## Step 2: Run Database Migrations

The 500 error is likely because the database tables don't exist yet. Let's run migrations:

### Using Railway CLI (Recommended):

```bash
# 1. Install Railway CLI (if not already installed)
npm i -g @railway/cli

# 2. Login
railway login

# 3. Link to your project
railway link
# (Select your project when prompted)

# 4. Run migrations
railway run python manage.py migrate
```

### Using Railway Dashboard:

1. Go to your service → **"Deployments"** tab
2. Click on latest deployment
3. Look for **"Shell"** or **"Terminal"** button
4. If available, open terminal and run:
   ```bash
   python manage.py migrate
   ```

## Step 3: Check Logs Again

After running migrations, check if the error is resolved:
1. Visit your site: `https://makolamarketplace-production.up.railway.app`
2. If still 500 error, check logs again for new errors

## Step 4: Create Superuser (After migrations)

```bash
railway run python manage.py createsuperuser
```

## Common Issues:

### Issue: "relation does not exist"
**Solution:** Run migrations (Step 2 above)

### Issue: "Database connection failed"
**Solution:** 
- Check that PostgreSQL service is running
- Verify `DATABASE_URL` is set (Railway sets this automatically)

### Issue: "Static files not found"
**Solution:**
```bash
railway run python manage.py collectstatic --noinput
```

---

**Please check the Railway logs and share the error message you see!**




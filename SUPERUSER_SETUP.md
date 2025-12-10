# Superuser Setup Guide

## Automatic Superuser Creation

The superuser will be created automatically on each deployment if it doesn't exist.

## Option 1: Set Environment Variables (Recommended)

Add these to your Railway environment variables:

1. Go to Railway → Your Django service → **Variables** tab
2. Add these variables:

**Variable 1:**
- **Name:** `SUPERUSER_USERNAME`
- **Value:** `admin` (or your preferred username)

**Variable 2:**
- **Name:** `SUPERUSER_EMAIL`
- **Value:** `admin@makolamarketplace.com` (or your email)

**Variable 3:**
- **Name:** `SUPERUSER_PASSWORD`
- **Value:** `your-secure-password-here` (choose a strong password)

3. Save the variables
4. Railway will automatically redeploy and create the superuser

## Option 2: Let it Generate Automatically

If you don't set `SUPERUSER_PASSWORD`, the script will:
- Generate a random password
- Display it in the Railway logs
- You can find it in: Service → Deployments → Latest deployment → View Logs

## Access Admin Panel

After deployment:
1. Go to: `https://makolamarketplace-production.up.railway.app/admin`
2. Login with:
   - Username: `admin` (or your SUPERUSER_USERNAME)
   - Password: Your SUPERUSER_PASSWORD (or the generated one from logs)

## Change Password Later

If you need to change the password later, you can:
1. Login to admin panel
2. Go to Users → Select your user → Change password
3. Or run: `npx @railway/cli run python manage.py changepassword admin`

---

**The superuser will be created automatically on the next deployment!**








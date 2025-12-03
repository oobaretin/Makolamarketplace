# Deploying Makola Marketplace to Vercel

## ⚠️ Important Limitations

**Vercel is NOT ideal for Django applications** because:
1. **No persistent database** - You'll need an external PostgreSQL database (e.g., Supabase, Neon, Railway)
2. **Serverless limitations** - Cold starts, execution time limits
3. **File system** - Read-only, so media uploads won't persist (use S3/Cloudinary)
4. **Static files** - Need special handling with WhiteNoise or CDN

## Recommended Alternatives (Better for Django)

### 1. **Railway** (Easiest - Recommended)
- Free tier available
- Automatic PostgreSQL database
- Simple deployment from GitHub
- Visit: https://railway.app

### 2. **Render**
- Free tier with PostgreSQL
- Easy Django deployment
- Visit: https://render.com

### 3. **DigitalOcean App Platform**
- $5/month starter plan
- Managed PostgreSQL
- Visit: https://www.digitalocean.com/products/app-platform

## If You Still Want to Deploy to Vercel

### Prerequisites

1. **External PostgreSQL Database** (Required)
   - Sign up for [Supabase](https://supabase.com) (free tier)
   - Or [Neon](https://neon.tech) (free tier)
   - Or [Railway PostgreSQL](https://railway.app) (free tier)

2. **Media Storage** (Required for file uploads)
   - [Cloudinary](https://cloudinary.com) (free tier)
   - Or AWS S3

3. **Vercel Account**
   - Sign up at https://vercel.com

### Deployment Steps

1. **Set up External Database**
   ```bash
   # Get your database URL from Supabase/Neon/Railway
   # Format: postgresql://user:password@host:port/dbname
   ```

2. **Configure Environment Variables in Vercel**
   Go to your Vercel project settings and add:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.vercel.app,yourdomain.com
   DB_NAME=your-db-name
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_HOST=your-db-host
   DB_PORT=5432
   STRIPE_PUBLIC_KEY=your-stripe-key
   STRIPE_SECRET_KEY=your-stripe-secret
   ```

3. **Update settings.py for Vercel**
   - Already configured to use environment variables
   - Make sure `whitenoise` is in requirements.txt (already added)

4. **Deploy**
   ```bash
   # Install Vercel CLI
   npm i -g vercel
   
   # Login
   vercel login
   
   # Deploy
   vercel
   ```

5. **Run Migrations**
   ```bash
   # After first deployment, run migrations
   vercel env pull .env.local
   python manage.py migrate
   ```

### Important Notes

- **Static Files**: Use `python manage.py collectstatic` before deploying
- **Media Files**: Configure Cloudinary or S3 for user uploads
- **Database**: Must be external (Vercel doesn't provide databases)
- **Cold Starts**: First request after inactivity may be slow

## Quick Deploy to Railway (Recommended)

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Add PostgreSQL
railway add postgresql

# 5. Deploy
railway up
```

Railway will automatically:
- Detect Django
- Set up PostgreSQL
- Configure environment variables
- Deploy your app

## Quick Deploy to Render

1. Connect your GitHub repository
2. Create a new "Web Service"
3. Select your repository
4. Render will auto-detect Django
5. Add PostgreSQL database
6. Deploy!

---

**For showing to your client quickly, I recommend Railway or Render as they're much simpler for Django applications.**




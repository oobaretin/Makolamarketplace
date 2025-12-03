# Railway Deployment Checklist

## ✅ Current Status

### Code Setup
- ✅ Context processor created and registered
- ✅ Categories dropdown in navigation menu
- ✅ Category grid on homepage
- ✅ Logo left-aligned in navigation
- ✅ All 19 categories exist in database

### Railway Configuration
- ✅ `Procfile` configured
- ✅ `start.sh` script for migrations
- ✅ `runtime.txt` for Python version
- ✅ `requirements.txt` with all dependencies

## 🔍 Verification Steps

### 1. Check Railway Environment Variables
Make sure these are set in Railway:
- `SECRET_KEY` - Django secret key
- `DEBUG=False` - Set to False in production
- `ALLOWED_HOSTS` - Should include your Railway domain (e.g., `*.railway.app`)
- `DATABASE_URL` - Automatically set by Railway PostgreSQL
- `SUPERUSER_USERNAME` - For admin access
- `SUPERUSER_EMAIL` - For admin access
- `SUPERUSER_PASSWORD` - For admin access

### 2. Verify Categories Are Showing
After deployment, check:
1. Navigation menu → Click "Categories" dropdown
2. Homepage → Scroll to "Shop by Category" section
3. Filter sidebar → Category dropdown should show all categories

### 3. Verify Logo Position
- Logo should be on the far left
- Navigation items on the right
- Works on both mobile and desktop

## 🐛 Troubleshooting

### If Categories Don't Show:
1. **Restart Railway service** - Context processors need a restart
2. **Check logs** - `railway logs` or Railway dashboard
3. **Verify database** - Categories should exist:
   ```bash
   railway run python manage.py shell
   >>> from products.models import Category
   >>> Category.objects.filter(is_active=True).count()
   # Should return 19
   ```

### If Logo Not Left-Aligned:
- Check browser cache - Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Verify template is updated - Check `templates/base.html` line 27-33

### Common Issues:
- **500 Error**: Check `ALLOWED_HOSTS` includes Railway domain
- **No categories**: Restart the service after context processor changes
- **Static files not loading**: Run `collectstatic` (should be in `start.sh`)

## 📝 Quick Commands

### Check Categories in Railway:
```bash
railway run python manage.py shell
>>> from products.models import Category
>>> Category.objects.filter(is_active=True).count()
```

### Create Categories if Missing:
```bash
railway run python manage.py create_categories
```

### Check Logs:
```bash
railway logs
```

## 🚀 Deployment Steps

1. **Push to GitHub** (already done)
2. **Railway auto-deploys** from GitHub
3. **Check deployment logs** in Railway dashboard
4. **Verify site is live** at your Railway URL
5. **Test categories dropdown** in navigation
6. **Test category grid** on homepage

## 💡 Free Tier Notes

Railway's free tier ($1/month credit) is sufficient for:
- ✅ Django apps
- ✅ PostgreSQL databases
- ✅ Low to moderate traffic
- ✅ Static file serving

You don't need a paid plan unless you have high traffic or need more resources.


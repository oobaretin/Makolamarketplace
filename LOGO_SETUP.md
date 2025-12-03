# Logo Setup Instructions

## Quick Setup

1. **Place your logo file** in the `static/logo/` folder
   - File name: `logo.png`
   - Recommended size: 150-200px width, auto height
   - Format: PNG with transparent background (preferred) or JPG

2. **The logo will automatically appear** in the navigation bar

## Folder Location

```
Africanstore/
  static/
    logo/
      logo.png    ← Place your logo here
      README.md   ← Instructions
```

## Logo Specifications

### Recommended Dimensions
- **Width**: 150-200px
- **Height**: Auto (maintain aspect ratio)
- **Format**: PNG (with transparency) or JPG
- **File Size**: Under 100KB for fast loading

### Design Tips
- Use a transparent background (PNG) for best results
- Ensure logo is readable on orange background (#ea580c)
- Keep it simple and recognizable at small sizes
- Consider both light and dark versions if needed

## Adding Your Logo

### Method 1: Using File Manager
1. Navigate to: `/Users/osagieobaretin/Africanstore/static/logo/`
2. Copy your logo file
3. Rename it to `logo.png` (if needed)
4. Refresh your browser

### Method 2: Using Terminal
```bash
# Copy your logo file to the logo folder
cp /path/to/your/logo.png /Users/osagieobaretin/Africanstore/static/logo/logo.png
```

### Method 3: Drag and Drop
- Open the `static/logo/` folder in Finder
- Drag your logo file into the folder
- Rename to `logo.png` if needed

## Testing

After adding your logo:
1. Refresh the browser (Ctrl+F5 or Cmd+Shift+R for hard refresh)
2. The logo should appear in the top-left navigation
3. If logo doesn't appear, check:
   - File is named exactly `logo.png`
   - File is in `static/logo/` folder
   - Run `python manage.py collectstatic` if in production

## Alternative Formats

If you have different formats:
- `logo.svg` - Vector format (best quality, update template to use it)
- `logo.jpg` - Update template to reference `logo.jpg` instead
- `favicon.ico` - For browser tab icon (16x16 or 32x32px)

## Customization

To change logo size, edit `templates/base.html`:
```html
<!-- Current: h-10 (40px height) -->
<img src="{% static 'logo/logo.png' %}" class="h-10 w-auto" ...>

<!-- Make it larger: h-12 (48px) -->
<img src="{% static 'logo/logo.png' %}" class="h-12 w-auto" ...>

<!-- Make it smaller: h-8 (32px) -->
<img src="{% static 'logo/logo.png' %}" class="h-8 w-auto" ...>
```

## Need Help?

- Check that the file path is correct: `static/logo/logo.png`
- Ensure file permissions allow reading
- Clear browser cache if logo doesn't update
- Check browser console for 404 errors


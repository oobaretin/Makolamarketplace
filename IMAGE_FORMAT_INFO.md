# Image Format Information

## JPEG vs PNG for Hero Images

### Current Format: JPEG ✅
- **File Size**: Smaller (better for web performance)
- **Quality**: Good for photos/product images
- **Best For**: Hero carousels with product photos
- **Transparency**: No (but not needed for hero images)

### PNG Format
- **File Size**: Larger (slower loading)
- **Quality**: Better for graphics/logos with text
- **Best For**: Logos, icons, graphics with transparency
- **Transparency**: Yes (supports transparent backgrounds)

## Recommendation

**Keep JPEG format** for hero carousel images because:
1. ✅ Smaller file sizes = faster page loading
2. ✅ Better for photos/product images
3. ✅ No transparency needed for hero backgrounds
4. ✅ Standard format for web images

## If You Want to Convert to PNG

If you still want PNG format, you can use this command:

```bash
# Install ImageMagick if needed: brew install imagemagick
cd static/logo
for file in *.jpg; do
    convert "$file" "${file%.jpg}.png"
done
```

But **it's not necessary** - JPEG works perfectly fine for hero images!

## Current Issue: File Naming

The real issue was **spaces in filenames**, not the format. We've renamed the files to use underscores instead of spaces, which should fix the loading issue.








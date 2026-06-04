# Google Drive Setup - Quick Guide (5 Minutes)

## Step 1: Install (2 min)
```
https://www.google.com/drive/download/
→ Download & Install
→ Sign in
```

## Step 2: Create Folder (1 min)
```
Google Drive (browser)
→ New Folder: "SEO Pages"
→ Move your doc there
```

## Step 3: Update .env (1 min)
```env
FOODAMIGO_SEO_DIR=C:/Users/Arohi/Google Drive/My Drive/SEO Pages
```

## Step 4: Test (1 min)
```bash
python main.py
```

## Done! ✅

**Now when you edit Google Doc, automation sees changes automatically.**

---

## Daily Use

```
1. Edit Google Doc
2. Run: python main.py
```

That's it. No downloads needed.

---

## Troubleshooting

**Path error?**
```env
# Use forward slashes
FOODAMIGO_SEO_DIR=C:/Users/Arohi/Google Drive/My Drive/SEO Pages
```

**Not syncing?**
- Check Google Drive icon in system tray
- Wait 10 seconds after editing doc
- Right-click file → "Available offline"

---

See `GOOGLE_DRIVE_SETUP.md` for full details.

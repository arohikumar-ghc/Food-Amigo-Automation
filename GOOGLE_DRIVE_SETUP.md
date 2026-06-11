# Google Drive Desktop Setup - Production Guide

## 🎯 Why This Solution?

✅ **Real-time sync** - Edit Google Doc, changes appear instantly  
✅ **No manual download** - Zero extra steps  
✅ **Production-grade** - Used by all major companies  
✅ **Team collaboration** - Multiple people can edit  
✅ **Version history** - Google keeps all versions  
✅ **Zero maintenance** - Set up once, works forever  

---

## 📥 Step 1: Install Google Drive Desktop

### Download & Install

1. Go to: **https://www.google.com/drive/download/**
2. Click **"Download Drive for desktop"**
3. Run the installer
4. Sign in with your Google account

### Choose Sync Method

You'll see two options:

- **Stream files** (Recommended) - Files stored in cloud, accessed on-demand
- **Mirror files** - Full copy on your computer

**Choose:** Stream files (saves disk space)

---

## 📁 Step 2: Locate Your Synced Folder

After installation, your Google Drive folder appears at:

```
C:\Users\Arohi\Google Drive\My Drive\
```

**How to verify:**
1. Open File Explorer
2. Look for "Google Drive" in left sidebar
3. Click it → You'll see "My Drive" folder

---

## 📄 Step 3: Organize Your Google Docs

### In Google Drive (Browser)

1. Go to **https://drive.google.com**
2. Create folder: **"SEO Pages"**
3. Move your Google Doc into this folder
4. **Important:** The doc will auto-convert to .docx format in synced folder

### Result

**In Browser:**
```
Google Drive/
└── SEO Pages/
    └── Untitled document (Google Doc format)
```

**On Your Computer (Auto-synced):**
```
C:\Users\Arohi\Google Drive\My Drive\SEO Pages\
└── Untitled document.docx (Word format)
```

---

## ⚙️ Step 4: Update Your Configuration

### Option A: Edit .env File (Recommended)

Open `.env` and update:

```env
# Google Drive sync folder path
FOODAMIGO_SEO_DIR=C:\Users\Arohi\Google Drive\My Drive\SEO Pages
```

**Full .env example:**
```env
FOODAMIGO_EMAIL=antlerdemo@tabless.io
FOODAMIGO_PASSWORD=UdV3B80OV7Hr
FOODAMIGO_RESTAURANT=HWY TO INDIA
FOODAMIGO_HEADLESS=false
FOODAMIGO_TIMEOUT=30000

# Google Drive sync folder
FOODAMIGO_SEO_DIR=C:\Users\Arohi\Google Drive\My Drive\SEO Pages
```

### Option B: Edit config.py Directly

If you don't use .env, edit `config.py`:

```python
seo_files_dir: str = r"C:\Users\Arohi\Google Drive\My Drive\SEO Pages"
```

---

## ✅ Step 5: Test the Setup

### Test 1: Verify Sync

1. Edit your Google Doc in browser
2. Add text: "TEST - 2026"
3. Save (Ctrl+S)
4. Wait 5 seconds
5. Check local folder: `C:\Users\Arohi\Google Drive\My Drive\SEO Pages\`
6. Open the .docx file
7. **Verify:** You should see "TEST - 2026"

### Test 2: Run Parser

```bash
python parser.py "C:\Users\Arohi\Google Drive\My Drive\SEO Pages\Untitled document.docx"
```

**Expected:** Shows parsed content with latest changes

### Test 3: Run Automation

```bash
python main.py
```

**Expected:** Processes files from Google Drive folder

---

## 🔄 Daily Workflow (After Setup)

### Old Way (Manual)
```
1. Edit Google Doc
2. File → Download → Word
3. Save to seo_files/
4. Replace old file
5. Run automation
```

### New Way (Automatic)
```
1. Edit Google Doc
2. Run automation ✓

(That's it! Sync happens automatically)
```

---

## 🎯 How It Works

```
┌─────────────────────────────────────┐
│  Google Doc (Browser)               │
│  - You edit here                    │
└─────────────┬───────────────────────┘
              │
              ▼ (Auto-sync by Google Drive Desktop)
              │
┌─────────────▼───────────────────────┐
│  Local Folder                       │
│  C:\Users\Arohi\Google Drive\...   │
│  - .docx file appears here          │
│  - Updates in real-time             │
└─────────────┬───────────────────────┘
              │
              ▼ (Automation reads from here)
              │
┌─────────────▼───────────────────────┐
│  parser.py                          │
│  - Reads latest .docx               │
│  - Always has fresh content         │
└─────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### Issue 1: "Folder not found"

**Cause:** Google Drive Desktop not installed or not signed in

**Solution:**
```bash
# Check if folder exists
dir "C:\Users\Arohi\Google Drive"

# If not found, install Google Drive Desktop
```

---

### Issue 2: File not syncing

**Cause:** Google Drive Desktop not running

**Solution:**
1. Check system tray (bottom-right)
2. Look for Google Drive icon
3. If not there, open "Google Drive" from Start Menu

---

### Issue 3: Old content in .docx file

**Cause:** Sync delay or cached file

**Solution:**
1. Right-click .docx file
2. Click "Available offline" to force download
3. Wait 10 seconds
4. Try again

---

### Issue 4: Path error in Python

**Cause:** Backslashes in Windows path

**Solution:**

**Wrong:**
```env
FOODAMIGO_SEO_DIR=C:\Users\Arohi\Google Drive\My Drive\SEO Pages
```

**Correct (use raw string or forward slashes):**
```env
# Option 1: Forward slashes
FOODAMIGO_SEO_DIR=C:/Users/Arohi/Google Drive/My Drive/SEO Pages

# Option 2: Double backslashes
FOODAMIGO_SEO_DIR=C:\\Users\\Arohi\\Google Drive\\My Drive\\SEO Pages
```

---

## 🏢 Team Collaboration

### Sharing with Team

1. Right-click "SEO Pages" folder in Google Drive
2. Click "Share"
3. Add team members' emails
4. Set permission: "Editor"

Now:
- ✅ Anyone can edit docs
- ✅ Everyone sees latest version
- ✅ Changes sync to all computers
- ✅ No manual file sharing needed

---

## 📊 Benefits Summary

| Feature | Before | After (Google Drive) |
|---------|--------|---------------------|
| Edit doc | Browser | Browser |
| Download | Manual ❌ | Auto ✅ |
| Update project | Copy file ❌ | Auto ✅ |
| Team sync | Email files ❌ | Auto ✅ |
| Version control | None ❌ | Google ✅ |
| Time per update | 2 minutes | 0 seconds ✅ |

---

## 🎓 Pro Tips

### Tip 1: Use Descriptive Folder Names

```
Google Drive/
├── SEO Pages - Lancaster/
├── SEO Pages - Philadelphia/
└── SEO Pages - Archive/
```

Update `.env`:
```env
FOODAMIGO_SEO_DIR=C:/Users/Arohi/Google Drive/My Drive/SEO Pages - Lancaster
```

### Tip 2: Check Sync Status

Look at file icon in File Explorer:
- ✅ Green checkmark = Synced
- 🔄 Blue arrows = Syncing
- ☁️ Cloud icon = Not downloaded yet

### Tip 3: Work Offline

Google Drive Desktop caches recent files. You can work even without internet!

### Tip 4: Monitor Sync

Click Google Drive icon in system tray → See sync status

---

## 🔐 Security Notes

- Google Drive uses encryption
- Files only accessible with your account
- You can revoke access anytime
- Two-factor authentication recommended

---

## 📝 Configuration Reference

### .env File (Complete)

```env
# Login credentials
FOODAMIGO_EMAIL=antlerdemo@tabless.io
FOODAMIGO_PASSWORD=UdV3B80OV7Hr

# Restaurant
FOODAMIGO_RESTAURANT=HWY TO INDIA

# Google Drive sync folder (IMPORTANT)
FOODAMIGO_SEO_DIR=C:/Users/Arohi/Google Drive/My Drive/SEO Pages

# Optional settings
FOODAMIGO_HEADLESS=false
FOODAMIGO_TIMEOUT=30000
```

### config.py (If not using .env)

```python
@dataclass
class AutomationConfig:
    email: str
    password: str
    restaurant_name: str
    
    base_url: str = "https://restaurant.foodamigos.io"
    
    # Google Drive sync folder
    seo_files_dir: str = r"C:\Users\Arohi\Google Drive\My Drive\SEO Pages"
    logs_dir: str = "logs"
    
    headless: bool = False
    timeout: int = 30000
```

---

## ✅ Setup Checklist

- [ ] Google Drive Desktop installed
- [ ] Signed in with Google account
- [ ] "SEO Pages" folder created in Google Drive
- [ ] Google Doc moved to "SEO Pages" folder
- [ ] Verified .docx file appears in local folder
- [ ] Updated `.env` with Google Drive path
- [ ] Tested parser with new path
- [ ] Tested automation end-to-end
- [ ] Edited doc and verified auto-sync

---

## 🚀 You're Done!

From now on:
1. Edit Google Doc in browser
2. Run automation
3. That's it!

**No more manual downloads. No more file copying. Production-ready.** ✅

---

**Questions?** Check the sync status in Google Drive Desktop app.

**Still having issues?** Make sure:
1. Google Drive Desktop is running (check system tray)
2. Internet connection is active
3. Path in `.env` is correct
4. File has synced (check for green checkmark icon)

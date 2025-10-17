# 🚀 Ngrok Setup Guide

## ✅ Account Created!
- **Authtoken**: `34BGjnjeplQoiPQEepIRBcYvI3t_7NJE1Mp6kACPG2UyoEE3E`

---

## 📥 Download Ngrok

### Option 1: Direct Download
1. Visit: https://ngrok.com/download
2. Click **"Download for Windows (64-bit)"**
3. Save the ZIP file
4. Extract it (Right-click → Extract All)
5. Place `ngrok.exe` in an easy location:
   - Example: `C:\ngrok\`
   - Or: Desktop
   - Or: Your project folder

### Option 2: Using Chocolatey (if installed)
```powershell
choco install ngrok
```

---

## 🔧 Setup Commands

Once you have `ngrok.exe`, run these commands:

### 1. Navigate to ngrok folder
```powershell
cd "C:\path\to\ngrok\folder"
```

Or if on Desktop:
```powershell
cd "$env:USERPROFILE\Desktop"
```

### 2. Add Authtoken (IMPORTANT!)
```powershell
.\ngrok.exe config add-authtoken 34BGjnjeplQoiPQEepIRBcYvI3t_7NJE1Mp6kACPG2UyoEE3E
```

### 3. Start Tunnel (Make sure your Flask app is running!)
```powershell
.\ngrok.exe http 5000
```

---

## 🎯 What You'll See

After running step 3, you'll see:

```
ngrok

Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        India (in)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abcd-1234-xyz.ngrok-free.app -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy the Forwarding URL!** 🌐
Example: `https://abcd-1234-xyz.ngrok-free.app`

---

## ✅ Important Notes

1. **Keep your Flask app running** (`app.py` or `app2.py`)
2. **Keep ngrok terminal open** (don't close it)
3. **Share the Forwarding URL** with anyone
4. **URL changes** every time you restart ngrok (free tier)

---

## 🔥 Quick Start Checklist

- [ ] Download ngrok from https://ngrok.com/download
- [ ] Extract `ngrok.exe`
- [ ] Run: `.\ngrok.exe config add-authtoken 34BGjnjeplQoiPQEepIRBcYvI3t_7NJE1Mp6kACPG2UyoEE3E`
- [ ] Make sure Flask app is running (port 5000)
- [ ] Run: `.\ngrok.exe http 5000`
- [ ] Copy the `https://` URL
- [ ] Share with friends! 🎉

---

## 🌐 Your Public Link Will Look Like:

`https://random-name-12345.ngrok-free.app`

Anyone can access this link from anywhere! 🌍

---

## 🆘 Troubleshooting

### "ngrok not found"
- Make sure you're in the correct folder where `ngrok.exe` is located
- Use full path: `C:\path\to\ngrok.exe http 5000`

### "Failed to connect"
- Make sure your Flask app is running on port 5000
- Check: http://localhost:5000 (should work first)

### "Authtoken not found"
- Run the authtoken command again (step 2)

---

## 📞 Need Help?

Just ask! I'm here to help you get your public link! 🚀

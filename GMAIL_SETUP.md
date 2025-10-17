# 📧 Gmail OTP Setup Guide

## Step-by-Step Instructions

### 1️⃣ Create Gmail App Password

1. Go to your **Google Account**: https://myaccount.google.com/
2. Click **Security** (left sidebar)
3. Enable **2-Step Verification** if not already enabled:
   - Click "2-Step Verification"
   - Follow the setup process
4. Go back to **Security** page
5. Search for **"App passwords"** or scroll down to find it
6. Click **App passwords**
7. Select:
   - **App**: Mail
   - **Device**: Windows Computer
8. Click **Generate**
9. **Copy the 16-digit password** (format: `abcd efgh ijkl mnop`)
   - Remove spaces: `abcdefghijklmnop`

### 2️⃣ Update .env File

Open the `.env` file in your project and update these lines:

```env
SMTP_EMAIL=your-actual-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
```

**Example:**
```env
SMTP_EMAIL=rupamkumari@gmail.com
SMTP_PASSWORD=abcd1234efgh5678
```

### 3️⃣ Save and Restart Server

1. **Save** the `.env` file
2. **Stop** the current server (Ctrl+C in terminal)
3. **Restart** server:
   ```powershell
   .\start_server_app2.ps1
   ```

### 4️⃣ Test OTP Email

1. Open browser: `http://localhost:5000`
2. Enter your **real email address**
3. Click **"Send OTP"**
4. **Check your email inbox** for OTP
5. Enter the **6-digit code**
6. Click **"Verify & Continue"**

---

## 🔧 Troubleshooting

### Email Not Sending?

**Check these:**
- ✅ 2-Step Verification is enabled on Google Account
- ✅ App Password is correct (no spaces)
- ✅ Email address is correct in `.env`
- ✅ `.env` file is saved
- ✅ Server is restarted after editing `.env`

### Check Terminal for Errors

Look for messages like:
```
[DEV MODE] OTP for email@example.com: 123456  ← Dev mode (email not configured)
OTP sent to email@example.com                 ← Success!
Failed to send email: ...                     ← Error
```

---

## 🛡️ Security Notes

- ✅ **Never share** your App Password
- ✅ **Never commit** `.env` file to Git
- ✅ `.env` is already in `.gitignore`
- ✅ Use different passwords for production

---

## 📝 Alternative: Dev Mode (No Email)

If you don't want to setup email right now, you can test in **Dev Mode**:

1. Leave `.env` as is (empty `SMTP_EMAIL`)
2. OTP will be printed in **terminal/console**
3. Check terminal output for:
   ```
   [DEV MODE] OTP for test@example.com: 123456
   ```

---

## ✅ Current Status

**File created:** `.env`  
**Location:** `C:\Users\kumar\OneDrive\Desktop\Image Inpainting\.env`

**What to do:**
1. Edit `.env` file (opened in Notepad)
2. Replace `your-email@gmail.com` with your Gmail
3. Replace `your-16-digit-app-password` with your App Password
4. Save the file
5. Restart server

---

Built by Rupam Kumari 🎨

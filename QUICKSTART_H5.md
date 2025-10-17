# Quick Start Guide for H5 Model

## 🚀 Run app2.py (H5 Model - Recommended)

### Step 1: Start Flask Server
Open PowerShell in the project folder and run:

```powershell
.\start_server2.ps1
```

You should see:
```
=================================================
  Image Inpainting Server (H5 Model)
  Built by Rupam Kumari
=================================================

✅ Activating virtual environment...
✅ H5 model found: saved_model.h5 (207.78 MB)
✅ Environment file found: .env

🚀 Starting Flask server on http://localhost:5001
   (H5 Model Version)
```

### Step 2: Start Ngrok (For Public Access)
Open another PowerShell terminal and run:

```powershell
C:\Users\kumar\Downloads\ngrok.exe http 5001
```

### Step 3: Access the App

**Local Access:**
- Open browser: http://localhost:5001

**Public Access:**
- Copy the ngrok URL (e.g., `https://xxxx-xxxx.ngrok-free.app`)
- Share with anyone worldwide!

## 📝 Testing the App

1. Enter your email address
2. Click "Send OTP"
3. Check console for OTP (dev mode) or your email
4. Enter OTP code
5. Check "Remember Me" to stay logged in for 30 days
6. Click "Verify"
7. Upload an image and draw mask to inpaint!

## 🔄 Switching Between Models

**To use SavedModel (app.py):**
```powershell
.\start_server.ps1
# Then: ngrok http 5000
```

**To use H5 Model (app2.py):**
```powershell
.\start_server2.ps1  
# Then: ngrok http 5001
```

## ⚡ Why H5 Model is Better

- ✅ **52% smaller** (208 MB vs 435 MB)
- ✅ **Faster loading**
- ✅ **Same quality**
- ✅ **Better compatibility**

## 🛠️ Troubleshooting

**Model not found?**
- Run the Jupyter notebook `image-inpainting.ipynb`
- Execute the last cell to save `saved_model.h5`

**Port already in use?**
- Change port in `.env`: `PORT=5002`
- Or stop other Flask servers

**Virtual environment not found?**
- Create it: `python -m venv .venv`
- Activate: `.venv\Scripts\Activate.ps1`
- Install: `pip install -r requirements.txt`

---

**Built by Rupam Kumari** 🚀

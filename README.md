# 🎨 AI Image Inpainting Web App

Remove unwanted objects from photos using AI! Features OTP authentication, email integration, and easy public deployment.

**Built by Rupam Kumari** | MIT License

[![GitHub](https://img.shields.io/badge/GitHub-ImageInpainting-blue)](https://github.com/techietinker01/ImageInpainting)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://www.tensorflow.org/)

---

## ✨ Features

- 🎨 **AI-Powered Inpainting** - Remove unwanted objects using deep learning
- 🖌️ **Interactive Canvas** - Draw masks with adjustable brush size
- 🔐 **OTP Authentication** - Passwordless email-based login with "Remember Me"
- 📧 **Gmail Integration** - Automatic OTP delivery via email
- 🌐 **Public Access** - Share via Ngrok tunnel
- 💾 **Download Results** - Save your cleaned images
- 🔒 **Secure Sessions** - Encrypted Flask sessions

---

## 🚀 Quick Start

### 1. Clone & Setup

```powershell
# Clone repository
git clone https://github.com/techietinker01/ImageInpainting.git
cd ImageInpainting

# Create virtual environment
python -m venv .venv
& .\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

Create `.env` file for Gmail OTP:

```env
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SECRET_KEY=your-random-secret-key
PORT=5000
```

> **Note:** Without `.env`, OTP will print in terminal (dev mode)

### 3. Start Server

```powershell
python app.py
```

Open <http://localhost:5000>

### 4. Public Access (Optional)

```powershell
# Download ngrok from ngrok.com
ngrok http 5000
```

Share the generated URL with anyone! 🌍

---

## � Usage Guide

### Login with OTP

1. Enter your email address
2. Click "Send OTP"
3. Check email (or terminal in dev mode)
4. Enter 6-digit OTP code
5. ✅ Check "Remember me for 30 days" to stay logged in
6. Click "Verify"

### Inpaint Images

1. **Upload** - Click or drag & drop your photo
2. **Draw Mask** - Brush over objects to remove
3. **Adjust** - Use slider for brush size
4. **Generate** - Click to process with AI
5. **Download** - Save your result!

**Pro Tips:**

- 🎨 Larger brush for big areas
- ✏️ Smaller brush for details
- 🧹 Eraser tool to fix mistakes
- 🔄 Clear to start over

---

## 🔐 Gmail OTP Setup (Optional)

**For production, enable automatic email OTP:**

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Create **App Password** (Mail → Windows/Other)
4. Add to `.env`:

```env
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-16-digit-app-password
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

5.Restart: `python app.py`

Now OTPs will be sent via email! 📧

---

## 🌐 Deploy to Ngrok (Public Access)

1. Sign up at [ngrok.com](https://ngrok.com/signup)
2. Download ngrok
3. Get authtoken from dashboard
4. Configure: `ngrok config add-authtoken YOUR_TOKEN`
5. Start tunnel: `ngrok http 5000`
6. Share the URL!

---

## ☁️ Cloud Deployment (Render)

**For permanent URL with free hosting:**

1. Create account at [render.com](https://render.com)
2. New Web Service → Connect GitHub repo
3. **Build:** `pip install -r requirements.txt`
4. **Start:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4`
5. **Add Environment Variables:**
   - `SMTP_EMAIL`
   - `SMTP_PASSWORD`
   - `SECRET_KEY`
   - `TF_ENABLE_ONEDNN_OPTS=0`
6. Deploy!

Your app will be at `https://your-app.onrender.com` 🚀

---

## ️ Tech Stack

**Frontend:** HTML5 Canvas, Vanilla JavaScript, Modern CSS

**Backend:** Flask, Python 3.9+, TensorFlow/Keras, OpenCV, Pillow, NumPy

**Auth:** Flask Sessions, SMTP/Gmail, OTP System

**Deploy:** Ngrok, Render, Gunicorn

---

## 🐛 Troubleshooting

**OTP not receiving?**

- Check spam folder
- Verify Gmail App Password (16 digits, no spaces)
- Ensure 2-Step Verification enabled
- Dev mode: OTP prints in terminal

**Module not found?**

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Ngrok offline (ERR_NGROK_3200)?**

```powershell
# Restart both
python app.py
ngrok http 5000
```

**TensorFlow import error?**

- Use Python 3.9-3.11 (not 3.13)
- App falls back to OpenCV if TensorFlow unavailable

---

## � Project Structure

```text
ImageInpainting/
├── app.py                  # Main Flask app
├── requirements.txt        # Dependencies
├── .env                    # Config (not in git)
├── .gitignore             
├── README.md              
├── LICENSE                
├── static/
│   ├── index.html         # Login page
│   ├── app.html           # Inpainting UI
│   ├── main.js            # Canvas logic
│   └── styles.css         
├── saved_model.h5          # Trained model
├── uploads/               # User images
├── outputs/               # Results
└── image-inpainting.ipynb # Training notebook
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:

- Report bugs
- Suggest features  
- Submit pull requests

---

## 📄 License

MIT License - Free to use, modify, and distribute!

---

## 👩‍💻 Author

**Rupam Kumari:**

- GitHub: [@techietinker01](https://github.com/techietinker01)
- Project: [ImageInpainting](https://github.com/techietinker01/ImageInpainting)

---

**⭐ If you find this helpful, please star the repo!**

**🚀 Happy Inpainting!**

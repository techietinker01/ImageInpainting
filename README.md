# 🎨 Image Inpainting Web Application

AI-powered web app to remove unwanted objects from photos. Features modern OTP authentication, email integration, and public deployment support.

**Built by Rupam Kumari** | MIT License

[![GitHub](https://img.shields.io/badge/GitHub-ImageInpainting-blue)](https://github.com/techietinker01/ImageInpainting)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://www.tensorflow.org/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Ngrok-brightgreen)](https://grace-uncinate-blythe.ngrok-free.dev)

## 🌐 Live Demo

**Public URL:** <https://grace-uncinate-blythe.ngrok-free.dev>

Try it now! No installation required. ✨

> **Note:** This is a free Ngrok tunnel. URL may change if server restarts. For permanent deployment, see [Cloud Deployment](#%EF%B8%8F-cloud-deployment-render) section below.

---

## ✨ Features

### 🖼️ Core Features

- **AI-Powered Inpainting** - Remove objects from images using deep learning
- **Interactive Canvas** - Draw masks with adjustable brush size
- **Real-time Preview** - See changes instantly
- **Download Results** - Save cleaned images

### 🔐 Authentication & Security

- **OTP-Based Login** - No passwords needed, email-based authentication
- **Remember Me** - Stay logged in for 30 days (optional)
- **Gmail Integration** - Automated OTP delivery via email
- **Secure Sessions** - Flask session management with encryption
- **Environment Variables** - Secure credential storage

### 🌐 Deployment & Access

- **Public Access** - Share with anyone via Ngrok
- **Local Network** - Access from any device on same WiFi
- **Cloud Ready** - Easy deployment to Render, Heroku, etc.
- **No Warning Page** - Ngrok browser warning automatically skipped

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Git
- Gmail account (for OTP emails - optional for dev mode)

### Installation

#### Windows (PowerShell)

```powershell
# Clone repository
git clone https://github.com/techietinker01/ImageInpainting.git
cd ImageInpainting

# Create and activate virtual environment
python -m venv .venv
& .\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

# Configure environment (optional - for email OTP)
notepad .env

# Start the server
python app.py
```

#### Linux/Mac

```bash
# Clone repository
git clone https://github.com/techietinker01/ImageInpainting.git
cd ImageInpainting

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

# Configure environment (optional - for email OTP)
nano .env

# Start the server
python app.py
```

Open <http://localhost:5000> in your browser.

---

## 🔐 Authentication Setup

### Option 1: Dev Mode (No Email Required)

OTP will be printed in the terminal - perfect for testing!

```bash
python app.py
# OTP will appear in terminal output
```

### Option 2: Gmail OTP (Production)

**1. Create Gmail App Password:**

- Go to [Google Account Security](https://myaccount.google.com/security)
- Enable 2-Step Verification
- Go to App Passwords
- Select "Mail" and "Windows" (or your OS)
- Copy the 16-digit password

**2. Configure .env File:**

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-16-digit-app-password
SECRET_KEY=your-random-secret-key
```

**3. Restart Server:**

```bash
python app.py
```

Now OTP emails will be sent automatically! 📧

---

## 🌐 Public Deployment with Ngrok

Share your app with anyone on the internet!

### Setup Ngrok

1. **Sign up** at [ngrok.com](https://ngrok.com/signup) (free)
2. **Download** ngrok for your OS
3. **Get Authtoken** from [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)
4. **Configure** ngrok:

   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

5. **Start Tunnel** (in new terminal):

   ```bash
   ngrok http 5000
   ```

6. **Share the URL:**

   ```text
   https://your-unique-name.ngrok-free.dev
   ```

Anyone can now access your app! 🌍

**Note:** Free tier URL changes on restart. For permanent URL, deploy to Render.

---

## 📖 How to Use

### First Time Login

1. **Enter Email** - Your email address
2. **Receive OTP** - Check your email (or terminal in dev mode)
3. **Verify OTP** - Enter the 6-digit code
4. **Remember Me** - Check to stay logged in for 30 days ✅
5. **Start Inpainting!**

### Image Inpainting

1. **Upload Image** - Click or drag & drop your photo
2. **Draw Mask** - Brush over unwanted objects
3. **Adjust Brush** - Use slider to change brush size
4. **Erase Mistakes** - Switch to eraser tool if needed
5. **Generate** - Click to process with AI
6. **Download** - Save your cleaned image!

### Pro Tips

- 🎨 Use larger brush for big areas
- ✏️ Use smaller brush for details
- 🧹 Eraser tool fixes mask mistakes
- 🔄 Clear button to start over
- 💾 Download button saves result

---

## 🔌 API Endpoints

### Authentication

- `POST /api/send-otp` - Request OTP code
- `POST /api/verify-otp` - Verify OTP and login
- `GET /api/check-auth` - Check if logged in
- `POST /api/logout` - Logout user

### Application

- `GET /` - Login page (redirects to app if logged in)
- `GET /app` - Main inpainting interface
- `POST /upload_mask` - Process image (returns inpainted result)
- `GET /api/status` - Check model status
- `GET /about` - Project information

---

## ☁️ Cloud Deployment (Render)

Permanent URL with free hosting!

1. **Create Account** at [render.com](https://render.com)

2. **New Web Service** → Connect GitHub repo

3. **Build Command:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start Command:**

   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 4
   ```

5. **Environment Variables:**

   ```text
   SMTP_EMAIL=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SECRET_KEY=random-secret-key
   TF_ENABLE_ONEDNN_OPTS=0
   ```

6. **Deploy!** Your app will be at `https://your-app.onrender.com`

**Notes:**

- Free tier sleeps after 15 min inactivity (30-50 sec cold start)
- 512 MB RAM (sufficient for this app)
- CPU-only (no GPU on free tier)
- Perfect for portfolio projects!

---

## 📁 Project Structure

```text
ImageInpainting/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── LICENSE                    # MIT License
├── static/                    # Frontend files
│   ├── index.html            # Login page
│   ├── app.html              # Inpainting interface
│   ├── main.js               # Canvas & drawing logic
│   └── styles.css            # CSS styling
├── saved_model.h5             # Trained model (H5 format)
├── uploads/                   # Uploaded images (gitignored)
├── outputs/                   # Generated outputs (gitignored)
└── image-inpainting.ipynb    # Training notebook
```

---

## 🛠️ Tech Stack

**Frontend:**

- HTML5 Canvas - Interactive mask drawing
- Vanilla JavaScript - No frameworks needed
- Modern CSS - Responsive design

**Backend:**

- Flask 2.x - Web framework
- Python 3.9+ - Programming language
- TensorFlow 2.x - Deep learning
- Keras - Neural network API
- OpenCV - Fallback inpainting
- Pillow - Image processing
- NumPy - Array operations
- python-dotenv - Environment management

**Authentication:**

- Flask Sessions - Session management
- SMTP/Gmail - Email delivery
- OTP System - Passwordless authentication

**Deployment:**

- Waitress - Windows WSGI server
- Gunicorn - Linux WSGI server
- Ngrok - Public tunnel service
- Render - Cloud hosting

---

## 🔒 Security Features

- ✅ **No Password Storage** - OTP-only authentication
- ✅ **Encrypted Sessions** - Flask secret key encryption
- ✅ **Environment Variables** - Sensitive data in .env
- ✅ **Session Expiration** - Auto-logout after 30 days
- ✅ **Rate Limiting** - Max 5 OTP attempts
- ✅ **Secure Headers** - HTTPS recommended
- ✅ **Email Verification** - User owns the email

---

## 🎯 Remember Me Feature

**How It Works:**

- Check "Remember me for 30 days" during OTP verification
- Session stored securely with Flask sessions
- Auto-login on return visits (within 30 days)
- Works across browser restarts
- Different browsers = separate sessions

**Privacy:**

- Sessions stored in browser cookies (HttpOnly)
- Server-side validation
- Clear cookies = logout
- Private browsing = no persistence

---

## 🐛 Troubleshooting

### Common Issues

**Issue: "ERR_NGROK_3200 - endpoint offline":**

Solution: Restart both Flask and ngrok

```bash
python app.py
ngrok http 5000
```

**Issue: OTP not receiving in email:**

- Check spam folder
- Verify Gmail App Password (16 digits, no spaces)
- Ensure 2-Step Verification is enabled
- Check .env file configuration

**Issue: "Module not found" error:**

Solution: Activate virtual environment

```bash
# Windows
.\.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

**Issue: TensorFlow import errors on Python 3.13:**

- Solution: Use Python 3.9-3.11
- App will fallback to OpenCV if TensorFlow unavailable

---

## 📝 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Email Configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-16-digit-app-password

# Flask Configuration
SECRET_KEY=your-random-secret-key-here
PORT=5000

# Model Configuration
MODEL_DIR=saved_models/generator_saved_model

# Directories
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs

# TensorFlow Configuration
TF_ENABLE_ONEDNN_OPTS=0
```

**Generate Secret Key:**

```python
import secrets
print(secrets.token_hex(32))
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Free to use, modify, and distribute!

---

## 👩‍💻 Author

**Rupam Kumari (techietinker01):**

- GitHub: [@techietinker01](https://github.com/techietinker01)
- Project: [ImageInpainting](https://github.com/techietinker01/ImageInpainting)

---

## 🙏 Acknowledgments

- TensorFlow team for the deep learning framework
- Flask team for the web framework
- Ngrok for easy public deployment
- OpenCV for fallback inpainting algorithm

---

## 📊 Project Stats

- **Language:** Python
- **Framework:** Flask
- **AI/ML:** TensorFlow, Keras
- **Frontend:** Vanilla JavaScript
- **Authentication:** OTP-based
- **Deployment:** Render, Ngrok
- **License:** MIT

---

**⭐ If you find this project helpful, please star it on GitHub!**

**🚀 Happy Inpainting!**

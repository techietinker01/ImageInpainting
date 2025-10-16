# Image Inpainting Web Application

Remove unwanted objects from photos by painting a mask. The web UI lets you upload an image, brush over areas to remove, and generate a clean result. Backend uses a TensorFlow/Keras model if available, with an OpenCV fallback.

**Built by Rupam Kumari**  MIT License

## Quick Start

### Windows (PowerShell)

```powershell
git clone https://github.com/techietinker01/ImageInpainting.git
cd ImageInpainting

# Create and activate virtual environment
python -m venv .venv
& .\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

# Start the server (uses waitress on Windows)
.\start_server.ps1
```

### Linux/Mac

```bash
git clone https://github.com/techietinker01/ImageInpainting.git
cd ImageInpainting

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

# Start the Flask development server
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Usage

1. **Upload** - Choose an image file (drag & drop or click to browse)
2. **Paint Mask** - Brush over objects/areas you want to remove
3. **Generate** - Click to process the image with AI inpainting
4. **Download** - Save the cleaned result

### Brush Controls

- Adjustable brush size slider
- Eraser tool to fix mask mistakes
- Clear button to start over

## API Endpoints

- `GET /` - Web interface
- `POST /upload_mask` - Process image and return inpainted result (JSON with base64 images)
- `GET /api/status` - Check if model is loaded
- `GET /about` - Project information

## Deployment

### Render (Free Tier)

This project is configured for easy deployment to Render:

1. **Create Web Service** on Render and connect your GitHub repository (`techietinker01/ImageInpainting`)

2. **Build Command**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Start Command**:

   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 4
   ```

4. **Environment Variables** (optional):
   - `MODEL_DIR` - Path to saved model (default: `saved_models/generator_saved_model`)
   - `UPLOAD_DIR` - Upload directory (default: `uploads`)
   - `OUTPUT_DIR` - Output directory (default: `outputs`)
   - `TF_ENABLE_ONEDNN_OPTS` - Set to `0` to suppress TensorFlow warnings
   - `SECRET_KEY` - Flask secret key for sessions

5. **Deploy** - Render will build and start your application

**Notes:**

- Render automatically sets `$PORT` environment variable
- TensorFlow installation may take 5-10 minutes on free tier
- Model files are large - consider using Git LFS or external storage for production
- Free tier has no GPU support (CPU inference only)
- If model is not available, the app falls back to OpenCV inpainting

## Project Structure

```plaintext
ImageInpainting/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── start_server.ps1      # Windows server startup script
├── static/               # Frontend assets
│   ├── index.html       # Web interface
│   ├── main.js          # Canvas drawing logic
│   └── styles.css       # Styling
├── image-inpainting.ipynb # Training notebook
├── saved_model.h5        # Trained model weights
└── saved_models/         # TensorFlow SavedModel format
    └── generator_saved_model/
```

## Tech Stack

**Frontend:**

- HTML5 Canvas for drawing masks
- Vanilla JavaScript (no frameworks)
- Modern CSS with responsive design

**Backend:**

- Flask - Web framework
- TensorFlow/Keras - Deep learning model
- OpenCV - Fallback inpainting algorithm
- Pillow - Image processing
- NumPy - Array operations
- Gunicorn - Production WSGI server (Linux)
- Waitress - Production server (Windows)

## License

MIT License - see [LICENSE](LICENSE) file

---

**Built by Rupam Kumari:**

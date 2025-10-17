# Model Comparison: app.py vs app2.py

## Overview

This project now supports **two different model formats**:

| Feature | app.py (SavedModel) | app2.py (H5) |
|---------|---------------------|--------------|
| **Model Format** | TensorFlow SavedModel | Keras H5 |
| **Model Path** | `saved_models/generator_saved_model/` | `saved_model.h5` |
| **Model Size** | ~435 MB | ~208 MB (52% smaller!) |
| **Port** | 5000 | 5001 |
| **Startup Script** | `start_server.ps1` | `start_server2.ps1` |
| **Loading Method** | `tf.keras.layers.TFSMLayer` | `keras.models.load_model` |
| **Compatibility** | Keras 3 / TensorFlow 2.x | All Keras versions |

## Quick Start

### Option 1: SavedModel (app.py)
```powershell
# Terminal 1: Start Flask server
.\start_server.ps1

# Terminal 2: Start ngrok
C:\Users\kumar\Downloads\ngrok.exe http 5000
```

### Option 2: H5 Model (app2.py) - **Recommended**
```powershell
# Terminal 1: Start Flask server
.\start_server2.ps1

# Terminal 2: Start ngrok  
C:\Users\kumar\Downloads\ngrok.exe http 5001
```

## Which One to Use?

### Use **app2.py (H5)** if:
- ✅ You want **smaller model size** (208 MB vs 435 MB)
- ✅ You want **faster loading** times
- ✅ You need **better compatibility** across different environments
- ✅ You're deploying to **cloud platforms** with storage limits

### Use **app.py (SavedModel)** if:
- ✅ You need **TensorFlow Serving** compatibility
- ✅ You want to use **TensorFlow.js** for browser deployment
- ✅ You need **production-grade serving** infrastructure

## Recommendation

**For this project, use app2.py (H5 model)** because:
1. Much smaller file size (52% reduction)
2. Faster loading time
3. Simpler deployment
4. Same inference quality

## Environment Variables

Both apps use the same `.env` file with these key differences:

```env
# For app.py (SavedModel)
PORT=5000
MODEL_DIR=saved_models/generator_saved_model

# For app2.py (H5)
PORT=5001
H5_MODEL_PATH=saved_model.h5
```

## Testing Both Versions

You can run both servers simultaneously on different ports:

1. **Terminal 1**: `.\start_server.ps1` → http://localhost:5000
2. **Terminal 2**: `.\start_server2.ps1` → http://localhost:5001
3. Compare performance and results!

## Notes

- Both versions use the **same trained model weights**
- Both support **OTP authentication** and **Remember Me** feature
- Both include **ngrok browser warning skip**
- Both fall back to **OpenCV inpainting** if model loading fails

---

**Built by Rupam Kumari** 🚀

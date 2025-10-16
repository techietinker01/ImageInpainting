from flask import Flask, render_template, request, jsonify, send_file, abort, make_response
import base64
import os
import io
from PIL import Image
import numpy as np
import cv2

# Try to import TensorFlow at module level
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False 
    tf = None

app = Flask(__name__, static_folder='static')
APP_CREDIT = 'Built by Rupam Kumari'

# Paths and config via environment variables (safer for production)
UPLOAD_DIR = os.environ.get('UPLOAD_DIR', 'uploads')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', 'outputs')
SAVED_MODEL_PATH = os.environ.get('MODEL_PATH', 'saved_model.h5')  # H5 file path
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Other configurable values
APP_PORT = int(os.environ.get('PORT', 5000))
APP_SECRET = os.environ.get('SECRET_KEY', None)

# Lazy-loaded model holder
_model = None

def try_load_model():
    global _model
    if _model is not None:
        return True
    if not TF_AVAILABLE:
        print('TensorFlow not available')
        return False
    try:
        if os.path.exists(SAVED_MODEL_PATH):
            # Load Keras H5 model
            _model = tf.keras.models.load_model(SAVED_MODEL_PATH, compile=False)
            print(f'Loaded Keras H5 model from {SAVED_MODEL_PATH}')
            return True
        else:
            print(f'Model file not found at {SAVED_MODEL_PATH}')
            return False
    except Exception as e:
        print(f'Failed to load model: {e}')
        return False


@app.route('/')
def index():
    # Serve the static/index.html directly so we don't need a templates/ folder
    resp = make_response(app.send_static_file('index.html'))
    resp.headers['X-Powered-By'] = APP_CREDIT
    return resp

@app.after_request
def add_powered_by(resp):
    # Add credit header to all responses
    resp.headers.setdefault('X-Powered-By', APP_CREDIT)
    return resp

@app.route('/about')
def about():
    return jsonify({
        'name': 'Image Inpainting',
        'credit': APP_CREDIT,
        'license': 'MIT',
    })


def read_base64_image(data_url):
    # data_url is like 'data:image/png;base64,iVBORw0...'
    header, encoded = data_url.split(',', 1)
    data = base64.b64decode(encoded)
    return Image.open(io.BytesIO(data)).convert('RGB')


@app.route('/upload_mask', methods=['POST'])
def upload_mask():
    data = request.get_json()
    if not data or 'original' not in data or 'mask' not in data:
        return jsonify({'error': 'original and mask required'}), 400

    try:
        orig_img = read_base64_image(data['original'])
        mask_img = read_base64_image(data['mask'])
    except Exception as e:
        return jsonify({'error': f'failed to decode images: {e}'}), 400

    # Save uploads for debugging
    orig_path = os.path.join(UPLOAD_DIR, 'original.png')
    mask_path = os.path.join(UPLOAD_DIR, 'mask.png')
    orig_img.save(orig_path)
    mask_img.save(mask_path)

    # Try to load model if available
    if try_load_model():
        try:
            # Preprocess to numpy array in [0,1]
            inp = np.array(mask_img).astype('float32') / 255.0
            # Ensure shape (1, H, W, C)
            if inp.ndim == 3:
                inp = np.expand_dims(inp, 0)

            # Run model prediction with H5 model
            pred = _model.predict(inp, verbose=0)

            # Convert prediction to image
            out = (np.clip(pred[0], 0, 1) * 255).astype('uint8')
            out_img = Image.fromarray(out)

            out_path = os.path.join(OUTPUT_DIR, 'inpainted.png')
            out_img.save(out_path)

            # Return the image bytes
            buf = io.BytesIO()
            out_img.save(buf, format='PNG')
            buf.seek(0)
            return send_file(buf, mimetype='image/png')
        except Exception as e:
            print('Error during inference:', e)
            # fall through to OpenCV fallback

    # Fallback: use OpenCV inpainting with provided mask
    try:
        # Convert PIL to numpy and ensure correct sizes
        orig_np = np.array(orig_img)
        mask_np = np.array(mask_img)

        # Ensure mask matches original spatial size
        H, W = orig_np.shape[:2]
        if mask_np.shape[:2] != (H, W):
            mask_np = cv2.resize(mask_np, (W, H), interpolation=cv2.INTER_NEAREST)

        # original image to BGR
        orig_bgr = cv2.cvtColor(orig_np, cv2.COLOR_RGB2BGR)

        # mask expected white bg (255) with black strokes (0) → convert to gray
        mask_gray = cv2.cvtColor(mask_np, cv2.COLOR_RGB2GRAY)
        # invert so strokes become white (255), background 0
        inv = 255 - mask_gray
        # binarize to 0/255 uint8
        _, binmask = cv2.threshold(inv, 10, 255, cv2.THRESH_BINARY)
        binmask = binmask.astype(np.uint8)

        # extra safety: ensure types
        if orig_bgr.dtype != np.uint8:
            orig_bgr = orig_bgr.astype(np.uint8)

        # Save debug mask for inspection
        cv2.imwrite(os.path.join(OUTPUT_DIR, 'debug_binmask.png'), binmask)

        # inpaint: all inputs must share same HxW, binmask single channel 8-bit
        inpainted = cv2.inpaint(orig_bgr, binmask, 3, cv2.INPAINT_TELEA)
        out_rgb = cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)
        out_img = Image.fromarray(out_rgb)

        out_path = os.path.join(OUTPUT_DIR, 'inpainted_telea.png')
        out_img.save(out_path)

        buf = io.BytesIO()
        out_img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print('OpenCV inpaint fallback failed:', e)
        return jsonify({'error': f'fallback inpaint failed: {e}'}), 500


@app.route('/api/status')
def status():
    return jsonify({
        'status': 'ok', 
        'model_available': _model is not None,
        'model_path': SAVED_MODEL_PATH,
        'tensorflow_available': TF_AVAILABLE
    })


if __name__ == '__main__':
    # Run on 0.0.0.0 for external access on your network
    print(f"\n=== {APP_CREDIT} ===\n")
    print(f"Looking for model at: {SAVED_MODEL_PATH}")
    print(f"TensorFlow available: {TF_AVAILABLE}")
    # In production, Render (or your host) will set PORT in the environment
    app.run(debug=False, host='0.0.0.0', port=APP_PORT)

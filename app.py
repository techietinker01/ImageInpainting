from flask import Flask, render_template, request, jsonify, send_file, abort, make_response, session
import base64
import os
import io
from PIL import Image
import numpy as np
import cv2
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to import TensorFlow at module level
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False 
    tf = None

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
APP_CREDIT = 'Built by Rupam Kumari'

# Paths and config via environment variables (safer for production)
UPLOAD_DIR = os.environ.get('UPLOAD_DIR', 'uploads')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', 'outputs')
SAVED_MODEL_DIR = os.environ.get('MODEL_DIR', os.path.join('saved_models', 'generator_saved_model'))
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Other configurable values
APP_PORT = int(os.environ.get('PORT', 5000))

# OTP Storage (in production, use Redis or database)
otp_storage = {}  # {email: {'otp': '123456', 'expires': datetime, 'attempts': 0}}

# Email configuration (optional - set environment variables)
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_EMAIL = os.environ.get('SMTP_EMAIL', '')  # Your email
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')  # Your app password

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
        if os.path.exists(SAVED_MODEL_DIR):
            # Keras 3 requires TFSMLayer for SavedModel format
            _model = tf.keras.layers.TFSMLayer(SAVED_MODEL_DIR, call_endpoint='serving_default')
            print('Loaded SavedModel from', SAVED_MODEL_DIR)
            return True
    except Exception as e:
        print('Failed to load model:', e)
        try:
            # Fallback: try loading as regular SavedModel
            _model = tf.saved_model.load(SAVED_MODEL_DIR)
            print('Loaded SavedModel using tf.saved_model.load from', SAVED_MODEL_DIR)
            return True
        except Exception as e2:
            print('Fallback loading also failed:', e2)
    return False


@app.route('/')
def index():
    # If user is already logged in, redirect to app
    if session.get('logged_in'):
        return main_app()
    # Serve the login page first (index.html with OTP)
    resp = make_response(app.send_static_file('index.html'))
    resp.headers['X-Powered-By'] = APP_CREDIT
    return resp

@app.route('/app')
def main_app():
    # Serve the main inpainting app (app.html)
    resp = make_response(app.send_static_file('app.html'))
    resp.headers['X-Powered-By'] = APP_CREDIT
    return resp

@app.route('/login')
def login():
    # Alternative route for login page
    resp = make_response(app.send_static_file('index.html'))
    resp.headers['X-Powered-By'] = APP_CREDIT
    return resp

@app.after_request
def add_powered_by(resp):
    # Add credit header to all responses
    resp.headers.setdefault('X-Powered-By', APP_CREDIT)
    # Add header to skip ngrok browser warning
    resp.headers['ngrok-skip-browser-warning'] = 'true'
    return resp

@app.route('/about')
def about():
    return jsonify({
        'name': 'Image Inpainting',
        'credit': APP_CREDIT,
        'license': 'MIT',
    })


# OTP Helper Functions
def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    """Send OTP via email (optional - requires SMTP configuration)"""
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        print(f'[DEV MODE] OTP for {email}: {otp}')
        return True
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = email
        msg['Subject'] = 'Your Image Inpainting OTP'
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #667eea;">Image Inpainting - Verification Code</h2>
            <p>Your One-Time Password (OTP) is:</p>
            <h1 style="color: #764ba2; font-size: 36px; letter-spacing: 5px;">{otp}</h1>
            <p>This code will expire in 10 minutes.</p>
            <p>If you didn't request this code, please ignore this email.</p>
            <hr style="margin-top: 30px;">
            <p style="color: #7f8c8d; font-size: 12px;">Built by Rupam Kumari</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f'OTP sent to {email}')
        return True
    except Exception as e:
        print(f'Failed to send email: {e}')
        print(f'[DEV MODE] OTP for {email}: {otp}')
        return True  # Return True anyway for dev mode


@app.route('/api/send-otp', methods=['POST'])
def api_send_otp():
    """Send OTP to user's email"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    
    # Generate OTP
    otp = generate_otp()
    expires = datetime.now() + timedelta(minutes=10)
    
    # Store OTP
    otp_storage[email] = {
        'otp': otp,
        'expires': expires,
        'attempts': 0
    }
    
    # Send email
    if send_otp_email(email, otp):
        return jsonify({
            'success': True,
            'message': 'OTP sent successfully',
            'dev_otp': otp if not SMTP_EMAIL else None  # Show OTP in dev mode only
        })
    else:
        return jsonify({'success': False, 'message': 'Failed to send OTP'}), 500


@app.route('/api/check-auth', methods=['GET'])
def api_check_auth():
    """Check if user is logged in"""
    if session.get('logged_in'):
        return jsonify({
            'success': True,
            'logged_in': True,
            'email': session.get('user_email')
        })
    else:
        return jsonify({
            'success': True,
            'logged_in': False
        })


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Log out user"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })


@app.route('/api/verify-otp', methods=['POST'])
def api_verify_otp():
    """Verify OTP and log in user"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    otp = data.get('otp', '').strip()
    remember_me = data.get('remember_me', False)
    
    if not email or not otp:
        return jsonify({'success': False, 'message': 'Email and OTP are required'}), 400
    
    # Check if OTP exists
    if email not in otp_storage:
        return jsonify({'success': False, 'message': 'No OTP found for this email'}), 400
    
    stored_data = otp_storage[email]
    
    # Check if OTP expired
    if datetime.now() > stored_data['expires']:
        del otp_storage[email]
        return jsonify({'success': False, 'message': 'OTP expired. Please request a new one.'}), 400
    
    # Check attempts
    if stored_data['attempts'] >= 5:
        del otp_storage[email]
        return jsonify({'success': False, 'message': 'Too many failed attempts. Please request a new OTP.'}), 400
    
    # Verify OTP
    if otp == stored_data['otp']:
        # OTP is correct - log in user
        session['user_email'] = email
        session['logged_in'] = True
        
        # Set session permanence based on remember_me
        if remember_me:
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=30)  # Remember for 30 days
        else:
            session.permanent = False  # Expires when browser closes
        
        del otp_storage[email]  # Clear OTP after successful verification
        
        return jsonify({
            'success': True,
            'message': 'Verification successful'
        })
    else:
        # Incorrect OTP
        stored_data['attempts'] += 1
        remaining = 5 - stored_data['attempts']
        return jsonify({
            'success': False,
            'message': f'Invalid OTP. {remaining} attempts remaining.'
        }), 400


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

            # Run model prediction
            if hasattr(_model, 'predict'):
                # Keras model
                pred = _model.predict(inp)
            elif hasattr(_model, '__call__'):
                # TFSMLayer or tf.saved_model
                pred = _model(inp)
                if isinstance(pred, dict):
                    # TFSMLayer returns dict, get the output
                    pred = list(pred.values())[0]
            else:
                # tf.saved_model.load result
                pred = _model.signatures['serving_default'](tf.constant(inp))
                pred = list(pred.values())[0]

            # Convert to numpy if tensor
            if hasattr(pred, 'numpy'):
                pred = pred.numpy()
            
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
    return jsonify({'status': 'ok', 'model_available': _model is not None})


if __name__ == '__main__':
    # Run on 0.0.0.0 for external access on your network
    print(f"\n=== {APP_CREDIT} ===\n")
    # In production, Render (or your host) will set PORT in the environment
    app.run(debug=False, host='0.0.0.0', port=APP_PORT)

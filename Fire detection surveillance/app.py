import os
import cv2
import time
import threading
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from flask import Flask, render_template, Response, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ultralytics import YOLO
from twilio.rest import Client

# ================= CONFIGURATION =================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# --- EMAIL CONFIG (GMAIL EXAMPLE) ---
EMAIL_ADDRESS = "kambleajinkya490@gmail.com"
EMAIL_PASSWORD = "mzyq azrl vtaa yzxs"
 # Use App Password, not login password

# --- TWILIO SMS CONFIG ---
TWILIO_SID = "AC5d02c38c87cbcec691a42f12d9bc4f6f"
TWILIO_AUTH_TOKEN = "d979dbfdd9dfdde1f1cfc2b825ac3c50"
TWILIO_PHONE = "+17085787339"

# --- FIRE DETECTION CONFIG ---
# Load YOLO model (Ensure 'yolov8n.pt' or your custom 'fire.pt' is in the folder)
model = YOLO('best.pt') 
target_class_id = 0  # 0 is 'person' in standard YOLO. CHANGE TO FIRE CLASS ID IF USING CUSTOM MODEL.
CONFIDENCE_THRESHOLD = 0.5

# Setup Upload Folder
CAPTURE_FOLDER = os.path.join('static', 'captures')
os.makedirs(CAPTURE_FOLDER, exist_ok=True)

# ================= DATABASE SETUP =================
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create DB
with app.app_context():
    db.create_all()

# ================= GLOBAL VARIABLES =================
camera = cv2.VideoCapture(0)  # Use 0 for webcam
alert_cooldown = False  # To prevent spamming
cooldown_time = 30 # Seconds between alerts

# ================= NOTIFICATION LOGIC =================

def send_sms(to_number, message_body):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE,
            to=to_number
        )
        print(f"SMS Sent to {to_number}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def send_email(to_email, subject, body, image_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach Image
        with open(image_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(image_path)}")
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email Sent to {to_email}")
    except Exception as e:
        print(f"Failed to send Email: {e}")

def trigger_alerts(user_email, user_phone, image_path):
    global alert_cooldown
    
    # Send SMS (Threaded to not block video)
    sms_thread = threading.Thread(target=send_sms, args=(user_phone, "WARNING: FIRE DETECTED! Check your dashboard."))
    sms_thread.start()

    # Send Email (Threaded)
    email_thread = threading.Thread(target=send_email, args=(user_email, "FIRE ALERT", "Fire detected by system.", image_path))
    email_thread.start()

    # Reset cooldown after X seconds
    def reset_cooldown():
        global alert_cooldown
        time.sleep(cooldown_time)
        alert_cooldown = False
        print("System Ready for new alerts.")

    threading.Thread(target=reset_cooldown).start()

# ================= VIDEO STREAM LOGIC =================

def generate_frames(user_email, user_phone):
    global alert_cooldown
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # 1. Run YOLO Detection
        results = model(frame, stream=True, verbose=False)
        fire_detected = False

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                # Check if detected object is Fire (or Person for testing)
                if cls == target_class_id and conf > CONFIDENCE_THRESHOLD:
                    fire_detected = True
                    
                    # Draw Bounding Box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, "FIRE DETECTED", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 2. Logic: If Fire Detected + No Cooldown -> Save & Alert
        if fire_detected and not alert_cooldown:
            alert_cooldown = True
            
            # Save Image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fire_{timestamp}.jpg"
            filepath = os.path.join(CAPTURE_FOLDER, filename)
            cv2.imwrite(filepath, frame)
            print(f"Fire Detected! Image Saved: {filepath}")

            # Trigger Alerts to the SPECIFIC USER passed in args
            trigger_alerts(user_email, user_phone, filepath)

        # 3. Encode for Web Stream
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# ================= ROUTES =================

@app.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.username)

@app.route('/video_feed')
@login_required
def video_feed():
    # We pass the CURRENT logged-in user's details to the generator
    return Response(generate_frames(current_user.email, current_user.phone), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check details.')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        # Check if exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.')
            return redirect(url_for('register'))
            
        new_user = User(
            email=email, 
            username=username, 
            phone=phone,
            password=generate_password_hash(password, method='scrypt')
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Threaded=True is important for streaming to not block the server
    app.run(debug=True, threaded=True, port=5001)
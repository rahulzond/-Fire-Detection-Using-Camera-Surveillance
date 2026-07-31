# 🔥 Fire Detection Using Camera Surveillance

A real-time fire detection system that monitors a live camera feed using a custom-trained **YOLOv8** model, streams the annotated video through a **Flask** web application, and automatically sends **Email and SMS alerts** the moment fire is detected.

---

## 📌 Overview

Conventional smoke/heat sensors only react once a fire has already spread. This project instead applies computer vision directly to camera footage, allowing fire to be recognized visually — often earlier — and paired with an automated notification pipeline so the right people are alerted immediately, with photographic evidence attached.

The system is built as a self-contained Flask web app: users register/log in, view a live annotated video stream, and receive Email + SMS alerts tied to their own account whenever fire is detected.

---

## ✨ Key Features

- **Real-time detection** — Custom-trained YOLOv8 model (`best.pt`) analyzes each frame of the live camera feed.
- **Live web dashboard** — Video stream with bounding-box overlays served directly in the browser via Flask.
- **User authentication** — Registration and login (Flask-Login + SQLAlchemy/SQLite), so alerts are routed to the correct user's email/phone.
- **Automated Email alerts** — Sends a notification with the captured fire frame attached via SMTP (Gmail).
- **Automated SMS alerts** — Sends an instant text warning via the Twilio API.
- **Automatic image capture** — Saves a timestamped snapshot of each detection event to `static/captures/`.
- **Alert cooldown** — A configurable cooldown window (default 30s) prevents alert spam from continuous detections.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Web Framework | Flask |
| Object Detection | YOLOv8 (Ultralytics) |
| Computer Vision | OpenCV |
| Authentication | Flask-Login, Werkzeug (password hashing) |
| Database | SQLite via Flask-SQLAlchemy |
| Email Alerts | SMTP (Gmail) |
| SMS Alerts | Twilio API |
| Config | python-dotenv |

---

## 🏗️ System Architecture

1. **Video Capture** — OpenCV reads frames from the connected camera (webcam or IP camera).
2. **Inference** — Each frame is passed through the YOLOv8 model (`best.pt`) to detect fire above a confidence threshold.
3. **Annotation & Streaming** — Detected regions are boxed and labeled, then streamed to the browser as an MJPEG feed via Flask's `/video_feed` route.
4. **Event Handling** — On a fire detection (and if not in cooldown), the frame is saved and an alert cycle is triggered.
5. **Notification** — Email (with image attachment) and SMS alerts are dispatched in parallel threads to the logged-in user's registered contact details.
6. **Cooldown Reset** — A timer prevents repeated alerts for the same ongoing event.

---

## 📂 Project Structure

```
Fire-Detection-Using-Camera-Surveillance/
└── Fire detection surveillance/
    ├── app.py                # Main Flask app: auth, video stream, detection, alerts
    ├── best.pt                # Custom-trained YOLOv8 fire-detection weights
    ├── mail_test.py           # Standalone script to test email alert delivery
    ├── requirements.txt
    ├── templates/
    │   ├── index.html         # Live video dashboard
    │   ├── login.html
    │   └── register.html
    └── instance/               # SQLite database (auto-generated)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- A webcam or accessible camera feed
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) (not your regular password)
- A [Twilio](https://www.twilio.com/) account, phone number, SID, and auth token

### Installation

```bash
git clone https://github.com/rahulzond/-Fire-Detection-Using-Camera-Surveillance.git
cd "Fire-Detection-Using-Camera-Surveillance/Fire detection surveillance"
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project directory (do **not** commit this file):

```env
SECRET_KEY=your-secret-key
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
TWILIO_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE=+1XXXXXXXXXX
```

> ⚠️ Update `app.py` to load these values with `python-dotenv` (`os.getenv(...)`) instead of hardcoding credentials, and set the correct fire class ID from your trained model in place of the placeholder `target_class_id`.

### Running the App

```bash
python app.py
```

Then open `http://localhost:5001` in your browser, register an account, and log in to view the live detection dashboard.

---

## 🔔 Alert Workflow

When fire is detected above the confidence threshold and the system isn't in cooldown:
1. A snapshot is saved to `static/captures/`.
2. An SMS alert is sent to the logged-in user's phone via Twilio.
3. An email with the snapshot attached is sent to the user's registered email address.
4. A 30-second cooldown prevents duplicate alerts before resetting automatically.

---

## 🔮 Future Enhancements

- Support for multiple simultaneous camera feeds
- Admin dashboard with detection history and analytics
- Deployment on edge devices (Jetson Nano / Raspberry Pi) for on-site inference
- Configurable alert thresholds and cooldown per user
- Push notifications via a companion mobile app

---

## 🤝 Contributing

Contributions are welcome — feel free to open an issue or submit a pull request.

---

## 👤 Author

**Rahul Zond**
[GitHub](https://github.com/rahulzond)

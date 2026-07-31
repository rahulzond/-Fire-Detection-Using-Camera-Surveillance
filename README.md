# 🔥 Fire Detection Using Camera Surveillance

An AI-powered fire detection system that leverages real-time camera surveillance and YOLO (You Only Look Once) deep learning to identify fire and smoke instances, triggering automated alerts to enable rapid response and minimize damage.

---

## 📌 Overview

Traditional fire alarm systems rely on heat or smoke sensors, which often detect fires only after they have spread significantly. This project addresses that limitation by using computer vision to detect visual indicators of fire directly from live camera feeds — enabling **earlier detection**, **wider area coverage**, and **automated notification** of relevant stakeholders.

The system is built around a YOLO-based object detection model trained to recognize fire and smoke patterns in real time, making it suitable for deployment in surveillance setups across homes, offices, warehouses, and industrial sites.

---

## ✨ Key Features

- **Real-Time Detection** — Processes live video streams to identify fire/smoke instances with minimal latency.
- **YOLO-Based Deep Learning Model** — Uses a YOLO object detection architecture for high-speed, high-accuracy inference.
- **Automated Alerts** — Triggers notifications (e.g., email/SMS/on-screen alerts) immediately upon fire detection.
- **Camera Surveillance Integration** — Compatible with standard IP/CCTV camera feeds.
- **Scalable Deployment** — Designed to run on single or multi-camera setups.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Deep Learning Framework | PyTorch / TensorFlow *(update based on your implementation)* |
| Object Detection Model | YOLO (v5/v8) |
| Computer Vision | OpenCV |
| Alerting | SMTP / Twilio API *(update as applicable)* |

---

## 🏗️ System Architecture

1. **Video Input** — Live feed captured from surveillance camera(s).
2. **Preprocessing** — Frames extracted and resized for model input.
3. **Fire Detection (YOLO Model)** — Each frame is passed through the trained YOLO model to detect fire/smoke with bounding boxes and confidence scores.
4. **Alert Trigger** — On detection above a confidence threshold, an automated alert is dispatched.
5. **Logging** — Detection events and frames are logged for review and auditing.

---

## 📂 Project Structure

```
Fire-Detection-Using-Camera-Surveillance/
├── data/                  # Training/validation datasets
├── models/                # Trained YOLO weights
├── src/
│   ├── detect.py          # Real-time detection script
│   ├── train.py           # Model training script
│   └── alert.py           # Alert notification module
├── results/               # Sample detection outputs
├── requirements.txt
└── README.md
```



---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/<your-username>/Fire-Detection-Using-Camera-Surveillance.git
cd Fire-Detection-Using-Camera-Surveillance
pip install -r requirements.txt
```

### Usage

Run real-time detection using a webcam or connected camera feed:

```bash
python src/detect.py --source 0
```

Run detection on a video file:

```bash
python src/detect.py --source path/to/video.mp4
```

---

## 📊 Results

- Model achieves **[X]% mAP** on the validation dataset.
- Average inference speed: **[X] FPS** on [hardware used, e.g., NVIDIA GTX 1660].
- Sample detection outputs are available in the `results/` folder.



---

## 🔔 Alert System

Upon detecting fire with a confidence score above the configured threshold, the system automatically:
- Sends an alert notification (email/SMS) to designated recipients
- Logs the event with a timestamped snapshot for reference

---

## 🔮 Future Enhancements

- Multi-camera simultaneous monitoring dashboard
- Mobile app integration for push notifications
- Edge deployment (Jetson Nano / Raspberry Pi) for on-site processing
- Smoke-only detection sensitivity tuning to reduce false positives

---

## 🤝 Contributing

Contributions are welcome. Please open an issue to discuss proposed changes or submit a pull request.

---

## 👤 Author

**[Rahul Zond]**
[LinkedIn](#) · [GitHub](#) · [Email](#)

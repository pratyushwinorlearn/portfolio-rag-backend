# 🧭 BlindNav (WalkAble)

An AI-powered indoor navigation system developed for Hackaccino 2026 to assist visually impaired individuals with safe, independent spatial mobility.

## 🏗️ Technical Architecture Overview
BlindNav operates without relying on GPS, which frequently fails indoors. Instead, the system uses a dual-layered approach:
* **Indoor Positioning:** Utilizes WiFi RSSI (Received Signal Strength Indicator) fingerprinting to continuously map and track the user's location.
* **On-Device Obstacle Detection:** A custom TensorFlow Lite (TFLite) model processes visual data locally to identify physical hazards in real time with minimal latency.
* **Audio Routing:** The TypeScript core processes the position and obstacle data to deliver intuitive, turn-by-turn voice guidance.
* **Accessibility Services:** The application is deeply integrated with custom native Android accessibility services, ensuring the interface is fully operable by visually impaired users out of the box.

## 🚀 Installation & Compilation
*(Note: Because this project relies on custom native Android services for full accessibility support, it must be compiled natively.)*

### Prerequisites
* Android Studio (latest stable version)
* Node.js & npm (for the TypeScript environment)
* TensorFlow Lite Support Library

### Steps
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/blindnav.git](https://github.com/pratyushwinorlearn/BlindNav.git)

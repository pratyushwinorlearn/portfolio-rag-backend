# persona-ai

# Persona.ai 🎙️✨
**Real-Time 3D AI Interview Simulator**

Persona.ai is a full-stack, real-time 3D interview simulation platform designed to replicate the pressure and dynamic conversation of a real human interview. Meet **Payton**, our photorealistic MetaHuman hiring manager, who analyzes your speech, evaluates your technical accuracy, and reacts to your performance in real-time.

---

## 🚀 Key Features

* **Photorealistic 3D Avatar:** Powered by Unreal Engine 5 Pixel Streaming, Payton is rendered with high-fidelity graphics directly in the browser with sub-second latency.
* **Expressive Body Language & Lip-Sync:** Custom architecture converts AI-generated audio into real-time mouth movements (*visemes*). Payton dynamically triggers non-verbal cues—nodding, smiling at strong answers, and showing concern during struggles.
* **Lightning-Fast AI Brain:** Integrated with **Groq AI** to dynamically generate context-aware questions and evaluate candidate answers instantly, eliminating awkward conversational delays.
* **Advanced WebRTC Networking:** Engineered with custom **Metered TURN servers** to bypass strict NATs and firewalls (e.g., corporate/university networks), ensuring global accessibility and seamless video streaming.
* **Secure User Onboarding:** Utilizes the **Resend API** for a reliable, automated email delivery system, handling seamless account registration and secure OTP verification.
* **Immersive UI/UX:** A highly optimized React frontend featuring custom GSAP canvas image sequence animations for a buttery-smooth landing page experience.
* **Comprehensive Debriefs:** Generates a detailed performance report post-interview, breaking down technical depth, communication skills, confidence, and structure.

---

## 🛠️ Tech Stack

**Frontend:**
* React.js
* GSAP (ScrollTrigger & Custom Canvas Animations)
* WebRTC (DataChannels for Viseme transmission)

**Backend:**
* Node.js & Express.js
* WebSockets (Signaling Server)
* Groq AI (Ultra-low latency LLM for question generation & evaluation)
* Resend API (OTP & Email Delivery)

**Rendering & Infrastructure:**
* Unreal Engine 5 (MetaHuman, Pixel Streaming Plugin)
* Metered TURN/STUN Servers (NAT Traversal)
* Railway (Backend Deployment) / Vercel (Frontend Deployment)

---

## 📐 System Architecture

1. **Client -> Backend:** The user initiates an interview in the React frontend. The Node.js backend contacts Groq AI to set the context (Job Role, Experience Level) and fetch the first question.
2. **WebRTC Handshake:** The frontend establishes a WebSocket connection to the signaling server, exchanging SDP and ICE candidates (via Metered TURN) with the local/cloud UE5 instance.
3. **Audio/Video Stream:** A P2P WebRTC stream is established. The user sees Payton rendering in real-time.
4. **Live Interaction Loop:**
   * User speaks -> Transcribed to text -> Sent to Backend.
   * Groq AI evaluates the answer -> Generates feedback, next question, and emotion tags.
   * Text-to-Speech generates audio -> Audio to Viseme processor creates lip-sync data.
   * Audio plays on the client -> Visemes and emotion triggers (smile, nod, concern) are sent via WebRTC DataChannel to UE5 to drive Payton's facial rig.

---

## ⚙️ Local Development Setup

### Prerequisites
* Node.js (v18+)
* Unreal Engine 5.x (with Pixel Streaming Plugin enabled)
* API Keys: Groq AI, Resend API, Metered (TURN server credentials)

### 1. Backend Setup
\`\`\`bash
cd backend
npm install
\`\`\`
Create a \`.env\` file and add your credentials:
\`\`\`env
PORT=8000
GROQ_API_KEY=your_groq_key
RESEND_API_KEY=your_resend_key
JWT_SECRET=your_jwt_secret
\`\`\`
Start the backend server:
\`\`\`bash
npm start
\`\`\`

### 2. Frontend Setup
\`\`\`bash
cd frontend
npm install
\`\`\`
Start the React development server:
\`\`\`bash
npm run dev
\`\`\`

### 3. Unreal Engine 5 Pixel Streaming
1. Open your UE5 project and ensure the **Pixel Streaming** plugin is active.
2. Package the project or run it as a Standalone Game with the following launch arguments:
   \`-AudioMixer -PixelStreamingIP=localhost -PixelStreamingPort=8888\`
3. Start the Signaling Web Server (provided by Epic Games or your custom implementation) and configure the `config.json` with your Metered TURN credentials to allow external WebRTC connections.

---




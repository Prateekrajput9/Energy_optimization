working Prototype:
https://sih25105.vercel.app/
<DashBoard>
<img width="1912" height="906" alt="image" src="https://github.com/user-attachments/assets/916eb727-0402-464e-b3b2-d49e19480f36" />


<img width="1893" height="882" alt="image" src="https://github.com/user-attachments/assets/0a1f39d0-0b05-4942-80b9-a33d4ab5e403" />
<img width="1887" height="888" alt="image" src="https://github.com/user-attachments/assets/88639516-b2e5-4fa7-8022-67e9f3213326" />




# ⚡ Smart Energy Orchestration System

A data-driven, software-centric solution for optimizing renewable energy utilization across public-sector campuses — integrating **solar**, **wind**, **battery**, and **grid** resources into a unified intelligent dashboard.

---

## 🌍 Problem Statement

Many institutes have installed solar panels and wind turbines but still depend heavily on grid power due to poor coordination between these sources.
Existing systems work in isolation, lack predictive insights, and require manual monitoring — leading to inefficiency and higher costs.

---

## 💡 Proposed Solution

We developed a **Smart Energy Orchestration Platform** that acts as a **virtual power plant (VPP)** — integrating all energy resources via software intelligence.
It uses **machine learning** to forecast demand and renewable generation, and **reinforcement learning** to optimize battery charging/discharging and load scheduling in real time.

### 🧠 Key Features

* Real-time monitoring of solar, wind, battery, and grid power
* Predictive analytics for next-hour/day energy demand and production
* RL-based decision engine for cost/emission optimization
* Interactive React dashboard with live visualization
* Vendor-neutral data layer using REST APIs / MQTT for sensor integration
* Carbon footprint and savings report generation

---

## 🏗️ System Architecture

```
          ┌────────────────────────┐
          │ Sensors (Solar/Wind/Grid) │
          └──────────┬──────────────┘
                     │
             Data Stream (API/MQTT)
                     │
          ┌────────────────────────┐
          │ Backend (Flask/FastAPI)│
          │ - Data Ingestion        │
          │ - Preprocessing         │
          │ - ML & RL Models        │
          └──────────┬──────────────┘
                     │
          ┌────────────────────────┐
          │ React Dashboard (UI)   │
          │ - Real-time Charts     │
          │ - Insights & Controls  │
          └────────────────────────┘
```

---

## 🧩 Components

### 1. React Dashboard (`/frontend`)

* Displays live energy generation and usage
* Graphs for solar, wind, battery, and grid metrics
* Insights section for predictions and optimization advice

### 2. ML Model (`/models/ml_model.py`)

* Uses regression to forecast next-hour energy generation and demand
* Trained on simulated or historical time-series data

### 3. RL Model (`/models/rl_agent.py`)

* Reinforcement learning agent (e.g., DQN) to schedule battery charging/discharging
* Objective: minimize grid dependence and maximize renewable self-consumption

### 4. Backend API (`/backend/app.py`)

* Serves predictions to the dashboard
* Connects to sensors / simulated data sources
* Stores historical data for analytics

---

## ⚙️ Installation and Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/smart-energy-orchestration.git
cd smart-energy-orchestration
```

### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

### 4️⃣ View Dashboard

Open your browser → [http://localhost:3000](http://localhost:3000)

---

## 🧪 Data and Model Training

* Sample CSV data for energy generation and demand available in `/data/`
* Train ML model:

```bash
python models/ml_model.py
```

* Train RL model:

```bash
python models/rl_agent.py
```

---

## 🧠 Future Enhancements

* Integrate weather APIs for live forecast-driven optimization
* Deploy on cloud (AWS/GCP) for multiple campuses
* Add anomaly detection for equipment faults
* Build mobile-friendly dashboard

---

## 🏆 Innovation Highlights

* **Software-first approach**: No need for new hardware
* **AI-driven control**: Predicts, learns, and adapts in real-time
* **Scalable architecture**: Works with any renewable setup
* **Human-friendly interface**: Designed for non-technical staff

---

## 👥 Team

**Project by:**
Team ⚙️ Datatide — IIT Indore
Members: 

---

Would you like me to make this README **more visually rich** (with badges, emojis, and better formatting for GitHub presentation)? It’ll look stunning for submission.

<img width="1536" height="1024" alt="ChatGPT Image Oct 7, 2025, 02_04_51 PM" src="https://github.com/user-attachments/assets/1d5d4935-e3a4-45d8-bd81-5e5b76b43f3e" />

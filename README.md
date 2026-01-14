# 🏡 NestIQ - Intelligent Real Estate Forecasting

**NestIQ** is a next-generation property valuation engine that combines machine learning, geospatial analysis, and deep economic heuristics to provide accurate, future-proof real estate predictions. unlike traditional valuation tools that rely solely on historical transaction data, NestIQ analyzes the *livability* of a location—crime rates, accessibility, traffic, and amenities—to forecast property value growth over the next 5 years.

![NestIQ Banner](https://via.placeholder.com/1200x500.png?text=NestIQ+Intelligent+Forecasting)

## 🚀 Key Features

*   **Global Prediction Engine**: Supports property valuation across 7 major regions with calibrated economic models:
    *   🇮🇳 **India** (Detailed support for Mumbai, Bangalore, Hyderabad)
    *   🇬🇧 **United Kingdom**
    *   🇺🇸 **USA**
    *   🇨🇦 **Canada**
    *   🇦🇺 **Australia**
    *   🇳🇿 **New Zealand**
    *   🇪🇺 **Europe**
*   **Hyper-Local Insights**:
    *   **Crime Index**: Real-time safety analysis using geospatial data.
    *   **Accessibility Score**: Proximity to public transport, highways, and hubs.
    *   **Traffic Analysis**: Congestion modeling for accurate commute estimates.
    *   **Amenity Density**: automated scoring of schools, hospitals, and parks within 1.5km.
*   **Advanced ML & Heuristics**:
    *   Hybrid model combining Random Forest regression with rule-based economic multipliers.
    *   "Location Sensitivity Layer": Forces price differentiation based on livability metrics even for identical building specs.
    *   Exchange Rate Normalization: Automatically adjusts valuation baselines for local currencies (₹, £, $, C$, A$, €).
*   **Comparison Engine**: Side-by-side investment analysis of two different properties/locations (e.g., *Bandra, Mumbai* vs. *London, UK*).
*   **Interactive Design**:
    *   "Cinematic" Prediction Wizard with video transitions.
    *   Dynamic background data fetching (Cache Warming) during user interaction.
    *   Responsive, Dark-Mode first UI.

## 🛠️ Technology Stack

### **Frontend (Client)**
*   **Framework**: React 18 (TypeScript)
*   **Build Tool**: Vite
*   **Styling**: Custom CSS (Glassmorphism, Dark UI), Lucide React (Icons)
*   **Routing**: React Router DOM
*   **State**: React Hooks (Custom wizards)

### **Backend (Server)**
*   **Framework**: Django Rest Framework (Python 3.10+)
*   **Database**: SQLite (Dev) / PostgreSQL (Prod ready)
*   **Geospatial**: `OSMnx` (OpenStreetMap NetworkX), `Shapely`, `Geopy`
*   **ML Libraries**: `Scikit-Learn`, `Pandas`, `NumPy`
*   **Server**: Gunicorn (WSGI)
*   **Cache**: Custom File-based Caching / DB Caching for API calls.

### **Infrastructure**
*   **Cloud**: AWS EC2 (Ubuntu 24.04 LTS)
*   **Web Server**: Nginx (Reverse Proxy, SSL termination)
*   **Security**: SSL via Let's Encrypt (`nip.io`), UFW Firewall
*   **Optimization**: Swap Space Configured, Gunicorn Socket activation.

---

## ⚡ Installation & Local Setup

### Prerequisites
*   Node.js (v18+)
*   Python (v3.10+)
*   Git

### 1. Clone the Repository
```bash
git clone https://github.com/suchithsaraaaa/integrated_predictor.git
cd integrated_predictor
```

### 2. Backend Setup
```bash
cd house_price_prediction
python -m venv venv
# Activate Venv (Windows: venv\Scripts\activate, Mac/Linux: source venv/bin/activate)

pip install -r requirements.txt
cd core
python manage.py migrate
python manage.py runserver
```
The API will be available at `http://localhost:8000`.

### 3. Frontend Setup
 Open a new terminal:
```bash
cd nestiq-predict-main
npm install
npm run dev
```
The app will be available at `http://localhost:5173`.

---

## 🌐 API Overview

### `POST /api/warmup/`
Triggers background data fetching for a location while the user is typing/rendering the UI.
*   **Body**: `{"latitude": 51.5, "longitude": -0.1}`
*   **Effect**: Pre-computes/Caches OSM data.

### `POST /api/predict/`
Generates the final property valuation and insights.
*   **Body**:
    ```json
    {
      "latitude": 19.076,
      "longitude": 72.877,
      "area_sqft": 1200,
      "bedrooms": 2,
      "bathrooms": 2,
      "year": 2026
    }
    ```
*   **Response**:
    ```json
    {
      "predicted_price": 25000000.00,
      "currency": {"symbol": "₹", "code": "INR"},
      "price_trend": [...],
      "area_insights": { "crime_index": 0.12, "accessibility_score": 0.85 ... }
    }
    ```

---

## ☁️ Deployment (AWS EC2)

This project includes fully automated deployment scripts located in the `deploy/` directory.

### Quick Deploy (Ubuntu)
```bash
# 1. SSH into EC2
ssh -i key.pem ubuntu@<ip>

# 2. Clone & Run Setup
git clone https://github.com/suchithsaraaaa/integrated_predictor.git
cd integrated_predictor
sudo bash deploy/complete_setup.sh
```

### Key Scripts
*   `deploy/setup_ec2.sh`: Installs dependencies, Nginx, Gunicorn.
*   `deploy/rebuild_frontend.sh`: Builds React app and moves to `/var/www/nestiq`.
*   `deploy/fix_economics.sh`: Applies latest pricing models.
*   `deploy/enable_ssl.sh`: Auto-configures HTTPS using `nip.io`.

---

## 🏗️ Project Structure

```
integrated_predictor/
├── house_price_prediction/       # Backend (Django)
│   ├── core/
│   │   ├── ml/                   # ML Models & Logic
│   │   ├── properties/           # API Views & Services
│   │   │   ├── services/         # Crime, Traffic, OSM Logic
│   │   │   └── api/              # DRF Views
│   │   └── ...
│   └── ...
├── nestiq-predict-main/          # Frontend (React)
│   ├── src/
│   │   ├── components/           # UI Components (Wizard, Cards)
│   │   ├── pages/                # Predict, Compare, About
│   │   └── ...
│   └── ...
├── deploy/                       # Automation Scripts (Bash)
└── ...
```

## 📬 Contact / Contribution

*   **Author**: Suchith
*   **License**: MIT
*   **Status**: Active Development 🚧

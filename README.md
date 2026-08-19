# Full-Stack Editorial Portfolio

This project transforms a static HTML/CSS/JS editorial portfolio into a dynamic full-stack web application using a Python Flask REST API and a MySQL database.

## Architecture

- **Frontend**: Vanilla HTML/CSS/JS (GSAP for animations). Connects to the backend via `fetch()`.
- **Backend**: Python 3, Flask, PyMySQL.
- **Database**: MySQL.

---

## Local Setup Instructions

### 1. Database Setup (MySQL)
Ensure you have MySQL running locally.
1. Create a database: `CREATE DATABASE portfolio_db;`
2. Run the schema and seed scripts to create the tables and insert initial data:
   ```bash
   mysql -u root -p portfolio_db < backend/schema.sql
   mysql -u root -p portfolio_db < backend/seed.sql
   ```

### 2. Backend Setup
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On macOS/Linux: source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   Copy `.env.example` to `.env` and update `DB_PASSWORD` and other credentials if needed.
   ```bash
   cp .env.example .env
   ```
5. Run the Flask API:
   ```bash
   python app.py
   ```
   The backend will start at `http://localhost:5000`.

### 3. Frontend Setup
Because `flask-cors` is enabled, you can run the frontend on any port using a simple live server.
1. Navigate to the root directory containing `index.html`.
2. Run a simple HTTP server (e.g., using Python or an IDE Live Server plugin):
   ```bash
   python -m http.server 8000
   ```
3. Open `http://localhost:8000` in your browser. The frontend will automatically detect localhost and fetch projects from `http://localhost:5000/api/projects`.

---

## Free-Tier Cloud Deployment Guide

### Deploying to Render
1. Create a new **Web Service** on Render connected to this GitHub repo.
2. Under "Environment", select `Python 3`.
3. Set the **Build Command**:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Set the **Start Command**:
   ```bash
   cd backend && gunicorn app:app
   ```
5. **Database**: Create a MySQL instance (like Aiven or PlanetScale free tier) and copy the credentials.
6. Under Render's **Environment Variables**, add `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.

### Deploying to Railway
1. Click "New Project" -> "Deploy from GitHub repo".
2. Add a **MySQL plugin** database to your Railway project.
3. Railway will automatically inject `MYSQL_URL` and related variables. Map them to `DB_HOST`, `DB_USER`, `DB_PASSWORD`, etc., in the "Variables" tab of your Python app.
4. Railway will automatically detect the Python app and install `requirements.txt`.
5. Set your start command to `cd backend && gunicorn app:app` if it isn't auto-detected.

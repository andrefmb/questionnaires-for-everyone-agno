# 🏥 Questionnaires for Everyone: Modernized

> [!IMPORTANT]
> **This is a modernized fork** of the original [Questionnaires for Everyone](https://github.com/otsha/questionnaires-for-everyone) project. It replaces the legacy DeepL/OpenAI stack with a faster, locally-run, and provider-agnostic architecture using **Agno Agents** and **Argos Translate**.

This repository contains both the frontend and the backend server required to translate and evaluate questionnaires using AI.

## 📁 Repository Structure

- **[Frontend (React/Vite)](./questionnaires-for-everyone-agno-main)**: The web interface for users to input, tweak, and export translations.
- **[Backend (Flask/Agno)](./questionnaires-for-everyone-agno-server)**: The engine handling local translations and orchestrating AI Agents for quality assessment.

---

## 🚀 Quick Start (One Command)

To run the entire ecosystem (starting both the server and the client), simply run the automation script in the root folder:

```bash
chmod +x start.sh  # Ensure it's executable
./start.sh
```

This script will:
1. Automatically set up the Python virtual environment.
2. Install all backend and frontend dependencies.
3. Start the Backend on port **5001**.
4. Start the Frontend (Vite) concurrently.

---

## 🧠 What's Improved?

- **AI Orchestration**: Uses **Agno Agents** to perform evaluations. Defaults to **Gemini 2.0 Flash**, but is provider-agnostic.
- **Local Translation**: Moves away from DeepL API to **Argos Translate**. It runs locally on your machine—no API keys or costs for translation.
- **Optimized Performance**: Backend pre-loads ("warms up") models on startup to ensure instant results.
- **Zero Conflict**: Defaults to port 5001 to avoid common macOS AirPlay (port 5000) conflicts.

## 🛠️ Configuration

Before running, make sure to set up your `.env` in the server folder:
1. Copy [server/.env.example](./questionnaires-for-everyone-agno-server/.env.example) to `.env`.
2. Add your `GOOGLE_API_KEY` (Gemini).

---

## 📜 Documentation

- **[Backend Guide](./questionnaires-for-everyone-agno-server/README.md)**: Deep dive into the Agent architecture and local models.
- **[Frontend Guide](./questionnaires-for-everyone-agno-main/README.md)**: Details on UI customization and Vite configuration.

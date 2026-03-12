# ✨ Questionnaires for Everyone (FRONTEND)

> [!IMPORTANT]
> **Modernized Fork**: This is an updated version of the original [Questionnaires for Everyone](https://github.com/otsha/questionnaires-for-everyone).
> **Key Upgrade**: Integrated with **Agno Agents** for advanced AI-driven translation evaluation.
> 
> 🔗 **Looking for the engine?** Check out the [Backend Documentation](../questionnaires-for-everyone-agno-server/README.md).

## 🚀 Instant Setup
The fastest way to get started is by using the automation script in the parent directory:
```bash
./start.sh
```
This script handles the backend (Python/Vite) and frontend simultaneously.

---

## 🎨 Premium Features
-   **Step-by-Step UI**: Guidance from initial translation to AI evaluation.
-   **AI Intelligence**: Real-time feedback using **Gemini 2.0** via **Agno Agents**.
-   **Local Model Support**: Communicates with local Argos Translate models for privacy.
-   **CSV Export**: Export results directly to your local machine.

## 🛠️ Configuration

### API Connection (.env)
The frontend connects to the backend on port **5001** (to avoid macOS AirPlay conflicts):
```env
VITE_API_URL=http://localhost:5001
```

### Manual Development
```bash
npm install
npm run dev
```

## 🏗️ Technical Stack
- **Framework**: React (Vite)
- **State/UI**: Chakra UI
- **AI Backend**: Agno Orchestration (Google Gemini / OpenAI)
- **Local Language Models**: Argos Translate

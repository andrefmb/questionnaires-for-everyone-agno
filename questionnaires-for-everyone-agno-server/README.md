# 🤖 Questionnaires for Everyone (SERVER)

> [!IMPORTANT]
> **Modernized Fork**: This is an updated version of the original [Questionnaires for Everyone Server](https://github.com/otsha/questionnaires-for-everyone-server).
> **Key Upgrade**: Powered by **Agno Agents** and **Argos Translate** for local, intelligent processing.
> 
> 🔗 **Looking for the UI?** Check out the [Frontend Documentation](../questionnaires-for-everyone-agno-main/README.md).

## 🚀 Quick Start (Recommended)
The easiest way to run the entire project (Frontend + Backend) is using the unified startup script in the parent directory:
```bash
./start.sh
```
This script handles virtual environments, dependency installation, and port management automatically.

---

## 🧠 Powered by Agno Agents
This backend has been completely refactored to use [Agno](https://agno.com/) for AI orchestration:
- **Provider Agnostic**: Easily switch between **Gemini 2.0 Flash** (default) or OpenAI GPT-4.
- **Structured Intelligence**: Uses Pydantic schemas to ensure AI evaluations (GEMBA & SSA) are reliable and consistent.
- **Local First**: Built to work seamlessly alongside local translation models.

## 🌍 Offline Translation
By default, this server uses **Argos Translate** for private, local translations:
- No API keys required for translation.
- **Speed**: Optimized with model pre-loading ("warm-up") to ensure zero-latency first requests.

---

## ⚙️ Manual Configuration

### Environment Variables (.env)
```env
PORT=5001
FRONTEND_URL=http://localhost:5173,http://localhost:5174
LLM_PROVIDER=google
GOOGLE_API_KEY=your_gemini_key_here
```
*Note: We use port **5001** to avoid conflicts with macOS AirPlay.*

### References
- **Agno**: [Documentation](https://docs.agno.com/)
- **GEMBA-DA**: [Kocmi & Federmann (2023)](https://arxiv.org/abs/2302.14520)
- **SSA**: Custom Semantic Similarity Assessment.

<div align="center">
  <a href="https://youtu.be/4E1zzxORhWo">
    <img src="https://img.youtube.com/vi/4E1zzxORhWo/0.jpg" alt="GLiNER2.5 Router: This 340M AI Cuts Expensive LLM Calls by 70%!">
  </a>
  <h3>📺 <a href="https://youtu.be/4E1zzxORhWo">Watch the full tutorial on YouTube</a></h3>
</div>

# 🚀 GLiNER2.5-Decide: I Replaced an LLM Router With a 340M AI

This project demonstrates how a tiny 340M parameter zero-shot AI model (**fastino/GLiNER2.5-Decide**) can completely replace traditional, expensive LLM-based routing logic.

Instead of burning tokens to decide *which* model should handle a request, GLiNER2.5 classifies intent, priority, and task complexity in a single, blazing-fast pass (typically ~38-42ms on local hardware). It then routes the request instantly to the most appropriate parameterized backend without generating a single token!

## ⚡ The AI Router Pipeline

| 📥 Step 1: The Inbox | 🧠 Step 2: The 340M AI | 🚀 Step 3: Zero-Shot Routing |
|---|---|---|
| Read raw queries line-by-line from `inputs.txt`. | GLiNER2.5 instantly extracts the semantic `task_complexity`, `department`, and `priority`. | The request is seamlessly handed off to `llama3.2`, `qwen2.5-coder`, `gemini-3.5-flash-lite`, or dropped! |

---

## 🔥 Key Superpowers

- ⚡ **Sub-50ms Routing Latency**: Inspects query intent, complexity, and urgency in a single fast pass on local hardware (perfect for 4GB RAM setups).
- 💰 **Zero Token Generation**: Emits structured semantic classifications directly without autoregressive token generation overhead.
- 🎯 **Dynamic Parameterization**: Supports dynamic mapping to any local Ollama model (e.g., `llama3.2`, `qwen2.5-coder`) or cloud APIs (e.g., `gemini-3.5-flash-lite`).
- 🛑 **Native Moderation**: Capable of zero-shot spam detection and dropping payloads before they ever hit your expensive inference endpoints.

---

## 🛠️ Installation & Setup

### 1. Environment Setup
Install the required dependencies:

```powershell
pip install gliner2 python-dotenv huggingface_hub
```

*(Optional) Pre-download the model weights locally:*
```powershell
hf download fastino/GLiNER2.5-Decide
```

### 2. Configure API Keys
Create a `.env` file in the root directory:

```powershell
New-Item .env
```

Open the `.env` file and add your **Google Gemini API Key**. 
- Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
- Click **"Create API key"** and copy the key.
- Paste it into `.env`:
  ```env
  GEMINI_API_KEY=AIzaSy...
  GEMINI_MODEL=gemini-3.5-flash-lite
  ```

### 3. Setup Inputs
Open `inputs.txt` and write down your test prompts. Each line corresponds to one simulated user request.

### 4. Run the Router!
Execute the router:

```powershell
python main.py
```

This will process the inbox from `inputs.txt` and keep appending the routing decisions to `outputs/outputs.md`.

---

## 💻 Tech Stack

- **AI Router Engine**: `fastino/GLiNER2.5-Decide` (340M Parameters)
- **Base Architecture**: DeBERTa-v3-Large + Span Extraction
- **Local Fallback Targets**: Ollama Local Models (`llama3.2`, `qwen2.5-coder`)
- **Cloud Reasoning Target**: Google Gemini (`gemini-3.5-flash-lite`)

---

## 🎯 Real-World Use Cases

1. 💸 **LLM Traffic Cop**: Intercept trivial queries before they reach expensive models, sending them to small local instances.
2. 🛡️ **Spam & Injection Filter**: Zero-shot drop malicious payloads, spam, and PII leaks before downstream processing.
3. 🧠 **Agentic Orchestration**: Dynamically select the best expert agent for the job based on the semantic complexity of the prompt.
4. 🏢 **Helpdesk Triage**: Instantly categorize incoming customer support tickets and escalate angry customers directly to human agents.

---

## 📁 Repository Structure

```text
GLiNER2.5-Decide/
├── assets/
│   ├── gliner2.5_decide_overview.html # Visual presentation of the model
│   └── gliner2.5_decide_overview.md   # Markdown summary of the model
├── outputs/
│   └── outputs.md                   # Appending log of routing decisions
├── .env                             # Environment variables
├── inputs.txt                       # The simulated inbox prompts (one per line)
├── main.py                          # Core router logic
└── README.md
```

---
**Keywords:** AI Router, GLiNER2.5, LLM Cost Reduction, Semantic Routing, NLP, Local AI, Zero-Shot Classification, HuggingFace, Model Routing, Prompt Engineering

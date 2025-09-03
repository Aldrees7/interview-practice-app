# 💼 Interview Practice App

Streamlit app to **practice technical interviews**.  
Generate a **single tailored question** (with optional **JSON output**) or run a **multi-turn mock interview chat**. Includes **prompt-engineering modes**, **OpenAI parameter controls**, and **safety guards**.

---

## ✨ Features

- **Two modes**
  - **Question mode** – one question tailored to role, difficulty, and track (optional JSON schema).
  - **Chatbot (mock interview)** – back-and-forth interview with adaptive follow-ups.
- **Prompt engineering techniques**
  - Zero-shot, Few-shot, Chain-of-Thought, Role-play, Guardrailed.
- **Controls for OpenAI generation**
  - Model, temperature, top-p, max tokens, frequency & presence penalties.
- **Safety guard**
  - Length checks + banned terms filter (PII/unsafe categories).
- **NLP focus & difficulty**
  - Toggle **NLP Track** and choose **Easy/Medium/Hard**.
- **Optional external prompts**
  - Store system prompts in `prompts/system_prompts.json` and swap variants without touching code.
- **Code quality**
  - Formatted with **Black**, linted with **Ruff**, docstrings & constants (no “magic strings”).

---

## 🖼️ Screens

- Role, mode, and prompt-style selectors  
- Advanced model parameters expander  
- Structured JSON output (optional in Question mode)  
*(Add screenshots/GIFs here when you can.)*

---

## 🧱 Tech Stack

- **Python**, **Streamlit**
- **OpenAI API**
- Formatting: **Black**
- Linting: **Ruff**

---

## 🚀 Quick Start

### 1) Clone & install
```bash
git clone https://github.com/<you>/interview-practice-app.git
cd interview-practice-app
python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

*(If you don’t have a `requirements.txt` yet, create one with at least: `streamlit openai ruff black`.)*

### 2) Set your OpenAI key
```bash
# macOS/Linux
export OPENAI_API_KEY="sk-..."

# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
```

### 3) Run
```bash
streamlit run app.py
```

Open the local URL shown in the terminal.

---

## ⚙️ Configuration

### Environment variable
- `OPENAI_API_KEY` – your OpenAI API key (required)

### Optional: External prompts
Create `prompts/system_prompts.json` to override built-ins (file is **optional**; the app falls back to defaults):

```json
{
  "question": {
    "zero_shot": "You are a professional interviewer. Generate one technical interview question for the role: {role}. {tail}{json_hint}",
    "few_shot": "You are a professional interviewer.\nHere are examples...\nNow generate ONE new question for the role: {role}. {tail}{json_hint}",
    "chain_of_thought": "Think step by step...\n{tail}{json_hint}",
    "role_play": "Act as a senior hiring manager... {role}. {tail}{json_hint}",
    "guardrailed": "You are a professional interviewer... {role}.\nRules: ...\n{tail}{json_hint}"
  },
  "chat": {
    "system": "You are a seasoned interviewer for a {role} position. {focus}Conduct a realistic mock interview..."
  }
}
```

> Placeholders like `{role}`, `{tail}`, `{json_hint}`, `{focus}` are filled by the app.

---

## 🧪 Usage Tips

- **Question mode**  
  - Toggle **Structured JSON outputs** to get:
    ```json
    { "question": "...", "topic": "...", "difficulty": "Easy|Medium|Hard" }
    ```
  - If the model returns text, the app shows the raw output and warns you.

- **Chatbot mode**  
  - The system prompt adapts to **role**, **NLP track**, and **difficulty**.
  - The assistant asks one question at a time and follows up briefly.

---

## 🛡️ Safety

- Client-side guard blocks oversized inputs and banned/sensitive terms (PII/unsafe content list).
- Guard can be disabled via the UI (checkbox).

---

## 🧹 Code Quality

- **Black** (formatting)
  ```bash
  pip install black
  black app.py
  ```
- **Ruff** (linting & import sorting)
  ```bash
  pip install ruff
  ruff check .
  ruff format .
  ```

The code uses:
- **Docstrings** and type hints for clarity  
- **Constants** for roles/strings (`USER_ROLE`, `ASSISTANT_ROLE`, etc.)  
- Optional **external prompts** for maintainability

---

## 📁 Project Structure

```
interview-practice-app/
│
├─ app.py
├─ requirements.txt
└─ prompts/
   └─ system_prompts.json     # optional, overrides built-in templates
```

---

## ❓ Troubleshooting

- **`OPENAI_API_KEY not set`** → export the key in your shell (see Quick Start).
- **JSON output missing** → models may occasionally return plain text; the app will show raw output and warn you.
- **File not found: prompts/system_prompts.json** → the app falls back to defaults; creating the file is optional.

---

## 📄 License

MIT (or your preferred license)

---

## 🙌 Credits

Built by **Abdullah Aldrees** as part of AI/ML practice (MSc in AI, Tech & Sustainability + Turing AI Engineering track).

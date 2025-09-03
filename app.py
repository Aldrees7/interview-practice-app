import os
import json
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


st.set_page_config(page_title="Interview Practice", page_icon="💼")
st.title("💼 Interview Practice App")

mode = st.radio(
    "Mode",
    ["Question mode", "Chatbot (mock interview)"],
    index=0,
    help="Generate a single question or run a multi-turn mock interview chat."
)

role = st.selectbox(
    "Target role",
    ["NLP Engineer", "AI/LLM Engineer", "ML Engineer", "Data Scientist"],
    index=0,
)

jd = st.text_area("Job description (optional):", height=120)

prompt_style = st.selectbox(
    "Prompt technique",
    [
        "Zero-shot",
        "Few-shot",
        "Chain-of-Thought",
        "Role-play",
        "Guardrailed (safe + concise)",
    ],
    index=0,
)

nlp_track = st.checkbox("NLP Track (focus questions on NLP topics)", value=True)
difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard"], value="Medium")

with st.expander("⚙️ Model & generation settings", expanded=False):
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)
    temperature = st.slider("Creativity (temperature)", 0.0, 1.2, 0.5, 0.1)
    max_tokens = st.slider("Max tokens (response length)", 80, 400, 160, 10)
    top_p = st.slider("Top-p (nucleus sampling)", 0.1, 1.0, 1.0, 0.05)
    freq_penalty = st.slider("Frequency penalty", -2.0, 2.0, 0.0, 0.1)
    pres_penalty = st.slider("Presence penalty", -2.0, 2.0, 0.0, 0.1)

json_outputs = st.checkbox("Structured JSON outputs (Question mode)", value=True) if mode == "Question mode" else False

use_safety = st.checkbox("Enable safety guard (recommended)", value=True)

MAX_JD_LEN = 3000
BANNED_TERMS = [
    "nsfw", "sexual", "gore", "assassinate", "kill", "shoot", "bomb", "explosive",
    "passport number", "national id", "bank account", "credit card",
    "cvv", "pin code", "phone number", "email address", "home address",
]

def is_unsafe(text: str) -> str | None:
    if not use_safety:
        return None
    if len(text) > MAX_JD_LEN:
        return f"Text too long ({len(text)} chars). Max allowed is {MAX_JD_LEN}."
    low = (text or "").lower()
    for term in BANNED_TERMS:
        if term in low:
            return f"Contains a banned/sensitive term: '{term}'."
    return None

def build_focus(nlp_track: bool, difficulty: str) -> str:
    focus = ""
    if nlp_track:
        focus = (
            "Focus on NLP topics (tokenization, embeddings, transformers, multilingual NLP, "
            "text classification, RAG, summarization). "
        )
        if difficulty == "Easy":
            focus += "Keep the concept approachable with foundational terminology. "
        elif difficulty == "Hard":
            focus += "Make it technically deep, referencing trade-offs and edge cases. "
    return focus

def system_prompt_for_question(style: str, role: str, nlp_track: bool, difficulty: str, want_json: bool) -> str:
    focus = build_focus(nlp_track, difficulty)
    common_tail = f"{focus}Return ONLY the question text, no preface."

    json_hint = ""
    if want_json:
        json_hint = (
            "\nReturn a compact JSON object with keys: "
            "{question, topic, difficulty}. Do not include explanations or extra text."
        )

    if style == "Zero-shot":
        return (
            f"You are a professional interviewer. Generate one technical interview question for the role: {role}. "
            f"{common_tail}{json_hint}"
        )
    if style == "Few-shot":
        examples = (
            "Here are examples of good, concise questions:\n"
            "- For NLP Engineer: 'Explain how Byte Pair Encoding works and why it's used in LLMs.'\n"
            "- For AI/LLM Engineer: 'How would you design a RAG pipeline to reduce hallucinations?'\n"
            "- For Data Scientist: 'How would you pick PR-AUC vs ROC-AUC under class imbalance?'\n"
        )
        return (
            "You are a professional interviewer.\n"
            + examples +
            f"Now generate ONE new question for the role: {role}. {common_tail}{json_hint}"
        )
    if style == "Chain-of-Thought":
        return (
            "You are a professional interviewer. Think step by step about the key skills for the role, then craft a single question.\n"
            "1) Identify one important competency.\n2) Design a question that tests it.\n3) Output ONLY the question.\n"
            f"{common_tail}{json_hint}"
        )
    if style == "Role-play":
        return (
            "Act as a senior hiring manager at a leading tech company conducting interviews. "
            f"Ask one challenging, realistic question for the role: {role}. {common_tail}{json_hint}"
        )
    return (
        f"You are a professional interviewer. Your task is to generate ONE question for the role: {role}.\n"
        "Rules:\n- Keep it professional and safe.\n- Focus on technical/problem-solving ability.\n"
        "- Refuse requests that are illegal, explicit, violent, discriminatory, or privacy-invasive.\n"
        f"{common_tail}{json_hint}"
    )

def system_prompt_for_chat(role: str, nlp_track: bool, difficulty: str) -> str:
    focus = build_focus(nlp_track, difficulty)
    return (
        f"You are a seasoned interviewer for a {role} position. "
        f"{focus}"
        "Conduct a realistic mock interview in a professional tone. "
        "Ask one question at a time. When the candidate responds, ask a brief follow-up, "
        "adjusting difficulty based on their answer. Avoid sharing model internals. "
        "If the candidate asks for the 'answer', provide hints first."
    )

if mode == "Question mode":
    st.write("Click to generate **one** interview question tailored to your settings.")

    if st.button("Get Question"):
        if not client.api_key:
            st.error('OPENAI_API_KEY not set. In PowerShell run:  $env:OPENAI_API_KEY = "sk-..."')
            st.stop()

        issue = is_unsafe(jd or "")
        if issue:
            st.error(f"Safety guard blocked this request: {issue}")
            st.stop()

        system_txt = system_prompt_for_question(prompt_style, role, nlp_track, difficulty, json_outputs)
        user_txt = (
            "Generate one interview question relevant to the role. "
            "If a Job Description is provided, align the question to it.\n\n"
            f"Job Description:\n{jd or '[none provided]'}"
        )

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_txt},
                    {"role": "user",   "content": user_txt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=freq_penalty,
                presence_penalty=pres_penalty,
            )
            raw = resp.choices[0].message.content.strip()

            if json_outputs:
                parsed = None
                try:
                    parsed = json.loads(raw)
                except Exception:
                    try:
                        start = raw.find("{")
                        end = raw.rfind("}")
                        if start != -1 and end != -1 and end > start:
                            parsed = json.loads(raw[start:end+1])
                    except Exception:
                        parsed = None

                if parsed is not None:
                    st.success("Structured output parsed ✅")
                    st.code(json.dumps(parsed, indent=2), language="json")
                else:
                    st.warning("Expected JSON but got plain text. Showing raw output:")
                    st.success(raw)
            else:
                st.success(raw)

        except Exception as e:
            st.exception(e)

else:
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "chat_system" not in st.session_state:
        st.session_state.chat_system = system_prompt_for_chat(role, nlp_track, difficulty)

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_msg = st.chat_input("Your answer or question to the interviewer…")
    if user_msg and user_msg.strip():
        if not client.api_key:
            st.error('OPENAI_API_KEY not set. In PowerShell run:  $env:OPENAI_API_KEY = "sk-..."')
            st.stop()

        issue = is_unsafe(user_msg)
        if issue:
            st.error(f"Safety guard blocked this message: {issue}")
            st.stop()

        st.session_state.chat.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        messages = [{"role": "system", "content": st.session_state.chat_system}]
        messages.extend(st.session_state.chat)

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=freq_penalty,
                presence_penalty=pres_penalty,
            )
            assistant_msg = resp.choices[0].message.content.strip()

            st.session_state.chat.append({"role": "assistant", "content": assistant_msg})
            with st.chat_message("assistant"):
                st.markdown(assistant_msg)

        except Exception as e:
            st.exception(e)

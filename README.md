---

```markdown
# 🦙 Chat App – Streamlit + LLaMA 3

A lightweight, locally-run conversational AI app built using [Streamlit](https://streamlit.io/) and [Meta’s LLaMA 3](https://ai.meta.com/llama/). This project marks my **first practical step into Generative AI** using open-source language models.

This app lets users interact with LLaMA 3 in a real-time chat interface, hosted locally — no external API calls or OpenAI dependencies required.

---

## 🔍 Features

- 🦙 Runs **LLaMA 3 (2nd gen)** locally via `llama-cpp-python`
- ⚡ Efficient with support for quantized `.gguf` models
- ✨ Real-time chatbot interface using Streamlit
- 💬 Maintains conversation state per session
- 🌙 Dark theme by default using Streamlit config

---

## 🚀 Demo

Coming soon — but you can run it locally in under a minute!

---

## 🛠 Installation

### 1. Clone the repo and set up your environment

```bash
git clone https://github.com/YoussefIbraheem/chat-app-streamlit.git
cd chat-app-streamlit

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download a LLaMA 3 GGUF model

Download a quantized `.gguf` model (e.g. `llama-3-8b-instruct.Q4_K_M.gguf`) from:

- [TheBloke on Hugging Face](https://huggingface.co/TheBloke)

Place the downloaded model file in:

```bash
models/llama-3-8b-instruct.Q4_K_M.gguf
```

> You can modify the model path in `app.py`.

### 3. Run the app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
chat-app-streamlit/
├── app.py                   # Main Streamlit app
├── requirements.txt         # Python dependencies
├── .gitignore
├── models/                  # Folder to store your .gguf model
└── .streamlit/
    └── config.toml          # Enables dark theme
```

---

## ⚙️ Model Notes

- Uses [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python)
- Supports **quantized GGUF format** for local LLaMA 3 inference
- No external API keys or cloud models required

---

## 💡 Future Enhancements

- [ ] Token streaming for better UX
- [ ] RAG-style context injection (with PDFs or notes)
- [ ] Dockerization for deployment
- [ ] Prompt templates & personas

---

## 🧑‍💻 Author

**Youssef Ibraheem** – Backend Developer diving into GenAI with open-source tooling  
[LinkedIn](https://www.linkedin.com/in/youssefibraheem/) · [GitHub](https://github.com/YoussefIbraheem)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

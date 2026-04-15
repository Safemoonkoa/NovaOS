<div align="center">
  <img src="https://via.placeholder.com/150/000000/00FFFF?text=NovaOS" alt="NovaOS Logo" width="150"/>
  <h1>NovaOS</h1>
  <p><b>The desktop AI that sees, thinks and acts on your computer — fully local.</b></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
  [![Local First](https://img.shields.io/badge/Local-First-success.svg)](#)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#)
</div>

---

## 🚀 What is NovaOS?

NovaOS is an autonomous AI assistant that **controls your entire PC** just like a human would. It moves the mouse, clicks, types, opens applications, browses the web, manages files, and executes commands. 

Everything runs **100% local-first**, ensuring your privacy and security. It's the natural evolution of AI assistants: while others live in chat windows, NovaOS lives directly on your desktop and takes action.

> **Star if you want an AI that actually uses your computer!** ⭐

---

## ✨ Key Features

- ⚡ **One-Command Install**: Get started instantly with `npx novaos@latest` or `docker run`.
- 🔒 **Fully Offline**: Powered by Ollama and local models (Llama 3.2, Qwen 2.5, Phi-4).
- 👁️ **Local Vision**: Understands your screen using VLMs like LLaVA, Moondream, or Qwen2-VL.
- 🧠 **Persistent Memory**: Remembers your preferences and past interactions using vector and graph memory.
- 🛡️ **Safety First**: Always asks for confirmation before performing sensitive actions (mouse/keyboard control).
- 🎨 **Beautiful UI**: Minimalist floating overlay, chat sidebar, and voice mode.
- 💻 **Cross-Platform**: Supports Windows, macOS, and Linux.

---

## 🛠️ MVP Capabilities

1. **Chat Mode**: Interact via text or voice.
2. **Computer Use Mode**: Tell it to "Open Chrome, check NVIDIA's stock price, and take a screenshot" — it does it step-by-step using vision.
3. **Hands-Free Voice Mode**: Press a global hotkey (e.g., `Ctrl+Alt+N`) and speak directly.
4. **Task Planning**: Break down complex tasks ("Prepare a weekly sales report") into actionable steps.
5. **Safety Confirmations**: Previews and requests approval before destructive or input actions.
6. **Long-Term Memory**: Recalls file locations, frequent projects, and user habits.
7. **Plug-and-Play Skills**: Easily add new capabilities like `skill_browser`, `skill_files`, or `skill_terminal`.
8. **Local Dashboard**: A web interface to view history, agent status, and model configurations.

---

## 📦 Installation

### Prerequisites
- Python 3.12+
- [Ollama](https://ollama.ai/) (for local models)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/novaos.git
   cd novaos
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env to configure your preferred models and settings
   ```

4. **Run NovaOS Doctor (Check dependencies):**
   ```bash
   python -m novaos.cli --doctor
   ```

5. **Start the Agent:**
   ```bash
   python -m novaos.cli --command "Hello, NovaOS!"
   ```

---

## 🏗️ Project Structure

```text
novaos/
├── README.md                  ← You are here!
├── LICENSE                    ← MIT License
├── pyproject.toml             ← Project metadata and dependencies
├── requirements.txt           ← Python dependencies
├── docker-compose.yml         ← Docker setup (coming soon)
├── novaos/
│   ├── __init__.py
│   ├── core/                  ← Main agent logic and LangGraph workflows
│   ├── vision/                ← Screen capture and VLM reasoning
│   ├── control/               ← Mouse, keyboard, and window management
│   ├── memory/                ← Vector and graph memory systems
│   ├── voice/                 ← STT (Speech-to-Text) and TTS (Text-to-Speech)
│   ├── skills/                ← Plug-and-play skills directory
│   ├── ui/                    ← Floating overlay and web dashboard
│   └── config.py              ← Configuration management
├── examples/                  ← Example scripts and use cases
├── scripts/                   ← Utility scripts (e.g., setup.sh)
└── tests/                     ← Unit and integration tests
```

---

## 🤝 Contributing

We welcome contributions! Whether it's adding new skills, improving the vision module, or fixing bugs, your help is appreciated.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <i>Built with ❤️ by the open-source community. Let's break GitHub! 🔥</i>
</div>

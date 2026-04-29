# 🚀 React Factory Agent (LangGraph)

An autonomous multi-agent system designed to design, code, and review React components based on natural language descriptions. This project demonstrates advanced agentic workflows, self-correction loops, and local LLM integration.

## 🛠️ Tech Stack

- **AI Framework:** LangGraph, LangChain
- **LLM:** Qwen2.5-Coder (via Ollama)
- **Runtime:** Python 3.10+
- **Styling:** Tailwind CSS
- **Hardware:** Local execution on NVIDIA RTX 4060 (GPU Acceleration)

## 🧠 System Architecture (Multi-Agent Flow)

The system operates in a closed-loop **Self-Correction** architecture:

1. **Architect Node**: Analyzes user prompts and generates a technical blueprint (props, HTML structure, state logic).
2. **Coder Node**: Produces clean JSX code using Tailwind CSS classes.
3. **Reviewer Node**: Performs self-reflection, checking for syntax errors, missing imports, or export statements.
4. **Conditional Edge**: If the Reviewer detects issues, the graph routes back to the Coder with specific feedback.
5. **Saver Node**: Upon a successful review, the code is extracted using **Regex** and saved as a physical `.jsx` file.

## 🚀 Getting Started

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Plutoteo0/react_factory_agent
   cd component-generator
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup LLM:**
   Make sure [Ollama](https://ollama.com) is running and pull the model:
   ```bash
   ollama pull qwen2.5-coder
   ```
4. **Run the generator:**
   ```bash
   python main.py
   ```

## 📈 Future Roadmap

- **Component Assembler**: Building a high-level orchestrator to generate full project structures (e.g., `App.jsx`, `main.jsx`, and folder hierarchies).
- **Task Decomposition**: Implementing logic to split complex UI requests into multiple atomic components (e.g., decomposing a "Dashboard" prompt into `Sidebar`, `Header`, and `StatsCard`).
- **Automated Validation**: Integrating ESLint or headless testing to verify code validity before the saving phase.

## 🎓 Project Context

This project was developed by a 2nd-year Computer Science student from Wrocław as part of an AI/ML Engineer Trainee portfolio. It focuses on moving beyond simple RAG systems into **Deterministic Agentic Workflows**.

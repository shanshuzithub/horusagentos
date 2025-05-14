# HorusAgentOS: Autonomous Agent Operating System

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

<!-- Add other relevant badges here: build status, version, etc. -->

**HorusAgentOS** is a revolutionary open-source framework for building intelligent agents that can autonomously operate computers, much like a human user. It integrates state-of-the-art Large Language Models (LLMs), multi-modal perception, and reinforcement learning to provide powerful and flexible desktop automation across multiple platforms.

**Core Vision:** "Empower AI to become your digital twin, autonomously executing complex desktop tasks."

## ✨ Features

*   **Cross-Platform GUI Automation:** Seamlessly controls applications on **Windows, macOS, and Linux**.
*   **Multi-Modal Perception:** Understands user interfaces by combining:
    *   Screen Capture Analysis
    *   Accessibility Tree Parsing
    *   Optical Character Recognition (OCR)
*   **Precise Interaction:** Accurately simulates human-like mouse clicks, keyboard inputs, and other UI interactions.
*   **Enhanced Memory System:**
    *   **Narrative Memory:** Records overall task trajectories and reflections.
    *   **Episodic Memory:** Stores detailed sub-task execution processes and summaries.
    *   **Knowledge Accumulation:** Continuously learns from experiences to improve efficiency and decision-making.
*   **Advanced Planning & Decision-Making:**
    *   **Hierarchical Task Planning:** Decomposes complex user requests into manageable sub-tasks using LLMs.
    *   **Dynamic Strategy Adjustment:** Adapts plans in real-time based on execution feedback.
    *   **Reinforcement Learning:** Optimizes decision strategies over time.
*   **Multi-Agent Collaboration (Future Goal):** Designed to support multiple agents working in concert to tackle complex workflows.
*   **Developer-Friendly:**
    *   **Unified Python API:** Clean and easy-to-use interfaces.
    *   **Modular Architecture:** Clear separation of concerns for extensibility.
    *   **(Planned) Comprehensive Documentation:** Detailed guides and examples.

## 🏛️ Technical Architecture

HorusAgentOS utilizes a modular architecture composed of five key layers:

1.  **Perception Layer:** Responsible for understanding the computer's screen and UI elements.
    *   _Components:_ Screen Analysis, OCR, Accessibility Tree Parsing, Multi-Modal Fusion.
    *   _Key Technologies:_ `mss`, `pytesseract`, `pywinauto` (Windows), `pyobjc` (macOS AXAPI), `python-atspi` (Linux), `OpenCV`, `Pillow`.

2.  **Decision Layer:** The "brain" of the agent, responsible for task planning and execution management.
    *   _Components:_ Task Planner (LLM-based), Execution Controller, Reinforcement Learning Engine, Multi-Agent Coordinator.
    *   _Key Technologies:_ LLM APIs (e.g., OpenAI), Transformers, HTN/PDDL concepts, `Stable Baselines3`/`RLlib`.

3.  **Action Layer:** Executes the planned actions on the GUI.
    *   _Components:_ GUI Interaction Engine, Cross-Platform Drivers, Automation Script Generation, Error Recovery.
    *   _Key Technologies:_ `pyautogui`, `pywinauto`, AppleScript/JXA, `xdotool`.

4.  **Memory Layer:** Enables the agent to learn from past experiences.
    *   _Components:_ Long-Term Memory Storage (Vector DBs), Knowledge Retrieval, Experience Summarization & Generalization, Memory Update Strategy.
    *   _Key Technologies:_ Vector Databases (`FAISS`, `Weaviate`, etc.), Sentence Transformers, `SQLite`/`PostgreSQL`.

5.  **Communication Layer:** Facilitates interaction between modules, other agents, and external systems.
    *   _Components:_ Internal Communication Protocol, External System Integration, API Interface, Multi-Agent Communication.
    *   _Key Technologies:_ Message Queues (`RabbitMQ`, `Kafka`), RPC (`gRPC`), API Frameworks (`FastAPI`, `Flask`).

For a more detailed breakdown, please see the [Technical Specification (tech.md)](tech.md).

## 🚀 Getting Started

This project is currently under active development. The following provides a conceptual overview of installation and usage.

### Prerequisites

*   Python 3.9+ (Recommended: 3.10 or 3.11 for broader library compatibility)
*   `pip` (Python package installer)
*   Platform-specific dependencies for GUI automation and perception (details to be provided).
    *   **Windows:** May require specific C++ build tools for some libraries.
    *   **macOS:** Xcode command-line tools.
    *   **Linux:** `tesseract-ocr`, `scrot`, `xdotool`, `libxtst-dev`, `python3-tk`, `python3-dev`, etc.

### Installation

```bash
# Clone the repository (once public)
# git clone https://github.com/yourusername/horusagentos.git
# cd horusagentos

# Create and activate a virtual environment (recommended)
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate

# Install dependencies (a requirements.txt will be provided)
# pip install -r requirements.txt

# For now, if you have the source code directly:
# pip install . 
# or for editable mode:
# pip install -e .
```

(Note: `pip install HorusAgentOS` from PyPI will be available upon official release.)

### Basic Usage (Conceptual)

```python
from horusagentos import HorusAgentOS

# Configuration for the LLM (example for OpenAI)
llm_config = {
    "provider": "openai", # or "huggingface", "local_llm_provider"
    "model": "gpt-4o",    # Choose your preferred model
    "api_key": "YOUR_OPENAI_API_KEY" # Securely manage your API keys
}

# Optional agent-wide configurations for different modules
agent_settings = {
    'perception_config': {'ocr_engine': 'tesseract_best'}, # Example
    'action_config': {'default_delay_ms': 200},      # Example
    'memory_config': {'db_path': './agent_memory.sqlite'} # Example
}

# Initialize the agent
agent = HorusAgentOS(llm_provider_config=llm_config, agent_config=agent_settings)

# Define a task in natural language
task_instruction = "Open the Chrome browser, search for the official HorusAgentOS GitHub page, and save the link to a file named 'horus_link.txt' on the desktop."

# Execute the task
result = agent.execute_task(task_instruction)

# Print the outcome
print(f"Task Status: {result.get('status')}")
print(f"Message: {result.get('message')}")
if result.get('plan'):
    print("Generated Plan:")
    for i, step in enumerate(result['plan']):
        print(f"  Step {i+1}: {step.get('description', step.get('action'))} - Params: {step.get('params')}")
if result.get('results') and result['results'].get('step_results'):
    print("Execution Details:")
    for i, step_res in enumerate(result['results']['step_results']):
        print(f"  Step {i+1} Outcome: Success={step_res.get('success')}, Details: {step_res.get('details')}")

```

## 🛠️ Project Structure

The core logic is primarily within the `horusagentos/` directory:

```
horusagentos/
├── __init__.py              # Makes horusagentos a package
├── agent.py                 # Core HorusAgentOS class orchestrating modules
├── perception_module.py     # Handles screen analysis, OCR, UI element detection
├── decision_module.py       # Task planning, LLM interaction, execution logic
├── action_module.py         # Executes low-level GUI actions (clicks, typing)
├── memory_module.py         # Stores and retrieves past experiences
├── communication_module.py  # Inter-module and inter-agent communication
└── (utils_module.py)        # (Potential) Shared utilities

main.py                      # Example script to run the agent
tech.md                      # Detailed technical specification
proj.md                      # Project overview (original, may contain non-English)
README.md                    # This file
requirements.txt             # (To be added) Python dependencies
LICENSE                      # Project License (MIT)
.gitignore
pyproject.toml               # Project metadata and build system configuration
```

## 🤝 Contributing

Contributions are welcome! As the project matures, we will establish contribution guidelines, including:

*   Reporting bugs and suggesting features via GitHub Issues.
*   Submitting Pull Requests with well-tested code and documentation.
*   Coding standards and style guides.

(Details to be formalized soon.)

## 🗺️ Roadmap

*   **Alpha Release:** Core functionality for single-agent task execution on one platform.
*   **Beta Release:** Cross-platform stability, refined memory and learning, basic multi-agent communication.
*   **V1.0:** Robust and well-tested framework with comprehensive documentation and examples.
*   **Future Enhancements (from `tech.md`):
    *   Advanced Reinforcement Learning for self-improvement.
    *   Security and Sandboxing for agent actions.
    *   Improved User Intent Disambiguation.
    *   Proactive Assistance capabilities.
    *   Standardized Skill/Plugin System for easy extension.
    *   Deeper Visual Grounding beyond current perception techniques.

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

*   Inspiration from existing agent frameworks and the broader AI community.
*   (To be expanded as the project develops and incorporates external libraries/ideas)
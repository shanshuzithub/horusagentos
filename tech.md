# HorusAgentOS: Technical Specification

## 1. Introduction

HorusAgentOS is a revolutionary open-source framework designed to build intelligent agents capable of autonomously operating computers, mirroring human-like interaction. It integrates cutting-edge large language models (LLMs), multi-modal perception, and reinforcement learning techniques to deliver robust and flexible desktop automation capabilities.

## 2. Core Value Proposition

"Enable AI to become your digital twin, autonomously executing complex desktop tasks."

Key benefits include:
-   **Cross-Platform Automation:** Support for Windows, macOS, and Linux.
-   **Enhanced Memory System:** Facilitates long-term learning and experience accumulation.
-   **Advanced LLM Integration:** Improves environmental understanding and decision-making.
-   **Developer-Friendly Tools:** Lowers the barrier to entry with intuitive APIs and development tools.
-   **Multi-Agent Collaboration:** Enables automation of complex workflows through coordinated agent efforts.

## 3. Product Features

### 3.1. Cross-Platform GUI Automation
-   **Platform Compatibility:** Seamless operation across Windows, macOS, and Linux.
-   **Multi-Modal Perception:** Understands GUIs by combining screen capture analysis, accessibility tree parsing, and OCR.
-   **Precise Interaction:** Simulates human-like mouse clicks, keyboard inputs, and other interactions.

### 3.2. Enhanced Memory System
-   **Narrative Memory:** Records the overall trajectory and reflections of task execution.
-   **Episodic Memory:** Stores detailed sub-task execution processes and summarized experiences.
-   **Knowledge Accumulation:** Continuously learns and optimizes to improve task execution efficiency.

### 3.3. Advanced Planning and Decision-Making
-   **Hierarchical Task Planning:** Decomposes complex tasks into manageable sub-tasks.
-   **Dynamic Adjustment:** Adapts strategies in real-time based on execution feedback.
-   **Multi-Agent Collaboration:** Supports multiple agents working together to complete complex workflows.

### 3.4. Developer Friendliness
-   **Unified API:** Simple and easy-to-use interface design.
-   **Comprehensive Documentation:** Detailed development guides and examples.
-   **Community Support:** Active community and technical assistance.

## 4. Technical Architecture

HorusAgentOS employs a modular design, with the following primary components:

### 4.1. Perception Layer
-   **Screen Analysis:** Real-time capture and processing of desktop screenshots.
-   **OCR Technology:** Recognizes text content within the user interface.
-   **Accessibility Tree Parsing:** Understands UI structure and element attributes.
-   **Multi-Modal Fusion:** Integrates visual and textual information for comprehensive understanding.

    **Key Technologies/Libraries:**
    *   Screen Capture: `mss` (Python) for cross-platform screen capture.
    *   OCR: `Tesseract OCR` (via `pytesseract` wrapper).
    *   Accessibility: `pywinauto` (Windows), `AXAPI` (macOS via `pyobjc`), `AT-SPI` (Linux via `python-atspi`).
    *   Image Processing: `OpenCV`, `Pillow`.

### 4.2. Decision Layer
-   **Task Planner:** Breaks down complex tasks into sub-tasks. Utilizes LLMs for understanding natural language instructions and generating task plans.
-   **Execution Controller:** Manages the task execution flow.
-   **Reinforcement Learning Engine:** Optimizes decision-making strategies based on feedback.
-   **Multi-Agent Coordinator:** Supports distributed task execution among multiple agents.

    **Key Technologies/Libraries:**
    *   LLM Integration: `OpenAI API`, `Hugging Face Transformers`.
    *   Planning: Hierarchical Task Network (HTN) planners, PDDL (Planning Domain Definition Language) concepts.
    *   Reinforcement Learning: `Stable Baselines3`, `RLlib`.

### 4.3. Action Layer
-   **GUI Interaction Engine:** Executes mouse clicks, keyboard inputs, and other GUI operations.
-   **Cross-Platform Drivers:** Adapts interaction methods for different operating systems.
-   **Automation Script Generation:** Dynamically generates executable code for actions.
-   **Error Recovery Mechanism:** Handles exceptions and errors during execution.

    **Key Technologies/Libraries:**
    *   GUI Automation: `pyautogui`, `pywinauto` (Windows), AppleScript/JXA (macOS), `xdotool` (Linux).
    *   Scripting: Python for dynamic script generation.

### 4.4. Memory Layer
-   **Long-Term Memory Storage:** Persists historical task experiences (e.g., using vector databases).
-   **Knowledge Retrieval System:** Quickly retrieves relevant experiences based on similarity.
-   **Experience Summarization and Generalization:** Extracts generalizable knowledge from specific cases.
-   **Memory Update Strategy:** Periodically optimizes and prunes outdated memories.

    **Key Technologies/Libraries:**
    *   Vector Databases: `FAISS`, `Annoy`, `Pinecone`, `Weaviate`.
    *   Embedding Models: Sentence Transformers (e.g., `sentence-transformers` library).
    *   Databases: `SQLite`, `PostgreSQL` for structured metadata.

### 4.5. Communication Layer
-   **Internal Communication Protocol:** Enables efficient collaboration between modules (e.g., using message queues or RPC).
-   **External System Integration:** Interfaces with other tools and services.
-   **API Interface:** Provides standardized development interfaces (e.g., RESTful APIs, gRPC).
-   **Multi-Agent Communication:** Facilitates information exchange between agents (e.g., using `MQTT`, `ZeroMQ`).

    **Key Technologies/Libraries:**
    *   Message Queues: `RabbitMQ`, `Kafka`.
    *   RPC: `gRPC`.
    *   API Frameworks: `FastAPI`, `Flask`.

## 5. Core Agent Class (Conceptual)

```python
class HorusAgentOS:
    def __init__(self, llm_provider, platform_os):
        """
        Initializes the HorusAgentOS.

        Args:
            llm_provider: Configuration for the Large Language Model (e.g., OpenAI API key, model name).
            platform_os: The current operating system ('windows', 'macos', 'linux').
        """
        self.platform_os = platform_os

        # Initialize Layers
        self.perception_layer = PerceptionLayer(platform_os)
        self.decision_layer = DecisionLayer(llm_provider)
        self.action_layer = ActionLayer(platform_os)
        self.memory_layer = MemoryLayer()
        self.communication_layer = CommunicationLayer() # Potentially for multi-agent setup

        # Link layers (simplified example)
        self.decision_layer.set_perception_layer(self.perception_layer)
        self.decision_layer.set_action_layer(self.action_layer)
        self.decision_layer.set_memory_layer(self.memory_layer)

    def execute_task(self, natural_language_instruction: str) -> str:
        """
        Executes a task described in natural language.

        Args:
            natural_language_instruction: The user's instruction (e.g., "Open Chrome, search for HorusAgentOS, and save the first three results").

        Returns:
            A string summarizing the outcome of the task execution.
        """
        try:
            # 1. Understand the instruction and create a plan
            # This would involve the Decision Layer (Task Planner) using LLMs
            # and potentially Memory Layer for past similar tasks.
            task_plan = self.decision_layer.create_plan(natural_language_instruction)
            
            # 2. Execute the plan
            # The Decision Layer (Execution Controller) would iterate through plan steps,
            # using Perception to understand the current state and Action to interact.
            execution_results = self.decision_layer.execute_plan(task_plan)

            # 3. Learn from the execution
            # The Memory Layer would store the experience (narrative, episodic).
            # The Decision Layer (RL Engine) might update its policies.
            self.memory_layer.record_experience(natural_language_instruction, task_plan, execution_results)
            self.decision_layer.learn_from_execution(execution_results)

            return f"Task executed successfully: {execution_results.summary}"

        except Exception as e:
            # Error handling and potentially using the Error Recovery Mechanism from Action Layer
            error_summary = f"Error during task execution: {str(e)}"
            self.memory_layer.record_error(natural_language_instruction, error_summary)
            return error_summary

# --- Placeholder Classes for Layers (to be defined in detail) ---

class PerceptionLayer:
    def __init__(self, platform_os):
        self.platform_os = platform_os
        # Initialize screen capture, OCR, accessibility tools based on OS
        pass
    def get_current_state(self):
        # Capture screen, analyze UI elements, extract text
        pass

class DecisionLayer:
    def __init__(self, llm_provider):
        self.llm_provider = llm_provider
        # Initialize planner, RL engine, LLM client
        self.perception = None
        self.action = None
        self.memory = None
        pass

    def set_perception_layer(self, perception_layer):
        self.perception = perception_layer

    def set_action_layer(self, action_layer):
        self.action = action_layer

    def set_memory_layer(self, memory_layer):
        self.memory = memory_layer
        
    def create_plan(self, instruction):
        # Use LLM to parse instruction and generate a sequence of actions
        # Consult memory for similar plans
        pass
    def execute_plan(self, plan):
        # Iterate through plan steps, using perception and action layers
        pass
    def learn_from_execution(self, results):
        # Update RL policies or other learning models
        pass

class ActionLayer:
    def __init__(self, platform_os):
        self.platform_os = platform_os
        # Initialize GUI automation tools based on OS
        pass
    def perform_action(self, action_details):
        # Execute mouse click, keyboard input, etc.
        pass

class MemoryLayer:
    def __init__(self):
        # Initialize database connections, vector stores
        pass
    def record_experience(self, instruction, plan, results):
        # Store narrative and episodic memory
        pass
    def record_error(self, instruction, error_summary):
        pass
    def retrieve_relevant_experience(self, query):
        # Search for similar past experiences
        pass

class CommunicationLayer:
    def __init__(self):
        # Initialize communication channels (e.g., message queue client)
        pass
    def send_message_to_agent(self, agent_id, message):
        pass
    def receive_message(self):
        pass

```

## 6. Installation and Initialization (Example from proj.md)

### Installation
```bash
pip install HorusAgentOS # Placeholder, actual package name might differ
```

### Initialization (Conceptual Python Example)
```python
from HorusAgentOS import HorusAgentOS # This will be the main class

# Initialize HorusAgentOS
# LLM provider details (e.g., API keys, model choice) would be part of engine_params
# Grounding_agent might relate to how the agent perceives/interacts with specific UIs or APIs
agent = HorusAgentOS(
    llm_provider={"model": "gpt-4o", "api_key": "YOUR_API_KEY"}, # Example
    platform_os="windows" # or "macos", "linux"
)

# Execute a task
task_instruction = "Open Chrome browser, search for HorusAgentOS, and save the first three results as a text file on the desktop."
result_summary = agent.execute_task(task_instruction)
print(result_summary)
```

## 7. Future Considerations / Roadmap
*   **Advanced RL:** More sophisticated reinforcement learning for self-improvement.
*   **Security and Sandboxing:** Ensuring safe execution of agent actions.
*   **User Intent Disambiguation:** Better handling of ambiguous instructions.
*   **Proactive Assistance:** Agent suggesting tasks or optimizations.
*   **Standardized Skill/Plugin System:** Allowing easy extension of agent capabilities.
*   **Visual Grounding:** Deeper understanding of UI elements beyond OCR/Accessibility trees.

This document provides a foundational technical overview. Each layer and component will require more detailed design and specification during development.

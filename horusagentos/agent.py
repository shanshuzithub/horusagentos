# tech.md: 5. Core Agent Class (Conceptual)

import platform
import traceback

# Adjusted imports for flattened structure
from .perception_module import PerceptionModule
from .decision_module import DecisionModule
from .action_module import ActionModule
from .memory_module import MemoryModule
from .communication_module import CommunicationModule
# from .utils import get_platform_specific_config # Example utility


class HorusAgentOS:
    def __init__(self, llm_provider_config: dict, agent_config: dict = None):
        """
        Initializes the HorusAgentOS.

        Args:
            llm_provider_config (dict): Configuration for the Large Language Model 
                                        (e.g., {"provider": "openai", "model": "gpt-4o", "api_key": "YOUR_API_KEY"}).
            agent_config (dict, optional): General configuration for the agent and its modules.
        """
        self.platform_os = platform.system().lower()
        self.llm_provider_config = llm_provider_config
        self.agent_config = agent_config if agent_config else {}

        print(f"Initializing HorusAgentOS on {self.platform_os}...")

        # Initialize Modules (Layers)
        self.perception_module = PerceptionModule(
            config=self.agent_config.get('perception_config'))
        self.action_module = ActionModule(
            config=self.agent_config.get('action_config'))
        self.memory_module = MemoryModule(
            config=self.agent_config.get('memory_config'))

        self.decision_module = DecisionModule(
            llm_provider_config=self.llm_provider_config,
            perception_module=self.perception_module,
            action_module=self.action_module,
            memory_module=self.memory_module,
            config=self.agent_config.get('decision_config')
        )

        self.communication_module = CommunicationModule(
            config=self.agent_config.get('communication_config'))

        print("HorusAgentOS initialized successfully.")

    def execute_task(self, natural_language_instruction: str) -> dict:
        """
        Executes a task described in natural language.

        Args:
            natural_language_instruction: The user's instruction.

        Returns:
            A dictionary summarizing the outcome of the task execution.
        """
        print(f"Received task: {natural_language_instruction}")
        task_summary = {
            "instruction": natural_language_instruction,
            "status": "failed",
            "message": "",
            "plan": None,
            "results": None
        }

        try:
            task_plan = self.decision_module.create_plan(
                natural_language_instruction)
            task_summary["plan"] = task_plan

            if not task_plan:
                task_summary["message"] = "Failed to create a task plan."
                self.memory_module.record_error(
                    natural_language_instruction, None, task_summary, None)
                return task_summary

            print(f"Generated Plan: {task_plan}")

            execution_results = self.decision_module.execute_plan(task_plan)
            task_summary["results"] = execution_results
            task_summary["message"] = execution_results.get(
                "summary", "Plan execution finished.")

            # Check if all steps in the plan were successful
            all_steps_succeeded = True
            if execution_results and execution_results.get("step_results"):
                for step_result in execution_results["step_results"]:
                    if not step_result.get("success", False):
                        all_steps_succeeded = False
                        break
            else:  # No steps or no results implies failure/incompletion
                all_steps_succeeded = False

            if all_steps_succeeded:
                task_summary["status"] = "success"
            elif execution_results and execution_results.get("step_results"):
                task_summary["status"] = "partially_completed"
            else:
                task_summary["status"] = "failed"

            self.decision_module.learn_from_execution(
                natural_language_instruction, task_plan, execution_results)

            return task_summary

        except Exception as e:
            error_message = f"Critical error during task execution: {str(e)}"
            print(error_message)
            task_summary["message"] = error_message
            tb_str = traceback.format_exc()
            print(tb_str)
            self.memory_module.record_error(natural_language_instruction, task_summary.get("plan"),
                                            {"error": str(e), "traceback": tb_str}, None)
            return task_summary

    def get_agent_status(self):
        """Returns the current status of the agent and its modules."""
        return {
            "platform": self.platform_os,
            "llm_config_model": self.llm_provider_config.get("model", "N/A"),
            "modules_initialized": {
                "perception": hasattr(self, 'perception_module') and self.perception_module is not None,
                "decision": hasattr(self, 'decision_module') and self.decision_module is not None,
                "action": hasattr(self, 'action_module') and self.action_module is not None,
                "memory": hasattr(self, 'memory_module') and self.memory_module is not None,
                "communication": hasattr(self, 'communication_module') and self.communication_module is not None
            }
        }


# Example of how to run if this file is executed directly (for testing)
if __name__ == "__main__":
    print("Running HorusAgentOS Core (agent.py) direct execution example...")

    mock_llm_config = {
        "provider": "mock_llm",
        "model": "mock_model_v1",
        "api_key": "mock_key_123"
    }
    mock_agent_config = {
        'perception_config': {'os_override': None},  # Example config
        'action_config': {'default_timeout': 10},  # Example config
        'memory_config': {'db_type': 'sqlite', 'path': './horus_memory.db'},
        'decision_config': {'max_retries': 3},
        'communication_config': {'port': 0}  # 0 for dynamic port or None
    }

    try:
        agent = HorusAgentOS(
            llm_provider_config=mock_llm_config, agent_config=mock_agent_config)
        print("\nAgent Status Before Task:")
        print(agent.get_agent_status())

        task = "Simulate opening a file and typing hello."
        result = agent.execute_task(task)

        print("\nTask Execution Result:")
        print(f"Instruction: {result['instruction']}")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        print(f"Plan: {result['plan']}")
        print(f"Results: {result['results']}")

        print("\nAgent Status After Task:")
        print(agent.get_agent_status())

    except Exception as e:
        print(f"Error in agent.py main execution block: {e}")
        print(traceback.format_exc())

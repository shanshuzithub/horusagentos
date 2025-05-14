# HorusAgentOS Main Package (Flattened Structure)

# Import core components to be available at the package level
from .agent import HorusAgentOS
from .perception_module import PerceptionModule
from .decision_module import DecisionModule
from .action_module import ActionModule
from .memory_module import MemoryModule
from .communication_module import CommunicationModule
# Placeholder for a utility module if needed later
# from .utils_module import some_utility_function # Assuming utils_module.py

__all__ = [
    "HorusAgentOS",
    "PerceptionModule",
    "DecisionModule",
    "ActionModule",
    "MemoryModule",
    "CommunicationModule",
    # "some_utility_function"
]

print("HorusAgentOS package initialized.")

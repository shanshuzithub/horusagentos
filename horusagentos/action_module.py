# tech.md: 4.3. Action Layer
import platform
import time
import subprocess
import os
# Potential future imports: pyautogui, pywinauto, AppKit (for macOS via pyobjc)


class ActionModule:
    def __init__(self, config: dict = None):
        self.config = config if config else {}
        self.os_type = self.config.get(
            'os_override', platform.system().lower())
        self.gui_controller = self._initialize_gui_controller()
        print(f"ActionModule initialized for {self.os_type}")

    def _initialize_gui_controller(self):
        print(f"Mock: GUI controller initialized for {self.os_type}.")
        # Placeholder for pyautogui, pywinauto, AppleScript/JXA, xdotool
        if self.os_type == "windows":
            # For example: from pywinauto.application import Application; return Application()
            return "MockPyAutoWin"
        elif self.os_type == "darwin":  # macOS
            # For example: import pyautogui; return pyautogui
            return "MockPyAutoGUI_macOS"
        elif self.os_type == "linux":
            # For example: import pyautogui; return pyautogui
            return "MockPyAutoGUI_Linux"
        return "MockGUIController"

    def perform_action(self, action_type: str, parameters: dict, current_state=None) -> dict:
        """Performs a specified action on the GUI."""
        print(
            f"Action: Performing action '{action_type}' with params: {parameters} using {self.gui_controller}")
        success = False
        result_details = {"action_type": action_type, "parameters": parameters}
        default_delay = self.config.get(
            'default_delay_ms', 100) / 1000.0  # convert ms to s

        try:
            if action_type == "click":
                x = parameters.get('x')
                y = parameters.get('y')
                element_id = parameters.get('element_id')
                # In a real scenario, if element_id is provided, use accessibility to find its coordinates
                # then use self.gui_controller.click(coords)
                print(
                    f"Action: Simulating click at ({x}, {y}) or element {element_id}")
                # import pyautogui; pyautogui.click(x,y) # Example with actual library
                success = True
            elif action_type == "type_text":
                text_to_type = parameters.get('text', '')
                # Could be used to focus element first
                element_id = parameters.get('element_id')
                print(
                    f"Action: Simulating typing text '{text_to_type}' into element {element_id}")
                # import pyautogui; pyautogui.typewrite(text_to_type, interval=0.05) # Example
                success = True
            elif action_type == "press_key":
                key_name = parameters.get('key_name')
                print(f"Action: Simulating pressing key: {key_name}")
                # import pyautogui; pyautogui.press(key_name) # Example
                success = True
            elif action_type == "open_app":
                app_name = parameters.get('app_name')
                success = self._open_application(app_name)
                result_details["message"] = f"Application '{app_name}' opened: {success}"
            elif action_type == "scroll":
                direction = parameters.get('direction', 'down')
                # Arbitrary unit (pixels or lines)
                amount = parameters.get('amount', 100)
                print(f"Action: Simulating scroll {direction} by {amount}")
                # import pyautogui; pyautogui.scroll(-amount if direction == 'down' else amount) # Example
                success = True
            elif action_type == "wait":
                duration_s = parameters.get('duration_s', 1.0)
                print(f"Action: Waiting for {duration_s} seconds.")
                time.sleep(duration_s)
                success = True
            else:
                result_details["error"] = f"Unknown action type: {action_type}"
                print(f"Action: Unknown action type '{action_type}'")
                success = False

            if success:
                # Small delay after action for UI to update
                time.sleep(default_delay)

        except Exception as e:
            error_msg = f"Error performing action {action_type}: {e}"
            print(f"Action: {error_msg}")
            result_details["error"] = error_msg
            success = False
            self.handle_error(action_type, parameters, e)

        result_details["success"] = success
        return result_details

    def _open_application(self, app_name_or_path: str) -> bool:
        print(f"Action: Attempting to open application: {app_name_or_path}")
        try:
            if self.os_type == "windows":
                os.startfile(app_name_or_path)
                return True
            elif self.os_type == "darwin":  # macOS
                subprocess.run(["open", "-a", app_name_or_path], check=True)
                return True
            elif self.os_type == "linux":
                # This is a simplistic approach; might need `xdg-open` or specific commands
                subprocess.run([app_name_or_path], check=True, shell=True)
                return True
        except FileNotFoundError:
            print(f"Action: Application '{app_name_or_path}' not found.")
        except subprocess.CalledProcessError as e:
            print(
                f"Action: Error opening application '{app_name_or_path}': {e}")
        except Exception as e:
            print(
                f"Action: Unexpected error opening '{app_name_or_path}': {e}")
        return False

    def generate_automation_script(self, action_sequence: list) -> str:
        """Dynamically generates a Python script (e.g., using pyautogui) for an action sequence."""
        print(
            f"Action: Generating automation script for {len(action_sequence)} actions.")
        script_lines = ["import pyautogui", "import time"]
        for action in action_sequence:
            action_type = action.get("action")
            params = action.get("params", {})
            if action_type == "click":
                script_lines.append(
                    f"pyautogui.click(x={params.get('x')}, y={params.get('y')})")
            elif action_type == "type_text":
                script_lines.append(
                    f"pyautogui.typewrite('{params.get('text', '')}', interval=0.05)")
            elif action_type == "press_key":
                script_lines.append(
                    f"pyautogui.press('{params.get('key_name')}')")
            elif action_type == "wait":
                script_lines.append(
                    f"time.sleep({params.get('duration_s', 1.0)})")
            # Add more mappings as needed
            # Small delay between actions
            script_lines.append("time.sleep(0.1)")
        return "\n".join(script_lines)

    def handle_error(self, failed_action_type: str, failed_parameters: dict, error: Exception):
        """Handles errors during action execution, potentially attempting recovery."""
        print(
            f"Action: Error handler triggered for action '{failed_action_type}' with error: {error}")
        # Placeholder for error recovery logic (e.g., retry, alternative action, notify decision layer)
        return {"recovery_attempted": False, "recovery_details": "Error logged, no recovery implemented yet."}


if __name__ == '__main__':
    print("Testing ActionModule...")
    config = {'os_override': None, 'default_delay_ms': 50}
    action_module = ActionModule(config=config)
    print(f"Initialized for OS: {action_module.os_type}")

    # Test click
    res_click = action_module.perform_action(
        "click", {"x": 100, "y": 150, "element_id": "test_btn"})
    print(f"Click result: {res_click}")

    # Test type_text
    res_type = action_module.perform_action(
        "type_text", {"text": "Hello from ActionModule!", "element_id": "test_input"})
    print(f"Type text result: {res_type}")

    # Test open_app (will likely fail if app doesn't exist or path is wrong)
    # Use a common app for testing, e.g., 'Notepad' on Windows, 'TextEdit' on macOS
    app_to_test = 'Calculator' if platform.system(
    ) == "Darwin" else 'notepad'  # Basic example
    # res_open = action_module.perform_action("open_app", {"app_name": app_to_test})
    # print(f"Open app ('{app_to_test}') result: {res_open}")

    # Test unknown action
    res_unknown = action_module.perform_action(
        "fly_to_moon", {"speed": "warp9"})
    print(f"Unknown action result: {res_unknown}")

    # Test script generation
    script = action_module.generate_automation_script([
        {"action": "click", "params": {"x": 10, "y": 20}},
        {"action": "type_text", "params": {"text": "Generated script"}}
    ])
    print(f"Generated script:\n{script}")

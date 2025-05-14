# tech.md: 4.5. Communication Layer
# Potential future imports: paho-mqtt, pyzmq, fastapi, flask

class CommunicationModule:
    def __init__(self, config: dict = None):
        self.config = config if config else {}
        self.host = self.config.get('host', 'localhost')
        # 0 might mean dynamic or not used for some methods
        self.port = self.config.get('port', 0)

        self.message_queue_client = self._initialize_mq_client()
        self.api_server_instance = self._initialize_api_server()  # If agent exposes an API
        print(f"CommunicationModule initialized (config: {self.config})")

    def _initialize_mq_client(self):
        # Placeholder for RabbitMQ, Kafka, ZeroMQ client
        mq_type = self.config.get('mq_type', 'mock')
        print(f"Mock: Message Queue client initialized (type: {mq_type}).")
        # Example: if mq_type == 'zmq': import zmq; context = zmq.Context(); socket = context.socket(zmq.REQ); return socket
        return "MockMQClient"

    def _initialize_api_server(self):
        # Placeholder for FastAPI or Flask app if the agent needs to serve API requests
        api_type = self.config.get('api_type', None)
        if api_type:
            print(
                f"Mock: API server ({api_type}) would be initialized here on host {self.host}, port {self.port}.")
            # Example: if api_type == 'fastapi': from fastapi import FastAPI; return FastAPI()
            return "MockAPIServer"
        return None

    def send_internal_message(self, target_module_name: str, message_type: str, payload: dict) -> dict:
        """Sends a message to another internal module of the agent (conceptual for monolithic)."""
        print(
            f"Communication: Sending internal message to '{target_module_name}' (type: '{message_type}'): {payload}")
        # In a truly monolithic agent where modules are just classes, this might not be used.
        # If modules were microservices, this would use an internal bus.
        return {"success": True, "response": "Internal message dispatched (mock)."}

    def send_message_to_agent(self, target_agent_id: str, message_content: dict) -> dict:
        """Sends a message to another agent in a multi-agent setup."""
        print(
            f"Communication: Sending message to agent '{target_agent_id}' via {self.message_queue_client}: {message_content}")
        # Example with ZMQ:
        # self.message_queue_client.connect(f"tcp://{target_agent_address}:{port}")
        # self.message_queue_client.send_json(message_content)
        # response = self.message_queue_client.recv_json()
        # return {"success": True, "response_from_agent": response}
        return {"success": True, "response": f"Message sent to agent {target_agent_id} (mock)."}

    def receive_message_from_topic(self, topic: str, timeout_ms: int = 100) -> dict or None:
        """Receives a message from a specific topic (e.g., via MQTT or Kafka subscription)."""
        print(
            f"Communication: Checking for incoming messages on topic '{topic}' (timeout: {timeout_ms}ms) via {self.message_queue_client}...")
        # Placeholder for actual message receiving logic from a pub/sub system
        # Example: message = self.mqtt_client.check_msg()
        #          if message: return message.payload
        return None  # Return received message or None if no message / timeout

    def register_external_service(self, service_name: str, service_details: dict):
        """Registers an external tool or service that the agent can interact with."""
        if not hasattr(self, 'external_services'):
            self.external_services = {}
        self.external_services[service_name] = service_details
        print(
            f"Communication: Registered external service: '{service_name}' with details: {service_details}")

    def call_external_service(self, service_name: str, method: str, params: dict) -> dict:
        """Calls a method of a registered external service (e.g., via HTTP API)."""
        print(
            f"Communication: Calling external service '{service_name}', method '{method}' with params: {params}")
        if hasattr(self, 'external_services') and service_name in self.external_services:
            service_config = self.external_services[service_name]
            # Example: if service_config['type'] == 'http_api':
            #    import requests
            #    url = f"{service_config['base_url']}/{method}"
            #    response = requests.post(url, json=params) if params else requests.get(url)
            #    return {"success": response.ok, "data": response.json() if response.ok else response.text}
            return {"success": True, "data": f"Mock call to {service_name}/{method} successful."}
        return {"success": False, "error": f"External service '{service_name}' not registered or call not implemented."}

    # Example methods for an agent exposing its own API (if self.api_server_instance is used)
    # def start_api_server_thread(self):
    #     if self.api_server_instance and hasattr(self.api_server_instance, 'run'):
    #         import threading
    #         # Define API endpoints on self.api_server_instance first
    #         thread = threading.Thread(target=self.api_server_instance.run, args=(self.host, self.port))
    #         thread.daemon = True
    #         thread.start()
    #         print(f"Mock API server started on {self.host}:{self.port}")


if __name__ == '__main__':
    print("Testing CommunicationModule...")
    config = {'mq_type': 'mock_zmq', 'host': '127.0.0.1',
              'port': 5555, 'api_type': 'fastapi'}
    comm_module = CommunicationModule(config=config)

    comm_module.send_internal_message(
        "DecisionModule", "task_update", {"status": "in_progress"})

    comm_module.send_message_to_agent("Agent007", {"request": "status_report"})

    msg = comm_module.receive_message_from_topic("agent/tasks/new")
    if msg:
        print(f"Received external message: {msg}")
    else:
        print("No external message received on topic.")

    comm_module.register_external_service(
        "WeatherAPI", {"type": "http_api", "base_url": "https://api.weather.com"})
    weather_data = comm_module.call_external_service(
        "WeatherAPI", "getCurrent", {"location": "London"})
    print(f"Weather API call result: {weather_data}")

    # if comm_module.api_server_instance:
    #     print("API server instance seems to be initialized (mock). Consider testing start_api_server_thread if implemented.")

import zmq
import json
from .command_handler import CommandHandler, MathCommandHandler, OSCommandHandler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="server.log",
)

class Server:
    def __init__(self, port: int = 5555):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)

        self.processors = {
            "os": OSCommandHandler(),
            "compute": MathCommandHandler(),
        }

    def start(self):
        self.socket.bind(f"tcp://*:{self.port}")
        while True:
            try:
                message = self.socket.recv_string()
                logging.info(f"Received raw message: {message}")

                response = self.process_request(message)
                self.socket.send_json(response)
                logging.info(f"Sent response: {response}")

            except Exception as e:
                self.socket.send_json({
                    "status": "error",
                    "error": "Internal server error"
                })
                logging.error(f"Error response: {e}")
            
    def process_request(self, message: str) -> dict:
        try:
            command_data = json.loads(message)
            logging.info(f"Received command: {command_data}")

            command_type = command_data.get("command_type")
            if not command_type:
                return {
                    "status": "error",
                    "error": "Missing command_type"
                }
            if command_type not in self.processors:
                return {
                    "status": "error",
                    "error": f"Unknown command type: {command_type}"
                }
            processor = self.processors[command_type]
            return processor.process(command_data)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON received: {message}")
            return {
                "status": "error",
                "error": f"Invalid JSON format: {str(e)}"
            }
        except Exception as e:
            logging.error(f"Error processing command: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    def stop(self):
        try:
            self.executor.shutdown(wait=False)
            self.socket.close()
            self.context.term()
            logging.info("Server stopped")
        except Exception as e:
            logging.error(f"Error stopping server: {e}")

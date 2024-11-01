import zmq
import json
from .command_handler import MathCommandHandler, OSCommandHandler
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="server.log",
)

class Server:
    def __init__(self, port: int = 5555, max_workers: int = 10):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.Lock()
        self.pending_tasks: Dict[str, Future] = {}


        self.processors = {
            "os": OSCommandHandler(),
            "compute": MathCommandHandler(),
        }

    def start(self):
        self.socket.bind(f"tcp://*:{self.port}")
        try:
            while True:
                client_id, empty, message = self.socket.recv_multipart()
                message_str = message.decode('utf-8')
                logging.info(f"Received message from {client_id}: {message_str}")
                
                task = self.executor.submit(self.process_request, message_str)
                task_id = str(uuid.uuid4())
                
                with self.lock:
                    self.pending_tasks[task_id] = (task, client_id)
                
                # Add callback to send response when task completes
                task.add_done_callback(
                    lambda future, task_id=task_id: self.send_response(task_id, future)
                )
        except Exception as e:
            logging.error(f"Server error: {e}")
            self.stop()
            
    def send_response(self, task_id: str, future: Future):
        try:
            result = future.result()
            with self.lock:
                _, client_id = self.pending_tasks.pop(task_id)
                self.socket.send_multipart([
                    client_id,
                    b'',
                    json.dumps(result).encode('utf-8')
                ])
                logging.info(f"Sent response to {client_id}: {result}")
        except Exception as e:
            logging.error(f"Error sending response: {e}")
            with self.lock:
                _, client_id = self.pending_tasks.pop(task_id)
                error_response = {
                    "status": "error",
                    "error": "Internal server error"
                }
                self.socket.send_multipart([
                    client_id,
                    b'',
                    json.dumps(error_response).encode('utf-8')
                ])

    def process_request(self, message: str) -> dict:
        try:
            command_data = json.loads(message)
            logging.info(f"Processing command: {command_data}")

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
            self.executor.shutdown(wait=True)
            self.socket.close()
            self.context.term()
            logging.info("Server stopped")
        except Exception as e:
            logging.error(f"Error stopping server: {e}")

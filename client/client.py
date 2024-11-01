import json

import zmq


class Client:
    def __init__(self, server_address: str = "tcp://localhost:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(server_address)

    def send_command(self, command_data):
        try:
            self.socket.send_string(json.dumps(command_data))
            response = self.socket.recv_json()
            return response
        except Exception as e:
            return {"status": "error", "error": f"{str(e)}"}

    def stop(self):
        self.socket.close()
        self.context.term()

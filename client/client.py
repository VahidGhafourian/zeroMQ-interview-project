import json

import zmq


class Client:
    def __init__(self, server_address: str = "tcp://localhost:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect(server_address)

    def send_command(self, command_data):
        try:
            self.socket.send_multipart([b'', json.dumps(command_data).encode('utf-8')])
            empty, response = self.socket.recv_multipart()
            return response.decode('utf-8')
        except Exception as e:
            return {"status": "error", "error": f"{str(e)}"}

    def stop(self):
        self.socket.close()
        self.context.term()

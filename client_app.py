import json

from client.client import Client

if __name__ == "__main__":
    client = Client()

    # Example OS command
    command = {
        "command_type": "os",
        "command_name": "ping",
        "parameters": ["127.0.0.1", "-c", "6"],
    }

    response = client.send_command(command)
    print(f"Response: {json.dumps(response, indent=2)}")

    math_command = {"command_type": "compute", "expression": "(8 / 4) * 10"}
    response = client.send_command(math_command)
    print(f"Response: {json.dumps(response, indent=2)}")
    client.stop()

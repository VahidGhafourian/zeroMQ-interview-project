from client.client import Client

if __name__ == "__main__":
    client = Client()

    os_command = {
        "command_type": "os",
        "command_name": "ping",
        "parameters": ["127.0.0.1", "-c", "6"],
    }

    print("Sending OS command...")
    response = client.send_command(os_command)
    print(f"Response: {response}")

    math_command = {"command_type": "compute", "expression": "(2 + 2) * 10"}

    print("\nSending Math command...")
    response = client.send_command(math_command)
    print(f"Response: {response}")
    client.stop()

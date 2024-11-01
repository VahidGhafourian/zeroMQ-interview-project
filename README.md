# ZMQ Command Processor

A client-server application that processes OS and Math commands using ZeroMQ (ZMQ) for communication. The server handles multiple types of commands concurrently and returns results in a structured JSON format.

## Features

- **Modular Command Processing**: Extensible architecture using the Command pattern
- **Multiple Command Types**:
  - OS Commands (ping, ls, dir)
  - Math Commands (arithmetic expressions)
- **Concurrent Request Handling**: Thread pool executor for processing multiple requests
- **Comprehensive Error Handling**: Robust error handling and logging
- **Security Features**: Command whitelisting and safe math expression evaluation
- **Unit Tests**: Test coverage for core functionality

## Project Structure

```
zmq-command-processor/
├── client/
│   └── client.py
├── server/
│   ├── command_handler.py
│   └── server.py
├── server_app.py
├── client_app.py
└── requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/VahidGhafourian/zeroMQ-interview-project.git zmq-command-processor
cd zmq-command-processor
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the server:
```bash
python server_app.py
```

2. In a separate terminal, run the client:
```bash
python client_app.py
```

## Usage Examples

### OS Command
```python
command = {
    "command_type": "os",
    "command_name": "ping",
    "parameters": ["127.0.0.1", "-c", "6"]
}
```

### Math Command
```python
command = {
    "command_type": "compute",
    "expression": "(8 + 2) * 10"
}
```


## Design Decisions

1. **Command Pattern**
   - Used the Command pattern to encapsulate different types of commands
   - Makes it easy to add new command types without modifying existing code
   - Each command type has its own processor class

2. **Concurrent Processing**
   - Implemented ThreadPoolExecutor for handling multiple requests
   - Configurable number of worker threads
   - Each command runs in its own thread

3. **Security Considerations**
   - Whitelisted OS commands to prevent unauthorized command execution
   - Math expressions are evaluated using AST to prevent code injection
   - Command timeouts to prevent resource exhaustion

4. **Error Handling**
   - Comprehensive exception handling at all levels
   - Structured error responses
   - Server-side logging for debugging and monitoring

## Configuration

Server configuration can be modified in `main_server.py`:
- Default port: 5555
- Max worker threads: 10
- Logging level: INFO

## Extending the Application

To add a new command type:

1. Create a new processor class inheriting from `CommandProcessor`
2. Implement the `process` method
3. Register the processor in `CommandServer.__init__`

Example:
```python
class NewCommandProcessor(CommandProcessor):
    def process(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation here
        pass

# In CommandServer.__init__:
self.processors['new_type'] = NewCommandProcessor()
```

## Limitations

- OS commands are limited to a predefined whitelist
- Math commands support only basic arithmetic operations
- No authentication/authorization mechanism
- Single server instance (no clustering)

## Future Improvements

- Add authentication/authorization
- Implement command queueing
- Add support for more complex mathematical operations
- Implement server clustering
- Implement unit tests for the client and server.
- Add command history and result caching

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

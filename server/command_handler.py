import abc
import subprocess
import ast
import operator


class CommandHandler(abc.ABC):
    @abc.abstractmethod
    def process(self, command_data):
        pass


class OSCommandHandler(CommandHandler):
    ALLOWED_COMMANDS = {"ping", "dir", "ls"}

    def process(self, command_data):
        command_name = command_data.get("command_name", "").lower()
        if command_name not in self.ALLOWED_COMMANDS:
            raise ValueError(f"Command '{command_name}' is not allowed")

        parameters = command_data.get("parameters", [])
        try:
            result = subprocess.run(
                [command_name, *parameters], capture_output=True, text=True, timeout=30
            )
            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": "Command timed out"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

class MathCommandHandler(CommandHandler):
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(self, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            op = type(node.op)
            if op not in self.OPERATORS:
                raise ValueError(f"Unsupported operator: {op.__name__}")
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return self.OPERATORS[op](left, right)
        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")

    def process(self, command_data):
        expression = command_data.get("expression", "")
        try:
            tree = ast.parse(expression, mode="eval")
            result = self.evaluate(tree.body)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

class CodeExecutor:
    def __init__(self, sandbox_dir="./sandbox"):
        self.sandbox_dir = sandbox_dir
        
    def execute(self, code: str) -> str:
        import sys
        import io
        import contextlib
        
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                exec(code, {"__builtins__": __builtins__}, {})
            except Exception as e:
                print(f"Execution Error: {str(e)}")
                
        return output.getvalue().strip()

if __name__ == "__main__":
    executor = CodeExecutor()
    print(executor.execute("print('Hello from LogicLoom Engine!')\nx = 5+5\nprint(x)"))
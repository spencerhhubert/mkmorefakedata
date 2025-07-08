class Logger:
    def __init__(self, debug_level: int):
        self.debug_level = debug_level

    def info(self, message: str) -> None:
        if self.debug_level > 0:
            print(f"INFO: {message}")

    def warning(self, message: str) -> None:
        if self.debug_level > 0:
            print(f"WARNING: {message}")

    def error(self, message: str) -> None:
        if self.debug_level > 0:
            print(f"ERROR: {message}")

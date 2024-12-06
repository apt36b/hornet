# exceptions.py
from rich.table import Table
from typing import Dict, Any
from rich.console import Console

class HornetRansomwareException(Exception):
    def __init__(self, message: str, context: Dict[str, Any]) -> None:
        """
        Initializes the exception and automatically prints the error details using rich.

        Args:
            message (str): The error message.
            context (Dict[str, Any]): Additional context for the error.
        """
        super().__init__(message)
        self.message: str = message
        self.context: Dict[str, Any] = context
        # Automatically render error details when the exception is instantiated
        self._print_error()

    def _print_error(self) -> None:
        """
        Prints the error message and context using rich.
        """
        console = Console()
        console.print(f"[bold red]Error: {self.message}[/bold red]")
        table = Table(title="Error Context")
        table.add_column("Key", style="bold cyan")
        table.add_column("Value", style="bold magenta")
        for key, value in self.context.items():
            table.add_row(key, str(value))
        console.print(table)

    def __str__(self) -> str:
        """
        Returns a string representation of the error for logging or debugging.
        """
        return f"{self.message} (see rich logs for more details)"

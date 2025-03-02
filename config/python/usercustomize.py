
from rich.traceback import install

from rich.console import Console
console = Console()


install(
  show_locals=True,
  width=console.width,
  code_width=90,
)

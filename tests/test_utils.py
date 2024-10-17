from typing import Any, Callable

"""
This method is called whenever emit is called from a test.
Use it to assert the correct information is being sent to the frontend.
"""
emit_callback: Callable[[str, Any], None] = None

class Emit:
    def __init__(self, event: str, args: Any = None) -> None:
        self.event = event
        self.args = args
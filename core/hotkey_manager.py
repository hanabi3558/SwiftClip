"""Global hotkey management module."""

from typing import Callable, Optional

import keyboard


class HotkeyManager:
    """Manager for global hotkey registration."""

    def __init__(self):
        """Initialize the hotkey manager."""
        self._hotkey_id: Optional[int] = None
        self._hotkey: Optional[str] = None

    def register(self, hotkey: str, callback: Callable[[], None]) -> bool:
        """
        Register a global hotkey.

        Args:
            hotkey: Hotkey combination (e.g., "ctrl+shift+t")
            callback: Function to call when hotkey is pressed

        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Unregister existing hotkey if any
            self.unregister()

            # Register new hotkey
            self._hotkey_id = keyboard.add_hotkey(
                hotkey,
                callback,
                suppress=True
            )
            self._hotkey = hotkey

            print(f"Hotkey registered: {hotkey}")
            return True

        except Exception as e:
            print(f"Failed to register hotkey '{hotkey}': {e}")
            return False

    def unregister(self) -> None:
        """Unregister the current hotkey."""
        if self._hotkey_id is not None:
            try:
                keyboard.remove_hotkey(self._hotkey_id)
            except Exception:
                pass
            self._hotkey_id = None
            self._hotkey = None

    def get_current_hotkey(self) -> Optional[str]:
        """Get the currently registered hotkey."""
        return self._hotkey

    def wait(self) -> None:
        """Block and wait for hotkey events."""
        keyboard.wait()

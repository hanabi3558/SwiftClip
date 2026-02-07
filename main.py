"""
SwiftClip Application

A Windows application that allows you to select a screen region,
capture it, and open it in Google Lens for text recognition and translation.

Usage:
    1. Run this application
    2. It will appear in the system tray
    3. Press Ctrl+Shift+T to select a screen region
    4. Drag to select the area you want to translate
    5. Google Lens opens - press Ctrl+V to paste the image
    6. Right-click tray icon and select Exit to quit
"""

import sys
import threading
import time
from typing import Optional, Tuple

# Set DPI awareness before importing Tkinter
from core.screenshot_capture import set_dpi_awareness
set_dpi_awareness()

import config
from core.hotkey_manager import HotkeyManager
from core.overlay_selector import OverlaySelector
from core.screenshot_capture import capture_region
from core.lens_integration import open_google_lens
from core.tray_icon import TrayIcon
from utils.clipboard import copy_image_to_clipboard


class SwiftClip:
    """Main application class for SwiftClip."""

    def __init__(self):
        """Initialize the SwiftClip application."""
        self.hotkey_manager = HotkeyManager()
        self.tray_icon = TrayIcon(on_quit=self._on_quit)
        self._is_selecting = False
        self._running = True

    def start(self) -> None:
        """Start the application."""
        # Start tray icon
        self.tray_icon.start(config.HOTKEY)

        # Register hotkey
        if not self.hotkey_manager.register(config.HOTKEY, self._on_hotkey):
            self.tray_icon.notify("Error", "Failed to register hotkey")
            sys.exit(1)

        # Show startup notification
        self.tray_icon.notify(
            "SwiftClip",
            f"Press {config.HOTKEY.upper()} to select region"
        )

        # Keep running
        try:
            while self._running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        """Stop the application."""
        self._running = False
        self.hotkey_manager.unregister()
        self.tray_icon.stop()

    def _on_quit(self) -> None:
        """Handle quit from tray menu."""
        self.stop()
        sys.exit(0)

    def _on_hotkey(self) -> None:
        """Handle hotkey press."""
        if self._is_selecting:
            return  # Already selecting

        self._is_selecting = True

        # Run selection in a new thread to avoid blocking keyboard listener
        thread = threading.Thread(target=self._start_selection)
        thread.start()

    def _start_selection(self) -> None:
        """Start the screen region selection process."""
        try:
            # Create and show overlay
            overlay = OverlaySelector(
                alpha=config.OVERLAY_ALPHA,
                selection_color=config.SELECTION_COLOR,
                border_width=config.SELECTION_BORDER_WIDTH
            )

            # Use a simple callback mechanism
            result = {"coords": None}

            def on_selection(coords: Optional[Tuple[int, int, int, int]]) -> None:
                result["coords"] = coords

            overlay.show(on_selection)

            # Process the selection
            coords = result["coords"]

            if coords is None:
                return  # Cancelled

            self._process_selection(coords)

        finally:
            self._is_selecting = False

    def _process_selection(self, coords: Tuple[int, int, int, int]) -> None:
        """
        Process the selected region.

        Args:
            coords: Selection coordinates (x1, y1, x2, y2)
        """
        x1, y1, x2, y2 = coords

        # Capture screenshot
        image = capture_region(x1, y1, x2, y2)

        if image is None:
            self.tray_icon.notify("Error", "Failed to capture screenshot")
            return

        # Copy to clipboard
        if not copy_image_to_clipboard(image):
            self.tray_icon.notify("Error", "Failed to copy to clipboard")
            return

        # Open Google Lens
        if open_google_lens():
            self.tray_icon.notify(
                "Screenshot Copied",
                "Press Ctrl+V in Google Lens to paste"
            )
        else:
            self.tray_icon.notify("Error", "Failed to open browser")


def main():
    """Main entry point."""
    app = SwiftClip()
    app.start()


if __name__ == "__main__":
    main()

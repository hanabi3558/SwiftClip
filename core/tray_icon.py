"""System tray icon module."""

import os
import sys
import threading
from typing import Callable, Optional

from PIL import Image, ImageDraw
import pystray


def get_icon_path() -> Optional[str]:
    """Get the path to icon.ico file."""
    # Check if running as frozen exe
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    icon_path = os.path.join(base_path, 'icon.ico')
    if os.path.exists(icon_path):
        return icon_path
    return None


def create_default_icon() -> Image.Image:
    """Create a simple default icon."""
    # Create a 64x64 image with a "T" letter
    size = 64
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw a rounded rectangle background
    draw.rounded_rectangle(
        [(4, 4), (size - 4, size - 4)],
        radius=8,
        fill=(70, 130, 180)  # Steel blue
    )

    # Draw "T" letter
    draw.text(
        (size // 2, size // 2),
        "T",
        fill=(255, 255, 255),
        anchor="mm"
    )

    return image


class TrayIcon:
    """System tray icon manager."""

    def __init__(
        self,
        on_quit: Optional[Callable[[], None]] = None
    ):
        """
        Initialize the tray icon.

        Args:
            on_quit: Callback when quit is selected
        """
        self._on_quit = on_quit
        self._icon: Optional[pystray.Icon] = None
        self._thread: Optional[threading.Thread] = None

    def _load_icon(self) -> Image.Image:
        """Load icon from file or create default."""
        icon_path = get_icon_path()
        if icon_path:
            try:
                img = Image.open(icon_path)
                # 確保轉換為 RGBA 模式以保留透明度
                img = img.convert('RGBA')
                # 調整到適合系統匣的尺寸 (32x32 或 64x64)
                target_size = 64
                if img.size[0] != target_size or img.size[1] != target_size:
                    img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
                return img
            except Exception:
                pass
        return create_default_icon()

    def start(self, hotkey: str) -> None:
        """Start the tray icon in a background thread."""
        menu = pystray.Menu(
            pystray.MenuItem(
                f"SwiftClip",
                lambda: None,
                enabled=False
            ),
            pystray.MenuItem(
                f"Hotkey: {hotkey.upper()}",
                lambda: None,
                enabled=False
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._quit)
        )

        self._icon = pystray.Icon(
            name="SwiftClip",
            icon=self._load_icon(),
            title="SwiftClip",
            menu=menu
        )

        self._thread = threading.Thread(target=self._icon.run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the tray icon."""
        if self._icon:
            self._icon.stop()
            self._icon = None

    def notify(self, title: str, message: str) -> None:
        """Show a notification from the tray icon."""
        if self._icon:
            self._icon.notify(message, title)

    def _quit(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Handle quit menu item."""
        self.stop()
        if self._on_quit:
            self._on_quit()

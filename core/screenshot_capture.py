"""Screenshot capture module using mss library."""

import ctypes
from io import BytesIO
from typing import Tuple, Optional

import mss
from PIL import Image


def set_dpi_awareness():
    """Set DPI awareness to avoid coordinate offset issues on Windows."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def capture_region(
    x1: int, y1: int, x2: int, y2: int
) -> Optional[Image.Image]:
    """
    Capture a specific region of the screen.

    Args:
        x1: Left coordinate
        y1: Top coordinate
        x2: Right coordinate
        y2: Bottom coordinate

    Returns:
        PIL Image object of the captured region, or None on failure
    """
    # Ensure coordinates are in correct order
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)

    # Calculate width and height
    width = right - left
    height = bottom - top

    if width <= 0 or height <= 0:
        return None

    try:
        with mss.mss() as sct:
            monitor = {
                "left": left,
                "top": top,
                "width": width,
                "height": height
            }
            screenshot = sct.grab(monitor)

            # Convert to PIL Image
            img = Image.frombytes(
                "RGB",
                (screenshot.width, screenshot.height),
                screenshot.rgb
            )
            return img
    except Exception as e:
        print(f"Screenshot capture failed: {e}")
        return None


def image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    """
    Convert PIL Image to bytes.

    Args:
        image: PIL Image object
        format: Image format (PNG, JPEG, etc.)

    Returns:
        Image data as bytes
    """
    buffer = BytesIO()
    image.save(buffer, format=format)
    buffer.seek(0)
    return buffer.getvalue()


def get_screen_size() -> Tuple[int, int]:
    """
    Get the total screen size (including all monitors).

    Returns:
        Tuple of (width, height)
    """
    with mss.mss() as sct:
        # monitors[0] is the "all monitors" virtual screen
        all_monitors = sct.monitors[0]
        return all_monitors["width"], all_monitors["height"]

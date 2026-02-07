"""Clipboard utilities for copying images."""

import io
from PIL import Image


def copy_image_to_clipboard(image: Image.Image) -> bool:
    """
    Copy a PIL Image to the Windows clipboard.

    Args:
        image: PIL Image object to copy

    Returns:
        True if successful, False otherwise
    """
    try:
        import win32clipboard
        from io import BytesIO

        # Convert to BMP format for clipboard
        output = BytesIO()

        # Convert to RGB if necessary (clipboard doesn't support alpha)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Save as BMP
        image.save(output, format='BMP')
        bmp_data = output.getvalue()[14:]  # Remove BMP file header (14 bytes)
        output.close()

        # Copy to clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
        win32clipboard.CloseClipboard()

        return True

    except ImportError:
        print("Error: pywin32 is required. Install with: pip install pywin32")
        return False
    except Exception as e:
        print(f"Failed to copy to clipboard: {e}")
        return False

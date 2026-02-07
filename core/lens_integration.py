"""Google Lens integration module."""

import webbrowser


GOOGLE_LENS_URL = "https://lens.google.com/"


def open_google_lens() -> bool:
    """
    Open Google Lens in browser.

    Returns:
        True if browser was opened successfully, False otherwise
    """
    try:
        # Try to open with Chrome specifically
        chrome_opened = _try_open_chrome(GOOGLE_LENS_URL)

        if not chrome_opened:
            # Fall back to default browser
            print("Chrome not found, opening in default browser...")
            webbrowser.open(GOOGLE_LENS_URL)

        return True

    except Exception as e:
        print(f"Failed to open Google Lens: {e}")
        return False


def _try_open_chrome(url: str) -> bool:
    """
    Try to open URL in Chrome browser.

    Args:
        url: URL to open

    Returns:
        True if Chrome was opened successfully, False otherwise
    """
    # Common Chrome paths on Windows
    chrome_paths = [
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]

    for chrome_path in chrome_paths:
        try:
            chrome = webbrowser.get(f'"{chrome_path}" %s')
            chrome.open(url)
            return True
        except webbrowser.Error:
            continue

    # Try registered Chrome browser
    try:
        chrome = webbrowser.get('chrome')
        chrome.open(url)
        return True
    except webbrowser.Error:
        pass

    # Try google-chrome (common alias)
    try:
        chrome = webbrowser.get('google-chrome')
        chrome.open(url)
        return True
    except webbrowser.Error:
        pass

    return False

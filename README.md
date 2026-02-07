# SwiftClip

A lightweight Windows tool that lets you select a screen region, capture it, and instantly open it in Google Lens for text recognition and translation.

## Features

- System tray application with hotkey support
- Screen region selection with overlay
- Automatically copies screenshot to clipboard
- Opens Google Lens for OCR and translation

## Usage

1. Run `SwiftClip.exe` (or `python main.py`)
2. The app appears in the system tray
3. Press `Ctrl+Shift+T` to select a screen region
4. Drag to select the area you want to translate
5. Google Lens opens — press `Ctrl+V` to paste the image

## Installation

### From source

```bash
pip install -r requirements.txt
python main.py
```

### Build executable

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name SwiftClip --icon=icon.ico --add-data "icon.ico;." main.py
```

The executable will be in the `dist/` folder.

## Requirements

- Windows 10/11
- Python 3.8+ (if running from source)

## License

MIT

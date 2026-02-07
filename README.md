<p align="center">
  <img src="app.png" alt="SwiftClip Icon" width="150">
</p>

<h1 align="center">SwiftClip</h1>

<p align="center"><strong>Redefining On-Screen Intelligence</strong></p>

SwiftClip is a cutting-edge productivity tool designed for users who value speed and precision. Taking inspiration from the agility of its namesake, the app allows you to capture any segment of your Windows screen and instantly initiate a deep search using advanced image recognition technology.

## Key Features

- **Intuitive Selection** — Effortlessly highlight images, text, or complex diagrams with a simple click-and-drag motion.
- **Seamless Integration** — Bridge the gap between your local desktop environment and the web's most powerful search engines.
- **Boosted Productivity** — Eliminate the tedious process of saving, uploading, and searching manually. Get the information you need in a fraction of the time.
- **Minimalist Interface** — A lightweight and elegant design that stays out of your way until the moment you need it.

Whether you are a researcher identifying complex components, a designer seeking visual references, or a student translating academic texts, SwiftClip transforms your screen into an interactive gateway of information.

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

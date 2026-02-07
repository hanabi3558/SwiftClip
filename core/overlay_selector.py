"""Transparent overlay for screen region selection."""

import tkinter as tk
from typing import Callable, Optional, Tuple


class OverlaySelector:
    """Full-screen transparent overlay for selecting screen regions."""

    def __init__(
        self,
        alpha: float = 0.3,
        selection_color: str = "#00FF00",
        border_width: int = 2
    ):
        """
        Initialize the overlay selector.

        Args:
            alpha: Overlay transparency (0.0-1.0)
            selection_color: Color of the selection rectangle
            border_width: Width of the selection rectangle border
        """
        self.alpha = alpha
        self.selection_color = selection_color
        self.border_width = border_width

        self.root: Optional[tk.Tk] = None
        self.canvas: Optional[tk.Canvas] = None
        self.selection_rect: Optional[int] = None

        self.start_x: int = 0
        self.start_y: int = 0
        self.end_x: int = 0
        self.end_y: int = 0

        self._callback: Optional[Callable[[Tuple[int, int, int, int]], None]] = None
        self._cancelled: bool = False

    def show(self, callback: Callable[[Tuple[int, int, int, int]], None]) -> None:
        """
        Show the overlay and wait for user selection.

        Args:
            callback: Function to call with selection coordinates (x1, y1, x2, y2)
                     Will be called with None if cancelled
        """
        self._callback = callback
        self._cancelled = False

        # Create main window
        self.root = tk.Tk()
        self.root.withdraw()  # Hide initially

        # Configure window
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.alpha)
        self.root.configure(cursor="cross")

        # Make window transparent on Windows
        self.root.attributes('-transparentcolor', '')

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=screen_width,
            height=screen_height,
            highlightthickness=0,
            bg='gray'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind events
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.root.bind("<Escape>", self._on_escape)
        self.root.bind("<Return>", self._on_confirm)

        # Show window
        self.root.deiconify()
        self.root.focus_force()

        # Run event loop
        self.root.mainloop()

    def _on_press(self, event: tk.Event) -> None:
        """Handle mouse press event."""
        self.start_x = event.x
        self.start_y = event.y
        self.end_x = event.x
        self.end_y = event.y

        # Create selection rectangle
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)

        self.selection_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y,
            outline=self.selection_color,
            width=self.border_width
        )

    def _on_drag(self, event: tk.Event) -> None:
        """Handle mouse drag event."""
        self.end_x = event.x
        self.end_y = event.y

        # Update selection rectangle
        if self.selection_rect:
            self.canvas.coords(
                self.selection_rect,
                self.start_x, self.start_y,
                self.end_x, self.end_y
            )

    def _on_release(self, event: tk.Event) -> None:
        """Handle mouse release event - automatically confirm selection."""
        self.end_x = event.x
        self.end_y = event.y

        # Only confirm if there's a valid selection area
        if abs(self.end_x - self.start_x) > 5 and abs(self.end_y - self.start_y) > 5:
            self._confirm_selection()

    def _on_escape(self, event: tk.Event) -> None:
        """Handle escape key - cancel selection."""
        self._cancelled = True
        self._close()
        if self._callback:
            self._callback(None)

    def _on_confirm(self, event: tk.Event) -> None:
        """Handle enter key - confirm selection."""
        self._confirm_selection()

    def _confirm_selection(self) -> None:
        """Confirm the current selection."""
        # Get absolute screen coordinates
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()

        # Calculate absolute coordinates
        x1 = root_x + min(self.start_x, self.end_x)
        y1 = root_y + min(self.start_y, self.end_y)
        x2 = root_x + max(self.start_x, self.end_x)
        y2 = root_y + max(self.start_y, self.end_y)

        self._close()

        if self._callback and not self._cancelled:
            self._callback((x1, y1, x2, y2))

    def _close(self) -> None:
        """Close the overlay window."""
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None


from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from gradient import create_gradient


class PrivacyOverlay(QWidget):

    def __init__(self, screen):
        super().__init__()

        self.screen = screen
        self.center = 50
        self.edge = 65
        self.corner = 75
        self.gradient_image = None

        # Configure a borderless overlay window
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.Tool
        )

        # Allow transparent pixels in the window
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        # Don't take focus from other apps
        self.setAttribute(
            Qt.WidgetAttribute.WA_ShowWithoutActivating
        )

        self.setGeometry(screen.geometry())
        self.rebuild()

    def rebuild(self):
        if self.width() < 1 or self.height() < 1:
            return

        self.gradient_image = create_gradient(
            self.width(),
            self.height(),
            self.center,
            self.edge,
            self.corner
        )
        self.update()

    def set_darkness(self, center, edge, corner):
        self.center = center
        self.edge = edge
        self.corner = corner
        self.rebuild()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.rebuild()

    def paintEvent(self, event):
        if self.gradient_image is None:
            return

        painter = QPainter(self)
        painter.drawImage(0, 0, self.gradient_image)
        painter.end()

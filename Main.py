
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QRadialGradient
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QSlider,
    QVBoxLayout,
    QWidget
)


# Class 1: Gradient preview
class GradientPreview(QWidget):

    def __init__(self):
        super().__init__()

        self.center = 50
        self.corner = 75

        self.setMinimumHeight(260)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        # Background for the preview
        painter.fillRect(
            self.rect(),
            QColor("#d7e5f5")
        )

        width = self.width()
        height = self.height()

        radius = (
            (width / 2) ** 2
            + (height / 2) ** 2
        ) ** 0.5

        gradient = QRadialGradient(
            width / 2,
            height / 2,
            radius
        )

        gradient.setColorAt(
            0,
            QColor(0, 0, 0, round(self.center * 2.55))
        )

        gradient.setColorAt(
            1,
            QColor(0, 0, 0, round(self.corner * 2.55))
        )

        painter.fillRect(self.rect(), gradient)
        painter.end()


# Class 2: Main application window
class PrivacyVeil(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PrivacyVeil")
        self.resize(520, 430)

        layout = QVBoxLayout(self)

        title = QLabel("PrivacyVeil - Gradient Preview")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.preview = GradientPreview()
        layout.addWidget(self.preview)

        # Center darkness slider
        self.center_label = QLabel(
            "Center darkness: 50%"
        )
        layout.addWidget(self.center_label)

        self.center_slider = QSlider(
            Qt.Orientation.Horizontal
        )
        self.center_slider.setRange(0, 85)
        self.center_slider.setValue(50)

        self.center_slider.valueChanged.connect(
            self.change_center
        )
        layout.addWidget(self.center_slider)

        # Corner darkness slider
        self.corner_label = QLabel(
            "Corner darkness: 75%"
        )
        layout.addWidget(self.corner_label)

        self.corner_slider = QSlider(
            Qt.Orientation.Horizontal
        )
        self.corner_slider.setRange(0, 95)
        self.corner_slider.setValue(75)

        self.corner_slider.valueChanged.connect(
            self.change_corner
        )
        layout.addWidget(self.corner_slider)

    def change_center(self, value):
        self.preview.center = value

        self.center_label.setText(
            f"Center darkness: {value}%"
        )

        self.preview.update()

    def change_corner(self, value):
        self.preview.corner = value

        self.corner_label.setText(
            f"Corner darkness: {value}%"
        )

        self.preview.update()


# Start the application
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = PrivacyVeil()
    window.show()

    sys.exit(app.exec())


import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
)

from overlay import PrivacyOverlay


class PrivacyVeil(QWidget):

    def __init__(self, app):
        super().__init__()

        self.overlay = PrivacyOverlay(app.primaryScreen())

        self.setWindowTitle("PrivacyVeil Settings")
        self.resize(420, 340)

        # Keep Settings accessible above the overlay
        self.setWindowFlag(
            Qt.WindowType.WindowStaysOnTopHint
        )

        layout = QVBoxLayout(self)

        title = QLabel("PrivacyVeil")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.center_slider = self.add_slider(
            layout, "Center", 50
        )

        self.edge_slider = self.add_slider(
            layout, "Edges", 65
        )

        self.corner_slider = self.add_slider(
            layout, "Corners", 75
        )

        buttons = QHBoxLayout()

        self.enable_button = QPushButton("Enable Film")
        self.enable_button.clicked.connect(self.toggle_film)

        buttons.addWidget(self.enable_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        buttons.addWidget(self.exit_button)

        layout.addLayout(buttons)

        self.status = QLabel("Privacy film is OFF")
        layout.addWidget(self.status)

        # The overlay starts disabled
        self.overlay.hide()

    def add_slider(self, layout, name, value):
        label = QLabel(f"{name}: {value}%")
        layout.addWidget(label)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 95)
        slider.setValue(value)

        slider.valueChanged.connect(
            lambda v: self.slider_changed(label, name, v)
        )

        layout.addWidget(slider)
        return slider

    def slider_changed(self, label, name, value):
        label.setText(f"{name}: {value}%")
        self.update_gradient()

    def update_gradient(self):
        center = self.center_slider.value()
        edge = self.edge_slider.value()
        corner = self.corner_slider.value()

        self.overlay.set_darkness(
            center, edge, corner
        )

    def toggle_film(self):
        if self.overlay.isVisible():
            self.overlay.hide()
            self.enable_button.setText("Enable Film")
            self.status.setText("Privacy film is OFF")
        else:
            self.update_gradient()
            self.overlay.show()

            self.enable_button.setText("Disable Film")
            self.status.setText("Privacy film is ON")

            self.raise_()
            self.activateWindow()

    def closeEvent(self, event):
        self.overlay.hide()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PrivacyVeil(app)
    window.show()

    sys.exit(app.exec())

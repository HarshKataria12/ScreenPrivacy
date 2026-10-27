
import numpy as np
from PySide6.QtGui import QImage


def create_gradient(width, height,
                    center=50, edge=65, corner=75):

    # Create horizontal and vertical coordinates
    x = np.linspace(-1, 1, width, dtype=np.float32)
    y = np.linspace(-1, 1, height, dtype=np.float32)

    xx, yy = np.meshgrid(np.abs(x), np.abs(y))

    # Measure distance toward edges and corners
    outer = np.maximum(xx, yy) ** 1.5
    diagonal = np.minimum(xx, yy) ** 1.5

    # Calculate opacity at every pixel
    alpha = (
        center
        + (edge - center) * outer
        + (corner - edge) * diagonal
    )

    alpha = np.clip(alpha, 0, 100)

    # Build a transparent RGBA image
    pixels = np.zeros((height, width, 4), dtype=np.uint8)
    pixels[:, :, 3] = np.rint(alpha * 2.55).astype(np.uint8)

    image = QImage(
        pixels.data,
        width,
        height,
        pixels.strides[0],
        QImage.Format.Format_RGBA8888
    )

    return image.copy()

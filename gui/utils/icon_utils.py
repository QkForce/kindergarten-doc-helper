from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt


def get_svg_pixmap(icon_path: str, color: str, size: int) -> QPixmap:
    try:
        with open(icon_path, "r", encoding="utf-8") as f:
            svg_data = f.read()

        # Color change (for Lucide icons)
        new_svg_data = svg_data.replace("currentColor", color)
        new_svg_data = new_svg_data.replace('stroke="#000"', f'stroke="{color}"')

        renderer = QSvgRenderer(new_svg_data.encode("utf-8"))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        if renderer.isValid():
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            renderer.render(painter)
            painter.end()
            return pixmap

    except Exception as e:
        print(f"Icon rendering error: {e}")

    return QPixmap()

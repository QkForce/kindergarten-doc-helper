from PySide6.QtWidgets import QWidget


def center_on_screen(widget: QWidget):
    # 1. Identify the screen where the widget is located
    screen = widget.screen()
    if not screen:
        return

    # 2. Get the available screen geometry (excluding taskbar)
    screen_geo = screen.availableGeometry()

    # 3. Get the widget's current geometry
    widget_geo = widget.geometry()

    # 4. Calculate coordinates
    x = screen_geo.left() + (screen_geo.width() - widget_geo.width()) // 2
    y = screen_geo.top() + (screen_geo.height() - widget_geo.height()) // 2

    # 5. Move the widget to the calculated position
    widget.move(x, y)

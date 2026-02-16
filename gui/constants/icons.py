from pathlib import Path

# The path to the main folder of the project (root)
ICON_DIR = Path(__file__).parent.parent / "resources" / "icons"


class IconPaths:
    # Hub page icons
    FEATURE_DOCX_GENERATOR = str(ICON_DIR / "file-plus.svg")
    FEATURE_TEMPLATE_FILLER = str(ICON_DIR / "file-pen.svg")
    FEATURE_ENTRY_XLSX = str(ICON_DIR / "table.svg")

    # For navigation
    BACK = str(ICON_DIR / "arrow_back.png")
    FORWARD = str(ICON_DIR / "arrow_forward.png")

    # Status icons
    SUCCESS = str(ICON_DIR / "check_circle.png")
    ERROR = str(ICON_DIR / "error.png")

    # Other icons
    DROP_DOWN = str(ICON_DIR / "arrow_drop_down.png")
    DROP_UP = str(ICON_DIR / "arrow_drop_up.png")

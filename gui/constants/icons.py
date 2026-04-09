from pathlib import Path

# The path to the main folder of the project (root)
ICON_DIR = Path(__file__).parent.parent / "resources" / "icons"
ANIM_DIR = Path(__file__).parent.parent / "resources" / "animations"


class IconPaths:
    # Hub page icons
    FEATURE_DOCX_GENERATOR = str(ICON_DIR / "file-plus.svg")
    FEATURE_TEMPLATE_FILLER = str(ICON_DIR / "file-pen.svg")
    FEATURE_ENTRY_XLSX = str(ICON_DIR / "table.svg")

    # For navigation
    BACK = str(ICON_DIR / "arrow_back.png")
    FORWARD = str(ICON_DIR / "arrow_forward.png")

    # Status icons
    SUCCESS = str(ICON_DIR / "circle-check.svg")
    EMPTY = str(ICON_DIR / "search-x.svg")
    ERROR = str(ICON_DIR / "circle-alert.svg")

    # Other icons
    HOUSE = str(ICON_DIR / "house.svg")
    SETTINGS = str(ICON_DIR / "settings.svg")
    CHEVRON_DOWN = str(ICON_DIR / "chevron-down.svg")
    CHEVRON_LEFT = str(ICON_DIR / "chevron-left.svg")
    CHEVRON_RIGHT = str(ICON_DIR / "chevron-right.svg")
    DROP_DOWN = str(ICON_DIR / "arrow_drop_down.png")
    DROP_UP = str(ICON_DIR / "arrow_drop_up.png")
    EXPAND = str(ICON_DIR / "maximize-2.svg")
    COLLAPSE = str(ICON_DIR / "minimize-2.svg")

    # Smart Entry icons
    ENTRY_COMPLETED = str(ICON_DIR / "circle-check-big.svg")
    ENTRY_PARTIAL = str(ICON_DIR / "circle-dashed.svg")


class AnimationPaths:
    LOADING = str(ANIM_DIR / "loading.gif")

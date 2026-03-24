class Palette:
    White = "#FFFFFF"

    Slate50 = "#F8FAFC"
    Slate100 = "#F0F2F5"
    Slate200 = "#E2E8F0"
    Slate300 = "#D1D5DB"
    Slate400 = "#94A3B8"
    Slate800 = "#1E293B"
    Slate900 = "#0F172A"

    Blue600 = "#2563EB"
    Blue700 = "#1D4ED8"

    Rose50 = "#FFF1F2"
    Rose100 = "#FFE4E6"
    Rose200 = "#FECDD3"
    Rose500 = "#FB7185"
    Rose600 = "#E11D48"

    Amber50 = "#FFFBEB"
    Amber100 = "#FDE68A"
    Amber200 = "#FDE68A"
    Amber500 = "#FBBF24"
    Amber600 = "#D97706"

    Emerald50 = "#F0FDF4"
    Emerald100 = "#D1FAE5"
    Emerald200 = "#BBF7D0"
    Emerald500 = "#34D399"
    Emerald600 = "#059669"


class AppColors:
    BG = Palette.Slate100  # Негізгі фон (slate-100)
    CANVAS = Palette.White  # Негізгі ақ парақ (white)
    PRIMARY = Palette.Blue600  # Негізгі көк түс (blue-600)
    PRIMARY_DARK = Palette.Blue700  # Күңгірт көк (blue-700)
    DARK = Palette.Slate900  # Domain тақырыптары (slate-900)
    TEXT_MAIN = Palette.Slate800  # Негізгі мәтін (slate-800)
    TEXT_MUTED = Palette.Slate400  # Көмекші мәтін (slate-400)
    BORDER = Palette.Slate200  # Жиектер (slate-200)
    SIDEBAR = Palette.Slate50  # Sidebar фоны (slate-50)
    ICON_MAIN = Palette.Slate800  # Негізгі икондар (slate-800)

    # Scoring colors
    SCORE_BTN_BASE_BG = Palette.Slate100
    SCORE_BTN_BASE_HOVER_BG = Palette.Slate50
    SCORE_BTN_BASE_TEXT = Palette.Slate400

    SCORE_BTN_DOMAIN_BG = Palette.Slate800
    SCORE_BTN_DOMAIN_HOVER_BG = Palette.Slate100
    SCORE_BTN_DOMAIN_TEXT = Palette.Slate400

    SCORE_HIGH_BG = Palette.Emerald500  # Emerald 500
    SCORE_MID_BG = Palette.Amber500  # Amber 500
    SCORE_LOW_BG = Palette.Rose500  # Rose 500

    SCORE_HIGH_TEXT = Palette.Emerald600
    SCORE_MID_TEXT = Palette.Amber600
    SCORE_LOW_TEXT = Palette.Rose600

    # Status colors
    SUCCESS = Palette.Emerald500  # Emerald 500
    WARNING = Palette.Amber500  # Amber 500
    ERROR = Palette.Rose500  # Red 500

    STATUS_TITLE = Palette.Slate800
    STATUS_DESC = Palette.Slate400

    # Button colors
    BTN_PRIMARY_BG = Palette.Slate900
    BTN_PRIMARY_HOVER = Palette.Blue700
    BTN_PRIMARY_PRESSED = Palette.Blue600

    BTN_GHOST_TEXT = Palette.Slate400
    BTN_GHOST_HOVER_TEXT = Palette.Slate800
    BTN_GHOST_PRESSED_TEXT = Palette.Slate900

    BTN_SUCCESS_BG = Palette.Emerald600
    BTN_SUCCESS_PRESSED = Palette.Emerald500

    BTN_DANGER_BG = Palette.Rose600
    BTN_DANGER_PRESSED = Palette.Rose500

    BTN_NEUTRAL_BG = Palette.Slate100
    BTN_NEUTRAL_BORDER = Palette.Slate300
    BTN_NEUTRAL_TEXT = Palette.Slate800
    BTN_NEUTRAL_PRESSED = Palette.Slate200

    BTN_DISABLED_BG = Palette.Slate100
    BTN_DISABLED_BORDER = Palette.Slate200
    BTN_DISABLED_TEXT = Palette.Slate400

    # Table colors
    HEADER_CELL_BACKGROUND = Palette.Slate50
    CELL_BACKGROUND_SELECTED = Palette.Slate200
    CELL_BORDER = Palette.Slate200
    CELL_TEXT = Palette.Slate800
    CELL_SELECTED_BG = Palette.Slate200

    # Table cell scoring colors
    SOFT_RED_BG = Palette.Rose50  # Өте ақшыл қызыл (Rose 50)
    SOFT_RED_BORDER = Palette.Rose200  # Rose 200
    SOFT_YELLOW_BG = Palette.Amber50  # Өте ақшыл сары (Amber 50)
    SOFT_YELLOW_BORDER = Palette.Amber200  # Amber 200
    SOFT_GREEN_BG = Palette.Emerald50  # Өте ақшыл жасыл (Emerald 50)
    SOFT_GREEN_BORDER = Palette.Emerald200  # Emerald 200

    # Scrollbar colors
    SCROLLBAR_TRACK = Palette.Slate50
    SCROLLBAR_HANDLE = Palette.Slate300
    SCROLLBAR_HOVER_HANDLE = Palette.Slate400

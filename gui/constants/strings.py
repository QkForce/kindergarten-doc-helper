class AppStrings:
    # App General
    APP_NAME = "KinderDoc Helper"
    WARNING_TITLE = "Ескерту"

    # Hub Page Strings
    HUB_TITLE = "Жұмыс кеңістігі"
    HUB_SUBTITLE = "Қажетті құралды таңдап, құжаттарды дайындаңыз"

    # Feature Cards
    CARD_GEN_TITLE = "Document Generator"
    CARD_GEN_DESC = "Build DOCX files from scratch using XLSX source data."

    CARD_TPL_TITLE = "Template Filler"
    CARD_TPL_DESC = "Auto-fill existing Word templates with Excel variables."

    CARD_ENTRY_TITLE = "Smart Entry"
    CARD_ENTRY_DESC = "Create student data tables with an intuitive grid."

    CARD_MONFORM_TITLE = "Monitoring Formatter"
    CARD_MONFORM_DESC = (
        "Excel кестесінің стильдерін және формулаларын автоматты түрде ретке келтіру."
    )

    CARD_GROWFORM_TITLE = "Grow Card Formatter"
    CARD_GROWFORM_DESC = (
        "Даму картасы файлының стильдерін автоматты түрде ретке келтіру."
    )

    LOADING_CHILDREN_SCORES_TITLE = "Балалардың бағалары жүктелуде..."
    LOADING_CHILDREN_SCORES_DESC = "Файлдағы балалардың бағалары оқылуда. Күте тұрыңыз."

    EMPTY_CHILDREN_SCORES_TITLE = "Балалардың бағалары табылмады"
    EMPTY_CHILDREN_SCORES_DESC = (
        "• Файлда балалардың бағалары бар екеніне көз жеткізіңіз<br>"
        "• Немесе файлдағы деректердің дұрыстығына көз жеткізіңіз"
    )

    ASSESSMENT_WARNING_TITLE = "Ескерту"
    ASSESSMENT_WARNING_DESC_EMPTY_CHILD_LIST = (
        "Балалардың тізімі бос. "
        "Құжатты дайындау үшін тізімде кемінде бір бала болуы керек."
    )
    ASSESSMENT_WARNING_DESC_INCOMPLETED = (
        "Балалардың бағалары толық қойылмаған. "
        "Құжатты дайындау үшін барлық бағаларды қою керек."
    )

    ERROR_CHILDREN_SCORES_TITLE = "Балалардың бағаларын жүктеу кезінде қате"
    ERROR_CHILDREN_SCORES_DESC = "Автоматты жүктеу кезінде қате: {}"

    MONFORM_NO_ACTION_SELECTED = "Кем дегенде бір әрекетті таңдаңыз."

    EXPORT_BTN_LBL_SAVE_FILE = "Нәтижені жүктеу (сақтау)"
    EXPORT_DIALOG_TITLE_ASK_FILE_PATH = "Құжатты қайда сақтау керек?"
    EXPORT_SUCCESS_TITLE_SAVE_FILE = "Сақтау сәтті аяқталды!"
    EXPORT_SUCCESS_DESC_SAVE_FILE = "Құжат сақталды: {}"
    EXPORT_ERROR_TITLE = "Қате!"
    EXPORT_ERROR_DESC = "Экспорт кезінде қате: {}"
    EXPORT_WARNING_TITLE = "Ескерту"
    EXPORT_WARNING_DESC_NOT_PROCESSED_RESULT_FILE = "Құжатты дайындау керек!"


GENERATOR_OPTIONS = [
    {
        "title": "Файлды таңдау",
        "desc": "Excel файлын таңдаңыз, өңделетін парақты (лист) және топты көрсетіңіз.",
    },
    {
        "title": "Балалардың бағаларын жүктеу",
        "desc": "Төмендегі тізімнен деректердің дұрыстығын растаңыз.",
    },
    {
        "title": "Үлгі файлды (docx) таңдау",
        "desc": "Генерациялау үлгісін (шаблон) таңдап, генерацияланған нәтижені сақтаңыз.",
    },
    {
        "title": "Құжатты дайындау",
        "desc": "Егер құжат сәтті дайындалса, онда нәтижені керекті орынға жүктеңіз.",
    },
]


FILLER_OPTIONS = [
    {
        "title": "Файлды таңдау",
        "desc": "Excel файлын таңдаңыз, өңделетін парақты (лист) және топты көрсетіңіз.",
    },
    {
        "title": "Балалардың бағаларын жүктеу",
        "desc": "Төмендегі тізімнен деректердің дұрыстығын растаңыз.",
    },
    {
        "title": "Құжатты толтыру",
        "desc": "Шаблонды таңдап, бақылау түрін көрсетіңіз.",
    },
    {
        "title": "Құжатты дайындау",
        "desc": "Егер құжат сәтті дайындалса, онда нәтижені керекті орынға жүктеңіз.",
    },
]


SMART_ENTRY_OPTIONS = [
    {
        "title": "Файлды таңдау",
        "desc": "Excel файлын таңдаңыз, өңделетін парақты (лист) және топты көрсетіңіз.",
    },
    {
        "title": "Балаларды бағалау",
        "desc": "Балаларға бағаларын қойыңыз.",
    },
    {
        "title": "Құжатты дайындау",
        "desc": "Егер құжат сәтті дайындалса, онда нәтижені керекті орынға жүктеңіз.",
    },
]


MONITORING_FORMATTER_OPTIONS = [
    {
        "title": "Файлды таңдау",
        "desc": "Excel файлын таңдаңыз, өңделетін парақты (лист) және топты көрсетіңіз.",
    },
    {
        "title": "Әрекеттер",
        "desc": "Мониторинг файлына қолданылуы керек әрекеттерді таңдаңыз.",
    },
    {
        "title": "Құжатты дайындау",
        "desc": "Егер құжат сәтті дайындалса, онда нәтижені керекті орынға жүктеңіз.",
    },
]

GROW_CARD_FORMATTER_OPTIONS = [
    {
        "title": "Файлды таңдау",
        "desc": "Даму картасы файлын таңдаңыз.",
    },
    {
        "title": "Әрекеттер",
        "desc": "Даму картасы файлына қолданылуы керек әрекеттерді таңдаңыз.",
    },
    {
        "title": "Құжатты дайындау",
        "desc": "Егер құжат сәтті дайындалса, онда нәтижені керекті орынға жүктеңіз.",
    },
]

MONFORM_CHECKBOXES = [
    {
        "id": "fix_borders",
        "title": "Кесте жиектерін форматтау (жуан/жіңішке сызықтар)",
        "default": True,
    },
    {
        "id": "fix_typography",
        "title": "Парақ қаріптерін реттеу",
        "default": True,
    },
    {
        "id": "round_numbers",
        "title": "Бөлшек сандарды бүтінге айналдыру",
        "default": True,
    },
    {
        "id": "sync_formulas_with_student_count",
        "title": "Формулаларды кестедегі балалардың санына сәйкестендіру",
        "default": True,
    },
    {
        "id": "remove_empty_spaces",
        "title": "Бос жолдар мен бағандарды орындарды жою",
        "default": False,
    },
]

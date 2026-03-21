from gui.types import AgeGroup, Domain, Subject


class AppStrings:
    # App General
    APP_NAME = "KinderDoc Helper"

    # Hub Page Strings
    HUB_TITLE = "KinderDoc Helper"
    HUB_SUBTITLE = "Select a tool to get started with your documents"

    # Feature Cards
    CARD_GEN_TITLE = "Document Generator"
    CARD_GEN_DESC = "Build DOCX files from scratch using XLSX source data."

    CARD_TPL_TITLE = "Template Filler"
    CARD_TPL_DESC = "Auto-fill existing Word templates with Excel variables."

    CARD_ENTRY_TITLE = "Smart Entry"
    CARD_ENTRY_DESC = "Create student data tables with an intuitive grid."

    LOADING_CHILDREN_SCORES_TITLE = "Балалардың бағалары жүктелуде..."
    LOADING_CHILDREN_SCORES_DESC = "Файлдағы балалардың бағалары оқылуда. Күте тұрыңыз."

    EMPTY_CHILDREN_SCORES_TITLE = "Балалардың бағалары табылмады"
    EMPTY_CHILDREN_SCORES_DESC = (
        "• Файлда балалардың бағалары бар екеніне көз жеткізіңіз<br>"
        "• Немесе файлдағы деректердің дұрыстығына көз жеткізіңіз"
    )

    ERROR_CHILDREN_SCORES_TITLE = "Балалардың бағаларын жүктеу кезінде қате"
    ERROR_CHILDREN_SCORES_DESC = "Автоматты жүктеу кезінде қате: {}"

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
        "title": "Кезең 1 / 4: Файлды таңдау",
        "desc": "Excel файлын таңдаңыз, өңделетін парақты (лист) және топты көрсетіңіз.",
    },
    {
        "title": "Кезең 2 / 4: Балалардың бағаларын жүктеу",
        "desc": "Төмендегі тізімнен деректердің дұрыстығын растаңыз.",
    },
    {
        "title": "Кезең 3 / 4: Үлгі файлды (docx) таңдау",
        "desc": "Генерациялау үлгісін (шаблон) таңдап, генерацияланған нәтижені сақтаңыз.",
    },
    {
        "title": "Кезең 4 / 4: Құжатты дайындау",
        "desc": "Егер құжат сәтті дайындалса, онда нәтижені керекті орынға жүктеңіз.",
    },
]


FILLER_OPTIONS = [
    {
        "title": "Кезең 1 / 4: Файлды таңдау",
        "desc": "Excel файлын таңдаңыз, өңделетін парақты (лист) және топты көрсетіңіз.",
    },
    {
        "title": "Кезең 2 / 4: Балалардың бағаларын жүктеу",
        "desc": "Төмендегі тізімнен деректердің дұрыстығын растаңыз.",
    },
    {
        "title": "Кезең 3 / 4: Құжатты толтыру",
        "desc": "Шаблонды таңдап, бақылау түрін көрсетіңіз.",
    },
    {
        "title": "Кезең 4 / 4: Құжатты дайындау",
        "desc": "Егер құжат сәтті дайындалса, онда нәтижені керекті орынға жүктеңіз.",
    },
]


SMART_ENTRY_OPTIONS = [
    {
        "title": "Кезең 1 / 3: Файлды таңдау",
        "desc": "Excel файлын таңдаңыз, өңделетін парақты (лист) және топты көрсетіңіз.",
    },
    {
        "title": "Кезең 2 / 3: Балаларды бағалау",
        "desc": "Балаларға бағаларын қойыңыз.",
    },
    {
        "title": "Кезең 3 / 3: Құжатты дайындау",
        "desc": "Егер құжат сәтті дайындалса, онда нәтижені керекті орынға жүктеңіз.",
    },
]


AGE_GROUPS = {
    AgeGroup.EARLY_AGE.value: "Бөбек (ерте жас)",
    AgeGroup.JUNIOR.value: "Кіші топ",
    AgeGroup.MIDDLE.value: "Ортаңғы топ",
    AgeGroup.SENIOR.value: "Ересек топ",
    AgeGroup.PRESCHOOL.value: "Мектепке даярлық тобы",
}

DOMAIN_NAMES = {
    Domain.PHYSICAL.value: "Физикалық қасиеттерді дамыту",
    Domain.COMMUNICATIVE.value: "Коммуникативтік дағдыларды дамыту",
    Domain.COGNITIVE.value: "Танымдық және зияткерлік дағдыларды дамыту",
    Domain.CREATIVITY.value: "Шығармашылық дағдыларын, зерттеу іс-әрекетін дамыту",
    Domain.SOCIAL.value: "Әлеуметтік-эмоционалды дағдыларды қалыптастыру",
}

SUBJECT_NAMES = {
    Subject.PHYS_ED.value: "Дене тәрбиесі",
    Subject.LANG_DEV.value: "Тіл дамыту",
    Subject.LITERATURE.value: "Көркем әдебиет",
    Subject.SENSORY.value: "Сенсорика",
    Subject.MODELING.value: "Мүсіндеу",
    Subject.MUSIC.value: "Музыка",
    Subject.WORLD_VIEW.value: "Қоршаған әлеммен танысу",
    Subject.DRAWING.value: "Сурет салу",
    Subject.APPLI.value: "Жапсыру",
    Subject.CONSTRUCT.value: "Құрастыру",
    Subject.KAZ_LANG.value: "Қазақ тілі",
    Subject.MATH.value: "Математика",
    Subject.LITERACY.value: "Сауат ашу негіздері",
    Subject.SPEECH_IMMERSION.value: "Тілге бойлау",
}

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

    class GENERATOR:
        STEP_1_TITLE = "Кезең 1 / 3: Файлды таңдау"
        STEP_1_DESC = (
            "Excel файлын таңдаңыз, өңделетін парақты (лист) және топты көрсетіңіз."
        )

        STEP_2_TITLE = "Кезең 2 / 3: Балалардың бағаларын жүктеу"
        STEP_2_DESC = "Төмендегі тізімнен деректердің дұрыстығын растаңыз."

        STEP_3_TITLE = "Кезең 3 / 3: Құжатты дайындау"
        STEP_3_DESC = "Дайын шаблонды таңдап, нәтижені сақтаңыз."

    class FILLER:
        STEP_3_TITLE = "Кезең 3 / 3: Құжатты толтыру"
        STEP_3_DESC = "Шаблонды таңдап, бақылау түрін көрсетіңіз."

    class SMART_ENTRY:
        STEP_2_TITLE = "Кезең 2 / 3: Балаларды бағалау"
        STEP_2_DESC = "Балаларға бағаларын қойыңыз."


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

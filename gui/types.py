from enum import Enum


class AgeGroup(Enum):
    EARLY_AGE = "early_age"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    PRESCHOOL = "preschool"


class Domain(Enum):
    PHYSICAL = "physical"
    COMMUNICATIVE = "communicative"
    COGNITIVE = "cognitive"
    CREATIVITY = "creativity"
    SOCIAL = "social"


class Subject(Enum):
    PHYS_ED = "phys_ed"
    LANG_DEV = "lang_dev"
    LITERATURE = "literature"
    SENSORY = "sensory"
    MODELING = "modeling"
    MUSIC = "music"
    WORLD_VIEW = "world_view"
    DRAWING = "drawing"
    APPLI = "appli"
    CONSTRUCT = "construct"
    KAZ_LANG = "kaz_lang"
    MATH = "math"
    LITERACY = "literacy"
    SPEECH_IMMERSION = "speech_immersion"

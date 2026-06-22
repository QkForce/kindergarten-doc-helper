import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env.test"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


@dataclass(frozen=True)
class TestConfig:
    window_min_width: int = int(os.getenv("TEST_WINDOW_MIN_WIDTH", 800))
    window_min_height: int = int(os.getenv("TEST_WINDOW_MIN_HEIGHT", 600))
    out_dir: Path = Path("output")
    out_file_name: str = "file_name"


@dataclass(frozen=True)
class DocxGenConfig(TestConfig):
    xlsx_path: Path = Path(os.getenv("TEST_UIE2E_DOCXGEN_XLSX_PATH", ""))
    sheet_idx: int = int(os.getenv("TEST_UIE2E_DOCXGEN_SHEET_IDX", 0))
    group_idx: int = int(os.getenv("TEST_UIE2E_DOCXGEN_AGEGROUP_IDX", 0))
    temp_path: Path = Path(os.getenv("TEST_UIE2E_DOCXGEN_TEMP_PATH", ""))
    out_file_name: str = os.getenv(
        "TEST_UIE2E_DOCXGEN_RES_FILE_NAME", "test_res_docxgen.docx"
    )


@dataclass(frozen=True)
class FillerConfig(TestConfig):
    xlsx_path: Path = Path(os.getenv("TEST_UIE2E_FILLER_XLSX_PATH", ""))
    sheet_idx: int = int(os.getenv("TEST_UIE2E_FILLER_SHEET_IDX", 0))
    group_idx: int = int(os.getenv("TEST_UIE2E_FILLER_AGEGROUP_IDX", 0))
    temp_path: Path = Path(os.getenv("TEST_UIE2E_FILLER_TEMP_PATH", ""))
    control_type_idx: int = int(os.getenv("TEST_UIE2E_FILLER_CONTROLTYPE_IDX", 0))
    out_file_name: str = os.getenv(
        "TEST_UIE2E_FILLER_RES_FILE_NAME", "test_res_filler.docx"
    )


@dataclass(frozen=True)
class SmartEntryConfig(TestConfig):
    xlsx_path: Path = Path(os.getenv("TEST_UIE2E_SMART_ENTRY_XLSX_PATH", ""))
    sheet_idx: int = int(os.getenv("TEST_UIE2E_SMART_ENTRY_SHEET_IDX", 0))
    group_idx: int = int(os.getenv("TEST_UIE2E_SMART_ENTRY_AGEGROUP_IDX", 0))
    out_file_name: str = os.getenv(
        "TEST_UIE2E_SMART_ENTRY_RES_FILE_NAME", "test_res_smart_entry.xlsx"
    )


@dataclass(frozen=True)
class MonFormConfig(TestConfig):
    xlsx_path: Path = Path(os.getenv("TEST_UIE2E_MONFORM_XLSX_PATH", ""))
    sheet_idx: int = int(os.getenv("TEST_UIE2E_MONFORM_SHEET_IDX", 0))
    group_idx: int = int(os.getenv("TEST_UIE2E_MONFORM_AGEGROUP_IDX", 0))
    out_file_name: str = os.getenv(
        "TEST_UIE2E_MONFORM_RES_FILE_NAME", "test_res_monform.xlsx"
    )


@dataclass(frozen=True)
class GrowFormConfig(TestConfig):
    grow_card_path: Path = Path(os.getenv("TEST_UIE2E_GROWFORM_GROW_CARD_PATH", ""))
    out_file_name: str = os.getenv(
        "TEST_UIE2E_GROWFORM_RES_FILE_NAME", "test_res_monform.docx"
    )


docx_gen_cfg = DocxGenConfig()
filler_cfg = FillerConfig()
smart_entry_cfg = SmartEntryConfig()
monform_cfg = MonFormConfig()
growform_cfg = GrowFormConfig()

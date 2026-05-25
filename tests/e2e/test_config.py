import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env.test"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


@dataclass(frozen=True)
class DocxGenConfig:
    xlsx_path: Path = Path(os.getenv("TEST_UIE2E_DOCXGEN_XLSX_PATH", ""))
    temp_path: Path = Path(os.getenv("TEST_UIE2E_DOCXGEN_TEMP_PATH", ""))
    sheet_idx: int = int(os.getenv("TEST_UIE2E_DOCXGEN_SHEET_IDX", 0))
    group_idx: int = int(os.getenv("TEST_UIE2E_DOCXGEN_AGEGROUP_IDX", 0))


@dataclass(frozen=True)
class SmartEntryConfig:
    input_xlsx: Path = Path(os.getenv("TEST_UIE2E_SMART_ENTRY_INPUT", ""))
    target_dir: Path = Path(os.getenv("TEST_UIE2E_SMART_ENTRY_TARGET_DIR", ""))


docx_gen_cfg = DocxGenConfig()
smart_entry_cfg = SmartEntryConfig()

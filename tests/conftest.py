import os
import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    test_env_path = os.path.join(base_dir, ".env.test")

    if os.path.exists(test_env_path):
        load_dotenv(test_env_path)
    else:
        os.environ.setdefault(
            "TEST_UIE2E_DOCXGEN_XLSX_PATH", "data/test.monitoring.generator.xlsx"
        )
        os.environ.setdefault("TEST_UIE2E_DOCXGEN_SHEET_IDX", 0)
        os.environ.setdefault("TEST_UIE2E_DOCXGEN_TEMP_PATH", "data/template.docx")

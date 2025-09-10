import json
import logging
from typing import List, Dict

from src.settings import settings

logger = logging.getLogger(__name__)

DATA_DIR = settings.json_data.data_dir
DRUGS_FILE = settings.json_data.drugs_file_name
SEIZURE_DRUG_MAP_FILE = settings.json_data.seizure_drug_map_file_name
MODIFIER_RULES_FILE = settings.json_data.modifier_rules_file_name


def get_drugs() -> Dict[str, dict]:
    try:
        with open(DATA_DIR / DRUGS_FILE, encoding="utf-8") as f:
            _DRUGS: Dict[str, dict] = json.load(f)
        return _DRUGS
    except Exception as e:
        logger.exception("Failed to read file %r", DRUGS_FILE, exc_info=e)
        return {}


def get_seizure_map() -> Dict[str, Dict[int, List[str]]]:
    try:
        with open(DATA_DIR / SEIZURE_DRUG_MAP_FILE) as f:
            _SEIZURE_MAP: Dict[str, Dict[int, List[str]]] = {
                k: {int(tier): drugs for tier, drugs in v.items()}
                for k, v in json.load(f).items()
            }
        return _SEIZURE_MAP
    except Exception as e:
        logger.exception("Failed to read file %r", SEIZURE_DRUG_MAP_FILE, exc_info=e)
        return {}


def get_modifier_rules() -> Dict[str, List[dict]]:
    try:
        with open(DATA_DIR / MODIFIER_RULES_FILE) as f:
            _MODIFIER_RULES: Dict[str, List[dict]] = json.load(f)
        return _MODIFIER_RULES
    except Exception as e:
        logger.exception("Failed to read file %r", MODIFIER_RULES_FILE, exc_info=e)
        return {}

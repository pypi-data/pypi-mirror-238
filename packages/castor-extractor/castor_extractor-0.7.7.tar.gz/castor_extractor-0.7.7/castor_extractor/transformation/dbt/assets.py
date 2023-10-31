from enum import Enum


class DbtAsset(Enum):
    """dbt assets"""

    MANIFEST = "manifest"
    RUN_RESULTS = "run_results"

from enum import Enum


class SigmaAsset(Enum):
    """Sigma assets"""

    DATASETS = "datasets"
    ELEMENTS = "elements"
    FILES = "files"
    LINEAGES = "lineages"
    MEMBERS = "members"
    QUERIES = "queries"
    WORKBOOKS = "workbooks"

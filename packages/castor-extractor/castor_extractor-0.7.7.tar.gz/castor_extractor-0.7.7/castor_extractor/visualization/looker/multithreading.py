import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List, Set

from tqdm import tqdm  # type: ignore

from ...utils import RetryStrategy, retry
from . import ApiClient
from .api.sdk import Folder, SDKError
from .assets import LookerAsset

logger = logging.getLogger(__name__)

LOOKER_EXCEPTIONS = (SDKError,)
RETRY_COUNT = 2
RETRY_BASE_MS = 1
RETRY_JITTER_MS = 1
RETRY_STRATEGY = RetryStrategy.LINEAR


@retry(
    exceptions=LOOKER_EXCEPTIONS,
    count=RETRY_COUNT,
    base_ms=RETRY_BASE_MS,
    jitter_ms=RETRY_JITTER_MS,
    strategy=RETRY_STRATEGY,
)
def _make_api_request(
    client: ApiClient,
    asset: LookerAsset,
    folder_id: str,
) -> List:
    """
    Calls the appropriate Looker API endpoint to retrieve either Looks or
    Dashboards withered by the given folder ID.
    """
    if asset == LookerAsset.LOOKS:
        return client.looks(folder_id=folder_id)
    return client.dashboards(folder_id=folder_id)


def fetch_assets_with_parallelization(
    folder_ids: Set[str],
    client: ApiClient,
    asset: LookerAsset,
    thread_pool_size: int,
) -> List:
    """
    Fetches Looks or Dashboards with a request per folder ID. Requests are
    parallelised.
    """
    final_assets = []
    total_folders = len(folder_ids)
    _fetch = partial(_make_api_request, client, asset)

    with ThreadPoolExecutor(max_workers=thread_pool_size) as executor:
        fetch_results = executor.map(_fetch, folder_ids)

        for result in tqdm(fetch_results, total=total_folders):
            final_assets.extend(result)

    logger.info(f"Fetched {len(final_assets)} {asset.value}")
    return final_assets

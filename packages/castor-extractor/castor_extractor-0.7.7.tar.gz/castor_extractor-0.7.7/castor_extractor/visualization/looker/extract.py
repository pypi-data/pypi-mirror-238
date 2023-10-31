import logging
from typing import Iterable, Optional, Set, Tuple

from ...logger import add_logging_file_handler
from ...utils import (
    SafeMode,
    current_timestamp,
    deep_serialize,
    get_output_filename,
    write_json,
    write_summary,
)
from .api import ApiClient, Credentials, explore_names_associated_to_dashboards
from .assets import LookerAsset
from .multithreading import fetch_assets_with_parallelization
from .parameters import get_parameters

logger = logging.getLogger(__name__)


def _safe_mode(directory: str) -> SafeMode:
    add_logging_file_handler(directory)
    return SafeMode((Exception,), float("inf"))


def _client(
    base_url: str,
    client_id: str,
    client_secret: str,
    timeout: Optional[int],
    safe_mode: Optional[SafeMode],
) -> ApiClient:
    credentials = Credentials(
        base_url=base_url,
        client_id=client_id,
        client_secret=client_secret,
        timeout=timeout,
    )
    return ApiClient(credentials=credentials, safe_mode=safe_mode)


def iterate_all_data(
    client: ApiClient,
    all_looks: bool,
    search_per_folder: bool,
    thread_pool_size: int,
) -> Iterable[Tuple[LookerAsset, list]]:
    """Iterate over the extracted Data From looker"""

    logger.info("Extracting users from Looker API")
    users = client.users()
    yield LookerAsset.USERS, deep_serialize(users)

    logger.info("Extracting folders from Looker API")
    folders = client.folders()
    folder_ids: Set[str] = {folder.id for folder in folders if folder.id}
    yield LookerAsset.FOLDERS, deep_serialize(folders)

    logger.info("Extracting looks from Looker API")
    if search_per_folder:
        looks = fetch_assets_with_parallelization(
            folder_ids=folder_ids,
            client=client,
            asset=LookerAsset.LOOKS,
            thread_pool_size=thread_pool_size,
        )
    else:
        looks = client.looks(all_looks)
    yield LookerAsset.LOOKS, deep_serialize(looks)
    del looks

    logger.info("Extracting dashboards from Looker API")
    if search_per_folder:
        dashboards = fetch_assets_with_parallelization(
            folder_ids=folder_ids,
            client=client,
            asset=LookerAsset.DASHBOARDS,
            thread_pool_size=thread_pool_size,
        )
    else:
        dashboards = client.dashboards()
    yield LookerAsset.DASHBOARDS, deep_serialize(dashboards)

    logger.info("Extracting lookml models from Looker API")
    lookmls = client.lookml_models()
    yield LookerAsset.LOOKML_MODELS, deep_serialize(lookmls)

    logger.info("Extracting explores from Looker API")
    explore_names = explore_names_associated_to_dashboards(lookmls, dashboards)
    yield LookerAsset.EXPLORES, deep_serialize(client.explores(explore_names))
    del lookmls
    del dashboards

    logger.info("Extracting connections from Looker API")
    yield LookerAsset.CONNECTIONS, deep_serialize(client.connections())

    logger.info("Extracting projects from Looker API")
    yield LookerAsset.PROJECTS, deep_serialize(client.projects())

    logger.info("Extracting groups hierarchy from Looker API")
    groups_hierarchy = client.groups_hierarchy()
    yield LookerAsset.GROUPS_HIERARCHY, deep_serialize(groups_hierarchy)

    logger.info("Extracting groups roles from Looker API")
    yield LookerAsset.GROUPS_ROLES, deep_serialize(client.groups_roles())

    logger.info("Extracting content views from Looker API")
    yield LookerAsset.CONTENT_VIEWS, deep_serialize(client.content_views())

    logger.info("Extracting users attributes from Looker API")
    users_attributes = client.users_attributes()
    yield LookerAsset.USERS_ATTRIBUTES, deep_serialize(users_attributes)


def extract_all(**kwargs) -> None:
    """
    Extract Data From looker and store it locally in files under the
    output_directory
    """
    parameters = get_parameters(**kwargs)
    output_directory = parameters.output_directory
    base_url = parameters.base_url

    is_safe_mode = parameters.is_safe_mode
    safe_mode = _safe_mode(output_directory) if is_safe_mode else None
    client = _client(
        base_url=base_url,
        client_id=parameters.client_id,
        client_secret=parameters.client_secret,
        timeout=parameters.timeout,
        safe_mode=safe_mode,
    )

    ts = current_timestamp()

    data = iterate_all_data(
        client=client,
        all_looks=parameters.all_looks,
        search_per_folder=parameters.search_per_folder,
        thread_pool_size=parameters.thread_pool_size,
    )
    for key, data in data:
        filename = get_output_filename(key.value, output_directory, ts)
        write_json(filename, data)

    write_summary(output_directory, ts, base_url=base_url)

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, Optional, Set, Tuple

import requests
from dateutil.parser import parse

from .credentials import CredentialsKey, DbtCredentials, get_value

logger = logging.getLogger(__name__)

_CLOUD_URL = "https://cloud.getdbt.com/api/v2/accounts"
_DATA_KEY = "data"
_SUCCESSFUL_RUN_STATUS = 10
_DELETED_JOB_STATE = 2

Artifact = Literal["manifest.json", "run_results.json"]


class ContentType(Enum):
    JSON = "application/json"
    TEXT = "text/html"


@dataclass(frozen=True)
class DbtRun:
    id: int
    finished_at: datetime


def _is_deleted(job: dict) -> bool:
    return job["state"] == _DELETED_JOB_STATE


class DbtClient:
    """
    Connect to dbt-cloud Administrative API and downloads manifest.
    https://docs.getdbt.com/docs/dbt-cloud-apis/admin-cloud-api
    """

    def __init__(self, **kwargs):
        self._credentials = DbtCredentials(
            token=get_value(CredentialsKey.TOKEN, kwargs),
            job_id=get_value(CredentialsKey.JOB_ID, kwargs),
        )
        self._session = requests.Session()
        self._account_id: int = self._infer_account_id()

    def _headers(self, content_type: ContentType) -> dict:
        return {
            "Accept": content_type.value,
            "Authorization": "Token " + self._credentials.token,
        }

    def _call(
        self,
        url: str,
        params: Optional[dict] = None,
        content_type: ContentType = ContentType.JSON,
    ) -> dict:
        headers = self._headers(content_type)
        response = self._session.get(
            url=url,
            headers=headers,
            params=params,
        )
        try:
            result = response.json()
        except:
            context = f"{url}, status {response.status_code}"
            raise ValueError(f"Couldn't extract data from {context}")
        else:
            if content_type == ContentType.JSON:
                return result[_DATA_KEY]
            return result

    def _infer_account_id(self) -> int:
        result = self._call(url=_CLOUD_URL)
        return result[0]["id"]

    def list_job_identifiers(self) -> Set[int]:
        """
        Return the IDs of all non-deleted jobs for this account
        https://docs.getdbt.com/dbt-cloud/api-v2-legacy#tag/Jobs/operation/listJobsForAccount
        """
        url = f"{_CLOUD_URL}/{self._account_id}/jobs/"
        jobs = self._call(url)
        return {job["id"] for job in jobs if not _is_deleted(job)}

    def last_run(
        self,
        job_id: Optional[int] = None,
        finished_at_range: Optional[Tuple[datetime, datetime]] = None,
    ) -> Optional[DbtRun]:
        """
        Extract the last successful run id, optionally filtered on a given datetime range
        https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/listRunsForAccount
        """
        url = f"{_CLOUD_URL}/{self._account_id}/runs/"

        params = {
            "job_definition_id": job_id or self._credentials.job_id,
            "order_by": "-finished_at",
            "status": _SUCCESSFUL_RUN_STATUS,
            "limit": 1,
        }

        if finished_at_range:
            # https://github.com/dbt-labs/dbt-cloud-openapi-spec/issues/33
            params["finished_at__range"] = json.dumps(
                [d.isoformat() for d in finished_at_range]
            )

        data = self._call(url, params)
        if not data:
            return None

        if not data[0]:
            raise ValueError("API result is empty")

        run = data[0]
        return DbtRun(id=run["id"], finished_at=parse(run["finished_at"]))

    def _fetch_run_artifact(self, run_id: int, artifact: Artifact) -> dict:
        """
        Fetch dbt manifest or run results
        https://docs.getdbt.com/dbt-cloud/api-v2-legacy#tag/Runs/operation/getArtifactsByRunId
        """
        url = f"{_CLOUD_URL}/{self._account_id}/runs/{run_id}/artifacts/{artifact}"
        logger.info(
            f"Extracting {artifact} from run id {run_id} with url {url}"
        )

        # setting text content as a workaround to this issue
        # https://stackoverflow.com/questions/68201659/dbt-cloud-api-to-extract-run-artifacts
        return self._call(url, content_type=ContentType.TEXT)

    def fetch_manifest(self, run_id: Optional[int] = None) -> dict:
        """
        Fetch the manifest or the given run, or of the latest run for the configured job
        """
        if not run_id:
            run = self.last_run()
            assert run, f"No run found for job {self._credentials.job_id}"
            run_id = run.id
        return self._fetch_run_artifact(run_id, "manifest.json")

    def fetch_run_results(self, run_id: int) -> dict:
        """Fetch the run results of the given run"""
        return self._fetch_run_artifact(run_id, "run_results.json")

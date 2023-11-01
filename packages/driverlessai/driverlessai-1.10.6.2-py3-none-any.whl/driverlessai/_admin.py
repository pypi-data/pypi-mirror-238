"""Admin module of official Python client for Driverless AI."""
import abc
import functools
import re
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from driverlessai import _commons
from driverlessai import _core
from driverlessai import _enums
from driverlessai import _utils

if TYPE_CHECKING:
    import fsspec  # noqa F401


def _requires_admin(func: Callable) -> Callable:
    """Decorates methods which require admin access."""

    @functools.wraps(func)
    def wrapped(self: "Admin", *args: Any, **kwargs: Any) -> Any:
        if not self.is_admin:
            raise Exception("Administrator access are required to access this feature.")
        return func(self, *args, **kwargs)

    return wrapped


class _EntityKind(str, Enum):
    DATASET = "dataset"
    EXPERIMENT = "model_summary"


class Admin:
    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self._is_admin: Optional[bool] = None

    @property
    def is_admin(self) -> Optional[bool]:
        """Returns ``True`` if the user is an admin."""
        if self._is_admin is None:
            try:
                self._client._backend.get_users_insights()
                self._is_admin = True
            except self._client._server_module.protocol.RemoteError:
                self._is_admin = False
        return self._is_admin

    @_requires_admin
    def list_users(self) -> List[str]:
        """Returns a list of users in the Driverless AI server."""
        return [
            user_insight.dump()["user"]
            for user_insight in self._client._backend.get_users_insights()
        ]

    @_requires_admin
    @_utils.beta
    @_utils.min_supported_dai_version("1.10.5")
    def list_current_users(self) -> List[str]:
        """Returns a list of users who are currently
        logged-in to the Driverless AI server."""
        return self._client._backend.get_current_users()

    @_requires_admin
    @_utils.beta
    def list_datasets(self, username: str) -> List["DatasetProxy"]:
        """List datasets of the specified user."""
        response = self._client._backend.admin_list_entities(
            username, _EntityKind.DATASET
        )
        return [DatasetProxy(self._client, username, item) for item in response.items]

    @_requires_admin
    @_utils.beta
    def list_experiments(self, username: str) -> List["ExperimentProxy"]:
        """List experiments of the specified user."""
        response = self._client._backend.admin_list_entities(
            username, _EntityKind.EXPERIMENT
        )
        return [
            ExperimentProxy(self._client, username, item) for item in response.items
        ]

    @_requires_admin
    def transfer_data(self, from_user: str, to_user: str) -> None:
        """Transfer all data of ``from_user`` to ``to_user``."""
        if from_user == to_user:
            raise ValueError("Cannot transfer data between the same user.")
        self._client._backend.admin_transfer_entities(from_user, to_user)

    @_requires_admin
    @_utils.min_supported_dai_version("1.10.5")
    def list_server_logs(self) -> List["DAIServerLog"]:
        """Lists the server logs of Driverless AI server."""
        log_files = self._client._backend.get_server_logs_details()

        return [
            DAIServerLog(
                client=self._client,
                raw_info=log_file,
            )
            for log_file in log_files
        ]


class DAIServerLog(_commons.ServerLog):
    """An entity to represent a log file in the server."""

    def __init__(self, client: "_core.Client", raw_info: Any):
        path = re.sub(
            "^.*?/files/",
            "",
            re.sub("^.*?/log_files/", "", raw_info.resource_url),
        )
        super().__init__(client=client, file_path=path)
        self._raw_info = raw_info

    def download(
        self,
        dst_dir: str = ".",
        dst_file: Optional[str] = None,
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> str:
        return super()._download(
            dst_dir=dst_dir,
            dst_file=dst_file,
            file_system=file_system,
            overwrite=overwrite,
            download_type=_enums.DownloadType.LOGS,
        )

    @property
    def size(self) -> int:
        """Size of the file in bytes."""
        return self._raw_info.size

    @property
    def created(self) -> str:
        """Time of created."""
        return self._raw_info.ctime_str

    @property
    def last_modified(self) -> str:
        """Time of last modification"""
        return self._raw_info.mtime_str


class ServerObjectProxy(abc.ABC):
    def __init__(self, client: "_core.Client", owner: str, key: str, name: str = None):
        self._client = client
        self._owner = owner
        self._key = key
        self._name = name

    @property
    def key(self) -> str:
        """Universally unique identifier."""
        return self._key

    @property
    def name(self) -> str:
        """Display name."""
        return self._name

    @property
    def owner(self) -> str:
        """Owner of the object."""
        return self._owner

    @property
    @abc.abstractmethod
    def _kind(self) -> _EntityKind:
        raise NotImplementedError

    def delete(self) -> None:
        """Delete this entity."""
        self._client._backend.admin_delete_entity(self.owner, self._kind, self.key)


class DatasetProxy(ServerObjectProxy):
    """A Proxy for admin access for a dataset in the Driverless AI server."""

    def __init__(self, client: "_core.Client", owner: str, raw_info: dict) -> None:
        super().__init__(
            client=client,
            owner=owner,
            key=raw_info["entity"]["key"],
            name=raw_info["entity"]["name"],
        )
        self._raw_info = raw_info

    @property
    def _kind(self) -> _EntityKind:
        return _EntityKind.DATASET


class ServerJobProxy(ServerObjectProxy):
    @abc.abstractmethod
    def _get_raw_info(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def _status(self) -> _enums.JobStatus:
        raise NotImplementedError

    def is_complete(self) -> bool:
        """Returns ``True`` if this job completed successfully."""
        return _commons.is_server_job_complete(self._status())

    def is_running(self) -> bool:
        """Returns ``True`` if this job is scheduled, running, or finishing."""
        return _commons.is_server_job_running(self._status())

    def status(self, verbose: int = 0) -> str:
        """Returns the status of this job.

        Args:
            verbose:
                - 0: short description
                - 1: short description with progress percentage
                - 2: detailed description with progress percentage
        """

        status = self._status()
        # server doesn't always show 100% complete
        progress = 1 if self.is_complete() else self._get_raw_info()["progress"]
        if verbose == 1:
            return f"{status.message} {progress:.2%}"
        elif verbose == 2:
            if status == _enums.JobStatus.FAILED:
                message = self._get_raw_info()["error"]
            elif "message" in self._get_raw_info():
                message = self._get_raw_info()["message"].split("\n")[0]
            else:
                message = ""
            return f"{status.message} {progress:.2%} - {message}"

        return status.message


class ExperimentProxy(ServerJobProxy):
    """A Proxy for admin access for an experiment in the Driverless AI server."""

    def __init__(self, client: "_core.Client", owner: str, raw_info: dict) -> None:
        super().__init__(
            client=client,
            owner=owner,
            key=raw_info["key"],
            name=raw_info["description"],
        )
        self._all_datasets: Optional[List["DatasetProxy"]] = None
        self._datasets: Optional[Dict[str, Optional["DatasetProxy"]]] = None
        self._raw_info = raw_info
        self._settings: Optional[Dict[str, Any]] = None

    def _get_dataset(self, key: str) -> Optional["DatasetProxy"]:
        if self._all_datasets is None:
            self._all_datasets = self._client.admin.list_datasets(self.owner)
        for dataset in self._all_datasets:
            if dataset.key == key:
                return dataset
        return None

    def _get_raw_info(self) -> dict:
        return self._raw_info

    @property
    def _kind(self) -> _EntityKind:
        return _EntityKind.EXPERIMENT

    def _status(self) -> _enums.JobStatus:
        return _enums.JobStatus(self._get_raw_info()["status"])

    @property
    def creation_timestamp(self) -> float:
        """Creation timestamp in seconds since the epoch (POSIX timestamp)."""
        return self._get_raw_info()["created"]

    @property
    def datasets(self) -> Dict[str, Optional["DatasetProxy"]]:
        """Dictionary of ``train_dataset``,``validation_dataset``,
        and ``test_dataset`` used for this experiment."""
        if not self._datasets:
            train_dataset = self._get_dataset(
                self._get_raw_info()["parameters"]["dataset"]["key"]
            )
            validation_dataset = None
            test_dataset = None
            if self._get_raw_info()["parameters"]["validset"]["key"]:
                validation_dataset = self._get_dataset(
                    self._get_raw_info()["parameters"]["validset"]["key"]
                )
            if self._get_raw_info()["parameters"]["testset"]["key"]:
                test_dataset = self._get_dataset(
                    self._get_raw_info()["parameters"]["testset"]["key"]
                )
            self._datasets = {
                "train_dataset": train_dataset,
                "validation_dataset": validation_dataset,
                "test_dataset": test_dataset,
            }

        return self._datasets

    @property
    def run_duration(self) -> Optional[float]:
        """Run duration in seconds."""
        return self._get_raw_info()["training_duration"]

    @property
    def settings(self) -> Dict[str, Any]:
        """Experiment settings."""
        if not self._settings:
            self._settings = self._client.experiments._parse_server_settings(
                self._get_raw_info()["parameters"]
            )
        return self._settings

    @property
    def size(self) -> int:
        """Size in bytes of all experiment's files on the Driverless AI server."""
        return self._get_raw_info()["model_file_size"]

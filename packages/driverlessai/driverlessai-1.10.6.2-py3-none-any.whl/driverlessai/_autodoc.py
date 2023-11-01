"""Autodoc module of official Python client for Driverless AI."""

import os
from typing import Any, Optional, TYPE_CHECKING

import toml

from driverlessai import (
    _commons,
    _core,
    _experiments,
)

if TYPE_CHECKING:
    import fsspec  # noqa F401


class AutoDoc(_commons.ServerObject):
    """Interact with a AutoDoc on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)
        self._experiment: Optional[_experiments.Experiment] = None

    @property
    def experiment(self) -> "_experiments.Experiment":
        """Experiment associated with this AutoDoc."""
        if self._experiment is None:
            self._experiment = _experiments.Experiments(self._client).get(
                self._get_raw_info().entity.model_key
            )
        return self._experiment

    @property
    def creation_time(self) -> float:
        """Creation timestamp in seconds since the epoch (POSIX timestamp)."""
        return self._get_raw_info().created

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_autoreport_job(self.key))
        self._set_name(os.path.basename(self._get_raw_info().entity.report_path))

    def download(
        self,
        dst_dir: str = ".",
        dst_file: Optional[str] = None,
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> str:
        """Downloads the AutoDoc."""
        path = self._client._backend.get_autoreport_job(self.key).entity.report_path

        return self._client._download(
            server_path=path,
            dst_dir=dst_dir,
            dst_file=dst_file,
            file_system=file_system,
            overwrite=overwrite,
        )


class AutoDocJob(_commons.ServerJob):
    """Monitor creation of a AutoDoc on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_autoreport_job(self.key))

    def result(self, silent: bool = False) -> AutoDoc:
        """Wait for job to complete, then return a AutoDoc object.
        Args:
            silent: if True, don't display status updates
        """

        self._wait(silent)
        return AutoDoc(self._client, self.key)


class AutoDocs:
    """Interact with AutoDocs on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def create(
        self,
        experiment: "_experiments.Experiment",
        **config_overrides: Any,
    ) -> AutoDoc:
        """
        Create a new AutoDoc.

        Args:
            experiment: Experiment to create AutoDoc
            **config_overrides: Config overrides for AutoDoc that needs to be generated.
                Please refer below page for available autodoc configs
                https://docs.h2o.ai/driverless-ai/1-10-lts/docs/userguide/expert_settings/autodoc_settings.html
        """
        return self.create_async(
            experiment,
            **config_overrides,
        ).result()

    def create_async(
        self,
        experiment: "_experiments.Experiment",
        **config_overrides: Any,
    ) -> AutoDocJob:
        """
        Launch creation of a new AutoDoc.

        Args:
            experiment: Experiment to create AutoDoc
            **config_overrides: Config overrides for AutoDoc that needs to be generated.
                Please refer below page for available autodoc configs
                https://docs.h2o.ai/driverless-ai/1-10-lts/docs/userguide/expert_settings/autodoc_settings.html
        """
        config_overrides_toml = ""
        if config_overrides:
            config_overrides_toml = toml.dumps(config_overrides)

        key = self._client._backend.make_autoreport(
            experiment.key,
            mli_key=None,
            individual_rows=None,
            autoviz_key=None,
            template_path="",
            placeholders={},
            external_dataset_keys=[],
            reuse_model_key=False if config_overrides_toml else True,
            config_overrides=config_overrides_toml,
        )
        return AutoDocJob(self._client, key)

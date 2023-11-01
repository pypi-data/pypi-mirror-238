import abc
import dataclasses
from typing import Any, List, Optional, Sequence, TYPE_CHECKING

from driverlessai import _commons, _core, _experiments, _utils

if TYPE_CHECKING:
    import fsspec  # noqa F401


class Deployment(_commons.ServerObject, abc.ABC):
    """Interact with a deployment on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)


class TritonDeployment(Deployment):
    """
    Interact with a deployment in a Triton inference server on the Driverless AI server.
    """

    def __init__(
        self, client: "_core.Client", key: str, is_local: bool, raw_info: Optional[Any]
    ) -> None:
        super().__init__(client=client, key=key)
        self._is_local = is_local
        self._set_raw_info(raw_info)

    @property
    def is_local_deployment(self) -> bool:
        """
        Whether this Triton deployment is deployed in the embedded (local) Triton
        server in the Driverless AI server or in a remote Triton server.
        """
        return self._is_local

    @property
    def state(self) -> str:
        """Current state of this Triton deployment."""
        self._update()  # The state might have changed, so fetch again.
        return self._get_raw_info().state

    @property
    @_utils.beta
    def triton_model(self) -> "TritonModel":
        """Triton model created by this Triton deployment."""
        raw_info = self._get_raw_info()
        return TritonModel(
            raw_info.inputs,
            raw_info.model_desc,
            raw_info.outputs,
            raw_info.platform,
            raw_info.versions,
        )

    @property
    def triton_server_hostname(self) -> str:
        """Hostname of the Triton server that this Triton deployment occurred."""
        return self._get_raw_info().host

    def _update(self) -> None:
        self._set_raw_info(
            self._client._backend.get_triton_model(self.is_local_deployment, self.key)
        )
        self._set_name(self._get_raw_info().model_desc)

    @_utils.beta
    def delete(self) -> None:
        """Delete this local Triton deployment."""
        if not self.is_local_deployment:
            raise Exception("Cannot delete a remote Triton deployment.")
        self.unload()
        self._client._backend.delete_triton_model(
            experiment_key=self.key,
            local=self.is_local_deployment,
        )

    @_utils.beta
    def load(self) -> None:
        """Load this Triton deployment."""
        self._client._backend.load_triton_model(
            experiment_key=self.key,
            local=self.is_local_deployment,
            config_json=None,
            files=None,
        )
        self._update()

    @_utils.beta
    def unload(self) -> None:
        """Unload this Triton deployment."""
        self._client._backend.unload_triton_model(
            experiment_key=self.key,
            local=self.is_local_deployment,
        )
        self._update()


class Deployments:
    """Interact with deployments on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def _deploy_to_triton(
        self,
        to_local: bool,
        experiment: _experiments.Experiment,
        deploy_predictions: bool = True,
        deploy_shapley: bool = False,
        deploy_original_shapley: bool = False,
        enable_high_concurrency: bool = False,
    ) -> TritonDeployment:
        key = self._client._backend.deploy_model_to_triton(
            experiment_key=experiment.key,
            local=to_local,
            deploy_preds=deploy_predictions,
            deploy_pred_contribs=deploy_shapley,
            deploy_pred_contribs_orig=deploy_original_shapley,
            dest_dir=None,
            high_concurrency=enable_high_concurrency,
        )
        return TritonDeployment(self._client, key, to_local, None)

    def _get_triton_deployment(self, in_local: bool, key: str) -> TritonDeployment:
        all_deployments = self._list_triton_deployments(in_local)
        deployments = [d for d in all_deployments if d.key == key]
        triton_server_type = "local" if in_local else "remote"
        if len(deployments) == 0:
            raise ValueError(
                f"Triton deployment '{key}' cannot be found "
                f"in the {triton_server_type} Triton server."
            )
        if len(deployments) > 1:
            raise Exception(
                f"Found {len(deployments)} Triton deployments "
                f"with the same key '{key}' in the {triton_server_type} Triton server."
            )
        return deployments[0]

    def _list_triton_deployments(
        self, in_local: bool, start_index: int = 0, count: int = None
    ) -> List["TritonDeployment"]:
        if count:
            data = self._client._backend.list_triton_models(
                in_local, start_index, count
            ).items
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._client._backend.list_triton_models(
                    in_local, page_position, page_size
                ).items
                data += page
                if len(page) < page_size:
                    break
                page_position += page_size
        return [TritonDeployment(self._client, d.model_name, in_local, d) for d in data]

    @_utils.beta
    def deploy_to_triton_in_local(
        self,
        experiment: _experiments.Experiment,
        deploy_predictions: bool = True,
        deploy_shapley: bool = False,
        deploy_original_shapley: bool = False,
        enable_high_concurrency: bool = False,
    ) -> TritonDeployment:
        """
        Deploys the model created by the specified experiment in the local Triton server
        on the Driverless AI server.

        Args:
            experiment: experiment model
            deploy_predictions: whether to deploy model predictions
            deploy_shapley: whether to deploy model Shapley
            deploy_original_shapley: whether to deploy model original Shapley
            enable_high_concurrency: whether to enable handling several requests at once
        """
        return self._deploy_to_triton(
            True,
            experiment,
            deploy_predictions,
            deploy_shapley,
            deploy_original_shapley,
            enable_high_concurrency,
        )

    @_utils.beta
    def deploy_to_triton_in_remote(
        self,
        experiment: _experiments.Experiment,
        deploy_predictions: bool = True,
        deploy_shapley: bool = False,
        deploy_original_shapley: bool = False,
        enable_high_concurrency: bool = False,
    ) -> TritonDeployment:
        """
        Deploys the model created by the specified experiment in a remote Triton server
        configured on the Driverless AI server.

        Args:
            experiment: experiment model
            deploy_predictions: whether to deploy model predictions
            deploy_shapley: whether to deploy model Shapley
            deploy_original_shapley: whether to deploy model original Shapley
            enable_high_concurrency: whether to enable handling several requests at once
        """
        return self._deploy_to_triton(
            False,
            experiment,
            deploy_predictions,
            deploy_shapley,
            deploy_original_shapley,
            enable_high_concurrency,
        )

    def get_from_triton_in_local(self, key: str) -> TritonDeployment:
        """
        Get the Triton deployment specified by the key, deployed in the local Triton
        server on the Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the Triton deployment
        """
        return self._get_triton_deployment(True, key)

    def get_from_triton_in_remote(self, key: str) -> TritonDeployment:
        """
        Get the Triton deployment specified by the key, deployed in a remote Triton
        server configured on the Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the Triton deployment
        """
        return self._get_triton_deployment(False, key)

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the deployments page on Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}deployments"
        )

    @_utils.beta
    def list_triton_deployments(
        self, start_index: int = 0, count: int = None
    ) -> Sequence["TritonDeployment"]:
        """Returns a list of Triton deployments on the Driverless AI server.

        Args:
            start_index: index on Driverless AI server of first deployment in list
            count: number of deployment to request from the Driverless AI server
        """
        local = self._list_triton_deployments(True, start_index, count)
        remote = self._list_triton_deployments(False, start_index, count)
        return local + remote


@dataclasses.dataclass(frozen=True)
class TritonModel:
    """A Triton model created by a Triton deployment."""

    inputs: List[str]
    """Inputs of this Triton model."""
    name: str
    """Name of this Triton model."""
    outputs: List[str]
    """Outputs of this Triton model."""
    platform: str
    """Supported platform of this Triton model."""
    versions: List[str]
    """Versions of this Triton model."""

"""Model diagnostics module of official Python client for Driverless AI."""

import math
import re
from typing import Any, Dict, List, Optional, Sequence, TYPE_CHECKING

from driverlessai import (
    _common_metric_plots,
    _commons,
    _core,
    _datasets,
    _experiments,
    _logging,
    _utils,
)

if TYPE_CHECKING:
    import fsspec  # noqa F401


class ModelDiagnosticMetricPlots(_common_metric_plots.CommonMetricPlots):
    """Interacts with metric plots of a model diagnostic on the Driverless AI server."""

    def __init__(
        self,
        client: "_core.Client",
        raw_info: Any,
        key: str,
        is_classification: bool,
    ) -> None:
        super().__init__(client, key, is_classification)
        self._raw_info = raw_info

    def _get_act_vs_pred_data(self) -> Any:
        return self._raw_info.act_vs_pred

    def _get_gains(self) -> Any:
        return self._raw_info.gains

    def _get_roc_data(self) -> Any:
        return self._raw_info.roc

    def _get_residual_plot_data(self) -> Any:
        return self._raw_info.residual_plot

    def _get_residual_loess_data(self) -> Any:
        return self._raw_info.residual_loess

    @property
    def residual_histogram(self) -> Optional[Dict[str, Any]]:
        """Residual Histogram of this model diagnostic.

        Returns:
            a residual histogram in Vega Lite (v3) format
        """
        if self._is_classification:
            return None

        raw_info = self._raw_info.residual_hist

        ticks = raw_info.ticks
        counts = raw_info.counts
        x_values = [float(t) for t in ticks if not math.isnan(float(t))]
        y_values = [
            float(c) for c in counts if not math.isnan(float(ticks[counts.index(c)]))
        ]

        values = [
            {
                "Residual": round(float(x_values[point]), 1),
                "Count": float(y_values[point]),
                "label": f"<{round(float(x_values[point]), 4)};"
                f"{round(float(x_values[point + 1]), 4)}>",
            }
            for point in range(min(len(x_values), len(y_values)))
        ]

        return self._get_single_layer_vega_plot(
            name="Residual Histogram",
            data=values,
            marks=["bar"],
            x_axis="Residual",
            y_axis="Count",
        )


class ModelDiagnostic(_commons.ServerObject):
    """Interact with a model diagnostic on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)
        self._experiment: Optional[_experiments.Experiment] = None
        self._scores: Optional[Dict[str, Dict[str, float]]] = None
        self._test_dataset: Optional[_datasets.Dataset] = None

    @property
    def experiment(self) -> "_experiments.Experiment":
        """Diagnosed experiment by this model diagnostic."""
        if self._experiment is None:
            self._experiment = _experiments.Experiment(
                self._client, self._get_raw_info().entity.model.key
            )
        return self._experiment

    @property
    @_utils.beta
    @_utils.min_supported_dai_version("1.9.0")
    def metric_plots(self) -> "ModelDiagnosticMetricPlots":
        """Metric plots of this model diagnostic."""
        model_summary = self._client._backend.get_model_summary(self.experiment.key)
        return ModelDiagnosticMetricPlots(
            client=self._client,
            raw_info=self._get_raw_info().entity,
            key=self.key,
            is_classification=model_summary.parameters.is_classification,
        )

    @property
    def scores(self) -> Dict[str, Dict[str, float]]:
        """Scores of this model diagnostic."""
        if self._scores is None:
            scores = {}
            for score in self._get_raw_info().entity.scores:
                scores[score.score_f_name] = {
                    "score": score.score,
                    "mean": score.score_mean,
                    "sd": score.score_sd,
                }
            self._scores = scores
        return self._scores

    @property
    def test_dataset(self) -> "_datasets.Dataset":
        """Test dataset that was used for this model diagnostic."""
        if self._test_dataset is None:
            try:
                self._test_dataset = self._client.datasets.get(
                    self._get_raw_info().entity.dataset.key
                )
            except self._client._server_module.protocol.RemoteError:
                # assuming a key error means deleted dataset, if not the error
                # will still propagate to the user else where
                self._test_dataset = self._get_raw_info().entity.dataset.dump()
        return self._test_dataset

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_model_diagnostic_job(self.key))
        self._set_name(self._get_raw_info().entity.name)

    def delete(self) -> None:
        """Delete this model diagnostic on Driverless AI server."""
        key = self.key
        self._client._backend.delete_model_diagnostic_job(key)
        _logging.logger.info(
            f"Driverless AI Server reported model diagnostic {key} deleted."
        )

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for this model diagnostic’s page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}diagnostics?"
            f"diagnostic_key={self.key}&model_key={self.experiment.key}"
        )

    def download_predictions(
        self,
        dst_dir: str = ".",
        dst_file: Optional[str] = None,
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> str:
        """Downloads the predictions into a csv file."""

        path = re.sub(
            "^.*?/files/",
            "",
            re.sub(
                "^.*?/datasets_files/", "", self._get_raw_info().entity.preds_csv_path
            ),
        )
        return self._client._download(
            server_path=path,
            dst_dir=dst_dir,
            dst_file=dst_file,
            file_system=file_system,
            overwrite=overwrite,
        )


class ModelDiagnosticJob(_commons.ServerJob):
    """Monitor creation of a model diagnostic on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_model_diagnostic_job(self.key))

    def result(self, silent: bool = False) -> ModelDiagnostic:
        """Wait for job to complete, then return a ModelDiagnostic object.
        Args:
            silent: if True, don't display status updates
        """

        self._wait(silent)
        return ModelDiagnostic(self._client, self.key)


class ModelDiagnostics:
    """Interact with model diagnostics on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def _list_model_diagnostics(self, offset: int, limit: int) -> List[Any]:
        response = self._client._backend.list_model_diagnostic(offset, limit)
        if _utils.is_server_version_less_than(self._client, "1.9.0.6"):
            return response
        return [mdj.entity for mdj in response.items]

    def create(
        self,
        diagnose_experiment: _experiments.Experiment,
        test_dataset: _datasets.Dataset,
    ) -> "ModelDiagnostic":
        """
        Create a new model diagnostic.

        Args:
            diagnose_experiment: experiment that created the diagnosing model
            test_dataset: test dataset for the diagnosis
        """
        return self.create_async(diagnose_experiment, test_dataset).result()

    def create_async(
        self,
        diagnose_experiment: _experiments.Experiment,
        test_dataset: _datasets.Dataset,
    ) -> "ModelDiagnosticJob":
        """
        Launch creation of a new model diagnostic.

        Args:
            diagnose_experiment: experiment that created the diagnosing model
            test_dataset: test dataset for the diagnosis
        """
        key = self._client._backend.get_model_diagnostic(
            diagnose_experiment.key, test_dataset.key
        )
        return ModelDiagnosticJob(self._client, key)

    def get(self, key: str) -> "ModelDiagnostic":
        """
        Get a ModelDiagnostic object corresponding to a model diagnostic
        on the Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the model diagnostic
        """
        return ModelDiagnostic(self._client, key)

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the Model Diagnostics page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}diagnostics"
        )

    def list(
        self, start_index: int = 0, count: int = None
    ) -> Sequence["ModelDiagnostic"]:
        """
        Return list of ModelDiagnostic objects on the Driverless AI server.

        Args:
            start_index: index on Driverless AI server of first model diagnostic in list
            count: number of model diagnostics to request from the Driverless AI server
        """
        if count:
            data = self._list_model_diagnostics(start_index, count)
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._list_model_diagnostics(page_position, page_size)
                data += page
                if len(page) < page_size:
                    break
                page_position += page_size
        return _commons.ServerObjectList(
            data=data, get_method=self.get, item_class_name=ModelDiagnostic.__name__
        )

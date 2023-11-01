"""MLI module of official Python client for Driverless AI."""

import abc
import collections
import dataclasses
import inspect
import json
import tempfile
import textwrap
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Union

import toml

from driverlessai import _commons
from driverlessai import _commons_mli
from driverlessai import _core
from driverlessai import _datasets
from driverlessai import _exceptions
from driverlessai import _experiments
from driverlessai import _logging
from driverlessai import _recipes
from driverlessai import _utils

if TYPE_CHECKING:
    import fsspec  # noqa F401
    import pandas  # noqa F401


@dataclasses.dataclass
class _ExplainerInfo:
    key: str
    name: str


class Artifacts(abc.ABC):
    """An abstract class that interact with files created by an MLI interpretation on
    the Driverless AI server."""

    def __init__(self, client: "_core.Client", paths: Dict[str, str]) -> None:
        self._client = client
        self._paths = paths

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {list(self._paths.keys())}"

    def __str__(self) -> str:
        return f"{list(self._paths.keys())}"

    def _download(
        self,
        only: Union[str, List[str]] = None,
        dst_dir: str = ".",
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Download interpretation artifacts from the Driverless AI server. Returns
        a dictionary of relative paths for the downloaded artifacts.

        Args:
            only: specify specific artifacts to download, use
                ``interpretation.artifacts.list()`` to see the available
                artifacts on the Driverless AI server
            dst_dir: directory where interpretation artifacts will be saved
            file_system: FSSPEC based file system to download to,
                instead of local file system
            overwrite: overwrite existing files
        """
        dst_paths = {}
        if isinstance(only, str):
            only = [only]
        if only is None:
            only = self._list()
        for k in only:
            path = self._paths.get(k)
            if path:
                dst_paths[k] = self._client._download(
                    server_path=path,
                    dst_dir=dst_dir,
                    file_system=file_system,
                    overwrite=overwrite,
                )
            else:
                _logging.logger.info(
                    f"'{k}' does not exist on the Driverless AI server."
                )
        return dst_paths

    def _list(self) -> List[str]:
        """List of interpretation artifacts that exist on the Driverless AI server."""
        return [k for k, v in self._paths.items() if v]


class Explainer(_commons.ServerJob):
    """Interact with an MLI explainers on the Driverless AI server."""

    _HELP_TEXT_WIDTH = 88
    _HELP_TEXT_INDENT = " " * 4

    def __init__(
        self,
        client: "_core.Client",
        key: str,
        mli_key: str,
    ) -> None:
        super().__init__(client=client, key=key)
        self._id: Optional[str] = None
        self._mli_key = mli_key
        self._frames: Optional[ExplainerFrames] = None
        self._help: Optional[
            Dict[str, Dict[str, Dict[str, List[Dict[str, Union[str, bool]]]]]]
        ] = None
        self._artifacts: Optional[ExplainerArtifacts] = None

        _commons_mli.update_method_doc(
            obj=self,
            method_to_update="get_data",
            updated_doc=self._format_help("data"),
            new_signature=self._method_signature("data"),
            custom_doc_update_func=self._custom_doc_update_func,
        )

    @property
    def artifacts(self) -> "ExplainerArtifacts":
        """Artifacts of this explainer."""
        if not self._artifacts:
            self._artifacts = ExplainerArtifacts(
                client=self._client, mli_key=self._mli_key, e_job_key=self.key
            )
        return self._artifacts

    @property
    def frames(self) -> Optional["ExplainerFrames"]:
        """An ``ExplainerFrames`` object that contains the paths to the explainer
        frames retrieved from Driverless AI Server. If the explainer frame is not
        available, the value of this propertiy is ``None``."""
        if not self._frames:
            frame_paths = self._client._backend.get_explainer_frame_paths(
                mli_key=self._mli_key, explainer_job_key=self.key
            )
            if frame_paths:
                self._frames = ExplainerFrames(
                    client=self._client, frame_paths=frame_paths
                )
        return self._frames

    @property
    def id(self) -> str:
        """This explainer's Id."""
        return self._get_raw_info().entity.id

    def __repr__(self) -> str:
        return (
            f"<class '{self.__class__.__name__}'> {self._mli_key}/{self.key} "
            f"{self.name}"
        )

    def __str__(self) -> str:
        return f"{self.name} ({self._mli_key}/{self.key})"

    def _check_has_data(self) -> None:
        if not self.is_complete():
            raise RuntimeError(
                f"'{ExplainerData.__name__}' is only available for successfully "
                "completed explainers."
            )

    @staticmethod
    def _custom_doc_update_func(orig: str, updated: str) -> str:
        # Only include the first three line so that we don't include line refering
        # to `help(explainer.get_data)`
        orig = "\n".join(orig.split("\n")[:3])
        return f"{orig}\n\n{updated}"

    def _format_help(self, method_name: str) -> str:
        return self._do_format_help(method_name=method_name, help_dict=self._get_help())

    @classmethod
    def _do_format_help(
        cls,
        method_name: str,
        help_dict: Optional[
            Dict[str, Dict[str, Dict[str, List[Dict[str, Union[str, bool]]]]]]
        ],
    ) -> str:
        formatted_help = ""
        if help_dict:
            method = help_dict.get("methods", {method_name: {}}).get(method_name, {})
            parameters = method.get("parameters")
            if parameters:
                title = "Keyword arguments"
                underline = "-" * len(title)
                formatted_help += f"{title}\n{underline}\n"
                for param in parameters:
                    required = "required" if param["required"] else "optional"
                    formatted_help += (
                        f"{param['name']} : {param['type']}    [{required}]\n"
                    )
                    if param["default"]:
                        formatted_help += (
                            cls._indent_and_wrap(f"Default: {param['default']}") + "\n"
                        )
                    if param["doc"]:
                        doc: str = str(param["doc"])
                        formatted_help += f"{cls._indent_and_wrap(doc)}\n"
            elif help_dict:
                formatted_help = "This method does not require any arguments."
        return formatted_help

    def _get_help(
        self,
    ) -> Optional[Dict[str, Dict[str, Dict[str, List[Dict[str, Union[str, bool]]]]]]]:
        if self._help is None:
            explainer_result_help = self._client._backend.get_explainer_result_help(
                mli_key=self._mli_key, explainer_job_key=self.key
            )
            self._help = json.loads(explainer_result_help.help)
        return self._help

    @classmethod
    def _indent_and_wrap(cls, text: str) -> str:
        wrapped = textwrap.wrap(
            text=text,
            width=cls._HELP_TEXT_WIDTH,
            initial_indent=cls._HELP_TEXT_INDENT,
            subsequent_indent=cls._HELP_TEXT_INDENT,
        )
        return "\n".join(wrapped)

    def _method_signature(self, method_name: str) -> Optional[inspect.Signature]:
        help_dict = self._get_help()
        if help_dict:
            parameters = (
                help_dict.get("methods", {method_name: {}})
                .get("data", {})
                .get("parameters")
            )
            param_objs: List[inspect.Parameter] = [
                inspect.Parameter(
                    name="self", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD
                )
            ]
            if parameters:
                for param in parameters:
                    param_objs.append(
                        inspect.Parameter(
                            name=str(param["name"]),
                            kind=inspect.Parameter.KEYWORD_ONLY,
                            default=inspect.Parameter.empty
                            if param["required"]
                            else None,
                            annotation=param["type"]
                            if param["type"]
                            else inspect.Parameter.empty,
                        )
                    )
            return inspect.Signature(parameters=param_objs)
        return None

    def _set_id(self, e_id: str) -> None:
        self._id = e_id

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_explainer_run_job(self.key))
        self._set_name(self._get_raw_info().entity.name)
        self._set_id(self._get_raw_info().entity.id)

    def get_data(self, **kwargs: Any) -> "ExplainerData":
        """Retrieve the ``ExplainerData`` from the Driverless AI server.
        Raises a ``RuntimeError`` exception if the explainer has not been completed
        successfully.

        Use ``help(explainer.get_data)`` to view help on available keyword arguments."""

        self._check_has_data()
        ExplainerResultDataArgs = (
            self._client._server_module.messages.ExplainerResultDataArgs
        )
        explainer_result_data_args = [
            ExplainerResultDataArgs(param_name, value)
            for param_name, value in kwargs.items()
        ]
        explainer_result_data = self._client._backend.get_explainer_result_data(
            mli_key=self._mli_key,
            explainer_job_key=self.key,
            args=explainer_result_data_args,
        )
        return ExplainerData(
            data=explainer_result_data.data,
            data_type=explainer_result_data.data_type,
            data_format=explainer_result_data.data_format,
        )

    def result(self, silent: bool = False) -> "Explainer":
        """Wait for the explainer to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self


class ExplainerArtifacts(Artifacts):
    """Interact with artifacts created by an explainer during interpretation on the
    Driverless AI server."""

    def __init__(self, client: "_core.Client", mli_key: str, e_job_key: str) -> None:
        super().__init__(client=client, paths={})
        self._mli_key = mli_key
        self._e_job_key = e_job_key
        self._paths["log"] = self._get_artifact(
            self._client._backend.get_explainer_run_log_url_path
        )
        self._paths["snapshot"] = self._get_artifact(
            self._client._backend.get_explainer_snapshot_url_path
        )

    @property
    def file_paths(self) -> Dict[str, str]:
        """Paths to explainer artifact files on the server."""
        return self._paths

    def _get_artifact(self, artifact_method: Callable) -> Optional[str]:
        try:
            return artifact_method(self._mli_key, self._e_job_key)
        except self._client._server_module.protocol.RemoteError:
            return ""

    def download(
        self,
        only: Union[str, List[str]] = None,
        dst_dir: str = ".",
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Download explainer artifacts from the Driverless AI server. Returns
        a dictionary of relative paths for the downloaded artifacts.

        Args:
            only: specify specific artifacts to download, use
                ``explainer.artifacts.list()`` to see the available
                artifacts on the Driverless AI server
            dst_dir: directory where interpretation artifacts will be saved
            file_system: FSSPEC based file system to download to,
                instead of local file system
            overwrite: overwrite existing files
        """
        return self._download(
            only=only, dst_dir=dst_dir, file_system=file_system, overwrite=overwrite
        )

    def list(self) -> List[str]:
        """List of explainer artifacts that exist on the Driverless AI server."""
        return self._list()


class ExplainerData:
    """Interact with the result data of an explainer on the Driverless AI server."""

    def __init__(self, data: str, data_type: str, data_format: str) -> None:
        self._data: str = data
        self._data_as_dict: Optional[Union[List, Dict]] = None
        self._data_as_pandas: Optional["pandas.DataFrame"] = None
        self._data_type: str = data_type
        self._data_format: str = data_format

    @property
    def data(self) -> str:
        """The explainer result data as string."""
        return self._data

    @property
    def data_format(self) -> str:
        """The explainer data format."""
        return self._data_format

    @property
    def data_type(self) -> str:
        """The explainer data type."""
        return self._data_type

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.data_type}"

    def __str__(self) -> str:
        return f"{self.data_type}"

    def data_as_dict(self) -> Optional[Union[List, Dict]]:
        """Return the explainer result data as a dictionary."""
        if self._data_as_dict is None and self._data:
            self._data_as_dict = json.loads(self._data)
        return self._data_as_dict

    @_utils.beta
    def data_as_pandas(self) -> Optional["pandas.DataFrame"]:
        """Return the explainer result data as a pandas frame."""
        if self._data_as_pandas is None and self._data:
            import pandas as pd

            self._data_as_pandas = pd.read_json(self._data)
        return self._data_as_pandas


class ExplainerFrames(Artifacts):
    """Interact with explanation frames created by an explainer during interpretation
    on the Driverless AI server."""

    def __init__(self, client: "_core.Client", frame_paths: Any) -> None:
        paths = {fp.name: fp.path for fp in frame_paths}
        super().__init__(client=client, paths=paths)

    @property
    def frame_paths(self) -> Dict[str, str]:
        """Frame names and paths to artifact files on the server."""
        return self._paths

    @_utils.beta
    def frame_as_pandas(
        self,
        frame_name: str,
        custom_tmp_dir: Optional[str] = None,
        keep_downloaded: bool = False,
    ) -> "pandas.DataFrame":
        """Download a frame with the given frame name to a temporary directory and
        return it as a ``pandas.DataFrame``.

        Args:
            frame_name: The name of the frame to open.
            custom_tmp_dir: If specified, use this directory as the temporary
                            directory instead of the default.
            keep_downloaded: If ``True``, do not delete the downloaded frame. Otherwise,
                             the downloaded frame is deleted before returning from this
                             method.
        """
        import pandas

        args = dict(
            suffix=f"explainer-frame-{frame_name}",
            prefix="python-api",
            dir=custom_tmp_dir,
        )

        def _open_as_pandas(tmp_dir: str) -> pandas.DataFrame:
            downloaded = self.download(frame_name=frame_name, dst_dir=tmp_dir)
            frame_file_path: str = downloaded[frame_name]
            return pandas.read_csv(frame_file_path)

        if keep_downloaded:
            return _open_as_pandas(tempfile.mkdtemp(**args))
        else:
            with tempfile.TemporaryDirectory(**args) as tmp_dir:
                return _open_as_pandas(tmp_dir)

    def frame_names(self) -> List[str]:
        """List of explainer frames that exist on the Driverless AI server."""
        return self._list()

    def download(
        self,
        frame_name: Union[str, List[str]] = None,
        dst_dir: str = ".",
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Download explainer frames from the Driverless AI server. Returns
        a dictionary of relative paths for the downloaded artifacts.

        Args:
            frame_name: specify specific frame to download, use
                ``explainer.frames.list()`` to see the available
                artifacts on the Driverless AI server
            dst_dir: directory where interpretation artifacts will be saved
            file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
            overwrite: overwrite existing files
        """
        ret: Dict[str, str] = self._download(
            only=frame_name,
            dst_dir=dst_dir,
            file_system=file_system,
            overwrite=overwrite,
        )
        return ret


class ExplainerList(collections.abc.Sequence):
    """List that lazy loads Explainer objects."""

    def __init__(
        self,
        explainer_infos: List[_ExplainerInfo],
        client: "_core.Client",
        mli_key: str,
    ):
        self._client = client
        self._mli_key = mli_key
        self._explainer_infos: Any = explainer_infos
        self._key_to_index = {}
        self._name_to_index = {}
        headers = ["", "Key", "Name"]
        data = [
            [
                i,
                d.key,
                d.name,
            ]
            for i, d in enumerate(explainer_infos)
        ]
        for idx, e_info in enumerate(explainer_infos):
            self._key_to_index[e_info.key] = idx
            self._name_to_index[e_info.name] = idx
        self._table = _utils.Table(headers=headers, data=data)

    def __getitem__(self, index: Union[int, slice, tuple]) -> Any:
        if isinstance(index, int):
            return self.__get_by_index(index)
        if isinstance(index, slice):
            return ExplainerList(
                self._explainer_infos[index], self._client, self._mli_key
            )
        if isinstance(index, tuple):
            return ExplainerList(
                [self._explainer_infos[i] for i in index], self._client, self._mli_key
            )

    def __len__(self) -> int:
        return len(self._explainer_infos)

    def __repr__(self) -> str:
        return self._table.__repr__()

    def _repr_html_(self) -> str:
        return self._table._repr_html_()

    @_utils.beta
    def get_by_key(self, key: str) -> Explainer:
        """Finds the explainer object that corresponds to the given key, and
        initializes it if it is not already initialized.

        Args:
            key: The job key of the desired explainer
        """
        return self.__get_by_index(self._key_to_index[key])

    def __get_by_index(self, idx: int) -> Explainer:
        """Finds the explainer object that corresponds to the given index, and
        initializes it if it is not already initialized.

        Args:
            index: The index of the desired explainer
        """
        data = self._explainer_infos[idx]
        if not isinstance(data, Explainer):
            self._explainer_infos[idx] = Explainer(
                client=self._client, mli_key=self._mli_key, key=data.key
            )
        return self._explainer_infos[idx]

    @_utils.beta
    def get_by_name(self, name: str) -> Explainer:
        """Finds the explainer object that corresponds to the given explainer name, and
        initializes it if it is not already initialized.

        Args:
            key: The name of the desired explainer
        """
        return self.__get_by_index(self._name_to_index[name])


@dataclasses.dataclass
class _ExplanationInfo:
    explainer_name: str
    explainer_key: str
    explainer_id: str


class ExplanationPlots:
    """Interact with an MLI explanation plots on the DriverlessAI server."""

    ORIG_SHAP_ID = (
        "h2oaicore.mli.byor.recipes.original_contrib_explainer.NaiveShapleyExplainer"
    )
    TRANS_SHAP_ID = (
        "h2oaicore.mli.byor.recipes.transformed_shapley_explainer."
        "TransformedShapleyExplainer"
    )
    DT_ID = (
        "h2oaicore.mli.byor.recipes.surrogates.dt_surrogate_explainer."
        "DecisionTreeSurrogateExplainer"
    )
    PD_ID = "h2oaicore.mli.byor.recipes.dai_pd_ice_explainer.DaiPdIceExplainer"
    SHAP_SUM_ID = (
        "h2oaicore.mli.byor.recipes.shapley_summary_explainer."
        "ShapleySummaryOrigFeatExplainer"
    )

    def __init__(self, client: "_core.Client", mli_key: str) -> None:
        self._client = client
        self._mli_key = mli_key
        self._id_explanation_info: Dict[str, _ExplanationInfo] = {}

    def _get_explanation_info(self, explainer_id: str) -> _ExplanationInfo:
        if explainer_id not in self._id_explanation_info:
            ed: Any
            try:
                ed = self._client._backend.get_explainer(explainer_id)
            except RuntimeError:
                raise ValueError(
                    f"Cannot find explainer '{explainer_id}' in MLI '{self._mli_key}'."
                )
            explainer_keys = self._client._backend.get_explainer_job_keys_by_id(
                self._mli_key, explainer_id
            )
            if not explainer_keys:
                raise _exceptions.ExplainerNotFound(
                    f"Explainer '{ed.name}' wasn't executed in MLI '{self._mli_key}'."
                )

            self._id_explanation_info[explainer_id] = _ExplanationInfo(
                ed.name,
                explainer_keys[0],
                explainer_id,
            )
        return self._id_explanation_info.get(explainer_id)

    def _get_decision_tree_explanation_data(self, filename: str) -> Dict[str, Any]:
        explainer_key = self._get_explanation_info(self.DT_ID).explainer_key
        server_path = (
            f"{self._client.server.username}/"
            f"mli_experiment_{self._mli_key}/"
            f"explainer_h2oaicore_mli_byor_recipes_surrogates_dt_surrogate_explainer_"
            f"DecisionTreeSurrogateExplainer_{explainer_key}/"
            f"global_decision_tree/application_json/{filename}"
        )
        return self._client._get_file(server_path).json()

    @staticmethod
    def _get_decision_tree_vega_plot(
        data: List[Dict[str, Any]], plot_metrics_string: str
    ) -> Dict[str, Any]:
        return {
            "title": {"text": plot_metrics_string, "align": "center"},
            "schema": "https://vega.github.io/schema/vega/v3.json",
            "width": 800,
            "height": 300,
            "data": [
                {
                    "name": "tree",
                    "values": data,
                    "transform": [
                        {"type": "stratify", "key": "key", "parentKey": "parent"},
                        {
                            "type": "tree",
                            "method": "tidy",
                            "size": [{"signal": "width"}, {"signal": "height"}],
                            "separation": "true",
                            "as": ["x", "y", "depth", "children"],
                        },
                    ],
                },
                {
                    "name": "links",
                    "source": "tree",
                    "transform": [{"type": "treelinks"}, {"type": "linkpath"}],
                },
            ],
            "marks": [
                {
                    "type": "path",
                    "from": {"data": "links"},
                    "encode": {
                        "update": {
                            "path": {"field": "path"},
                            "strokeWidth": {
                                "signal": "2 + 2 * (datum.target.edge_weight / 0.25)"
                            },
                            "opacity": {"value": 0.5},
                        }
                    },
                },
                {
                    "type": "symbol",
                    "from": {"data": "tree"},
                    "encode": {
                        "enter": {"size": {"value": 200}},
                        "update": {"x": {"field": "x"}, "y": {"field": "y"}},
                    },
                },
                {
                    "type": "text",
                    "from": {"data": "tree"},
                    "encode": {
                        "enter": {
                            "text": {"field": "name"},
                            "fontSize": {"value": 16},
                            "baseline": {"value": "middle"},
                            "angle": {"signal": "datum.children ? 0 : 30"},
                            "opacity": {"value": 1},
                            "limit": {"value": 200},
                        },
                        "update": {
                            "x": {"field": "x"},
                            "y": {"field": "y"},
                            "dx": {"signal": "datum.children ? -10 : 10"},
                            "align": {"signal": "datum.children ? 'right' : 'left'"},
                        },
                    },
                },
                {
                    "type": "text",
                    "from": {"data": "links"},
                    "encode": {
                        "enter": {
                            "text": {"field": "target.edgein"},
                            "baseline": {"value": "middle"},
                            "opacity": {"value": 0.9},
                            "limit": {"value": 200},
                        },
                        "update": {
                            "x": {
                                "signal": "datum.source.x + "
                                "((datum.target.x - datum.source.x) / 2)"
                            },
                            "y": {
                                "signal": "datum.source.y + "
                                "((datum.target.y - datum.source.y) / 2)"
                            },
                            "dx": {
                                "signal": "datum.source.x > datum.target.x ? -5 : 5"
                            },
                            "align": {
                                "signal": "datum.source.x > datum.target.x "
                                "? 'right' : 'left'"
                            },
                        },
                    },
                },
            ],
        }

    @staticmethod
    def _get_metric_info_string(metrics: List[Dict[str, Any]]) -> str:
        info_strings = []

        for metric in metrics:
            for key, value in metric.items():
                info_strings.append(f"{key}: {value}")

        return ",".join(info_strings)

    @staticmethod
    def _get_pdp_histogram_values(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for index, point in enumerate(data):
            if index != len(data) - 1:
                point["x_continuous"] = data[index + 1]["x"]

            if point["frequency"] is None:
                point["frequency"] = 0

        return data

    def _get_pdp_explanation_data(self, filename: str) -> Dict[str, Any]:
        explainer_key = self._get_explanation_info(self.PD_ID).explainer_key
        server_path = (
            f"{self._client.server.username}/"
            f"mli_experiment_{self._mli_key}/"
            f"explainer_h2oaicore_mli_byor_recipes_dai_pd_ice_explainer_"
            f"DaiPdIceExplainer_{explainer_key}/"
            f"global_partial_dependence/application_json/{filename}"
        )
        return self._client._get_file(server_path).json()

    def _get_pdp_local_result(
        self,
        default_pd_type: str,
        feature: str,
        class_name: str,
        row_number: int,
        pd_type: str = None,
    ) -> Dict[str, Any]:
        explanation_filter = [
            self._client._server_module.messages.FilterEntry(
                filter_by="explain_feature", value=feature
            ),
            self._client._server_module.messages.FilterEntry(
                filter_by="explain_class", value=class_name
            ),
        ]
        if default_pd_type == "numeric" and pd_type == "categorical":
            explanation_filter.append(
                self._client._server_module.messages.FilterEntry(
                    filter_by="explain_numcat", value=""
                )
            )
        local_result = self._client._backend.get_explainer_local_result(
            explainer_job_key=self._get_explanation_info(self.PD_ID).explainer_key,
            explanation_filter=explanation_filter,
            explanation_format="application/vnd.h2oai.json+datatable.jay",
            explanation_type="local-individual-conditional-explanation",
            id_column_name="",
            id_column_value=str(row_number),
            mli_key=self._mli_key,
            page_size=0,
            page_offset=0,
            result_format="application/vnd.h2oai.json+datatable.jay",
            row_limit=1,
        )
        return eval(local_result)

    @staticmethod
    def _get_pdp_vega_plot_categorical(
        name: str,
        data: List[Any],
        prediction_value: int,
        x_axis: str,
        y_axis: str,
        feature: str,
    ) -> Dict[str, Any]:
        plot_data: Dict[str, Any] = {
            "title": name,
            "schema": "https://vega.github.io/schema/vega-lite/v3.json",
            "vconcat": [
                {
                    "width": 800,
                    "height": 300,
                    "data": {"values": data[0]},
                    "layer": [
                        {
                            "mark": {"type": "bar", "opacity": 0.2},
                            "encoding": {
                                "x": {
                                    "field": x_axis,
                                    "type": "ordinal",
                                    "title": feature,
                                },
                                "y": {
                                    "field": "band_top",
                                    "type": "quantitative",
                                    "title": "Average prediction",
                                },
                                "y2": {
                                    "field": "band_bottom",
                                    "type": "quantitative",
                                    "title": "",
                                },
                                "tooltip": [
                                    {"field": "bin", "type": "ordinal"},
                                    {
                                        "field": "pd",
                                        "type": "quantitative",
                                        "title": "Average prediction",
                                    },
                                    {
                                        "field": "sd",
                                        "type": "quantitative",
                                        "title": "Standard deviation",
                                    },
                                ],
                            },
                        },
                        {
                            "mark": {"type": "point"},
                            "encoding": {
                                "y": {"field": y_axis, "type": "quantitative"},
                                "x": {"field": x_axis, "type": "ordinal"},
                            },
                        },
                        {
                            "data": {"values": data[1]},
                            "mark": "point",
                            "encoding": {
                                "x": {
                                    "field": "bin",
                                    "type": "ordinal",
                                    "title": feature,
                                },
                                "y": {
                                    "field": "ice",
                                    "type": "quantitative",
                                    "title": "Average prediction",
                                },
                                "color": {"value": "grey"},
                                "tooltip": [
                                    {"field": "bin", "type": "ordinal"},
                                    {"field": "ice", "type": "quantitative"},
                                ],
                            },
                        },
                    ],
                },
                {
                    "width": 800,
                    "height": 100,
                    "data": {"values": data[2]},
                    "mark": {"type": "bar"},
                    "encoding": {
                        "x": {
                            "field": "x",
                            "type": "ordinal",
                            "title": "x",
                            "scale": {"zero": "", "nice": ""},
                        },
                        "y": {"field": "frequency", "type": "quantitative"},
                        "tooltip": [{"field": "frequency", "type": "quantitative"}],
                    },
                    "config": {"binSpacing": 0},
                },
            ],
        }

        if prediction_value is not None:
            plot_data["vconcat"][0]["layer"].append(
                {
                    "mark": {"type": "rule", "strokeDash": [4, 4]},
                    "encoding": {
                        "y": {"datum": prediction_value},
                        "color": {"value": "red"},
                    },
                }
            )

        return plot_data

    @staticmethod
    def _get_pdp_vega_plot_numerical(
        name: str,
        data: List[Any],
        prediction_value: int,
        x_axis: str,
        y_axis: str,
        feature: str,
        is_temporal: bool,
    ) -> Dict[str, Any]:

        x_data_type = "temporal" if is_temporal else "quantitative"

        plot_data: Dict[str, Any] = {
            "title": name,
            "schema": "https://vega.github.io/schema/vega-lite/v3.json",
            "vconcat": [
                {
                    "width": 800,
                    "height": 300,
                    "data": {"values": data[0]},
                    "layer": [
                        {
                            "mark": "errorband",
                            "encoding": {
                                "y": {
                                    "field": "band_top",
                                    "type": "quantitative",
                                    "scale": {"zero": ""},
                                    "title": "",
                                },
                                "y2": {"field": "band_bottom", "title": ""},
                                "x": {
                                    "field": x_axis,
                                    "axis": "",
                                    "type": x_data_type,
                                },
                                "tooltip": "",
                            },
                        },
                        {
                            "mark": {"type": "line"},
                            "encoding": {
                                "x": {
                                    "field": x_axis,
                                    "type": x_data_type,
                                    "title": feature,
                                    "scale": {"zero": "", "nice": ""},
                                },
                                "y": {
                                    "field": y_axis,
                                    "type": "quantitative",
                                    "title": "Average prediction",
                                },
                                "color": {"field": "oor", "legend": {"disable": True}},
                            },
                        },
                        {
                            "data": {"values": data[1]},
                            "encoding": {
                                "x": {
                                    "field": "bin",
                                    "type": x_data_type,
                                    "scale": {"zero": "", "nice": ""},
                                },
                                "y": {
                                    "field": "ice",
                                    "type": "quantitative",
                                    "title": "Average prediction",
                                },
                                "color": {"value": "grey"},
                                "tooltip": [
                                    {"field": "bin", "type": "ordinal"},
                                    {"field": "ice", "type": "quantitative"},
                                ],
                            },
                            "layer": [
                                {
                                    "mark": {"type": "line"},
                                },
                                {
                                    "mark": {"type": "point"},
                                },
                            ],
                        },
                        {
                            "mark": {"type": "point"},
                            "encoding": {
                                "x": {
                                    "field": x_axis,
                                    "type": x_data_type,
                                    "title": "",
                                    "scale": {"zero": "", "nice": ""},
                                },
                                "y": {
                                    "field": y_axis,
                                    "type": "quantitative",
                                    "title": "",
                                },
                                "tooltip": [
                                    {"field": "bin", "type": "quantitative"},
                                    {
                                        "field": "pd",
                                        "type": "quantitative",
                                        "title": "Average prediction",
                                    },
                                    {
                                        "field": "sd",
                                        "type": "quantitative",
                                        "title": "Standard deviation",
                                    },
                                ],
                                "color": {"field": "oor"},
                            },
                        },
                    ],
                },
                {
                    "width": 800,
                    "height": 100,
                    "data": {"values": data[2]},
                    "mark": {"type": "bar", "orient": "vertical"},
                    "encoding": {
                        "x": {
                            "field": "x",
                            "type": x_data_type,
                            "title": "x",
                            "scale": {"zero": "", "nice": ""},
                        },
                        "x2": {
                            "field": "x_continuous",
                            "type": x_data_type,
                            "axis": "",
                        },
                        "y": {"field": "frequency", "type": "quantitative"},
                    },
                },
            ],
        }

        if prediction_value is not None:
            plot_data["vconcat"][0]["layer"].append(
                {
                    "mark": {"type": "rule", "strokeDash": [4, 4]},
                    "encoding": {
                        "y": {"datum": prediction_value},
                        "color": {"value": "red"},
                    },
                }
            )
        return plot_data

    def _pdp_compute(self, feature: str) -> Dict[str, Any]:
        interpret_summary = self._client._backend.get_interpretation_summary(
            self._mli_key
        )

        parameters = interpret_summary.parameters
        validset = self._client._server_module.DatasetReference("", display_name="")
        common_params = self._client._server_module.messages.CommonExplainerParameters(
            target_col=parameters.target_col,
            weight_col=parameters.weight_col,
            prediction_col=parameters.prediction_col,
            drop_cols=parameters.drop_cols,
            sample_num_rows=parameters.sample_num_rows,
        )

        run_job_key = self._client._backend.update_explainer_global_result(
            mli_key=self._mli_key,
            explainer_job_key=self._get_explanation_info(self.PD_ID).explainer_key,
            params=self._client._server_module.messages.CommonDaiExplainerParameters(
                common_params=common_params,
                model=parameters.dai_model,
                dataset=parameters.dataset,
                validset=validset,
                testset=parameters.testset,
                use_raw_features=parameters.use_raw_features,
                config_overrides=parameters.config_overrides,
                sequential_execution=True,
                debug_model_errors=parameters.debug_model_errors,
                debug_model_errors_class=parameters.debug_model_errors_class,
            ),
            explainer_params=json.dumps({"features": [feature]}),
            explanation_type="global-partial-dependence",
            explanation_format="application/json",
            update_params=json.dumps(
                {
                    "update_scope": "numcat",
                    "update_merge": "merge",
                    "params_source": "inherit",
                }
            ),
        )

        while True:
            explainer_run_job = self._client._backend.get_explainer_run_job(run_job_key)
            if not _commons.is_server_job_running(explainer_run_job.status):
                break

        return self._get_pdp_explanation_data("explanation.json")

    def _get_shapley_explanation_data(
        self, explanation: _ExplanationInfo, filename: str
    ) -> Dict[str, Any]:
        if "Transformed" in explanation.explainer_name:
            explainer_name = "transformed_shapley_explainer_TransformedShapleyExplainer"
        else:
            explainer_name = "original_contrib_explainer_NaiveShapleyExplainer"
        server_path = (
            f"{self._client.server.username}/"
            f"mli_experiment_{self._mli_key}/"
            f"explainer_h2oaicore_mli_byor_recipes_{explainer_name}_"
            f"{explanation.explainer_key}/"
            f"global_feature_importance/application_json/"
            f"{filename}"
        )
        return self._client._get_file(server_path).json()

    def _get_shapley_summary_explanation_data(self, filename: str) -> Dict[str, Any]:
        server_path = (
            f"{self._client.server.username}/"
            f"mli_experiment_{self._mli_key}/"
            f"explainer_h2oaicore_mli_byor_recipes_shapley_summary_explainer_"
            f"ShapleySummaryOrigFeatExplainer_"
            f"{self._get_explanation_info(self.SHAP_SUM_ID).explainer_key}/"
            f"global_summary_feature_importance/application_json/{filename}"
        )
        return self._client._get_file(server_path).json()

    @staticmethod
    def _get_shapley_summary_vega_plot(
        data_avg_is_none: List[Dict[str, Any]],
        data_avg_higher_than_zero: List[Dict[str, Any]],
        plot_metrics_info: str,
    ) -> Dict[str, Any]:
        return {
            "title": {
                "text": plot_metrics_info,
                "align": "right",
            },
            "schema": "https://vega.github.io/schema/vega-lite/v3.json",
            "width": 700,
            "height": 250,
            "data": {"values": data_avg_higher_than_zero},
            "layer": [
                {
                    "mark": "circle",
                    "encoding": {
                        "x": {"field": "shapley_value", "type": "quantitative"},
                        "y": {"field": "feature", "type": "ordinal", "sort": "-x"},
                        "color": {
                            "field": "avg_high_value",
                            "type": "quantitative",
                            "title": "Normalized feature value",
                            "condition": {
                                "value": "transparent",
                                "test": "datum.count === 0",
                            },
                        },
                        "tooltip": [
                            {"field": "feature", "type": "nominal"},
                            {
                                "field": "shapley_value",
                                "type": "quantitative",
                                "title": "Shapley value",
                            },
                            {
                                "field": "count",
                                "type": "quantitative",
                                "title": "Bin count",
                            },
                            {
                                "field": "avg_high_value",
                                "type": "quantitative",
                                "title": "Avg. normalized feature value",
                            },
                        ],
                    },
                },
                {
                    "data": {"values": data_avg_is_none},
                    "mark": "circle",
                    "encoding": {
                        "x": {"field": "shapley_value", "type": "quantitative"},
                        "y": {
                            "field": "feature",
                            "type": "ordinal",
                            "sort": "-x",
                            "axis": {"grid": "true"},
                        },
                        "color": {
                            "condition": {
                                "value": "transparent",
                                "test": "datum.count === 0",
                            },
                            "value": "grey",
                        },
                        "tooltip": [
                            {"field": "feature", "type": "nominal"},
                            {
                                "field": "shapley_value",
                                "type": "quantitative",
                                "title": "Shapley value",
                            },
                            {
                                "field": "count",
                                "type": "quantitative",
                                "title": "Bin count",
                            },
                        ],
                    },
                },
            ],
        }

    def _get_shapley_values(
        self,
        explanation: _ExplanationInfo,
        row_number: int = None,
        class_name: str = None,
    ) -> Dict[str, Any]:
        plot_info = self._get_shapley_explanation_data(explanation, "explanation.json")

        available_classes = list(plot_info["files"].keys())
        if class_name is None:
            class_name = available_classes[0]  # default class name
        else:
            if class_name not in available_classes:
                raise ValueError(
                    f"Invalid class name '{class_name}'. "
                    f"Possible values are {available_classes}."
                )

        if row_number is not None:
            if row_number < 0:
                raise ValueError("Row number must be a positive integer.")

            local_result = self._client._backend.get_explainer_local_result(
                explainer_job_key=explanation.explainer_key,
                explanation_filter=[
                    self._client._server_module.messages.FilterEntry(
                        filter_by="explain_feature", value=""
                    ),
                    self._client._server_module.messages.FilterEntry(
                        filter_by="explain_class", value=class_name
                    ),
                ],
                explanation_format="application/vnd.h2oai.json+datatable.jay",
                explanation_type="local-feature-importance",
                id_column_name="",
                id_column_value=str(row_number),
                mli_key=self._mli_key,
                page_size=0,
                page_offset=0,
                result_format="application/vnd.h2oai.json+datatable.jay",
                row_limit=1,
            )
            data_points = eval(local_result)["data"]
            bias = eval(local_result)["bias"]

            # format the label into the format of `<Feature> = <Feature value>`
            if "Original" in explanation.explainer_name:
                for index, point in enumerate(data_points):
                    label_name = point["label"]
                    for point_ in data_points[index + 1 :]:
                        if point_["label"] == label_name:
                            point_["label"] = (
                                f"{point_['label']} = " f"{point_['feature_value']}"
                            )
                            point["label"] = (
                                f"{point['label']} = " f"{point_['feature_value']}"
                            )
                            break

        else:
            explainer_data = self._get_shapley_explanation_data(
                explanation, plot_info["files"][class_name]
            )

            data_points = explainer_data["data"]
            bias = explainer_data["bias"]

        for point in data_points:
            point["value"] = round(point["value"], 6)
            point["value+bias"] = point["value"] + bias

        plot_metrics_string = self._get_metric_info_string(plot_info["metrics"])

        return self._get_shapley_vega_plot(
            data=data_points,
            x_axis="value",
            y_axis="label",
            plot_metrics_string=plot_metrics_string,
            height=len(data_points) * 30,
        )

    def _get_shapley_vega_plot(
        self,
        data: Dict[str, Any],
        x_axis: str,
        y_axis: str,
        plot_metrics_string: str,
        width: int = 600,
        height: int = 600,
    ) -> Dict[str, Any]:
        return {
            "title": {"text": plot_metrics_string, "align": "right"},
            "schema": "https://vega.github.io/schema/vega-lite/v3.json",
            "width": width,
            "height": height,
            "data": {"values": data},
            "encoding": {
                "y": {
                    "field": y_axis,
                    "type": "nominal",
                    "sort": {"field": "x", "op": "average"},
                    "title": "Feature name",
                },
                "x": {
                    "field": x_axis,
                    "type": "quantitative",
                    "title": "shapley value",
                },
                "color": {"field": "scope"},
                "yOffset": {"field": "scope"},
                "tooltip": [
                    {"field": y_axis, "type": "nominal", "title": "Feature name"},
                    {"field": x_axis, "type": "quantitative"},
                    {"field": "value+bias", "type": "quantitative"},
                ],
            },
            "layer": [
                {"mark": "bar"},
                {
                    "mark": {
                        "type": "text",
                        "align": "left",
                        "baseline": "middle",
                        "dx": 5,
                    },
                    "encoding": {"text": {"field": x_axis, "type": "quantitative"}},
                },
            ],
        }

    def partial_dependence_plot(
        self,
        partial_dependence_type: str = None,
        feature_name: str = None,
        class_name: str = None,
        row_number: int = None,
    ) -> Dict[str, Any]:
        """Partial dependence plot of this interpretation.

        Args:
            partial_dependence_type: type of the partial dependence
                                    (either `categorical` or `numeric`)
            feature_name: feature name
            class_name: name of the class
            row_number: row number

        Returns:
            a partial dependence plot
                in Vega Lite (v3) format
        """
        pdp_features = self._get_pdp_explanation_data("explanation.json")

        available_features = list(pdp_features["features"].keys())
        if feature_name is None:
            feature_name = available_features[0]
        else:
            if feature_name not in available_features:
                raise ValueError(
                    f"Invalid feature name '{feature_name}'. "
                    f"Possible values are {available_features}."
                )

        default_pd_type = pdp_features["features"][feature_name]["feature_type"][0]
        if partial_dependence_type is None:
            partial_dependence_type = default_pd_type
        else:
            available_pd_types = ["numeric", "categorical"]
            if partial_dependence_type not in available_pd_types:
                raise ValueError(
                    f"Invalid partial dependency type '{partial_dependence_type}'. "
                    f"Possible values are {available_pd_types}."
                )
            if (
                default_pd_type == "categorical"
                and partial_dependence_type == "numeric"
            ):
                raise ValueError(
                    "Partial dependence type 'numeric' not allowed, only 'categorical'."
                )

        available_classes = list(pdp_features["features"][feature_name]["files"].keys())
        if class_name is None:
            class_name = str(pdp_features["default_class"])
        else:
            if class_name not in available_classes:
                raise ValueError(
                    f"Invalid class name '{class_name}'. "
                    f"Possible values are {available_classes}."
                )

        if row_number is not None and row_number < 0:
            raise ValueError("Row number must be a positive integer.")

        if default_pd_type != partial_dependence_type:
            # recompute feature data for the new PD type
            feature_data = self._pdp_compute(feature_name)
            file_name = feature_data["features"][feature_name]["files_numcat_aspect"][
                class_name
            ]
        else:
            file_name = pdp_features["features"][feature_name]["files"][class_name]

        pdp_explanation = self._get_pdp_explanation_data(file_name)

        for index, point in enumerate(pdp_explanation["data"]):
            if not point["oor"]:
                # point not out of range
                point["band_top"] = point["pd"] + point["sd"]
                point["band_bottom"] = point["pd"] - point["sd"]

        local_result: Dict[str, Any] = {"prediction": None, "data": []}

        # obtains the local result if a row number is provided.
        if row_number is not None:
            local_result = self._get_pdp_local_result(
                default_pd_type,
                feature_name,
                class_name,
                row_number,
                partial_dependence_type,
            )
            for index, point in enumerate(local_result["data"]):
                if isinstance(point["bin"], str) and point["bin"].isdigit():
                    point["bin"] = float(point["bin"])

        if partial_dependence_type == "numeric":
            histogram_data = self._get_pdp_histogram_values(
                pdp_explanation["data_histogram_numerical"]
            )
            return self._get_pdp_vega_plot_numerical(
                name="Partial dependence plot",
                data=[pdp_explanation["data"], local_result["data"], histogram_data],
                prediction_value=local_result["prediction"],
                x_axis="bin",
                y_axis="pd",
                feature=feature_name,
                is_temporal="time" in feature_name.lower(),
            )
        else:
            # partial_dependence_type is categorical
            return self._get_pdp_vega_plot_categorical(
                name="Partial dependence plot",
                data=[
                    pdp_explanation["data"],
                    local_result["data"],
                    pdp_explanation["data_histogram_categorical"],
                ],
                prediction_value=local_result["prediction"],
                x_axis="bin",
                y_axis="pd",
                feature=feature_name,
            )

    def shapley_summary_plot_for_original_features(
        self, class_name: str = None
    ) -> Dict[str, Any]:
        """
        Shapley summary plot for original features of this interpretation

        Args:
            class_name: class name

        Returns:
            a shapley summary plot for original features
                in Vega Lite (v3) format
        """

        plot_info = self._get_shapley_summary_explanation_data("explanation.json")

        available_classes = list(plot_info["files"].keys())
        if class_name is None:
            class_name = str(plot_info["default_class"])  # default class name
        else:
            if class_name not in available_classes:
                raise ValueError(
                    f"Invalid class name '{class_name}'. "
                    f"Possible values are {available_classes}."
                )

        data_points = self._get_shapley_summary_explanation_data(
            list(plot_info["files"][class_name].values())[0]
        )["data"]
        data_avg_higher_than_zero = []
        data_avg_is_none = []
        for index, point in enumerate(data_points):
            if point["avg_high_value"] is None:
                point.pop("avg_high_value")
                data_avg_is_none.append(point)
            else:
                data_avg_higher_than_zero.append(data_points[index])

        plot_metrics_info = self._get_metric_info_string(plot_info["metrics"])
        return self._get_shapley_summary_vega_plot(
            data_avg_is_none, data_avg_higher_than_zero, plot_metrics_info
        )

    def shapley_values_for_transformed_features(
        self, class_name: str = None, row_number: int = None
    ) -> Dict[str, Any]:
        """shapley values for transformed features plot of this interpretation.

        Args:
            class_name: class name
            row_number: row number of data

        Returns:
            a shapley values for transformed features plot
             in Vega Lite (v3) format
        """
        return self._get_shapley_values(
            self._get_explanation_info(self.TRANS_SHAP_ID), row_number, class_name
        )

    def shapley_values_for_original_features(
        self, row_number: int = None, class_name: str = None
    ) -> Dict[str, Any]:
        """shapley values for transformed features plot of this interpretation.

        Args:
            row_number: row number
            class_name: class name

        Returns:
            a shapley values for original features plot
             in Vega Lite (v3) format
        """
        return self._get_shapley_values(
            self._get_explanation_info(self.ORIG_SHAP_ID), row_number, class_name
        )

    def surrogate_decision_tree(
        self, row_number: int = None, class_name: str = None
    ) -> Dict[str, Any]:
        """
        Surrogate decision tree of this interpretation.

        Args:
            row_number: row number
            class_name: class name

        Returns:
            a surrogate decision tree in Vega (v3) format

        """
        plot_info = self._get_decision_tree_explanation_data("explanation.json")

        available_classes = list(plot_info["files"].keys())
        if class_name is None:
            class_name = plot_info["default_class"]  # default class name
        else:
            if class_name not in available_classes:
                raise ValueError(
                    f"Invalid class name '{class_name}'. "
                    f"Possible values are {available_classes}."
                )

        if row_number is not None:
            if row_number < 0:
                raise ValueError("Row number must be a positive number.")

            local_result = self._client._backend.get_explainer_local_result(
                explainer_job_key=self._get_explanation_info(self.DT_ID).explainer_key,
                explanation_filter=[
                    self._client._server_module.messages.FilterEntry(
                        filter_by="explain_feature", value=""
                    ),
                    self._client._server_module.messages.FilterEntry(
                        filter_by="explain_class", value=class_name
                    ),
                ],
                explanation_format="application/json",
                explanation_type="local-decision-tree",
                id_column_name="",
                id_column_value=str(row_number),
                mli_key=self._mli_key,
                page_size=0,
                page_offset=0,
                result_format="application/json",
                row_limit=1,
            )
            local_result = local_result.replace("null", '""')
            local_result = local_result.replace("true", '"true"')
            local_result = local_result.replace("false", '""')
            data_points = eval(local_result)["data"]
        else:
            data_points = self._get_decision_tree_explanation_data(
                plot_info["files"][class_name]
            )["data"]

        plot_metrics_string = self._get_metric_info_string(plot_info["metrics"])
        return self._get_decision_tree_vega_plot(data_points, plot_metrics_string)


class Interpretation(_commons.ServerJob):
    """Interact with an MLI interpretation on the Driverless AI server."""

    def __init__(
        self,
        client: "_core.Client",
        key: str,
        update_method: Callable[[str], Any],
        url_method: Callable[["Interpretation"], str],
    ) -> None:
        # super() calls _update() which relies on _update_method()
        self._update_method = update_method
        super().__init__(client=client, key=key)
        self._artifacts: Optional[InterpretationArtifacts] = None
        self._dataset: Optional[_datasets.Dataset] = None
        self._experiment: Optional[_experiments.Experiment] = None
        self._explainer_list: Optional[ExplainerList] = None
        self._settings: Optional[Dict[str, Any]] = None
        self._url = url_method(self)

    @property
    def artifacts(self) -> "InterpretationArtifacts":
        """Interact with artifacts that are created when the
        interpretation completes."""
        if not self._artifacts:
            self._artifacts = InterpretationArtifacts(
                self._client, self._get_raw_info()
            )
        return self._artifacts

    @property
    def creation_timestamp(self) -> float:
        """Creation timestamp in seconds since the epoch (POSIX timestamp)."""
        return self._get_raw_info().created

    @property
    def dataset(self) -> Optional[_datasets.Dataset]:
        """Dataset for the interpretation."""
        if not self._dataset:
            if hasattr(self._get_raw_info().entity.parameters, "dataset"):
                try:
                    self._dataset = self._client.datasets.get(
                        self._get_raw_info().entity.parameters.dataset.key
                    )
                except self._client._server_module.protocol.RemoteError:
                    # assuming a key error means deleted dataset, if not the error
                    # will still propagate to the user else where
                    self._dataset = (
                        self._get_raw_info().entity.parameters.dataset.dump()
                    )
            else:
                # timeseries sometimes doesn't have dataset attribute
                try:
                    self._dataset = self.experiment.datasets["train_dataset"]
                except self._client._server_module.protocol.RemoteError:
                    # assuming a key error means deleted dataset, if not the error
                    # will still propagate to the user else where
                    self._dataset = None
        return self._dataset

    @property
    def experiment(self) -> Optional[_experiments.Experiment]:
        """Experiment for the interpretation."""
        if not self._experiment:
            try:
                self._experiment = self._client.experiments.get(
                    self._get_raw_info().entity.parameters.dai_model.key
                )
            except self._client._server_module.protocol.RemoteError:
                # assuming a key error means deleted experiment, if not the error
                # will still propagate to the user else where
                self._experiment = None
        return self._experiment

    @property
    @_utils.beta
    @_utils.min_supported_dai_version("1.10.5")
    def explainers(self) -> Sequence["Explainer"]:
        """Explainers that were ran as an ``ExplainerList`` object."""
        if self._explainer_list is None:
            try:
                job_statuses = self._client._backend.get_explainer_job_statuses(
                    self.key, []
                )
            except self._client._server_module.protocol.RemoteError:
                self._explainer_list = None
            else:
                explainer_infos = [
                    _ExplainerInfo(
                        key=js.explainer_job_key, name=js.explainer_job.entity.name
                    )
                    for js in job_statuses
                ]
                self._explainer_list = ExplainerList(
                    explainer_infos=explainer_infos,
                    client=self._client,
                    mli_key=self.key,
                )
        return self._explainer_list

    @property
    @_utils.beta
    @_utils.min_supported_dai_version("1.10.5")
    def explanation_plots(self) -> "ExplanationPlots":
        """Explanations that were created for the interpretation."""
        return ExplanationPlots(
            client=self._client,
            mli_key=self.key,
        )

    @property
    def run_duration(self) -> Optional[float]:
        """Run duration in seconds."""
        self._update()
        try:
            return self._get_raw_info().entity.training_duration
        except AttributeError:
            _logging.logger.warning(
                "Run duration not available for some time series interpretations."
            )
            return None

    @property
    def settings(self) -> Dict[str, Any]:
        """Interpretation settings."""
        if not _utils.is_server_version_less_than(self._client, "1.9.1"):
            raise RuntimeError(
                "Settings cannot be retrieved from server versions >= 1.9.1."
            )
        if not self._settings:
            self._settings = self._client.mli._parse_server_settings(
                self._get_raw_info().entity.parameters.dump()
            )
        return self._settings

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    def _update(self) -> None:
        self._set_raw_info(self._update_method(self.key))
        self._set_name(self._get_raw_info().entity.description)

    def delete(self) -> None:
        """Delete MLI interpretation on Driverless AI server."""
        key = self.key
        self._client._backend.delete_interpretation(key)
        _logging.logger.info(
            "Driverless AI Server reported interpretation {key} deleted."
        )

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the interpretation's page on the Driverless AI server."""
        return _utils.Hyperlink(self._url)

    def rename(self, name: str) -> "Interpretation":
        """Change interpretation display name.

        Args:
            name: new display name
        """
        self._client._backend.update_mli_description(self.key, name)
        self._update()
        return self

    def result(self, silent: bool = False) -> "Interpretation":
        """Wait for job to complete, then return an Interpretation object."""
        self._wait(silent)
        return self


class InterpretationArtifacts(Artifacts):
    """Interact with files created by an MLI interpretation on the
    Driverless AI server."""

    def __init__(self, client: "_core.Client", info: Any) -> None:
        paths = {
            "lime": getattr(info.entity, "lime_rc_csv_path", ""),
            "python_pipeline": getattr(info.entity, "scoring_package_path", ""),
        }
        super().__init__(client=client, paths=paths)
        self._key = info.entity.key
        if not _utils.is_server_version_less_than(self._client, "1.10.4"):
            self._paths["log"] = self._get_artifact(
                self._client._backend.get_interpretation_zipped_logs_url_path
            )

        if not _utils.is_server_version_less_than(self._client, "1.10.0"):
            self._paths["shapley_transformed_features"] = self._get_artifact(
                self._client._backend.get_transformed_shapley_zip_archive_url
            )

        if _utils.is_server_version_less_than(self._client, "1.9.2"):
            if not _utils.is_server_version_less_than(self._client, "1.9.1"):
                self._paths[
                    "shapley_original_features"
                ] = self._client._backend.get_orig_shapley_zip_archive_url(self._key)
        else:
            self._paths[
                "shapley_original_features"
            ] = self._client._backend.get_orig_shapley_zip_archive_url(self._key, False)

    @property
    def file_paths(self) -> Dict[str, str]:
        """Paths to interpretation artifact files on the server."""
        return self._paths

    def _get_artifact(self, artifact_method: Callable) -> Optional[str]:
        try:
            return artifact_method(self._key)
        except self._client._server_module.protocol.RemoteError:
            return ""

    def download(
        self,
        only: Union[str, List[str]] = None,
        dst_dir: str = ".",
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Download interpretation artifacts from the Driverless AI server. Returns
        a dictionary of relative paths for the downloaded artifacts.

        Args:
            only: specify specific artifacts to download, use
                ``interpretation.artifacts.list()`` to see the available
                artifacts on the Driverless AI server
            dst_dir: directory where interpretation artifacts will be saved
            file_system: FSSPEC based file system to download to,
                instead of local file system
            overwrite: overwrite existing files
        """
        return self._download(
            only=only, dst_dir=dst_dir, file_system=file_system, overwrite=overwrite
        )

    def list(self) -> List[str]:
        """List of interpretation artifacts that exist on the Driverless AI server."""
        return self._list()


class InterpretationMethods:
    """Methods for retrieving different interpretation types on the
    Driverless AI server."""

    def __init__(
        self,
        client: "_core.Client",
        list_method: Callable[[int, int], Any],
        update_method: Callable[[str], Any],
        url_method: Callable[[Interpretation], str],
    ):
        self._client = client
        self._list = list_method
        self._update = update_method
        self._url_method = url_method

    def _lazy_get(self, key: str) -> "Interpretation":
        """Initialize an Interpretation object but don't request information
        from the server (possible for interpretation key to not exist on server).
        Useful for populating lists without making a bunch of network calls.

        Args:
            key: Driverless AI server's unique ID for the MLI interpretation
        """
        return Interpretation(self._client, key, self._update, self._url_method)

    def get(self, key: str) -> "Interpretation":
        """Get an Interpretation object corresponding to an MLI interpretation
        on the Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the MLI interpretation
        """
        interpretation = self._lazy_get(key)
        interpretation._update()
        return interpretation

    def list(
        self, start_index: int = 0, count: int = None
    ) -> Sequence["Interpretation"]:
        """List of Interpretation objects available to the user.

        Args:
            start_index: index on Driverless AI server of first interpretation to list
            count: max number of interpretations to request from the
                Driverless AI server
        """
        if count:
            data = self._list(start_index, count)
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._list(page_position, page_size)
                data += page
                if len(page) < page_size:
                    break
                page_position += page_size
        return _commons.ServerObjectList(
            data=data,
            get_method=self._lazy_get,
            item_class_name=Interpretation.__name__,
        )


class IIDMethods(InterpretationMethods):
    pass


class TimeseriesMethods(InterpretationMethods):
    pass


class MLI:
    """Interact with MLI interpretations on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self._config_items = self._create_config_item()
        self._default_interpretation_settings = {
            name: c.default for name, c in self._config_items.items()
        }
        # legacy settings that should still be accepted
        self._default_legacy_interpretation_settings = {
            "sample_num_rows": -1,
            "dt_tree_depth": 3,
            "klime_cluster_col": "",
            "qbin_cols": [],
            "dia_cols": [],
            "pd_features": None,
            "debug_model_errors": False,
            "debug_model_errors_class": "False",
        }
        interpretation_url_path = getattr(
            self._client._backend, "interpretation_url_path", "/#/interpret_next"
        )
        ts_interpretation_url_path = getattr(
            self._client._backend, "ts_interpretation_url_path", "/mli-ts"
        )
        self._iid = IIDMethods(
            client=client,
            list_method=lambda x, y: client._backend.list_interpretations(x, y).items,
            update_method=client._backend.get_interpretation_job,
            url_method=lambda x: (
                f"{self._client.server.address}"
                f"{interpretation_url_path}"
                f"?interpret_key={x.key}"
            ),
        )
        self._timeseries = TimeseriesMethods(
            client=client,
            list_method=client._backend.list_interpret_timeseries,
            update_method=client._backend.get_interpret_timeseries_job,
            url_method=lambda x: (
                f"{self._client.server.address}"
                f"{ts_interpretation_url_path}"
                f"?model={x._get_raw_info().entity.parameters.dai_model.key}"
                f"&interpret_key={x.key}"
            ),
        )
        # convert setting name from key to value
        self._setting_for_server_dict = {
            "target_column": "target_col",
            "prediction_column": "prediction_col",
            "weight_column": "weight_col",
            "drop_columns": "drop_cols",
            "klime_cluster_column": "klime_cluster_col",
            "dia_columns": "dia_cols",
            "qbin_columns": "qbin_cols",
        }
        self._setting_for_api_dict = {
            v: k for k, v in self._setting_for_server_dict.items()
        }
        create_sig, create_async_sig = self._get_create_method_signature()
        _commons_mli.update_method_doc(
            obj=self, method_to_update="create", new_signature=create_sig
        )
        _commons_mli.update_method_doc(
            obj=self, method_to_update="create_async", new_signature=create_async_sig
        )

    @property
    def iid(self) -> IIDMethods:
        """Retrieve IID interpretations."""
        return self._iid

    @property
    def timeseries(self) -> TimeseriesMethods:
        """Retrieve timeseries interpretations."""
        if _utils.is_server_version_less_than(self._client, "1.10.0"):
            return self._timeseries
        raise _exceptions.NotSupportedByServer(
            "Timeseries is now an explainer and it's part "
            "of IID interpretation, use the property iid."
        )

    def _common_dai_explainer_params(
        self,
        experiment_key: str,
        target_column: str,
        dataset_key: str,
        validation_dataset_key: str = "",
        test_dataset_key: str = "",
        **kwargs: Any,
    ) -> Any:
        return self._client._server_module.messages.CommonDaiExplainerParameters(
            common_params=self._client._server_module.CommonExplainerParameters(
                target_col=target_column,
                weight_col=kwargs.get("weight_col", ""),
                prediction_col=kwargs.get("prediction_col", ""),
                drop_cols=kwargs.get("drop_cols", []),
                sample_num_rows=kwargs.get("sample_num_rows", -1),
            ),
            model=self._client._server_module.ModelReference(experiment_key),
            dataset=self._client._server_module.DatasetReference(dataset_key),
            validset=self._client._server_module.DatasetReference(
                validation_dataset_key
            ),
            testset=self._client._server_module.DatasetReference(test_dataset_key),
            use_raw_features=kwargs["use_raw_features"],
            config_overrides=kwargs["config_overrides"],
            sequential_execution=True,
            debug_model_errors=kwargs.get("debug_model_errors", False),
            debug_model_errors_class=kwargs.get("debug_model_errors_class", "False"),
        )

    def _create_config_item(self) -> Dict[str, _commons_mli.ConfigItem]:
        config_items: Dict[str, _commons_mli.ConfigItem] = {}

        def _construct_config_item_tuple(
            dai_config_item: Any,
        ) -> Tuple[str, _commons_mli.ConfigItem]:
            alias = (
                dai_config_item.name[4:]
                if dai_config_item.name.startswith("mli_")
                else dai_config_item.name
            )
            ci = _commons_mli.ConfigItem.create_from_dai_config_item(
                dai_config_item=dai_config_item, alias=alias
            )
            return ci.name, ci

        if _utils.is_server_version_less_than(self._client, "1.10.0"):
            config_items.update(
                {ci.name: ci for ci in _commons_mli.get_legacy_mli_config_options()}
            )

        config_items.update(
            dict(
                _construct_config_item_tuple(c)
                for c in self._client._backend.get_all_config_options()
                if "mli" in c.tags
            )
        )
        return config_items

    def _create_iid_interpretation_async(
        self,
        experiment: Optional[_experiments.Experiment] = None,
        explainers: Optional[List[_recipes.ExplainerRecipe]] = None,
        dataset: Optional[_datasets.Dataset] = None,
        test_dataset: Optional[_datasets.Dataset] = None,
        **kwargs: Any,
    ) -> str:
        if experiment and not dataset:
            dataset_key = experiment.datasets["train_dataset"].key
            experiment_key = experiment.key
            target_column = experiment.settings["target_column"]
        elif experiment and dataset:
            dataset_key = dataset.key
            experiment_key = experiment.key
            target_column = experiment.settings["target_column"]
        elif not experiment and dataset:
            dataset_key = dataset.key
            experiment_key = ""
            target_column = kwargs.get("target_col", None)
        else:
            raise ValueError("Must provide an experiment or dataset to run MLI.")

        if test_dataset:
            test_dataset_key = test_dataset.key
        else:
            test_dataset_key = (
                experiment.datasets["test_dataset"].key
                if experiment and experiment.datasets["test_dataset"]
                else ""
            )
        interpret_params = self._client._server_module.InterpretParameters(
            dai_model=self._client._server_module.ModelReference(experiment_key),
            dataset=self._client._server_module.DatasetReference(dataset_key),
            testset=self._client._server_module.DatasetReference(test_dataset_key),
            target_col=target_column,
            prediction_col=kwargs.get("prediction_col", ""),
            weight_col=kwargs.get("weight_col", ""),
            drop_cols=kwargs.get("drop_cols", []),
            # expert settings
            lime_method=kwargs["lime_method"],
            use_raw_features=kwargs["use_raw_features"],
            sample=kwargs["sample"],
            dt_tree_depth=kwargs.get("dt_tree_depth", 3),
            vars_to_pdp=kwargs["vars_to_pdp"],
            nfolds=kwargs["nfolds"],
            qbin_count=kwargs["qbin_count"],
            sample_num_rows=kwargs.get("sample_num_rows", -1),
            klime_cluster_col=kwargs.get("klime_cluster_col", ""),
            dia_cols=kwargs.get("dia_cols", []),
            qbin_cols=kwargs.get("qbin_cols", []),
            debug_model_errors=kwargs.get("debug_model_errors", False),
            debug_model_errors_class=kwargs.get("debug_model_errors_class", "False"),
            config_overrides=kwargs["config_overrides"],
        )
        if not explainers:
            return self._client._backend.run_interpretation(interpret_params)
        else:
            params = self._common_dai_explainer_params(
                experiment_key=experiment_key,
                target_column=target_column,
                dataset_key=dataset_key,
                **kwargs,
            )
            return self._client._backend.run_interpretation_with_explainers(
                explainers=[
                    self._client._server_module.messages.Explainer(
                        e.id, json.dumps(e.settings)
                    )
                    for e in explainers
                ],
                params=params,
                interpret_params=interpret_params,
                display_name="",
            ).mli_key

    def _create_timeseries_interpretation_async(
        self,
        experiment: _experiments.Experiment,
        explainers: Optional[List[_recipes.ExplainerRecipe]] = None,
        dataset: Optional[_datasets.Dataset] = None,
        test_dataset: Optional[_datasets.Dataset] = None,
        **kwargs: Any,
    ) -> str:
        dataset_key = experiment.datasets["train_dataset"].key
        experiment_key = experiment.key
        target_column = experiment.settings["target_column"]
        if dataset:
            dataset_key = dataset.key
        if test_dataset:
            test_dataset_key = test_dataset.key
        else:
            test_dataset_key = (
                experiment.datasets["test_dataset"].key
                if experiment.datasets["test_dataset"]
                else ""
            )
        interpret_params = self._client._server_module.InterpretParameters(
            dataset=self._client._server_module.ModelReference(dataset_key),
            dai_model=self._client._server_module.ModelReference(experiment_key),
            testset=self._client._server_module.DatasetReference(test_dataset_key),
            target_col=target_column,
            use_raw_features=None,
            prediction_col=None,
            weight_col=None,
            drop_cols=None,
            klime_cluster_col=None,
            nfolds=None,
            sample=None,
            qbin_cols=None,
            qbin_count=None,
            lime_method=None,
            dt_tree_depth=None,
            vars_to_pdp=None,
            dia_cols=None,
            debug_model_errors=False,
            debug_model_errors_class="",
            sample_num_rows=kwargs.get("sample_num_rows", -1),
            config_overrides="",
        )
        if not explainers:
            return self._client._backend.run_interpret_timeseries(interpret_params)
        else:
            params = self._common_dai_explainer_params(
                experiment_key=experiment_key,
                target_column=target_column,
                dataset_key=dataset_key,
                test_dataset_key=test_dataset_key,
                **kwargs,
            )
            return self._client._backend.run_interpretation_with_explainers(
                explainers=[
                    self._client._server_module.messages.Explainer(
                        e.id, json.dumps(e.settings)
                    )
                    for e in explainers
                ],
                params=params,
                interpret_params=interpret_params,
                display_name="",
            ).mli_key

    def _get_create_method_signature(
        self,
    ) -> Tuple[inspect.Signature, inspect.Signature]:
        params: List[inspect.Parameter] = []
        for ci in self._config_items.values():
            params.append(ci.to_method_parameter())
        return (
            _commons_mli.get_updated_signature(func=MLI.create, new_params=params),
            _commons_mli.get_updated_signature(
                func=MLI.create_async, new_params=params
            ),
        )

    def _parse_server_settings(self, server_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Driverless AI server interpretation settings to Python API format."""
        blacklist = ["config_overrides", "dai_model", "dataset", "testset"]
        settings: Dict[str, Any] = {}
        if server_settings.get("testset", None) and server_settings["testset"].get(
            "key", ""
        ):
            try:
                settings["test_dataset"] = self._client.datasets.get(
                    server_settings["testset"]["key"]
                )
            except self._client._server_module.protocol.RemoteError:
                # assuming a key error means deleted dataset, if not the error
                # will still propagate to the user else where
                settings["test_dataset"] = server_settings["testset"]
        for key, value in server_settings.items():
            if (
                key not in blacklist
                and value not in [None, "", [], -1]
                and value != self._default_interpretation_settings.get(key)
            ):
                settings[self._setting_for_api_dict.get(key, key)] = value
        if "target_column" not in settings and server_settings["dai_model"]["key"]:
            settings["target_column"] = self._client.experiments.get(
                server_settings["dai_model"]["key"]
            ).settings["target_column"]
        return settings

    def create(
        self,
        experiment: Optional[_experiments.Experiment] = None,
        dataset: Optional[_datasets.Dataset] = None,
        name: Optional[str] = None,
        force: bool = False,
        **kwargs: Any,
    ) -> "Interpretation":
        """Create an MLI interpretation on the Driverless AI server and return
        an Interpretation object corresponding to the created interpretation.

        Args:
            experiment: experiment to interpret, will use training dataset if
                ``dataset`` not specified
            dataset: dataset to use for interpretation
                (if dataset includes target and prediction columns, then an
                experiment is not needed)
            name: display name for the interpretation
            force: create new interpretation even if interpretation with same
                name already exists

        Keyword Args:
            explainers (List[ExplainerRecipe]): list of explainer recipe objects
            test_dataset (Dataset): Dataset object (timeseries only)
            target_column (str): name of column in ``dataset``
            prediction_column (str): name of column in ``dataset``
            weight_column (str): name of column in ``dataset``
            drop_columns (List[str]): names of columns in ``dataset``

        .. note::
            Any expert setting can also be passed as a ``kwarg``.
            To search possible expert settings for your server version,
            use ``mli.search_expert_settings(search_term)``.
        """
        return self.create_async(experiment, dataset, name, force, **kwargs).result()

    def create_async(
        self,
        experiment: Optional[_experiments.Experiment] = None,
        dataset: Optional[_datasets.Dataset] = None,
        name: Optional[str] = None,
        force: bool = False,
        validate_settings: bool = True,
        **kwargs: Any,
    ) -> "Interpretation":
        """Launch creation of an MLI interpretation on the Driverless AI server
        and return an Interpretation object to track the status.

        Args:
            experiment: experiment to interpret, will use training dataset if
                ``dataset`` not specified
            dataset: dataset to use for interpretation
                (if dataset includes target and prediction columns, then an
                experiment is not needed)
            name: display name for the interpretation
            force: create new interpretation even if interpretation with same
                name already exists

        Keyword Args:
            explainers (List[ExplainerRecipe]): list of explainer recipe objects
                (server versions >= 1.9.1)
            test_dataset (Dataset): Dataset object (timeseries only)
            target_column (str): name of column in ``dataset``
            prediction_column (str): name of column in ``dataset``
            weight_column (str): name of column in ``dataset``
            drop_columns (List[str]): names of columns in ``dataset``

        .. note::
            Any expert setting can also be passed as a ``kwarg``.
            To search possible expert settings for your server version,
            use ``mli.search_expert_settings(search_term)``.
        """
        if not force:
            _commons_mli.error_if_interpretation_exists(self._client, name)
        explainers = kwargs.pop("explainers", None)
        if explainers is not None:
            _utils.check_server_support(
                client=self._client,
                minimum_server_version="1.9.1",
                parameter="explainers",
            )
        test_dataset = kwargs.pop("test_dataset", None)
        config_overrides = toml.loads(kwargs.pop("config_overrides", ""))
        settings: Dict[str, Any] = {
            "prediction_col": "",
            "weight_col": "",
            "drop_cols": [],
        }
        if not _utils.is_server_version_less_than(self._client, "1.10.0"):
            settings.update(self._default_legacy_interpretation_settings)
        settings.update(self._default_interpretation_settings)
        for setting, value in kwargs.items():
            server_setting = self._setting_for_server_dict.get(setting, setting)
            if server_setting not in settings:
                raise RuntimeError(f"'{setting}' MLI setting not recognized.")
            ci = self._config_items.get(setting)
            if ci:
                if validate_settings:
                    ci.validate_value(value)
                config_overrides[ci.raw_name] = value
            settings[server_setting] = value
        # add any expert settings to config_override that have to be config override
        config_overrides["mli_pd_features"] = kwargs.get(
            "pd_features", settings.get("pd_features", None)
        )
        if experiment:
            # validate experiment before proceed
            if (
                experiment.is_deprecated
                or not experiment.is_complete()
                or not experiment.datasets["train_dataset"].name
                or not experiment.settings["target_column"]
            ):
                raise ValueError("Can't use a running or unsupervised experiment.")

            experiment_config_overrides = (
                experiment._get_raw_info().entity.parameters.config_overrides
            )
            experiment_config_overrides = toml.loads(experiment_config_overrides)
            experiment_config_overrides.update(config_overrides)
            config_overrides = experiment_config_overrides
        settings["config_overrides"] = toml.dumps(config_overrides)
        is_timeseries = bool(experiment.settings.get("time_column", ""))
        if (
            _utils.is_server_version_less_than(self._client, "1.10.0")
            and is_timeseries
            and explainers is None
        ):
            key = self._create_timeseries_interpretation_async(
                experiment, explainers, dataset, test_dataset, **settings
            )
            update_method = self.timeseries._update
            url_method = self.timeseries._url_method
        else:
            key = self._create_iid_interpretation_async(
                experiment, explainers, dataset, test_dataset, **settings
            )
            update_method = self.iid._update
            url_method = self.iid._url_method
        interpretation = Interpretation(self._client, key, update_method, url_method)
        if name:
            interpretation.rename(name)
        return interpretation

    def gui(self) -> _utils.Hyperlink:
        """Print full URL for the user's MLI page on Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}interpretations"
        )

    def search_expert_settings(
        self,
        search_term: str = "",
        show_description: bool = False,
        show_valid_values: bool = False,
    ) -> _utils.Table:
        """Search expert settings and print results. Useful when looking for
        kwargs to use when creating interpretations.

        Args:
            search_term: term to search for (case-insensitive)
            show_description: include description in results
            show_valid_values: include valid values that can be set for each setting
                in the results
        """
        headers: List[str] = ["Name", "Default Value"]
        if show_valid_values:
            headers.append("Valid Values")
        if show_description:
            headers.append("Description")

        data: List[List[str]] = []
        for name, c in self._config_items.items():
            if c.matches_search_term(search_term):
                row = [
                    self._setting_for_api_dict.get(name, name),
                    str(self._default_interpretation_settings[name.strip()]),
                ]
                if show_valid_values:
                    row.append(c.formatted_valid_values)
                if show_description:
                    row.append(c.formatted_description)
                data.append(row)
        return _utils.Table(headers=headers, data=data)

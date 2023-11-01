"""Server module of official Python client for Driverless AI."""

import re
import urllib.parse
from typing import Any, Dict, List

from driverlessai import _core
from driverlessai import _logging
from driverlessai import _utils


class License:
    """Get information about the Driverless AI server's license."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def _get_info(self) -> Any:
        info = self._client._backend.have_valid_license()
        if info.message:
            _logging.logger.info(info.message)
        return info

    def days_left(self) -> int:
        """Return days left on license.

        Examples::

            dai.server.license.days_left()
        """
        return self._get_info().days_left

    def is_valid(self) -> bool:
        """Return ``True`` if server is licensed.

        Examples::

            dai.server.license.is_valid()
        """
        return self._get_info().is_valid


class Server:
    """Get information about the Driverless AI server.

    Examples::

        # Connect to the DAI server
        dai = driverlessai.Client(
            address='http://localhost:12345',
            username='py',
            password='py'
        )

        dai.server.address
        dai.server.username
        dai.server.version
    """

    def __init__(self, client: "_core.Client", address: str) -> None:
        server_info = client._backend.get_app_version()
        user_info = client._backend.get_current_user_info()

        self._address = address
        self._client = client
        self._license = License(client)
        self._storage_enabled = server_info.enable_storage
        self._username = user_info.name
        self._version = server_info.version

    @property
    def address(self) -> str:
        """URL of the Driverless AI server connected to."""
        return self._address

    @property
    def license(self) -> License:
        """Get information about the license on the Driverless AI server."""
        return self._license

    @property
    def storage_enabled(self) -> bool:
        """Whether the Driverless AI server is connected to H2O.ai Storage."""
        return self._storage_enabled

    @property
    def username(self) -> str:
        """Current user connected as to a Driverless AI server."""
        return self._username

    @property
    def version(self) -> str:
        """Version of Driverless AI server currently connected to."""
        return re.search(r"^([\d.]+)", self._version).group(1)

    @property
    def disk_usage(self) -> Dict[str, int]:
        """Get disk usage(in bytes) of the Driverless AI server."""
        disk_usage = self._client._backend.get_disk_stats()
        return {
            "total": disk_usage.total,
            "available": disk_usage.available,
            "used": disk_usage.total - disk_usage.available,
        }

    @property
    def gpu_usages(self) -> List[Dict[str, float]]:
        """Get GPU statistics of the Driverless AI server."""
        gpu_stats = self._client._backend.get_gpu_stats()

        return [
            {
                "memory": gpu_stats.mems[index],
                "usage": gpu_stats.usages[index],
            }
            for index in range(gpu_stats.gpus)
        ]

    @property
    @_utils.beta
    @_utils.min_supported_dai_version("1.10.6")
    def cpu_usages(self) -> List[float]:
        """Get usage of each CPU of the Driverless AI server."""
        return self._client._backend.get_system_stats(force_cpu=True).per

    @property
    @_utils.min_supported_dai_version("1.10.6")
    def memory_usage(self) -> Dict[str, int]:
        """Get memory statistics(in bytes) of the Driverless AI server."""
        memory_stats = self._client._backend.get_system_stats(force_cpu=True).mem
        return {
            "total": memory_stats.total,
            "available": memory_stats.available,
            "used": memory_stats.total - memory_stats.available,
        }

    @property
    def experiment_stats(self) -> Dict[str, int]:
        """Get experiments related statistics of the Driverless AI server."""
        experiment_stats = self._client._backend.get_experiments_stats()
        return {
            "total": experiment_stats.total,
            "my_experiments_total": experiment_stats.my_total,
            "my_experiments_running": experiment_stats.my_running,
        }

    @property
    @_utils.beta
    @_utils.min_supported_dai_version("1.9.0.6")
    def workers(self) -> List[Dict[str, Any]]:
        """Get statistics each worker of the Driverless AI server."""
        health_info = self._client._backend.get_health()

        return [
            {
                "name": worker.name,
                "healthy": worker.healthy,
                "ip": worker.ip,
                "gpus": worker.total_gpus,
                "status": worker.status,
                "max_processes": worker.remote_processors,
                "current_processes": worker.remote_tasks,
                "upload_speed": getattr(worker, "upload_speed", ""),
                "download_speed": getattr(worker, "download_speed", ""),
            }
            for worker in health_info.workers
        ]

    def docs(self, search: str = None) -> _utils.Hyperlink:
        """Get link to documentation on the Driverless AI server.

        Args:
            search: if search terms are supplied, the link will go to
                documentation search results

        Example::

            # Search the DAI docs for "licenses"
            dai.server.docs(search='licenses')
        """
        if search is None:
            return _utils.Hyperlink(f"{self.address}/docs/userguide/index.html")
        else:
            search = urllib.parse.quote_plus(search)
            link = f"{self.address}/docs/userguide/search.html?q={search}"
            return _utils.Hyperlink(link)

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the Driverless AI server.

        Examples::

            dai.server.gui()
        """
        return _utils.Hyperlink(self.address)

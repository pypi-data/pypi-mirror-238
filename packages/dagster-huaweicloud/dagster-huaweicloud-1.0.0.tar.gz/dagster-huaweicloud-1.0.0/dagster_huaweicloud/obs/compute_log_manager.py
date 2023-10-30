import os
from typing import Mapping, Any, Optional, Sequence

from dagster._utils import ensure_file
from typing_extensions import Self

from dagster._config import UserConfigSchema
from dagster._config.config_type import Noneable
from dagster._core.storage.compute_log_manager import ComputeIOType
from dagster._core.storage.cloud_storage_compute_log_manager import (
    CloudStorageComputeLogManager,
    PollingComputeLogSubscriptionManager
)
from dagster._core.storage.local_compute_log_manager import LocalComputeLogManager, IO_TYPE_EXTENSION
import dagster._seven as seven
from dagster import (
    Field,
    Permissive,
    StringSource,
    _check as check,
)
from dagster._serdes import ConfigurableClass, ConfigurableClassData

from obs import DeleteObjectsRequest, Object, PutObjectHeader

from .util import create_obs_client, query_obs_lists_object, upload_local_file_to_obs


class ObsComputeLogManager(CloudStorageComputeLogManager, ConfigurableClass):
    """Logs compute function stdout and stderr to Huawei Cloud OBS.

    Users should not instantiate this class directly. Instead, use a YAML block in ``dagster.yaml``
    such as the following:

    .. code-block:: YAML

        compute_logs:
          module: dagster_huaweicloud.obs.compute_log_manager
          class: ObsComputeLogManager
          config:
            access_key_id: "your-ak"
            secret_access_key: "your-sk"
            bucket: "mycorp-dagster-compute-logs"
            server: "https://obs.ap-southeast-1.myhuaweicloud.com"
            client_other_params:
                ssl_verify: true
            local_dir: "/tmp/cool"
            prefix: "dagster"
            skip_empty_files: true
            upload_interval: 30

    Args:
        access_key_id (str): Access key ID (AK). It is left blank by default,
            which indicates that anonymous users are allowed for access. .
        secret_access_key (str): Secret access key (SK). It is left blank by default,
            which indicates that anonymous users are allowed for access.
        bucket (str): The name of the Huawei Cloud OBS bucket to which to log.
        server (str): Endpoint for accessing OBS, which can contain the protocol type, domain name,
            and port number. For example, https://your-endpoint:443.
            For security purposes, you are advised to use HTTPS.
        client_other_params (dict): OBS client initialization optional parameters,
            please refer to the following link:
            https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0601.html.
        security_token (Optional[str]): Security token in the temporary access keys..
        local_dir (Optional[str]): Path to the local directory in which to stage logs. Default:
            ``dagster._seven.get_system_temp_directory()``.
        prefix (Optional[str]): Prefix for the log file keys.
        skip_empty_files: (Optional[bool]): Skip upload of empty log files.
        upload_interval: (Optional[int]): Interval in seconds to upload partial
            log files to Huawei Cloud OBS. By default,
            will only upload when the capture is complete.
        inst_data (Optional[ConfigurableClassData]): Serializable representation off the compute
            log manager when newed up from config.
    """

    def __init__(self,
                 access_key_id: str,
                 secret_access_key: str,
                 bucket: str,
                 server: str,
                 prefix="dagster",
                 inst_data: Optional[ConfigurableClassData] = None,
                 local_dir=None,
                 client_other_params=None,
                 security_token=None,
                 skip_empty_files=False,
                 upload_interval=None):

        super().__init__()

        self._obs_client = create_obs_client(
            access_key_id, secret_access_key, server,
            client_other_params, security_token)

        if not local_dir:
            local_dir = seven.get_system_temp_directory()

        self._server = server
        self._bucket = check.str_param(bucket, "bucket")
        self._obs_prefix = check.str_param(prefix, "prefix")
        self._local_manager = LocalComputeLogManager(local_dir)
        self._subscription_manager = PollingComputeLogSubscriptionManager(self)
        self._inst_data = check.opt_inst_param(inst_data, "inst_data", ConfigurableClassData)
        self._skip_empty_files = check.bool_param(skip_empty_files, "skip_empty_files")
        self._upload_interval = check.opt_int_param(upload_interval, "upload_interval")

    @property
    def inst_data(self) -> Optional[ConfigurableClassData]:
        return self._inst_data

    @property
    def upload_interval(self) -> Optional[int]:
        return self._upload_interval if self._upload_interval else None

    @property
    def local_manager(self) -> LocalComputeLogManager:
        return self._local_manager

    def _obs_key(self, log_key, io_type, partial=False):
        check.inst_param(io_type, "io_type", ComputeIOType)
        extension = IO_TYPE_EXTENSION[io_type]
        [*namespace, file_base] = log_key
        filename = f"{file_base}.{extension}"
        if partial:
            filename = f"{filename}.partial"
        paths = [self._obs_prefix, "storage", *namespace, filename]
        return "/".join(paths)

    def delete_logs(self, log_key: Optional[Sequence[str]] = None, prefix: Optional[Sequence[str]] = None) -> None:
        self.local_manager.delete_logs(log_key=log_key, prefix=prefix)

        obs_keys_to_remove = None
        if log_key:
            obs_keys_to_remove = [
                self._obs_key(log_key, ComputeIOType.STDOUT),
                self._obs_key(log_key, ComputeIOType.STDERR),
                self._obs_key(log_key, ComputeIOType.STDOUT, partial=True),
                self._obs_key(log_key, ComputeIOType.STDERR, partial=True),
            ]
        elif prefix:
            # add the trailing '' to make sure that ['a'] does not match ['apple']
            obs_prefix = "/".join([self._obs_prefix, "storage", *prefix, ""])
            matching = query_obs_lists_object(self._obs_client, self._bucket, obs_prefix)
            obs_keys_to_remove = [obj["Key"] for obj in matching.get("Contents", [])]
        else:
            check.failed("Must pass in either `log_key` or `prefix` argument to delete_logs")

        if obs_keys_to_remove:
            to_delete = [Object(key=key, versionId=None) for key in obs_keys_to_remove]
            self._obs_client.deleteObjects(self._bucket, DeleteObjectsRequest(quiet=False, objects=to_delete))

    def download_url_for_type(self, log_key: Sequence[str], io_type: ComputeIOType):
        obs_key = self._obs_key(log_key, io_type)
        if self._server.endswith("/"):
            return "https://{}.{}{}".format(self._bucket, self._server.replace("https://", ""), obs_key)
        return "https://{}.{}/{}".format(self._bucket, self._server.replace("https://", ""), obs_key)

    def display_path_for_type(self, log_key: Sequence[str], io_type: ComputeIOType):
        obs_key = self._obs_key(log_key, io_type)
        return "obs://{}/{}".format(self._bucket, obs_key)

    def cloud_storage_has_logs(self, log_key: Sequence[str], io_type: ComputeIOType, partial: bool = False) -> bool:
        obs_key = self._obs_key(log_key, io_type)
        resp = self._obs_client.getObject(self._bucket, obs_key, loadStreamInMemory=False)

        if resp.status < 300:
            return True
        return False

    def upload_to_cloud_storage(
            self,
            log_key: Sequence[str],
            io_type: ComputeIOType,
            partial: bool = False,
            put_headers=None,
            metadata=None
    ) -> None:
        if put_headers is None:
            put_headers = PutObjectHeader()
            put_headers.contentType = 'text/plain'
        if metadata is None:
            metadata = dict()
        path = self.local_manager.get_captured_local_path(log_key, IO_TYPE_EXTENSION[io_type])
        ensure_file(path)

        if (self._skip_empty_files or partial) and os.stat(path).st_size == 0:
            return

        obs_key = self._obs_key(log_key, io_type, partial=partial)
        extra_params = {
            "metadata": metadata,
            "headers": put_headers,
        }
        upload_local_file_to_obs(self._obs_client, self._bucket, obs_key, path, extra_params)

    @classmethod
    def config_type(cls) -> UserConfigSchema:
        return {
            "access_key_id": StringSource,
            "secret_access_key": StringSource,
            "bucket": StringSource,
            "server": StringSource,
            "prefix": Field(StringSource, is_required=False),
            "client_other_params": Field(Noneable(Permissive()), is_required=False),
            "local_dir": Field(StringSource, is_required=False),
            "skip_empty_files": Field(bool, is_required=False, default_value=False),
            "upload_interval": Field(Noneable(int), is_required=False, default_value=None),
        }

    @classmethod
    def from_config_value(cls, inst_data: ConfigurableClassData, config_value: Mapping[str, Any]) -> Self:
        return ObsComputeLogManager(inst_data=inst_data, **config_value)




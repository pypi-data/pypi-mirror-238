import io
import pickle
from typing import Any, Optional, Dict, Union

from dagster import UPathIOManager, ConfigurableIOManager, InputContext, OutputContext, MetadataValue, \
    ResourceDependency, io_manager
from dagster._utils import PICKLE_PROTOCOL
from dagster._utils.cached_method import cached_method
from obs import ObsClient
from pydantic import Field
from upath import UPath

from .resources import ObsResource
from .util import upload_stream_to_obs, download_obs_object_to_local


class PickledObjectObsIOManager(UPathIOManager):
    def __init__(
            self,
            obs_bucket: str,
            obs_client: ObsClient,
            prefix: Optional[str] = None,
            get_extra_params: dict = None,
            put_extra_params: dict = None
    ):
        self._bucket = obs_bucket
        self._obs_client = obs_client
        self._get_extra_params = dict() if get_extra_params is None else get_extra_params
        self._put_extra_params = dict() if put_extra_params is None else put_extra_params
        base_path = UPath(prefix) if prefix else None
        super().__init__(base_path)

    def dump_to_path(self, context: OutputContext, obj: Any, path: UPath):
        if self.path_exists(path):
            context.log.warning(f"Removing existing OBS object: {path}")
            self.unlink(path)

        pickled_obj = pickle.dumps(obj, PICKLE_PROTOCOL)
        pickled_obj_bytes = io.BytesIO(pickled_obj)
        upload_stream_to_obs(self._obs_client, self._bucket, path.as_posix(), pickled_obj_bytes, self._put_extra_params)

    def load_from_path(self, context: InputContext, path: UPath) -> Any:
        self._get_extra_params["loadStreamInMemory"] = True
        resp = download_obs_object_to_local(
            self._obs_client, self._bucket, path.as_posix(), self._get_extra_params)
        return pickle.loads(resp.body.buffer)

    def path_exists(self, path: UPath) -> bool:

        resp = self._obs_client.getObject(self._bucket, path.as_posix(), loadStreamInMemory=False)

        if resp.status < 300:
            return True
        return False

    def unlink(self, path: UPath) -> None:
        resp = self._obs_client.deleteObject(self._bucket, path.as_posix())
        if resp.status > 300:
            raise Exception("errorCode: {}, errorMessage: {}".format(resp.errorCode, resp.errorMessage))

    def make_directory(self, path: UPath) -> None:
        # It is not necessary to create directories in obs
        return None

    def get_metadata(self, context: OutputContext, obj: Any) -> Dict[str, MetadataValue]:
        path = self._get_path(context)
        return {"uri": MetadataValue.path(self._uri_for_path(path))}

    def get_op_output_relative_path(self, context: Union[InputContext, OutputContext]) -> UPath:
        return UPath("storage", super().get_op_output_relative_path(context))

    def _uri_for_path(self, path: UPath) -> str:
        return f"obs://{self._bucket}/{path.as_posix()}"


class ObsPickleIOManager(ConfigurableIOManager):
    """Persistent IO manager using Huawei Cloud OBS for storage.

    Serializes objects via pickling. Suitable for objects storage for distributed executors, so long
    as each execution node has network connectivity and credentials for Huawei Cloud OBS and the backing bucket.

    Assigns each op output to a unique filepath containing run ID, step key, and output name.
    Assigns each asset to a single filesystem path, at "<base_dir>/<asset_key>". If the asset key
    has multiple components, the final component is used as the name of the file, and the preceding
    components as parent directories under the base_dir.

    Subsequent materializations of an asset will overwrite previous materializations of that asset.
    With a base directory of "/my/base/path", an asset with key
    `AssetKey(["one", "two", "three"])` would be stored in a file called "three" in a directory
    with path "/my/base/path/one/two/".

    Example usage:

    .. code-block:: python

        from dagster import asset, Definitions
        from dagster_huaweicloud.obs import ObsPickleIOManager, ObsResource


        @asset
        def asset1():
            # create df ...
            return df

        @asset
        def asset2(asset1):
            return asset1[:5]

        defs = Definitions(
            assets=[asset1, asset2],
            resources={
                "io_manager": ObsPickleIOManager(
                    obs_resource=ObsResource(),
                    obs_bucket="my-cool-bucket",
                    prefix="my-cool-prefix",
                )
            }
        )

    """
    obs_resource: ResourceDependency[ObsResource]
    obs_bucket: str = Field(description="OBS bucket to use for the file manager.")
    prefix: str = Field(
        default="dagster", description="Prefix to use for the OBS bucket for this file manager."
    )
    get_extra_params: Optional[dict[str, Any]] = Field(
        default={}, description="Please refer to the link for details: "
                                "https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0908.html"
    )
    put_extra_params: Optional[dict[str, Any]] = Field(
        default={}, description="Please refer to the link for details: "
                                "https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0903.html"
    )

    @cached_method
    def inner_io_manager(self) -> PickledObjectObsIOManager:
        return PickledObjectObsIOManager(
            obs_client=self.obs_resource.get_client(),
            obs_bucket=self.obs_bucket,
            prefix=self.prefix,
            get_extra_params=self.get_extra_params,
            put_extra_params=self.put_extra_params,
        )

    def load_input(self, context: InputContext) -> Any:
        return self.inner_io_manager().load_input(context)

    def handle_output(self, context: OutputContext, obj: Any) -> None:
        return self.inner_io_manager().handle_output(context, obj)


@io_manager(
    config_schema=ObsPickleIOManager.to_config_schema(),
    required_resource_keys={"obs"},
)
def obs_pickle_io_manager(init_context):
    """Persistent IO manager using Huawei Cloud OBS for storage.

    Serializes objects via pickling. Suitable for objects storage for distributed executors, so long
    as each execution node has network connectivity and credentials for Huawei Cloud OBS and the backing bucket.

    Assigns each op output to a unique filepath containing run ID, step key, and output name.
    Assigns each asset to a single filesystem path, at "<base_dir>/<asset_key>". If the asset key
    has multiple components, the final component is used as the name of the file, and the preceding
    components as parent directories under the base_dir.

    Subsequent materializations of an asset will overwrite previous materializations of that asset.
    With a base directory of "/my/base/path", an asset with key
    `AssetKey(["one", "two", "three"])` would be stored in a file called "three" in a directory
    with path "/my/base/path/one/two/".

    Example usage:

    1. Attach this IO manager to a set of assets.

    .. code-block:: python

        from dagster import Definitions, asset
        from dagster_huaweicloud.obs import obs_pickle_io_manager, obs_resource


        @asset
        def asset1():
            # create df ...
            return df

        @asset
        def asset2(asset1):
            return asset1[:5]

        defs = Definitions(
            assets=[asset1, asset2],
            resources={
                "io_manager": obs_pickle_io_manager.configured(
                    {"obs_bucket": "my-cool-bucket", "obs_prefix": "my-cool-prefix"}
                ),
                "obs": obs_resource,
            },
        )


    2. Attach this IO manager to your job to make it available to your ops.

    .. code-block:: python

        from dagster import job
        from dagster_huaweicloud.obs import obs_pickle_io_manager, obs_resource

        @job(
            resource_defs={
                "io_manager": obs_pickle_io_manager.configured(
                    {"obs_bucket": "my-cool-bucket", "obs_prefix": "my-cool-prefix"}
                ),
                "obs": obs_resource,
            },
        )
        def my_job():
            ...
    """

    obs_resource = init_context.resources.obs
    obs_bucket = init_context.resource_config["obs_bucket"]
    prefix = init_context.resource_config.get("prefix")  # prefix is optional
    get_extra_params = init_context.resource_config.get("get_extra_params")  # get_extra_params is optional
    put_extra_params = init_context.resource_config.get("put_extra_params")  # put_extra_params is optional
    pickled_io_manager = PickledObjectObsIOManager(
        obs_bucket=obs_bucket,
        obs_client=obs_resource,
        prefix=prefix,
        get_extra_params=get_extra_params,
        put_extra_params=put_extra_params
    )
    return pickled_io_manager

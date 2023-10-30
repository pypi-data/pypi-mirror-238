from typing import Any, Optional

from dagster import ConfigurableResource, IAttachDifferentObjectToOpContext, resource
from pydantic import Field

from .file_manager import ObsFileManager
from .util import create_obs_client


class ResourceWithObsConfiguration(ConfigurableResource):
    access_key_id: Optional[str] = Field(
        default=None, description="access key ID to use when creating the HuaweiCloud OBS client."
    )
    secret_access_key: Optional[str] = Field(
        default=None, description="secret access key to use when creating the HuaweiCloud OBS client."
    )
    server: str = Field(
        default="https://obs.ap-southeast-1.myhuaweicloud.com",
        description="Endpoint for accessing OBS, which can contain the protocol type, "
                    "domain name, and port number. For example, https://your-endpoint:443. "
                    "For security purposes, you are advised to use HTTPS."
    )

    client_other_params: Optional[dict[str, Any]] = Field(
        default=None,
        description="Initialize parameters that are not commonly used by the client, "
                    "please refer to the following link for details: "
                    "https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0601.html"
    )


class ObsResource(ResourceWithObsConfiguration, IAttachDifferentObjectToOpContext):
    """Resource that gives access to Huawei Cloud OBS.

    The underlying OBS client is created by calling
    :py:func:`obs.ObsClient <obs:ObsClient>`.
    The returned resource object is an OBS client, an instance of `obs.ObsClient`.

    Example:
        .. code-block:: python

            from dagster import job, op, Definitions
            from dagster_huaweicloud.obs import ObsResource

            @op
            def example_obs_op(obs: ObsResource):
                return obs.get_client().getObject("test", "test/test.txt", loadStreamInMemory=False)

            @job
            def example_job():
                example_obs_op()

            defs = Definitions(
                jobs=[example_job],
                resources={'obs': ObsResource(access_key_id='your-ak', secret_access_key='your-sk')}
            )

    """
    def get_client(self):
        return create_obs_client(
            self.access_key_id,
            self.secret_access_key,
            self.server,
            self.client_other_params,
        )

    def get_object_to_set_on_execution_context(self) -> Any:
        return self.get_client()


@resource(config_schema=ObsResource.to_config_schema())
def obs_resource(context) -> Any:
    """Resource that gives access to Huawei Cloud OBS.

    The underlying OBS client is created by calling
    :py:func:`obs.ObsClient <obs:ObsClient>`.
    The returned resource object is an OBS client, an instance of `obs.ObsClient`.

    Example:
        .. code-block:: python

            from dagster import build_op_context, job, op
            from dagster_huaweicloud.obs import ObsResource

            @op(required_resource_keys={'obs'})
            def example_obs_op(context):
                return context.resources.obs.getObject("test", "test/test.txt", loadStreamInMemory=False)

            @job(resource_defs={'obs': obs_resource})
            def example_job():
                example_obs_op()

            example_job.execute_in_process(
                run_config={
                    'resources': {
                        'obs': {
                            'config': {
                                'access_key_id': 'your-ak',
                                'secret_access_key': 'your-sk',
                            }
                        }
                    }
                }
            )

    Note that your ops must also declare that they require this resource with
    `required_resource_keys`, or it will not be initialized for the execution of their compute
    functions.

    You may configure this resource as follows:

    .. code-block:: YAML

        resources:
          obs:
            config:
              access_key_id: "your-ak"
              # str: Access key ID (AK). It is left blank by default,
              # which indicates that anonymous users are allowed for access..
              secret_access_key: "your-sk"
              # str: Secret access key (SK). It is left blank by default,
              # which indicates that anonymous users are allowed for access..
              server: ""
              # str: Endpoint for accessing OBS, which can contain the protocol type,
              # domain name, and port number. For example, https://your-endpoint:443.
              # For security purposes, you are advised to use HTTPS.
              client_other_params:
                max_retry_count: 3
                timeout: 10
                ssl_verify: false
              # Optional[dict]: OBS client initialization optional parameters,
              # please refer to the following link:
              # https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0601.html.

    """
    return ObsResource.from_resource_context(context).get_client()


class ObsFileManagerResource(ResourceWithObsConfiguration, IAttachDifferentObjectToOpContext):
    obs_bucket: str = Field(
        default=None, description="Bucket name"
    )
    prefix: str = Field(
        default=None, description="Name prefix that the objects to be listed must contain."
    )

    put_headers: Optional[dict[str, Any]] = Field(
        default={},
        description="Additional header of the request for uploading an object"
    )
    metadata: Optional[dict[str, Any]] = Field(
        default={},
        description="Customized metadata of the object"
    )

    def get_client(self):
        obs_client = create_obs_client(
            self.access_key_id,
            self.secret_access_key,
            self.server,
            self.client_other_params,
        )
        return ObsFileManager(
            obs_client=obs_client,
            obs_bucket=self.obs_bucket,
            prefix=self.prefix,
            put_headers=self.put_headers,
            metadata=self.metadata
        )

    def get_object_to_set_on_execution_context(self) -> Any:
        return self.get_client()


@resource(config_schema=ObsFileManagerResource.to_config_schema())
def obs_file_manager(context) -> Any:
    """FileManager that provides abstract access to OBS.

    Implements the :py:class:`~dagster._core.storage.file_manager.FileManager` API.
    """
    return ObsFileManagerResource.from_resource_context(context).get_client()

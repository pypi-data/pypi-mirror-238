from obs import ObsClient


def create_obs_client(
        access_key_id: str,
        secret_access_key: str,
        server: str,
        client_other_params: dict = None,
        security_token=None):
    """
    Initialize ObsClient and return ObsClient

    :param access_key_id: Access key ID (AK). It is left blank by default,
        which indicates that anonymous users are allowed for access.
    :param secret_access_key: Secret access key (SK). It is left blank by default,
        which indicates that anonymous users are allowed for access.
    :param server: Endpoint for accessing OBS, which can contain the protocol type, domain name,
        and port number. For example, https://your-endpoint:443.
        For security purposes, you are advised to use HTTPS.
    :param client_other_params: OBS client initialization optional parameters,
        please refer to the following link:
        https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0601.html.
    :param security_token: Security token in the temporary access keys.
    :return: ObsClient
    """
    # create obs_client instance
    if client_other_params is None:
        client_other_params = dict()

    if security_token is not None:
        obs_client = ObsClient(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            security_token=security_token,
            server=server,
            **client_other_params
        )
    else:
        obs_client = ObsClient(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            server=server,
            **client_other_params
        )

    return obs_client


def query_obs_lists_object(
        obs_client: ObsClient,
        bucket: str,
        prefix: str):
    """
    You can use this Function to list objects in a bucket.
    :param obs_client:
    :param bucket: Bucket name.
    :param prefix: Name prefix that the objects to be listed must contain.
    :return: key of objects list(excluding folders path)
    """
    objects_key = list()
    max_num = 1000
    mark = None
    while True:
        resp = obs_client.listObjects(bucket, marker=mark, max_keys=max_num, prefix=prefix)
        if resp.status < 300:
            index = 1
            for content in resp.body.contents:
                # excluding folders path
                objects_key.append(content.key) if content.size > 0 else None
                index += 1
            if resp.body.is_truncated is True:
                mark = resp.body.next_marker
            else:
                break
        else:
            raise Exception("errorCode: {}, errorMessage: {}".format(resp.errorCode, resp.errorMessage))
    return objects_key


def upload_local_file_to_obs(
        obs_client: ObsClient,
        bucket: str,
        object_key: str,
        file_path: str,
        extra_params: dict):
    """
    upload local file to Huawei Cloud OBS by file path
    :param obs_client:
    :param bucket: Bucket Name
    :param object_key: upload object path, don't start with /
    :param file_path: The path where the local file will be uploaded
    :param extra_params: Other optional parameters, such as headers and metadata
        https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0904.html
    :return: response
    """
    resp = obs_client.putFile(bucket, object_key, file_path, **extra_params)

    if resp.status > 300:
        raise Exception("errorCode: {}, errorMessage: {}".format(resp.errorCode, resp.errorMessage))
    return resp


def upload_stream_to_obs(
        obs_client: ObsClient,
        bucket: str,
        object_key: str,
        content,
        extra_params: dict):
    """
    upload local file to Huawei Cloud OBS by content
    :param obs_client:
    :param bucket: Bucket Name
    :param object_key: upload object path, don't start with /
    :param content: the content will be uploaded
    :param extra_params: Other optional parameters, such as headers and metadata
        https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0904.html
    :return: response
    """
    resp = obs_client.putContent(bucket, object_key, content, **extra_params)

    if resp.status > 300:
        raise Exception("errorCode: {}, errorMessage: {}".format(resp.errorCode, resp.errorMessage))
    return resp


def download_obs_object_to_local(
        obs_client: ObsClient,
        bucket: str,
        object_key: str,
        extra_params: dict):
    """
    Download Huawei Cloud OBS object to local, you can choose
    * Binary Download
    * Streaming Download
    * File-Based Download
    * Partial Download
    * Resumable Download
    Detailed reference: https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0908.html
    :param obs_client:
    :param bucket: Bucket Name
    :param object_key: upload object path, don't start with /
    :param extra_params: Other optional parameters, such as headers,
        loadStreamInMemory, getObjectRequest, downloadPath
        https://support.huaweicloud.com/intl/en-us/sdk-python-devg-obs/obs_22_0908.html
    :return: response
    """
    resp = obs_client.getObject(bucket, object_key, **extra_params)

    if resp.status > 300:
        raise Exception("errorCode: {}, errorMessage: {}".format(resp.errorCode, resp.errorMessage))
    return resp







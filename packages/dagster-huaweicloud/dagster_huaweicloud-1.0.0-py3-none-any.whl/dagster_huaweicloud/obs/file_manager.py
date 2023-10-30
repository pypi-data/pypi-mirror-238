import io
import uuid
from contextlib import contextmanager
from typing import Optional

from dagster import FileHandle
from dagster._core.storage.file_manager import FileManager, IOStream
from dagster._core.storage.temp_file_manager import TempfileManager
from obs import PutObjectHeader, GetObjectRequest, GetObjectHeader

from .util import download_obs_object_to_local, upload_stream_to_obs


class ObsFileHandle(FileHandle):
    """A reference to a file on Huawei Cloud OBS."""

    def __init__(self,
                 obs_bucket: str,
                 obs_key: str,
                 get_headers=None,
                 get_request=None):
        self._obs_bucket = obs_bucket
        self._obs_key = obs_key

        self._get_headers = GetObjectHeader() if get_headers is None else get_headers
        self._get_request = GetObjectRequest() if get_request is None else get_request

    @property
    def obs_bucket(self):
        """str: The name of the OBS bucket."""
        return self._obs_bucket

    @property
    def obs_key(self):
        """str: The OBS key."""
        return self._obs_key

    @property
    def path_desc(self) -> str:
        """str: The file's OBS URL."""
        return self.obs_path

    @property
    def obs_path(self) -> str:
        """str: The file's OBS URL."""
        return "obs://{}/{}".format(self.obs_bucket, self.obs_key)

    @property
    def get_headers(self):
        """GetObjectHeader: get obs object headers."""
        return self._get_headers

    @property
    def get_request(self):
        """GetObjectRequest: get obs object request."""
        return self._get_request


class ObsFileManager(FileManager):
    """An OBS File Manager"""
    def __init__(self,
                 obs_client,
                 obs_bucket,
                 prefix,
                 put_headers: dict = None,
                 metadata: dict = None):
        self._obs_client = obs_client
        self._obs_bucket = obs_bucket
        self._prefix = prefix
        self._local_handle_cache = {}
        self._temp_file_manager = TempfileManager()
        self._put_headers = PutObjectHeader() if put_headers is None else PutObjectHeader(**put_headers)
        self._metadata = dict() if metadata is None else metadata

    def copy_handle_to_local_temp(self, file_handle: ObsFileHandle) -> str:
        temp_path = self._get_local_path(file_handle)
        if temp_path:
            return temp_path
        temp_path = self._download_obs_object_to_temp_file(file_handle)
        return temp_path

    def _download_obs_object_to_temp_file(self, file_handle: ObsFileHandle):
        temp_file_obj = self._temp_file_manager.tempfile()
        temp_path = temp_file_obj.name
        extra_params = {
            "downloadPath": temp_path,
            "getObjectRequest": file_handle.get_request,
            "headers": file_handle.get_headers,
        }
        download_obs_object_to_local(
            self._obs_client,
            file_handle.obs_bucket,
            file_handle.obs_key,
            extra_params
            )
        self._local_handle_cache[file_handle.obs_path] = temp_path
        return temp_path

    def _get_local_path(self, file_handle):
        return self._local_handle_cache.get(file_handle.obs_path)

    def delete_local_temp(self) -> None:
        self._temp_file_manager.close()

    @contextmanager
    def read(self, file_handle: ObsFileHandle, mode: str = "rb"):
        temp_path = self._download_obs_object_to_temp_file(file_handle)
        encoding = None if mode == "rb" else "utf-8"
        with open(temp_path, mode, encoding=encoding) as file_obj:
            yield file_obj

    def read_data(self, file_handle: ObsFileHandle):
        with self.read(file_handle, mode="rb") as file_obj:
            return file_obj.read()

    def write(self, file_obj: IOStream, mode: str = "wb", ext: Optional[str] = None) -> ObsFileHandle:
        obs_key = self._get_full_path("{}.{}".format(str(uuid.uuid4()), "" if ext is None else ext))
        extra_params = {
            "metadata": self._metadata,
            "headers": self._put_headers,
        }
        upload_stream_to_obs(
            self._obs_client,
            self._obs_bucket,
            obs_key,
            file_obj,
            extra_params
        )
        return ObsFileHandle(self._obs_bucket, obs_key)

    def write_data(self, data: bytes, ext: Optional[str] = None) -> ObsFileHandle:
        return self.write(io.BytesIO(data), mode="wb", ext=ext)

    def _get_full_path(self, obs_key):
        if self._prefix.endswith("/"):
            return "{}{}".format(self._prefix, obs_key)
        return "/".join([self._prefix, obs_key])

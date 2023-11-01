from datetime import datetime
from io import BytesIO
from pathlib import Path
import tempfile
from typing import Dict, List, Optional, Union

from benchling_api_client.v2.beta.api.datasets import create_dataset, get_dataset, patch_dataset
from benchling_api_client.v2.beta.models.dataset import Dataset
from benchling_api_client.v2.beta.models.dataset_create import DatasetCreate
from benchling_api_client.v2.beta.models.dataset_create_manifest_manifest_item import (
    DatasetCreateManifestManifestItem,
)
from benchling_api_client.v2.beta.models.dataset_update import DatasetUpdate
from benchling_api_client.v2.beta.models.dataset_update_upload_status import DatasetUpdateUploadStatus
from benchling_api_client.v2.beta.models.file_status_upload_status import FileStatusUploadStatus
from benchling_api_client.v2.types import Response
import httpx

from benchling_sdk.errors import DatasetInProgressError, InvalidDatasetError, raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.models import AsyncTaskLink
from benchling_sdk.services.v2.base_service import BaseService

_DEFAULT_HTTP_TIMEOUT_UPLOAD_DATASET: float = 60.0


class V2BetaDatasetService(BaseService):
    """
    V2-Beta Datasets.

    Datasets are Benchling objects that represent tabular data with typed columns and rows of data.

    See https://benchling.com/api/v2-beta/reference#/Dataset
    """

    @api_method
    def get_by_id(self, dataset_id: str) -> Dataset:
        """
        Get a dataset and URLs to download its data.

        See https://benchling.com/api/v2-beta/reference#/Datasets/getDataset
        """
        response = get_dataset.sync_detailed(client=self.client, dataset_id=dataset_id)
        return model_from_detailed(response)

    @api_method
    def create(self, dataset: DatasetCreate) -> Dataset:
        """
        Create a dataset.

        See https://benchling.com/api/v2-beta/reference#/Datasets/createDataset
        """
        response = create_dataset.sync_detailed(client=self.client, json_body=dataset)
        return model_from_detailed(response)

    @api_method
    def update(self, dataset_id: str, dataset: DatasetUpdate) -> AsyncTaskLink:
        """
        Update a dataset.

        See https://benchling.com/api/v2-beta/reference#/Datasets/patchDataset
        """
        response = patch_dataset.sync_detailed(client=self.client, dataset_id=dataset_id, json_body=dataset)
        return model_from_detailed(response)

    def upload_bytes(
        self,
        url: str,
        input_bytes: Union[BytesIO, bytes],
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATASET,
    ) -> None:
        """Upload bytes to an existing dataset.

        :param url: The url provided by Benchling for uploading to the dataset
        :param input_bytes: Data to upload as bytes or BytesIO
        :param timeout_seconds: Extends the normal HTTP timeout settings since Dataset uploads can be large
            Use this to extend even further if streams are very large
        """
        # Use a completely different client instead of our configured self.client.httpx_client
        # Amazon will reject clients sending other headers besides the ones it expects
        httpx_response = httpx.put(
            url, headers=_aws_url_headers(), content=input_bytes, timeout=timeout_seconds
        )
        response = _response_from_httpx(httpx_response)
        raise_for_status(response)

    def upload_file(
        self, url: str, file: Path, timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATASET
    ) -> None:
        """Upload a file to an existing dataset.

        :param url: The url provided by Benchling for uploading to the dataset
        :param file: A valid Path to an existing file containing the data to upload
        :param timeout_seconds: Extends the normal HTTP timeout settings since Dataset uploads can be large
            Use this to extend even further if streams are very large
        """
        if file.is_dir():
            raise IsADirectoryError(f"Cannot write dataset from directory '{file}', specify a file instead")
        # Use a completely different client instead of our configured self.client.httpx_client
        # Amazon will reject clients sending other headers besides the ones it expects
        files = {"file": open(file, "rb")}
        httpx_response = httpx.put(url, headers=_aws_url_headers(), files=files, timeout=timeout_seconds)
        response = _response_from_httpx(httpx_response)
        raise_for_status(response)

    @api_method
    def create_from_bytes(
        self,
        dataset: DatasetCreate,
        input_bytes: Union[BytesIO, bytes],
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATASET,
    ) -> AsyncTaskLink:
        """Create a dataset from bytes or BytesIO data.

        :param dataset: The DatasetCreate specification for the data. This must be provided, as it cannot be inferred from file names.
        :param input_bytes: Data to upload as bytes or BytesIO
        :param timeout_seconds: Extends the normal HTTP timeout settings since Dataset uploads can be large
            Use this to extend even further if streams are very large
        :return: An AsyncTaskLink that can be polled to know when the dataset has completed processing
        :rtype: AsyncTaskLink
        """
        # This is a current limit of the Dataset API. We may need additional methods in the future
        # to allow multi upload
        if not dataset.manifest:
            raise InvalidDatasetError("The dataset manifest must contain exactly 1 item")
        elif len(dataset.manifest) != 1:
            raise InvalidDatasetError(
                f"The dataset manifest contains {len(dataset.manifest)} items. It must contain exactly 1"
            )
        created_dataset = self.create(dataset)
        manifest_item = created_dataset.manifest[0]

        # This would be unexpected and probably an error from the API return. Likely not a user error. This check appeases MyPy.
        if manifest_item.url is None:
            raise InvalidDatasetError(
                f"The dataset manifest URL is None. The dataset {created_dataset.id} is not available for data upload."
            )
        self.upload_bytes(url=manifest_item.url, input_bytes=input_bytes, timeout_seconds=timeout_seconds)
        dataset_update = DatasetUpdate(upload_status=DatasetUpdateUploadStatus.IN_PROGRESS)
        return self.update(dataset_id=created_dataset.id, dataset=dataset_update)

    @api_method
    def create_from_file(
        self,
        file: Path,
        dataset: Optional[DatasetCreate] = None,
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATASET,
    ) -> AsyncTaskLink:
        """Create a dataset from file data.

        :param file: A valid Path to an existing file containing the data to upload
        :param dataset: The DatasetCreate specification for the data. If not provided, it will be inferred from the file name
        :param timeout_seconds: Extends the normal HTTP timeout settings since Dataset uploads can be large
            Use this to extend even further if streams are very large
        :return: An AsyncTaskLink that can be polled to know when the dataset has completed processing
        :rtype: AsyncTaskLink
        """
        if file.is_dir():
            raise IsADirectoryError(f"Cannot write dataset from directory '{file}', specify a file instead")
        with open(file, "rb") as file_handle:
            input_bytes = file_handle.read()
        if not dataset:
            dataset = DatasetCreate(
                name=f"{datetime.now()} {file.name}",
                manifest=[DatasetCreateManifestManifestItem(file_name=file.name)],
            )
        return self.create_from_bytes(
            dataset=dataset, input_bytes=input_bytes, timeout_seconds=timeout_seconds
        )

    def download_dataset_bytes(
        self, dataset: Dataset, timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATASET
    ) -> List[BytesIO]:
        """Download dataset data to bytes.

        :param dataset: The dataset to download
        :param timeout_seconds: Extends the normal HTTP timeout settings since Dataset uploads can be large
            Use this to extend even further if streams are very large
        :return: An ordered list of BytesIO streams corresponding to a manifest item in the dataset
        :rtype: List[BytesIO]
        """
        if dataset.upload_status != FileStatusUploadStatus.SUCCEEDED:
            raise DatasetInProgressError(
                f"The dataset data cannot be downloaded until the status is {FileStatusUploadStatus.SUCCEEDED}. "
                f"The status of dataset {dataset.id} is {dataset.upload_status}"
            )
        dataset_bytes = []
        for manifest_item in dataset.manifest:
            # This should be present based on the status check above. Assertion satisfies MyPy
            assert manifest_item.url is not None, f"Unable to download dataset {dataset.id}, URL was empty"
            with httpx.stream("GET", manifest_item.url, timeout=timeout_seconds) as download_stream:
                target_bytes = BytesIO()
                for chunk in download_stream.iter_bytes():
                    target_bytes.write(chunk)
                target_bytes.seek(0)
                dataset_bytes.append(target_bytes)
        return dataset_bytes

    def download_dataset_files(
        self,
        dataset: Dataset,
        destination_path: Optional[Path] = None,
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATASET,
    ) -> List[Path]:
        """Download dataset data to files.

        :param dataset: The dataset to download
        :param destination_path: A target directory to place the files. File names will be created based on the manifest item file names.
            If not specified, a temp directory will be created. The caller is responsible for deleting this directory.
        :param timeout_seconds: Extends the normal HTTP timeout settings since Dataset uploads can be large
            Use this to extend even further if streams are very large
        :return: An ordered list of downloaded file paths corresponding to a manifest item in the dataset
        :rtype: List[Path]
        """
        dataset_files = []
        if not destination_path:
            destination_path = Path(tempfile.mkdtemp())
        elif destination_path.is_file():
            raise NotADirectoryError(
                f"The destination path '{destination_path}' is a file, specify a directory instead"
            )
        elif not destination_path.exists():
            raise NotADirectoryError(f"The destination path '{destination_path}' does not exist")
        if dataset.upload_status != FileStatusUploadStatus.SUCCEEDED:
            raise DatasetInProgressError(
                f"The dataset data cannot be downloaded until the status is {FileStatusUploadStatus.SUCCEEDED}. "
                f"The status of dataset {dataset.id} is {dataset.upload_status}"
            )
        for manifest_item in dataset.manifest:
            target_path = destination_path / manifest_item.file_name
            dataset_files.append(target_path)
            # This should be present based on the status check above. Assertion satisfies MyPy
            assert manifest_item.url is not None, f"Unable to download dataset {dataset.id}, URL was empty"
            with open(target_path, "wb") as dataset_handle:
                with httpx.stream("GET", manifest_item.url, timeout=timeout_seconds) as download_stream:
                    for chunk in download_stream.iter_bytes():
                        dataset_handle.write(chunk)
        return dataset_files

    @api_method
    def download_dataset_bytes_by_id(
        self, dataset_id: str, timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATASET
    ) -> List[BytesIO]:
        """Download dataset data to files by dataset_id.

        Fetches the dataset first, then downloads the files.

        :param dataset_id: The id of the dataset to download
        :param timeout_seconds: Extends the normal HTTP timeout settings since Dataset uploads can be large
            Use this to extend even further if streams are very large
        :return: An ordered list of BytesIO streams corresponding to a manifest item in the dataset
        :rtype: List[BytesIO]
        """
        dataset = self.get_by_id(dataset_id=dataset_id)
        return self.download_dataset_bytes(dataset=dataset, timeout_seconds=timeout_seconds)

    @api_method
    def download_dataset_files_by_id(
        self,
        dataset_id: str,
        destination_path: Optional[Path] = None,
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATASET,
    ) -> List[Path]:
        """Download dataset data to files by dataset_id.

        Fetches the dataset first, then downloads the files.

        :param dataset_id: The id of the dataset to download
        :param destination_path: A target directory to place the files. File names will be created based on the manifest item file names.
            If not specified, a temp directory will be created. The caller is responsible for deleting this directory.
        :param timeout_seconds: Extends the normal HTTP timeout settings since Dataset uploads can be large
            Use this to extend even further if streams are very large
        :return: An ordered list of downloaded file paths corresponding to a manifest item in the dataset
        :rtype: List[Path]
        """
        dataset = self.get_by_id(dataset_id=dataset_id)
        return self.download_dataset_files(
            dataset=dataset, destination_path=destination_path, timeout_seconds=timeout_seconds
        )


def _aws_url_headers() -> Dict[str, str]:
    return {"x-amz-server-side-encryption": "AES256"}


def _response_from_httpx(httpx_response: httpx.Response) -> Response:
    return Response(
        status_code=httpx_response.status_code,
        content=httpx_response.content,
        headers=httpx_response.headers,
        parsed=None,
    )

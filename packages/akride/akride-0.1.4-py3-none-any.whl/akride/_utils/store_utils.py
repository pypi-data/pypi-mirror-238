from typing import Any

from akride import logger
from akride._utils.rest.rest_client import RestClient, RestResponse
from akride._utils.rest.utils import default_rest_client


def upload_file_to_data_store(
    file_path: str,
    presigned_url: str,
    fields: Any,
    rest_client: RestClient = default_rest_client(),
):
    logger.debug(
        f"Uploading file {file_path} to datastore, pre-signed url "
        f"{presigned_url} with fields {fields}"
    )
    try:
        response: RestResponse = rest_client.exec_post_request(
            url=presigned_url, body=fields, file_paths=[file_path]
        )
    except Exception:
        raise Exception("Failed to upload file!")

    if not (200 <= response.status_code <= 299):
        raise Exception(f"Failed to upload, Upload response: {response}")

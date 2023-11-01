import logging
import os
import shutil
import tempfile
import uuid
import zipfile
from datetime import datetime
from io import BufferedRandom, BufferedReader, BytesIO
from os import PathLike
from pathlib import Path, PurePath
from sys import getsizeof
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Tuple, Union
import pandas as pd

from arthurai.common.constants import InputType, Stage
from arthurai.common.exceptions import UserValueError
from arthurai.core import util

#  imports ArthurModel for type checking, required due to circular import
if TYPE_CHECKING:
    from arthurai.core.models import ArthurModel

logger = logging.getLogger(__name__)

# fixed constants
MEGABYTE_SIZE = 1024 * 1024


class DatasetService:
    COUNTS = "counts"
    SUCCESS = "success"
    FAILURE = "failure"
    TOTAL = "total"
    FAILURES = "failures"
    DEFAULT_MAX_IMAGE_DATA_BYTES = 300000000  # 300 MB
    MAX_ROWS_PER_FILE = 500_000
    ROW_GROUP_SIZE = 5_000
    # TODO: a more robust approach would be to write a single row group, measure the file size, and use that to decide
    #  how big to make the files

    @staticmethod
    def chunk_image_set(directory_path: str, image_attribute: str,
                        max_image_data_bytes: int = DEFAULT_MAX_IMAGE_DATA_BYTES) -> str:
        return DatasetService.chunk_image_set_with_directory_path_or_files(image_attribute,
                                                                           directory_path=directory_path,
                                                                           max_image_data_bytes=max_image_data_bytes)

    @staticmethod
    def chunk_image_set_with_directory_path_or_files(image_attribute: str, directory_path: Optional[str] = None,
                                                     files: Optional[Union[List[str], List[Path], List[PathLike]]] = None,
                                                     max_image_data_bytes: int = DEFAULT_MAX_IMAGE_DATA_BYTES) -> str:
        """Takes in a directory path with parquet and/or json files containing image attributes.
        Divides images up into 300MB chunks, then zipped, the parquet/json file is also split up to match.
        The files will have random filename, and image zips will have matching name.

        """
        # make output dir for storing all chunks. At end will get:
        # tmp_dir/
        #    123.parquet, 123.zip, 456.parquet, 456.zip
        # TODO remove print statements, add logs to indicate processing, can take a while to run
        if directory_path is None and files is None:
            raise UserValueError("Exactly 1 of the params 'directory_path' and 'files' must be provided, but neither were supplied")
        if directory_path is not None and files is not None:
            raise UserValueError("1 and only 1 of the params 'directory_path' and 'files' must be provided, but both were supplied")

        output_dir = tempfile.mkdtemp()
        if directory_path is not None:
            files = util.retrieve_parquet_files(directory_path)
            files += util.retrieve_json_files(directory_path)
            if not files:
                raise UserValueError("The directory supplied does not contain any parquet or json files to upload")

        # loop through each file
        if files is None:
            return output_dir

        for file in files:
            # keep track of where we are in the file, in case file needs to be split
            # to match image chunk
            cur_size = 0
            last_df_chunk_index = 0
            cur_img_dir = tempfile.mkdtemp(prefix=output_dir + "/")

            file_name = file
            if not (isinstance(file, str) or isinstance(file, PathLike)):
                raise UserValueError("Buffered files cannot be uploaded for CV Image models. Please provide a path to the file instead of an IO buffer.")
            file_suffix = ""

            if ".parquet" in str(file_name):
                file_suffix = ".parquet"
                df = pd.read_parquet(file)
            elif ".json" in str(file_name):
                file_suffix = ".json"
                df = pd.read_json(file)
            else:
                continue

            if image_attribute not in df:
                # TODO should we raise exception here instead?
                logger.warning(f"Found file with missing image attribute, not including in reference set: {file_name}")
                continue

            # loop through each row in file
            for cur_df_index, image_path in enumerate(df[image_attribute]):
                # verify image exists
                if not os.path.exists(image_path):
                    # TODO raise error here?
                    logger.warning(f"Image does not exist for row, not including in reference set: {image_path}")
                    continue

                # move image to temp dir
                image_path = PurePath(image_path)
                temp_image_path = os.path.join(cur_img_dir, image_path.name)
                shutil.copyfile(image_path, temp_image_path)
                img_bytes = os.path.getsize(temp_image_path)
                cur_size += img_bytes

                # if we have reached max image file size, save and start new chunk
                if cur_size >= max_image_data_bytes:
                    chunk_name = str(uuid.uuid4())

                    # create chunk
                    df_chunk = df.iloc[last_df_chunk_index:cur_df_index + 1]
                    # replace image attribute with just the filename, no path
                    df_chunk[image_attribute] = df_chunk[image_attribute].apply(lambda x: PurePath(x).name)
                    df_chunk_filename = f"{chunk_name}{file_suffix}"
                    df_chunk_path = os.path.join(output_dir, df_chunk_filename)

                    if file_suffix == ".parquet":
                        df_chunk.to_parquet(df_chunk_path)
                    elif file_suffix == ".json":
                        df_chunk.to_json(df_chunk_path)

                    # zip images
                    image_zip_path = os.path.join(output_dir, chunk_name)
                    shutil.make_archive(image_zip_path, 'zip', cur_img_dir)

                    # reset for next chunk
                    shutil.rmtree(cur_img_dir)
                    cur_img_dir = tempfile.mkdtemp(prefix=output_dir + "/")
                    cur_size = 0
                    last_df_chunk_index = cur_df_index + 1
            # we have reached end of current file, close off the current chunk before next file
            # TODO maybe pull this into function so no repeated code, but so many things to pass in
            chunk_name = str(uuid.uuid4())

            # create the final chunk
            df_chunk = df.iloc[last_df_chunk_index:cur_df_index + 1]
            # replace image attribute with just the filename, no path
            df_chunk[image_attribute] = df_chunk[image_attribute].apply(lambda x: PurePath(x).name)
            df_chunk_filename = f"{chunk_name}{file_suffix}"
            df_chunk_path = os.path.join(output_dir, df_chunk_filename)

            if file_suffix == ".parquet":
                df_chunk.to_parquet(df_chunk_path)
            elif file_suffix == ".json":
                df_chunk.to_json(df_chunk_path)

            # zip images
            image_zip_path = os.path.join(output_dir, chunk_name)
            shutil.make_archive(image_zip_path, 'zip', cur_img_dir)

            # clean up
            shutil.rmtree(cur_img_dir)
        return output_dir

    @staticmethod
    def files_size(files: List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]], model_input_type: InputType) -> int:
        all_files = files.copy()

        # extra image zip file should have same path and name as parquet file if model is image model
        if model_input_type == InputType.Image:
            for f in files:
                if isinstance(f, str) or isinstance(f, PathLike):
                    f_path = Path(f)
                    all_files.append(Path(os.path.join(f_path.parent, f_path.stem) + ".zip"))
        total_size_bytes = 0
        for file in all_files:
            try:
                if isinstance(file, str) or isinstance(file, PathLike):
                    total_size_bytes += os.path.getsize(file)
                elif isinstance(file, BufferedReader) or isinstance(file, BufferedRandom):
                    total_size_bytes += getsizeof(file)
            except FileNotFoundError:
                pass
        return total_size_bytes

    @staticmethod
    def send_files_from_dir_iteratively(model: 'ArthurModel', directory_path: str,
                                        endpoint: str, upload_file_param_name: str,
                                        additional_form_params: Optional[Dict[str, Any]] = None,
                                        retries: int = 0) -> Tuple[List[Any], Dict[str, Any]]:
        """Sends parquet or json files iteratively from a specified directory to a specified url for a given model

        :param retries:                Number of times to retry the request if it results in a 400 or higher response code
        :param model:                  the :py:class:`!arthurai.client.apiv2.model.ArthurModel`
        :param directory_path:         local path containing parquet and/or json files to send
        :param endpoint:               POST url endpoint to send files to
        :param upload_file_param_name: key to use in body with each attached file
        :param additional_form_params: dictionary of additional form file params to send along with parquet or json file

        :raises MissingParameterError: the request failed

        :returns A list of files which failed to upload
        """
        file_types = "parquet"
        files = util.retrieve_parquet_files(directory_path)
        # don't search for json files if we're specifically uploading something like "inferences.parquet"
        if not upload_file_param_name.endswith(".parquet"):
            file_types = "json or parquet"
            files += util.retrieve_json_files(directory_path)
        if len(files) == 0:
            raise UserValueError(f"Could not find any {file_types} files int the given directory path: '{directory_path}'")

        return DatasetService.send_files_iteratively(model, files, endpoint, upload_file_param_name, additional_form_params, retries)

    @staticmethod
    def send_files_iteratively(model: 'ArthurModel', files: List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]], endpoint: str,
                               upload_file_param_name: str, additional_form_params: Optional[Dict[str, Any]] = None,
                               retries: int = 0) -> Tuple[List[Any], Dict[str, Any]]:
        if len(files) == 0:
            raise UserValueError(f"No files given to send")

        total_size = DatasetService.files_size(files, model.input_type)
        logger.info(f"Starting upload ({total_size / MEGABYTE_SIZE:.3f} MB in {len(files)} files), depending"
                    f" on data size this may take a few minutes")

        failed_files: List[Union[str, Path, PathLike]] = []
        succeeded_files: List[Union[str, Path, PathLike]] = []

        counts: Dict[str, int] = {
            DatasetService.SUCCESS: 0,
            DatasetService.FAILURE: 0,
            DatasetService.TOTAL: 0
        }
        failures: List[Any] = []

        for file in files:
            if isinstance(file, str) or isinstance(file, PathLike):
                file_path = Path(file)
                with open(file, 'rb') as open_file:
                    DatasetService._send_file(model, open_file, endpoint, upload_file_param_name, additional_form_params, retries, counts,
                                              failures, succeeded_files, failed_files, file_path=file_path)
            else:
                DatasetService._send_file(model, file, endpoint, upload_file_param_name, additional_form_params, retries, counts,
                                          failures, succeeded_files, failed_files)

        file_upload_info = {
            DatasetService.COUNTS: counts,
            DatasetService.FAILURES: failures
        }

        # Only log failed or succeeded files if they exist
        if len(failed_files) > 0:
            logger.error(f'Failed to upload {len(failed_files)} files')
        if len(succeeded_files) > 0:
            logger.info(f'Successfully uploaded {len(succeeded_files)} files')
        return failed_files, file_upload_info

    @staticmethod
    def _send_file(model: 'ArthurModel', open_file: Union[BytesIO, BufferedReader, BufferedRandom], endpoint: str, upload_file_param_name: str,
                   additional_form_params: Optional[Dict[str, Any]], retries: int, counts: Dict[str, int], failures: List[Any],
                   succeeded_files: List[Union[str, Path, PathLike]], failed_files: List[Union[str, PathLike]],
                   file_path: Optional[Union[str, Path, PathLike]] = None) -> None:
        if file_path is None:
            file_path = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4()}"
            logger.debug(f"No file path provided, assigning temporary file name: '{file_path}'.")
            if model.input_type == InputType.Image:
                raise UserValueError("Buffered files cannot be uploaded for CV Image models. Please provide a path to the file instead of an IO buffer.")
        expected_keys = {DatasetService.SUCCESS, DatasetService.FAILURE, DatasetService.TOTAL}
        headers = {'Content-Type': 'multipart/form-data'}
        form_parts = {} if additional_form_params is None else additional_form_params
        form_parts.update({upload_file_param_name: open_file})
        # add corresponding image data if image model
        if model.input_type == InputType.Image:
            # image zip file has same path and name as parquet or json file
            image_zip_name = str(os.path.join(Path(file_path).parent, Path(file_path).stem)) + ".zip"
            image_zip_file = open(image_zip_name, 'rb')
            form_parts.update({'image_data': (image_zip_name, image_zip_file, "application/zip")})
        resp = model._client.post(endpoint, json=None, files=form_parts, headers=headers,
                                  return_raw_response=True, retries=retries)
        if resp.status_code == 201:
            logger.info(f"Uploaded completed: {file_path}")
            succeeded_files.append(file_path)
        elif resp.status_code == 207:
            logger.info(f"Upload completed: {file_path}")
            result: Dict[str, Dict[str, int]] = resp.json()
            # ensure the response is in the correct format
            if DatasetService.COUNTS in result and DatasetService.FAILURES in result \
                    and set(result[DatasetService.COUNTS].keys()) == expected_keys:
                counts[DatasetService.SUCCESS] += \
                    result[DatasetService.COUNTS][DatasetService.SUCCESS]
                counts[DatasetService.FAILURE] += \
                    result[DatasetService.COUNTS][DatasetService.FAILURE]
                counts[DatasetService.TOTAL] += \
                    result[DatasetService.COUNTS][DatasetService.TOTAL]
                failures.append(result[DatasetService.FAILURES])
            else:
                failures.append(result)
        else:
            logger.error(f"Failed to upload file: {resp.text}")
            failed_files.append(file_path)
            failures.append(resp.json())
            counts[DatasetService.FAILURE] += 1
            counts[DatasetService.TOTAL] += 1

        # close image zip
        if model.input_type == InputType.Image:
            image_zip_file.close()
            try:
                os.remove(image_zip_file.name)
            except Exception:
                logger.warning(f"Failed to delete temporary image file at {image_zip_file.name}")


class ImageZipper:

    def __init__(self):
        self.temp_file = tempfile.NamedTemporaryFile()
        self.zip = zipfile.ZipFile(self.temp_file.name, 'w')

    def add_file(self, path: str):
        self.zip.write(path)

    def get_zip(self):
        self.zip.close()
        return self.temp_file

    def __del__(self):
        self.zip.close()
        self.temp_file.close()

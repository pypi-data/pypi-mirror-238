from typing import IO, Union
from datetime import datetime
from hashlib import pbkdf2_hmac
import binascii
import base64
import pickle as pkl
import gzip
from io import BytesIO
import blosc
import numpy as np
import os
from collections import defaultdict
from typing import Dict, List
from datetime import date
import nibabel as nib


def create_nifti(array: np.ndarray, affine: np.ndarray):
    """Takes a numpy array and header info to create a nifti file. The
    nifti file is created using nibabel.
    Parameters
    ----------
    array : np.ndarray
        The numpy array that will be saved as a nifti file

    affine : np.ndarray
        The dicom affine matrix

    Returns
    -------
    nifti: nibabel.Nifti1Image
        The nifti object
    """

    # We need to transpose the col and row axis to get the correct orientation for nifti images.
    # For NIFTI, x increases to the right and y increases to the front.
    # For DICOM, x increases to the left and y increases to the back.
    array_transposed = change_dicom_or_nifti_coords(array)

    # Get dtype of array
    dtype = array_transposed.dtype

    nifti_image = nib.Nifti1Image(array_transposed, affine=affine, dtype=dtype)
    return nifti_image


def change_dicom_or_nifti_coords(array: np.array) -> np.array:
    """change_coords is a helper function that changes the coordinates of the
    numpy array. This is used to swap from dicom to nifti coordinates and vice versa.

    Parameters
    ----------
    array : np.ndarray
        The numpy array to be transposed

    Returns
    -------
    array: np.array
        The transposed numpy array
    """

    # For NIFTI, x increases to the right and y increases to the front.
    # For DICOM, x increases to the left and y increases to the back.
    return array.transpose(1, 0, 2)


def format_mq_data(data: Dict[str, List[str | float | int | datetime | date]]):
    """The function formats the data from MedQuery from an object
    with each column as a key and a list of row values, to a list of
    dictionaries, where each dictionary is a row, and the keys are the
    column names.
    ----------
    data : dict
        The data to be formatted
        assumes data is formatted as such:
        data = {
            column1: [value1, value2, value3, ...],
            column2: [value1, value2, value3, ...],
        }
    Returns
    -------
    list
        The formatted data
        data = [
            {column1: value1, column2: value1},
            {column1: value2, column2: value2},
        ]
    """

    # Check of data is a dictionary
    if not isinstance(data, dict):
        raise ValueError('Data must be a dictionary')

    # Check that all columns have the same number of values
    expected_keys = set(data.keys())
    for values in data.values():
        if not isinstance(values, list):
            raise ValueError('Values must be a list')
        if set(data.keys()) != expected_keys:
            raise ValueError('All columns must have the same number of values')

    # Create a defaultdict to automatically add rows that don't exist
    rows = defaultdict(dict)

    # Create a dictionary for each row
    for column, row_values in data.items():
        for index, row_value in enumerate(row_values):
            value = row_value

            # Convert datetime objects to isoformat
            if isinstance(value, (datetime, date)):
                value = value.isoformat()

            rows[index][column] = value

    return list(rows.values())


def log_to_dateformat(line: str) -> str:
    """The function converts line of a log file to a date format.
    Parameters
    ----------
    line : str
        The line of the log file.
    Returns
    -------
    str
        The returned value is a date format.
    """
    lastest_timestamp = line.split(' ')
    latest_date = lastest_timestamp[0]
    latest_time = lastest_timestamp[1].split(',')[0]
    date_format = str(latest_date + ' ' + latest_time).split('m')[1]  # remove color codes
    return date_format


def hash_function(uuid: str, uuid_type: str, make_unique: bool, salt: str | None = None) -> str:
    """The function hashes uuids, which is to anonymize, by a pepper
    value setting. The algorithm uses a SHA512 and iterates enough times
    to create approximately random hashes.
    The function is as of now written to work on the most used uuids.
    Parameters
    ----------
    uuid : str
        Provide the string value for the `uuid` that has to hashed.
        Use it as the salt secret which is the way to decode the value again.
        The value is also going to be same for the salt secret.
    uuid_type : str
        Specify which uuid type to hash. The three types as of now are:
        (i) patient, (ii) study and (iii) series.
    make_unique : bool
        Specify if the uuid should be made unique. Uses time to make it unique
    salt: str | None
        Salt is base64 encoded string used for unique hashing. You can set salt as function argument or let it be None and use the environment variable which is more common for secrets.
    Returns
    -------
    str
        The returned value is an unique identifier string which is not possible
        to use for back tracing to the original source.
    """
    """Hash a uid for consistency and full anonymization."""
    uuid = uuid + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) if make_unique else uuid
    uid_hash = pbkdf2_hmac(
        hash_name='sha512',
        password=uuid.encode('utf-8'),
        salt=bytes(os.environ.get('SALT', salt).encode('utf-8')),
        iterations=100000,
    )
    uid_hash = binascii.hexlify(uid_hash).decode('utf-8')
    uid_hash = uuid_type + '_' + uid_hash
    return uid_hash


def encode_payload(
    payload: np.ndarray,
    blosc_compression: bool = True,
) -> Union[str, IO[bytes]]:
    """This functions encodes the payload to bytes then compression and placing it in an IO buffer.

    Parameters
    ----------
    payload : np.ndarray
        This is the payload containing the data that you want to ship as a HTTPS post request to the REST APi.
    Returns
    -------
    buffer : BytesIO()
        The buffer containing the payload in compressed bytes.
    """
    if blosc_compression:
        payload_c = blosc.compress(pkl.dumps(payload), cname='zstd')
        byte_buffer = base64.b64encode(payload_c)
        return byte_buffer.hex()
    else:
        # slow
        bytes_compressed = gzip.compress(bytes(payload))
        byte_buffer = BytesIO(bytes_compressed)
        byte_buffer.metadata = payload.shape
        return byte_buffer


def decode_payload(
    payload: str,
    blosc_compression: bool = True,
) -> np.ndarray:
    """the function decodes payload by first converting the hexstring to bytes and decompressing + decoding the buffer.
    The payload is then converted back to a dictionary from bytes.
    Parameters
    ----------
    payload : str
        the payload is the response from the RadiomPipe application
    Returns
    -------
    The dictionary contains two dataframes with radiomic features and diagnostic from the process as well
    as two dictionaries with masks from the segmentation and nested radiomics features.
    """
    if payload:
        if blosc_compression:
            # decode the buffer
            payload_b = bytes.fromhex(payload)
            payload_b = blosc.decompress(base64.b64decode(payload_b))
            return pkl.loads(payload_b)
        else:
            # slow but compresses better compared to blosc
            payload.seek(0)
            payload_b = gzip.decompress(payload.getvalue())
            array = np.frombuffer(payload_b)
            return np.reshape(array, payload.metadata)
    else:
        raise ValueError


def str2bool(string_value: str) -> bool:
    """str2bool will return True if the value is in the string tuple and False otherwise.

    Parameters
    ----------
    string_value : str
        string_value

    Returns
    -------
    bool

    """
    return string_value.lower() in ('yes', 'true', 't', '1')


def dir_exists(directory):
    """
    Check if directory exists.

    Parameters
    ----------
    directory : str
        directory

    Returns
    -------
    bool
    """
    return os.path.isdir(directory)


def create_dir_if_not_exists(directory):
    """
    Create directory if not exists.

    Parameters
    ----------
    directory : str
        directory

    Returns
    -------
    None
    """

    if not dir_exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass

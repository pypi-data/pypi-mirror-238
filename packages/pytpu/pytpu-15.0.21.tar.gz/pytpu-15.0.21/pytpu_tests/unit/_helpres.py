import os
import io
import re
import json
import shutil
import tempfile
import itertools
import zipfile
import numpy as np

from typing import Any
from typing import Dict
from typing import Generator
from typing import Optional
from typing import Tuple
from typing import Generator
from typing import Tuple
from typing import TypeVar


import pytpu as tpu


_TPU_PROGRAM_MEMBER_NAME = 'program.tpu'
_INPUTS_MEMBER_PREFIX = 'inputs'
_OUTPUTS_MEMBER_PREFIX = 'outputs'
_META_DATA_MEMBER_NAME = 'metadata.json'


MetaData = Dict  # Untyped JSON meda data dict


absolute_threshold = relative_threshold = 1e-2



def get_data_path():
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "../data"
    )


def get_programs_path(tpu_device: tpu.Device):
    dev_info = tpu_device.info()

    ddr_word_length = dev_info["axi_word_len"] // 8
    cache_word_length = dev_info["cache_word_len"] // 8
    programs_path = os.path.join(
        get_data_path(),
        "ddr_{}/cache_{}".format(ddr_word_length, cache_word_length)
    )
    if not os.path.isdir(programs_path):
        raise RuntimeError(
            "No device pytpu_tests for axi word length {} cache word length {}".format(ddr_word_length,
                                                                                       cache_word_length))
    return programs_path

def _sanitize_layer_name(name: Any) -> str:
    name = str(name)
    name = re.sub(r'[\,|,/,?,<,>,+,",*,:, ,.,%,!,@,(,),[,\]]+', r'_', name)
    return name


def _read_meta_data(tpu_program_zip: zipfile.ZipFile) -> MetaData:
    return json.load(io.BytesIO(tpu_program_zip.read(_META_DATA_MEMBER_NAME)))


def _read_tensor_dict(
        tpu_test: zipfile.ZipFile,
        meta_data: Dict,
        zip_file_member_path_prefix: str,
) -> Generator[Tuple[str, np.ndarray], None, None]:
    for _, region in meta_data[zip_file_member_path_prefix].items():
        for tensor_name, tensor_params in region.items():
            file_name = zip_file_member_path_prefix + '/' + _sanitize_layer_name(tensor_name) + '.bin'
            tensor_buffer = tpu_test.read(file_name)

            # non raw
            if tensor_params.get("user_dtype") and tensor_params.get("user_shape"):
                tensor_data = np.frombuffer(tensor_buffer, dtype=tensor_params['user_dtype'])
                tensor_data = tensor_data.reshape(tensor_params['user_shape'])
            # raw
            else:
                tensor_data = np.frombuffer(tensor_buffer, dtype="uint8")
                tensor_data = tensor_data.reshape(-1, meta_data['hardware_parameters']['ddr_word_len'])

            # LOGGER.debug(f'External file "{file_name}" associated with tensor "{tensor_name}" is loaded:'
            #              f' {tensor_data.shape} <{tensor_data.dtype}>')
            yield tensor_name, tensor_data


def _inspect_input_zip(
        path,
) -> Tuple[
    zipfile.ZipFile,
    Optional[Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]]
]:
    """If the input object is a TPU program - return that TPU program zip file and None;
    if the input object is a TPU test - return its TPU program and its IO pair of dicts;
    otherwise throw an exception."""

    tpu_program_or_tpu_test_zip = zipfile.ZipFile(path)
    names = set(tpu_program_or_tpu_test_zip.namelist())

    if {_INPUTS_MEMBER_PREFIX + '/', _OUTPUTS_MEMBER_PREFIX + '/', _TPU_PROGRAM_MEMBER_NAME} <= names:
        # TPU test provided!

        # ['inputs/', 'outputs/', 'program.tpu', 'outputs/output_Softmax.bin', 'inputs/input_input.bin']
        tpu_test = tpu_program_or_tpu_test_zip
        tpu_program = zipfile.ZipFile(io.BytesIO(tpu_test.read(_TPU_PROGRAM_MEMBER_NAME)))

        #  Get names of input and output tensors:
        meta_data = _read_meta_data(tpu_program)

        # Read inputs and outputs:
        inputs = dict(_read_tensor_dict(tpu_test, meta_data, _INPUTS_MEMBER_PREFIX))
        outputs = dict(_read_tensor_dict(tpu_test, meta_data, _OUTPUTS_MEMBER_PREFIX))

        return tpu_program, (inputs, outputs)

    elif 'metadata.json' in names:
        # TPU program only is provided
        return tpu_program_or_tpu_test_zip, None
    else:
        raise ValueError('Unrecognized zip-file content')


def _copy_zip_file_to(zip_file, file_name):
    with tempfile.TemporaryDirectory() as temporary_directory:
        zip_file.extractall(temporary_directory)
        shutil.make_archive(file_name, 'zip', temporary_directory)
        os.rename(file_name + '.zip', file_name)


def eval_deviation(data: np.ndarray, reference: np.ndarray, relative_threshold: float = relative_threshold,
         absolute_threshold: float = absolute_threshold) -> np.ndarray:
    abs_error = np.abs(reference - data)
    relative_error = np.abs(abs_error / reference)

    return np.logical_or(relative_error <= relative_threshold, abs_error <= absolute_threshold)

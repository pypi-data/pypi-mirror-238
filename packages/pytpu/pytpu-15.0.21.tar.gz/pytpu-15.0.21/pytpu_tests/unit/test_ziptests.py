import os
import threading as thr
import numpy as np
import tempfile
import contextlib
from itertools import cycle
from math import ceil
import concurrent.futures
from collections import deque

import pytpu as tpu
from ._helpres import get_data_path, _inspect_input_zip, _copy_zip_file_to, eval_deviation

from typing import Dict
from typing import Any
from typing import Any
from typing import Dict

import pytest


THREADS = 1


ziptests = [
    'non_raw_test_concat[int8-1-1-19].zip',
    'non_raw_test_concat[int8-1-4-19].zip',
    'raw_test_concat[int8-1-1-32].zip',
    'non_raw_test_concat[int8-1-1-32].zip',
    'raw_test_concat[int8-1-1-19].zip',
    'raw_test_concat[int8-1-4-19].zip'
]


def _check_test_result(
    result: Dict[str, np.ndarray],
    expected: Dict[str, np.ndarray],
):
    result_value = next(iter(result.values()))
    expected_value = next(iter(expected.values()))

    if expected_value.dtype in ['uint8', 'int8']:
        assert np.array_equal(result_value, expected_value) == True
        assert np.max(np.abs(result_value - expected_value)) == 0

    elif expected_value.dtype == 'float32':
        assert eval_deviation(result_value, expected_value).all()


def _sequential(
    tpu_program_path: str,
    inputs: Dict[str, np.ndarray],
    outputs: Dict[str, np.ndarray],
):
    inputs = [inputs for _ in range(100)]
    with contextlib.ExitStack() as tpu_device_stack:
        tpu_devices = [tpu_device_stack.enter_context(tpu.Device.open(i)) for i in tpu.Device.list_devices()]
        with contextlib.ExitStack() as tpu_program_stack:
            tpu_programs = [tpu_program_stack.enter_context(tpu.load(tpu_program_path)) for tpu in tpu_devices]
            with contextlib.ExitStack() as tpu_inference_stack:
                programs_merged_inputs = zip(cycle(tpu_programs), range(len(inputs)))

                for tpu_program, input_index in programs_merged_inputs:
                    inference = tpu_inference_stack.enter_context(tpu_program.inference())
                    input_ = inputs[input_index]

                    result = inference.sync(input_)

                    # for zip test
                    if outputs:
                        _check_test_result(result, outputs)

def _threading(
    tpu_program_path: str,
    inputs: Dict[str, np.ndarray],
    outputs: Dict[str, np.ndarray],
):
    _thread_to_inference = dict()
    _device_to_semaphore = dict()

    def worker_init():
        tpu_program = tpu_program_queque.pop()
        thread = thr.current_thread()
        inference = tpu.Inference(tpu_program)
        _thread_to_inference[thread] = inference
        _device_to_semaphore[str(inference._program._device)] = thr.BoundedSemaphore(value=THREADS)

    def target(input_):
        thread = thr.current_thread()
        inference = _thread_to_inference[thread]
        semaphore = _device_to_semaphore[str(inference._program._device)]

        with semaphore:
            result = inference.sync(input_)

        return result

    def calculate_predictions(inputs_lst):
        lst = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS, initializer=worker_init, initargs=()) as executor:
            futures = []

            for input_ in inputs_lst:
                futures.append(executor.submit(target, input_))

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                lst.append(result)

        for inference in _thread_to_inference.values():
           inference.close()

        return lst

    list_devices = tpu.Device.list_devices()
    with contextlib.ExitStack() as tpu_device_stack:
        tpu_devices = [tpu_device_stack.enter_context(tpu.Device.open(i)) for i in list_devices]

        with contextlib.ExitStack() as tpu_program_stack:
            tpu_programs = [tpu_program_stack.enter_context(tpu.load(tpu_program_path)) for tpu in tpu_devices]
            tpu_program_queque = deque(tuple(tpu_programs) * ceil(THREADS / len(tpu_devices)))

            # for zip test
            if outputs:
                inputs_lst = [inputs for _ in range(100)]
                predictions = calculate_predictions(inputs_lst)
                for result in predictions:
                    _check_test_result(result, outputs)


@pytest.mark.parametrize("ziptest", ziptests)
def test_ziptest_seq(ziptest: str):

    program_path = os.path.join(get_data_path(), 'ziptests', ziptest)

    tpu_program_zip, inputs_outputs = _inspect_input_zip(program_path)

    # if test zip
    if inputs_outputs:
        inputs, outputs = inputs_outputs
        with tempfile.TemporaryDirectory() as temporary_directory:
            # Dump to a temporary directory:
            program_path = os.path.join(temporary_directory, 'temporary_tpu_program.tpu')
            _copy_zip_file_to(tpu_program_zip, program_path)
            _sequential(program_path, inputs, outputs)


@pytest.mark.parametrize("ziptest", ziptests)
def test_ziptest_thread(ziptest):

    program_path = os.path.join(get_data_path(), 'ziptests', ziptest)

    tpu_program_zip, inputs_outputs = _inspect_input_zip(program_path)

    # if test zip
    if inputs_outputs:
        inputs, outputs = inputs_outputs
        with tempfile.TemporaryDirectory() as temporary_directory:
            # Dump to a temporary directory:
            program_path = os.path.join(temporary_directory, 'temporary_tpu_program.tpu')
            _copy_zip_file_to(tpu_program_zip, program_path)
            _threading(program_path, inputs, outputs)

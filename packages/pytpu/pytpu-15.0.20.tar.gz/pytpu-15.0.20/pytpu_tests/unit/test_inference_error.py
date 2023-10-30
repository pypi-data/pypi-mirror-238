import contextlib
import os.path
import numpy as np
import pytest

import pytpu as tpu

from pytpu import InferenceError
from pytpu_tests.unit._helpres import get_data_path


def test_HW_params_mismatch():

    with contextlib.ExitStack() as tpu_device_stack:
        tpu_devices = [tpu_device_stack.enter_context(tpu.Device.open(i)) for i in tpu.Device.list_devices()]
        tpu_device = tpu_devices[0]
        dev_info = tpu_device.info()

        # Choose wrong program path
        ddr_word_length = dev_info["axi_word_len"] // 8
        if ddr_word_length == 64:
            program_path = os.path.join(get_data_path(), 'ddr_32/cache_128', '128x128_program.tpu')
        elif ddr_word_length == 32:
            program_path = os.path.join(get_data_path(), 'ddr_64/cache_64', '64x64_fpga_program.tpu')

        with pytest.raises(ValueError): # Catch an exception
            tpu_program = tpu_device_stack.enter_context(tpu_device.load(program_path))
            inference = tpu_device_stack.enter_context(tpu_program.inference())

            shape = (1, 224, 224, 3)
            a = (10 * np.random.normal(size=shape)).astype(np.int8)
            b = (10 * np.random.normal(size=shape)).astype(np.int8)

            input_tensor = {'InputLayer0': a,
                            'InputLayer1': b}

            inference.sync(input_tensor)

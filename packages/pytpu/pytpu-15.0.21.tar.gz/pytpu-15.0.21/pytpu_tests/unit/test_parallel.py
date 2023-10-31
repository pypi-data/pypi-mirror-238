"""This is a basic example that demonstrates multithreading TPU inference with pytpu."""
import collections
import contextlib
import threading
import concurrent.futures
from typing import Dict
from typing import Deque
from datetime import datetime
from ._helpres import get_data_path

import numpy as np
import pytpu as tpu
import os

# Number of Python threads bound for each available TPU device
# (None or negative stands for single thread and single TPU)
WORKER_THREADS_PER_TPU_DEVICE = 8   # TODO: getting ....XXX.... here <---------------------------------------------------------------------------- !!!!!!!

# WORKER_THREADS_PER_TPU_DEVICE = None  # Works fine

# PATH_TO_TPU_PROGRAM = 'non_raw_add_1_17_17_128.tpu'
TPU_PROGRAM_NAME = '_1_224_224_3_program.tpu'
# PATH_TO_TPU_PROGRAM = 'pytpu.2/pytpu_tests/data/parallel/'


# NUMBER_OF_INPUT_SAMPLES = int(10 * 1e3)  # number of trials


NUMBER_OF_INPUT_SAMPLES = 10000  # number of trials

_INPUT_IMAGES = [None for i in range(NUMBER_OF_INPUT_SAMPLES)]  # Prepare dummy inputs


def test_parallel():
# if __name__ == '__main__':

    # Each Python thread upon initialization will be bound to a particular TPU device via inference descriptor object,
    # the following dictionary keeps track of that relation:
    _thread_to_inference: Dict[threading.Thread, tpu.Inference] = dict()

    # Upon initialization each worker will pop from this queue an interface descriptor:
    _inference_queue: Deque = collections.deque()


    def worker_init():
        """Initialize new Python worker thread"""

        thread = threading.current_thread()  # Get current working thread
        inference = _inference_queue.pop()  # Pop inference object to bound to

        print(f'New thread {thread} bound to inference descriptor {inference}!')

        _thread_to_inference[thread] = inference  # Bound current thread to an inference description and TPU device


    def worker_func(path: str):
        """ Inference function that is executed in a separate thread by each worker.
        :param path: full path to the i-th input image
        """

        # Get inference descriptor of the current thread:
        thread = threading.current_thread()
        inference = _thread_to_inference[thread]

        # Execute pre-processing function in the same thread as inference thus better this better utilizing parallelism
        # in possible numpy-function called in the pre-processing function.
        # TODO: call pre-processing here
        # input_tensor = _pre_processing(path)  # convert input image to input tensor

        shape = (1, 224, 224, 3)
        a = (10 * np.random.normal(size=shape)).astype(np.int8)
        b = (10 * np.random.normal(size=shape)).astype(np.int8)

        # Prepare dummy input:
        input_tensor = {'InputLayer0': a,
                        'InputLayer1': b}

        # Synchronous call of the inference function (called in a separate, current thread):
        output_tensor_dictionary = inference.sync(input_tensor)

        # Execute post-processing function in the same manner:
        # TODO: call post-processing here

        # Prepare dummy output
        score = output_tensor_dictionary['Add0']

        # print(score.flatten()[:10])
        # print(a.flatten()[:10])
        # print(b.flatten()[:10])

        if np.array_equal(score, a + b):
            print('.', end='')
        else:
            print('X', end='')

        return score


    # Prepare inference loop:
    with contextlib.ExitStack() as exit_stack:

        program_path = os.path.join(get_data_path(), 'parallel', TPU_PROGRAM_NAME)
        # Iterate over available TPU devices, open each device, load the same program
        # and make `WORKER_THREADS_PER_TPU_DEVICE` inference descriptors.
        # This will result in `WORKER_THREADS_PER_TPU_DEVICE` times the number of available devices threads.
        for tpu_device_path in tpu.Device.list_devices():
            tpu_device = exit_stack.enter_context(tpu.Device.open(tpu_device_path))  # open n-th TPU device
            tpu_program = exit_stack.enter_context(tpu_device.load(program_path))  # load TPU program

            if not WORKER_THREADS_PER_TPU_DEVICE:
                # If WORKER_THREADS_PER_TPU_DEVICE is None or <= 0 - run a single thread only:
                i = exit_stack.enter_context(tpu_program.inference())  # Make single inference descriptor
                _inference_queue.append(i)  # Append i-th inference to the queue

                break  # Exit TPU loop now
            else:
                # Make `WORKER_THREADS_PER_TPU_DEVICE` inference descriptors:
                for _ in range(WORKER_THREADS_PER_TPU_DEVICE):
                    i = exit_stack.enter_context(tpu_program.inference())  # Make i-th inference
                    _inference_queue.append(i)  # Append i-th inference to the queue

        # With the _inference_queue populated prepare thread pool:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(_inference_queue), initializer=worker_init,
                                                   initargs=()) as executor:

            futures = [executor.submit(worker_func, path) for path in _INPUT_IMAGES]  # Submit each input image

            begin_at = datetime.now()

            # Run main inference loop:
            counter = 0
            for future in concurrent.futures.as_completed(futures):
                output_data = future.result()

                # TODO: process scores here
                # print('.', end='')

                counter += 1

                if counter % 80 == 0:
                    print()

            print()

            time_delta = datetime.now() - begin_at
            print(f'Processing of {len(_INPUT_IMAGES)} images complete in {time_delta},'
                  f' average FPS is {len(_INPUT_IMAGES) / time_delta.total_seconds()}')

    ...

    # NOTE: exit_stack will release resources in the reversed order thus first closing inference description then
    # unloading TPU program then closing TPU device.

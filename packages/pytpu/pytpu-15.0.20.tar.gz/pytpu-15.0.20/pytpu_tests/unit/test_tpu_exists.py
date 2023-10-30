import pytpu as tpu


def test_tpu_exists():
    available_tpu_devices = tpu.Device.list_devices()

    assert available_tpu_devices, 'No TPU device available!? Check ls /dev/tpu*'

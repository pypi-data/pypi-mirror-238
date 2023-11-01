from k_lights_interface.k_serial_manager import KSerialManager
from k_lights_interface.k_logging import set_log_level, logging
import k_lights_interface.proto_protocol as kprot
from time import sleep


def test_set_channels():
    dev_manager = KSerialManager()
    all_connected_devices = dev_manager.connect_to_all()
    [print(dev) for dev in all_connected_devices]
    assert (len(all_connected_devices) > 0)
    device = all_connected_devices[0]
    print(f"Chosen device for tests: {device}")
    ret = device.set_emitter_output_type(kprot.EmitterOutputType.DAC_OUTPUT)
    if not ret:
        print("Couldnt set emitter output type")

    for i in range(1):
        test_list = [0]*6
        test_list[i] = 100
        device.set_rgbacl_emitter_channels_without_compensation_unsafe(test_list)
        print(f"THIS IS CHANNEL {i}")
        sleep(10)
    # sleep(0.4)
    device.set_rgbacl_emitter_channels_without_compensation_unsafe([0, 0, 0, 0, 0, 0])


def example_use_dac():
    dev_manager = KSerialManager()
    all_connected_devices = dev_manager.connect_to_all()
    [print(dev) for dev in all_connected_devices]
    assert (len(all_connected_devices) > 0)
    k_device = all_connected_devices[0]
    print(f"Chosen device for tests: {k_device}")
    sleep(0.5)

    ret = k_device.set_emitter_output_type(kprot.EmitterOutputType.PWM_OUTPUT)
    ret = k_device.set_rgbacl_emitter_channels_without_compensation_unsafe([100]*6)
    if not ret:
        print("Couldnt set emitter output type")
        return False    
    sleep(2)


if __name__ == "__main__":
    example_use_dac()

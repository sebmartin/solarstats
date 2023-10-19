from unittest import mock

import minimalmodbus


def create_fake_modbus():
    data = {
        0x000A: 0x3021,
        0x000B: 0x0400,
        0xE004: 0x0002,
        0x000C: " My Controller ",
        0x0014: [0x0010, 0x2234],
        0x0016: [0x0011, 0x3422],
        0x0018: [0x1234, 0x5678],
        0x001A: 0x1234,
        0x0100: 98,
        0x0101: 124,
        0x0102: 3112,
        0x0103: 0x8514,
        0x0104: 145,
        0x0105: 3211,
        0x0106: 460,
        0x0107: 125,
        0x0108: 2440,
        0x0109: 305,
        0x010B: 128,
        0x010C: 55,
        0x010D: 3011,
        0x010E: 205,
        0x010F: 385,
        0x0110: 105,
        0x0111: 170,
        0x0112: 12,
        0x0113: 13450,
        0x0114: 123,
        0x0115: 180,
        0x0116: 5,
        0x0117: 123,
        0x0118: [0x0053, 0x0101],
        0x011A: [0x0105, 0x0202],
        0x011C: [0x0106, 0x0203],
        0x011E: [0x0205, 0x0104],
        0x0120: 0xBE02,
        0x0121: [0x0101, 0x0202],
    }

    fake_controller = mock.Mock(spec=minimalmodbus.Instrument)
    fake_controller.serial = mock.Mock()
    fake_controller.address = "/dev/ttyUSB0"
    fake_controller.port = 123

    fake_controller.read_register.side_effect = lambda x, *args, **kwargs: data.get(x)
    fake_controller.read_registers.side_effect = lambda x, *args, **kwargs: data.get(x)
    fake_controller.read_string.side_effect = lambda x, *args, **kwargs: data.get(x)
    return fake_controller

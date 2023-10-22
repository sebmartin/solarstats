from unittest import mock

import minimalmodbus


def create_fake_modbus():
    data = {
        # 0x000A: 0x3021,
        # 0x000B: 0x0400,
        # 0xE004: 0x0002,
        # 0x000C: " My Controller ",
        # 0x0014: [0x0010, 0x2234],
        # 0x0016: [0x0011, 0x3422],
        # 0x0018: [0x01234, 0x5678],
        # 0x001A: 0x01234,
        # 0x0100: 98,
        # 0x0101: 124,
        # 0x0102: 3112,
        # 0x0103: 0x8514,
        # 0x0104: 145,
        # 0x0105: 3211,
        # 0x0106: 460,
        # 0x0107: 125,
        # 0x0108: 2440,
        # 0x0109: 305,
        # 0x010B: 128,
        # 0x010C: 55,
        # 0x010D: 3011,
        # 0x010E: 205,
        # 0x010F: 385,
        # 0x0110: 105,
        # 0x0111: 170,
        # 0x0112: 12,
        # 0x0113: 13450,
        # 0x0114: 123,
        # 0x0115: 180,
        # 0x0116: 5,
        # 0x0117: 123,
        # 0x0118: [0x0053, 0x0101],
        # 0x011A: [0x0105, 0x0202],
        # 0x011C: [0x0106, 0x0203],
        # 0x011E: [0x0205, 0x0104],
        # 0x0120: 0xBE02,
        # 0x0121: [0x0101, 0x0202],
        0x000A: 0x0C1E,
        0x000A: 0x0C1E,
        0x000B: 0x1400,
        0x000C: "  RNG-CTRL-WND30",
        0x0014: [0x0001, 0x0004],
        0x0016: [0x0001, 0x0003],
        0x0018: [0x110B, 0x0020],
        0x001A: 0x0001,
        0x0100: 0x0048,
        0x0101: 0x007E,
        0x0102: 0x0000,
        0x0103: 0x0B19,
        0x0104: 0x0000,
        0x0105: 0x0000,
        0x0106: 0x0000,
        0x0107: 0x0000,
        0x0108: 0x0000,
        0x0109: 0x0000,
        0x010B: 0x007E,
        0x010C: 0x0081,
        0x010D: 0x0000,
        0x010E: 0x0000,
        0x010F: 0x0000,
        0x0110: 0x0000,
        0x0111: 0x0000,
        0x0112: 0x0000,
        0x0113: 0x0000,
        0x0114: 0x0000,
        0x0115: 0x012E,
        0x0116: 0x0002,
        0x0117: 0x00BC,
        0x0118: [0x0000, 0x0968],
        0x011A: [0x0000, 0x0000],
        0x011C: [0x0000, 0x7FB8],
        0x011E: [0x0000, 0x0000],
        0x0120: 0x0000,
        0x0121: [0x0000, 0x0000],
        0xE002: 0x00C8,
        0xE003: 0x0C0C,
        0xE004: 0x0001,
        0xE005: 0x00A0,
        0xE006: 0x009B,
        0xE007: 0x0094,
        0xE008: 0x0092,
        0xE009: 0x008A,
        0xE00A: 0x0084,
        0xE00B: 0x007E,
        0xE00C: 0x0078,
        0xE00D: 0x006F,
        0xE00E: 0x006A,
        0xE00F: 0x6432,
        0xE010: 0x0005,
        0xE011: 0x0078,
        0xE012: 0x0078,
        0xE013: 0x001C,
        0xE014: 0x0003,
        0xE015: 0x0000,
        0xE016: 0x0000,
        0xE017: 0x0000,
        0xE018: 0x0000,
        0xE019: 0x0000,
        0xE01A: 0x0000,
        0xE01B: 0x0000,
        0xE01C: 0x0000,
        0xE01D: 0x000F,
        0xE01E: 0x0005,
        0xE01F: 0x0005,
        0xE020: 0x0294,
        0xE021: 0x0005,
    }

    fake_controller = mock.Mock(spec=minimalmodbus.Instrument)
    fake_controller.serial = mock.Mock()
    fake_controller.address = "/dev/ttyUSB0"
    fake_controller.port = 123

    fake_controller.read_register.side_effect = lambda x, *args, **kwargs: data.get(x)
    fake_controller.read_registers.side_effect = lambda x, *args, **kwargs: data.get(x)
    fake_controller.read_string.side_effect = lambda x, *args, **kwargs: data.get(x)
    return fake_controller

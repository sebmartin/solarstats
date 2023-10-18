from unittest import mock

import minimalmodbus
import pytest

from probes.renogy.renogy_rover import RenogyRoverController
from probes.renogy.types import BatteryType, ProductType


@pytest.fixture
def fake_modbus():
    data = {0x000A: 0x3021, 0x000B: 0x0400, 0xE004: 0x0002}

    fake_controller = mock.Mock(spec=minimalmodbus.Instrument)
    fake_controller.serial = mock.Mock()
    fake_controller.address = "/dev/ttyUSB0"
    fake_controller.port = 123
    fake_controller.read_register.side_effect = lambda x: data.get(x)
    fake_controller.read_registers.side_effect = lambda x, *args, **kwargs: data.get(x)
    return fake_controller


@pytest.fixture()
def controller(fake_modbus):
    with mock.patch(
        "probes.renogy.renogy_rover._create_controller"
    ) as mock_create_controller:
        mock_create_controller.return_value = fake_modbus
        yield RenogyRoverController(port=123, address="/dev/ttyUSB0")


def test_controller_init_fails_if_controller_serial_is_none(fake_modbus):
    fake_modbus.serial = None
    with mock.patch(
        "probes.renogy.renogy_rover._create_controller"
    ) as mock_create_controller:
        mock_create_controller.return_value = fake_modbus
        with pytest.raises(AssertionError):
            RenogyRoverController(port=123, address="/dev/ttyUSB0")


@pytest.mark.parametrize(
    "metric,expected",
    [
        ("max_system_voltage", 48),
        ("rated_charging_current", 33),
        ("rated_discharging_current", 4),
        ("product_type", ProductType.CHARGE_CONTROLLER),
        # ("product_model", None),
        # ("software_version", None),
        # ("hardware_version", None),
        # ("serial_number", None),
        # ("device_address", None),
        # ("battery_percentage", None),
        # ("battery_voltage", None),
        # ("charging_current", None),
        # ("controller_temperature", None),
        # ("battery_temperature", None),
        # ("load_voltage", None),
        # ("load_current", None),
        # ("load_power", None),
        # ("solar_voltage", None),
        # ("solar_current", None),
        # ("charging_power", None),
        # ("battery_min_voltage_today", None),
        # ("battery_max_voltage_today", None),
        # ("max_charging_current_today", None),
        # ("max_discharging_current_today", None),
        # ("max_charging_power_today", None),
        # ("max_discharging_power_today", None),
        # ("charging_amphours_today", None),
        # ("discharging_amphours_today", None),
        # ("power_generation_today", None),
        # ("power_consumption_today", None),
        # ("total_operating_days", None),
        # ("total_battery_over_discharges", None),
        # ("total_battery_full_charges", None),
        # ("total_battery_charge_amphours", None),
        # ("total_battery_discharge_amphours", None),
        # ("cumulative_power_generation", None),
        # ("cumulative_power_consumption", None),
        # ("set_street_light", None),
        # ("street_light_status", None),
        # ("set_street_light_brightness", None),
        # ("street_light_brightness", None),
        # ("charging_state", None),
        # ("controller_fault_information", None),
        # ("nominal_battery_capacity", None),
        # ("system_voltage_setting", None),
        # ("recognized_voltage", None),
        # ("battery_type", BatteryType.SEALED),
        # ("over_voltage_threshold", None),
        # ("charging_voltage_limit", None),
        # ("equalizing_charging_voltage", None),
        # ("boost_charging_voltage", None),
        # ("floating_voltage", None),
        # ("boost_charging_recovery_voltage", None),
        # ("over_discharge_recovery_voltage", None),
        # ("under_voltage_warning_level", None),
        # ("over_discharge_voltage", None),
        # ("discharging_limit_voltage", None),
        # ("end_of_charge_soc", None),
        # ("end_of_discharge_soc", None),
        # ("over_discharge_time_delay", None),
        # ("equalizing_charging_time", None),
        # ("boost_charging_time", None),
        # ("equalizing_charging_interval", None),
        # ("temperature_compensation_factor", None),
        # ("first_stage_operating_duration", None),
        # ("first_stage_operating_power", None),
        # ("second_stage_operating_duration", None),
        # ("second_stage_operating_power", None),
        # ("third_stage_operating_duration", None),
        # ("third_stage_operating_power", None),
        # ("morning_on_operating_duration", None),
        # ("morning_on_operating_power", None),
        # ("load_working_mode", None),
        # ("light_control_delay", None),
        # ("light_control_voltate", None),
        # ("led_load_current_setting", None),
        # ("charging_mode_controlled_by", None),
        # ("special_power_control_state", None),
        # ("each_night_on_function_state", None),
        # ("no_charging_below_freezing", None),
        # ("charging_method", None),
    ],
)
def test_controller_metrics(metric, expected, controller):
    repr(controller)
    assert hasattr(controller, metric), f"Controller does not have metric {metric}"
    assert getattr(controller, metric)() == expected

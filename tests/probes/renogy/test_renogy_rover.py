from unittest import mock

import pytest

from probes.renogy.renogy_rover import RenogyRoverController
from probes.renogy.types import BatteryType, ChargingState, Fault, Toggle, ProductType
from tests.probes.renogy.fakes.fake_modbus import create_fake_modbus


@pytest.fixture
def fake_modbus():
    return create_fake_modbus()


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
        ("product_model", "My Controller"),
        ("software_version", "16.34.52"),
        ("hardware_version", "17.52.34"),
        ("serial_number", 305419896),
        ("device_address", 4660),
        ("battery_percentage", 98),
        ("battery_voltage", 12.4),
        ("charging_current", 31.12),
        ("controller_temperature", -5),
        ("battery_temperature", 20),
        ("load_voltage", 14.5),
        ("load_current", 32.11),
        ("load_power", 460),
        ("solar_voltage", 12.5),
        ("solar_current", 24.4),
        ("charging_power", 305),
        ("battery_min_voltage_today", 12.8),
        ("battery_max_voltage_today", 5.5),
        ("max_charging_current_today", 30.11),
        ("max_discharging_current_today", 2.05),
        ("max_charging_power_today", 385),
        ("max_discharging_power_today", 105),
        ("charging_amphours_today", 170),
        ("discharging_amphours_today", 12),
        ("power_generation_today", 1.345),
        ("power_consumption_today", 0.0123),
        ("total_operating_days", 180),
        ("total_battery_over_discharges", 5),
        ("total_battery_full_charges", 123),
        ("total_battery_charge_amphours", 5439745),
        ("total_battery_discharge_amphours", 17105410),
        ("cumulative_power_generation", 1717.0947),
        ("cumulative_power_consumption", 3388.2372),
        ("street_light_status", Toggle.ON), # TODO test for both ON and OFF
        ("street_light_brightness", 62),
        ("charging_state", ChargingState.MPPT), # TODO add multiple tests for each state value
        ("controller_fault_information", [Fault.BATTERY_OVER_DISCHARGE, Fault.PHOTOVOLTAIC_INPUT_SHORT_CIRCUIT]), # TODO parameterized test for this
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
    assert hasattr(controller, metric), f"Controller does not have metric {metric}"
    assert getattr(controller, metric)() == expected, f"Unexpected value for metric {metric}"

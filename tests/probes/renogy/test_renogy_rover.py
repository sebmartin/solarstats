from unittest import mock

import pytest

from probes.renogy.renogy_rover import RenogyRoverController
from probes.renogy.types import BatteryType, ChargingMethod, ChargingModeController, ChargingState, Fault, LoadWorkingModes, Toggle, ProductType
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
        ("max_system_voltage", 12),
        ("rated_charging_current", 30),
        ("rated_discharging_current", 20),
        ("product_type", ProductType.CHARGE_CONTROLLER),
        ("product_model", "RNG-CTRL-WND30"),
        ("software_version", "1.0.4"),
        ("hardware_version", "1.0.3"),
        ("serial_number", 285933600),
        ("device_address", 1),
        ("battery_percentage", 72),
        ("battery_voltage", 12.6),
        ("charging_current", 29.51),
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
        ("nominal_battery_capacity", 200),
        ("system_voltage_setting", 12),
        ("recognized_voltage", 12),
        ("battery_type", BatteryType.OPEN),
        ("over_voltage_threshold", 16.0),
        ("charging_voltage_limit", 15.5),
        ("equalizing_charging_voltage", 14.8),
        ("boost_charging_voltage", 14.6),
        ("floating_voltage", 13.8),
        ("boost_charging_recovery_voltage", 13.2),
        ("over_discharge_recovery_voltage", 12.6),
        ("under_voltage_warning_level", 12.0),
        ("over_discharge_voltage", 11.1),
        ("discharging_limit_voltage", 10.6),
        ("end_of_charge_soc", 100),
        ("end_of_discharge_soc", 50),
        ("over_discharge_time_delay", 5),
        ("equalizing_charging_time", 120),
        ("boost_charging_time", 120),
        ("equalizing_charging_interval", 28),
        ("temperature_compensation_factor", 3),
        ("first_stage_operating_duration", 16),
        ("first_stage_operating_power", 35),
        ("second_stage_operating_duration", 17),
        ("second_stage_operating_power", 36),
        ("third_stage_operating_duration", 18),
        ("third_stage_operating_power", 37),
        ("morning_on_operating_duration", 19),
        ("morning_on_operating_power", 38),
        ("load_working_mode", LoadWorkingModes.MANUAL),
        ("light_control_delay", 5),
        ("light_control_voltate", 5),
        ("led_load_current_setting", 6.600),
        ("charging_mode_controlled_by", ChargingModeController.SOC),
        ("special_power_control_state", Toggle.ON),
        ("each_night_on_function_state", Toggle.OFF),
        ("no_charging_below_freezing", Toggle.ON),
        ("charging_method", ChargingMethod.PWM),
    ],
)
def test_controller_metrics(metric, expected, controller):
    assert hasattr(controller, metric), f"Controller does not have metric {metric}"
    assert getattr(controller, metric)() == expected, f"Unexpected value for metric {metric}"

"""
Driver for the Renogy Rover Solar Controller using the Modbus RTU protocol

This driver also works with the Renogy Wanderer controller, however, the
Wanderer does not support all of the features that the Rover does and will
therefore return fewer values.

based on:
    https://github.com/corbinbs/solarshed/blob/master/solarshed/controllers/renogy_rover.py
"""

from typing import Any, Union
import minimalmodbus
import logging

from probes.renogy.types import (
    BatteryType,
    ChargingMethod,
    ChargingModeController,
    ChargingState,
    Fault,
    LoadWorkingModes,
    OnOff,
    ProductType,
)

logger = logging.getLogger(__name__)


def _create_controller(port: int, address: str):
    return minimalmodbus.Instrument(port=port, slaveaddress=address)


class RenogyRoverController:
    """
    Communicates using the Modbus RTU protocol (via provided USB<->RS232 cable)
    """

    def __init__(self, port: int, address: str, baudrate=9600, timeout=0.5):
        self.device = _create_controller(port, address)
        assert (
            self.device.serial is not None
        ), f"modbus failed to initialize; port={port} address={address}"

        self.device.serial.baudrate = baudrate
        self.device.serial.timeout = timeout

    def all_data_keys(self) -> list[str]:
        return [
            key
            for key in dir(self)
            if (
                not key.startswith("_")
                and not key.startswith("all_data")
                and not key.startswith("set_")
                and not key in (
                    "stop_polling",
                )
                and callable(getattr(self, key))
            )
        ]

    def all_data(self) -> dict[str, Any]:
        return {
            key: getattr(self, key)()
            for key in self.all_data_keys()
        }

    def _read_register(self, address: int, **kwargs):
        value =  self.device.read_register(address, **kwargs)
        logger.debug(f"read_register[address={hex(address)} value={hex(value)}]")
        return value

    def _read_registers(self, address: int, number_of_registers: int, **kwargs):
        values =  self.device.read_registers(address, number_of_registers=number_of_registers, **kwargs)
        logger.debug(f"read_registers[address={hex(address)} value={(hex(v) for v in values)}]")
        return values

    def _read_string(self, address: int, number_of_registers: int, **kwargs):
        value =  self.device.read_string(address, number_of_registers=number_of_registers, **kwargs)
        logger.debug(f"read_string[address={hex(address)} value=\"{value}\"]")
        return value


    # System information
    def max_system_voltage(self) -> int:
        """
        Maximum voltage supported by the system (volts)
        """
        register = self._read_register(0x000A)
        return register >> 8

    def rated_charging_current(self) -> int:
        """
        Rated charging current (amps)
        """
        register = self._read_register(0x000A)
        return register & 0x00FF

    def rated_discharging_current(self) -> int:
        """
        Rated discharging current (amps)
        """
        register = self._read_register(0x000B)
        return register >> 8

    def product_type(self) -> Union[ProductType, int]:
        """
        Product type
        """
        register = self._read_register(0x000B)
        product_type = register & 0x00FF
        try:
            return ProductType(product_type)
        except ValueError:
            logger.warning(f"unknown product type ({product_type})")
            return product_type

    def product_model(self) -> str:
        """
        Product model
        """
        return self._read_string(0x000C, number_of_registers=8).trim()

    def software_version(self) -> str:
        """
        Software version
        """
        registers = self._read_registers(0x0014, number_of_registers=2)
        major = registers[0] & 0x00FF
        minor = registers[1] >> 8
        patch = registers[1] & 0x00FF
        return f"{major}.{minor}.{patch}"

    def hardware_version(self) -> str:
        """
        Hardware version
        """
        registers = self._read_registers(0x0016, number_of_registers=2)
        major = registers[0] & 0x00FF
        minor = registers[1] >> 8
        patch = registers[1] & 0x00FF
        return f"{major}.{minor}.{patch}"

    def serial_number(self) -> int:
        """
        Serial number
        """
        registers = self._read_registers(0x0018, number_of_registers=2)
        return registers[0] << 16 | registers[1]

    def device_address(self) -> int:
        """
        Device address
        """
        return self._read_register(0x001A)

    # Charging information
    def battery_percentage(self) -> int:
        """
        Current battery capacity value (percentage)
        """
        return self._read_register(0x0100)

    def battery_voltage(self) -> float:
        """
        Current battery voltage (volts)
        """
        return self._read_register(0x0101, number_of_decimals=1)

    def charging_current(self) -> float:
        """
        Charging current to battery (amps)
        """
        return self._read_register(0x0102, number_of_decimals=2)

    def controller_temperature(self) -> int:
        """
        Controller temperature (degrees C)
        """
        register = self._read_register(0x0103)
        temp_data = register >> 8
        temp_value = temp_data & (0xFF >> 1)
        sign = temp_data >> 7
        return -(temp_value) if sign == 1 else temp_value

    def battery_temperature(self) -> int:
        """
        Battery temperature (degrees C)
        """
        register = self._read_register(0x0103)
        temp_data = register & 0x00FF
        temp_value = temp_data & (0xFF >> 1)
        sign = temp_data >> 7
        return -(temp_value) if sign == 1 else temp_value

    # Load information
    def load_voltage(self) -> float:
        """
        Street light (load) voltage (volts)
        """
        return self._read_register(0x0104, number_of_decimals=1)

    def load_current(self) -> float:
        """
        Street light (load) current (amps)
        """
        return self._read_register(0x0105, number_of_decimals=2)

    def load_power(self) -> int:
        """
        Street light (load) power (watts)
        """
        return self._read_register(0x0106)

    # Solar panel information
    def solar_voltage(self) -> float:
        """
        Solar panel voltage to controller (volts)
        """
        return self._read_register(0x0107, number_of_decimals=1)

    def solar_current(self) -> float:
        """
        Solar panel current to controller (amps)
        """
        return self._read_register(0x0108, number_of_decimals=2)

    def charging_power(self) -> int:
        """
        Charging power (watts)
        """
        return self._read_register(0x0109)

    # Historical information
    def battery_min_voltage_today(self) -> float:
        """
        Minimum battery voltage for the current day (volts)
        """
        return self._read_register(0x010B, number_of_decimals=1)

    def battery_max_voltage_today(self) -> float:
        """
        Maximum battery voltage for the current day (volts)
        """
        return self._read_register(0x010C, number_of_decimals=1)

    def max_charging_current_today(self) -> float:
        """
        Maximum charging current for the current day (amps)
        """
        return self._read_register(0x010D, number_of_decimals=2)

    def max_discharging_current_today(self) -> float:
        """
        Maximum discharging current for the current day (amps)
        """
        return self._read_register(0x010E, number_of_decimals=2)

    def max_charging_power_today(self) -> int:
        """
        Maximum charging power for the current day (watts)
        """
        return self._read_register(0x010F)

    def max_discharging_power_today(self) -> int:
        """
        Maximum discharging power for the current day (watts)
        """
        return self._read_register(0x0110)

    def charging_amphours_today(self) -> int:
        """
        Charging amp hours for the current day
        """
        return self._read_register(0x0111)

    def discharging_amphours_today(self) -> int:
        """
        Discharging amp hours for the current day
        """
        return self._read_register(0x0112)

    def power_generation_today(self) -> float:
        """
        Power generated today (kilowatt hours)
        """
        return self._read_register(0x0113, number_of_decimals=4)

    def power_consumption_today(self) -> float:
        """
        Power consumed today (kilowatt hours)
        """
        return self._read_register(0x0114, number_of_decimals=4)

    def total_operating_days(self) -> int:
        """
        Total number of operating days
        """
        return self._read_register(0x0115)

    def total_battery_over_discharges(self) -> int:
        """
        Total number of battery over-discharges
        """
        return self._read_register(0x0116)

    def total_battery_full_charges(self) -> int:
        """
        Total number of battery full-charges
        """
        return self._read_register(0x0117)

    def total_battery_charge_amphours(self) -> int:
        """
        Total number of amp hours charged to the battery
        """
        return self._read_register(0x0118)

    def total_battery_discharge_amphours(self) -> int:
        """
        Total number of amp hours discharged from the battery
        """
        return self._read_register(0x011A)

    def cumulative_power_generation(self) -> float:
        """
        Total power generated (kilowatt hours)
        """
        return self._read_register(0x011C, number_of_decimals=4)

    def cumulative_power_consumption(self) -> float:
        """
        Total power consumed (kilowatt hours)
        """
        return self._read_register(0x011E, number_of_decimals=4)

    def set_street_light(self, state: OnOff):
        """
        Set street light (load) status on/off

        :param state: OnOff
        """
        self.device.write_register(0x010A, state.value)

    def street_light_status(self) -> Union[OnOff, None]:
        """
        Street light (load) status on/off
        """
        register = self._read_register(0x0120)
        high_byte = register >> 8
        try:
            return OnOff(high_byte >> 7)
        except ValueError:
            logger.warning(f"unknown street light status ({high_byte})")
            return None

    def set_street_light_brightness(self, intensity: int):
        """
        Set street light (load) brightness percentage

        :param intensity: 0-100 (%)
        """
        if intensity < 0 or intensity > 100:
            logger.warning(f"intensity ({intensity}) must be between 0 and 100")
            return
        self.device.write_register(0xE001, intensity)

    def street_light_brightness(self) -> int:
        """
        Street light (load) brightness percentage
        """
        register = self._read_register(0x0120)
        high_byte = register >> 8
        return high_byte & 0x7F

    def charging_state(self) -> Union[ChargingState, None]:
        """
        Charging state
        """
        register = self._read_register(0x0120)
        low_byte = register & 0x00FF
        try:
            return ChargingState(low_byte)
        except ValueError:
            logger.warning(f"unknown charging state ({low_byte})")
            return None

    # Controller fault information
    def controller_fault_information(self) -> list[Fault]:
        register = self._read_registers(0x0121, number_of_registers=2)
        double = register[0] << 16 | register[1]
        return [fault for fault in Fault if double & fault.value == fault.value]

    # Battery parameter settings
    def nominal_battery_capacity(self) -> int:
        """
        Nominal battery capacity (amp hours)
        """
        return self._read_register(0xE002)

    def system_voltage_setting(self) -> int:
        """
        System voltage setting (volts)
        """
        register = self._read_register(0xE003)
        return register >> 8

    def recognized_voltage(self) -> int:
        """
        Recognized voltage (volts)
        """
        register = self._read_register(0xE003)
        return register & 0x00FF

    def battery_type(self) -> Union[BatteryType, None]:
        """
        Battery type
        """
        register = self._read_register(0xE004)
        try:
            return BatteryType(register)
        except ValueError:
            logger.warning(f"unknown battery type ({register})")
            return None

    def over_voltage_threshold(self) -> int:
        """
        Over voltage threshold (volts)
        """
        return self._read_register(0xE005)

    def charging_voltage_limit(self) -> int:
        """
        Charging voltage limit (volts)
        """
        return self._read_register(0xE006)

    def equalizing_charging_voltage(self) -> int:
        """
        Equalizing charging voltage (volts)
        """
        return self._read_register(0xE007)

    def boost_charging_voltage(self) -> int:
        """
        Boost charging voltage (volts)
        """
        return self._read_register(0xE008)

    def floating_voltage(self) -> int:
        """
        Floating voltage (volts)
        """
        return self._read_register(0xE009)

    def boost_charging_recovery_voltage(self) -> int:
        """
        Boost charging recovery voltage (volts)
        """
        return self._read_register(0xE00A)

    def over_discharge_recovery_voltage(self) -> int:
        """
        Over discharge recovery voltage (volts)
        """
        return self._read_register(0xE00B)

    def under_voltage_warning_level(self) -> int:
        """
        Under voltage warning level (volts)
        """
        return self._read_register(0xE00C)

    def over_discharge_voltage(self) -> int:
        """
        Over discharge voltage (volts)
        """
        return self._read_register(0xE00D)

    def discharging_limit_voltage(self) -> int:
        """
        Discharging limit voltage (volts)
        """
        return self._read_register(0xE00E)

    def end_of_charge_soc(self) -> int:
        """
        End of charge SOC (state of charge)
        """
        register = self._read_register(0xE00F)
        return register >> 8

    def end_of_discharge_soc(self) -> int:
        """
        End of discharge SOC (state of charge)
        """
        register = self._read_register(0xE00F)
        return register & 0x00FF

    def over_discharge_time_delay(self) -> int:
        """
        Over discharge time delay (seconds)
        """
        return self._read_register(0xE010)

    def equalizing_charging_time(self) -> int:
        """
        Equalizing charging time (minutes)
        """
        return self._read_register(0xE011)

    def boost_charging_time(self) -> int:
        """
        Boost charging time (minutes)
        """
        return self._read_register(0xE012)

    def equalizing_charging_interval(self) -> int:
        """
        Equalizing charging interval (days)
        """
        return self._read_register(0xE013)

    def temperature_compensation_factor(self) -> int:
        """
        Temperature compensation factor (mV/degrees C/2V)
        """
        return self._read_register(0xE014)

    # Load operating duration and power settings
    def first_stage_operating_duration(self) -> int:
        """
        First stage operating duration (hours)
        """
        return self._read_register(0xE015)

    def first_stage_operating_power(self) -> int:
        """
        First stage operating power (%)
        """
        return self._read_register(0xE016)

    def second_stage_operating_duration(self) -> int:
        """
        Second stage operating duration (hours)
        """
        return self._read_register(0xE017)

    def second_stage_operating_power(self) -> int:
        """
        Second stage operating power (%)
        """
        return self._read_register(0xE018)

    def third_stage_operating_duration(self) -> int:
        """
        Third stage operating duration (hours)
        """
        return self._read_register(0xE019)

    def third_stage_operating_power(self) -> int:
        """
        Third stage operating power (%)
        """
        return self._read_register(0xE01A)

    def morning_on_operating_duration(self) -> int:
        """
        Morning on operating duration (hours)
        """
        return self._read_register(0xE01B)

    def morning_on_operating_power(self) -> int:
        """
        Morning on operating power (%)
        """
        return self._read_register(0xE01C)

    # Mode setting
    def load_working_mode(self) -> Union[LoadWorkingModes, None]:
        """
        Load working mode
        """
        register = self._read_register(0xE01D)
        try:
            return LoadWorkingModes(register)
        except ValueError:
            logger.warning(f"unknown load working mode ({register})")
            return None

    def light_control_delay(self) -> int:
        """
        Light control delay (minutes)
        """
        return self._read_register(0xE01E)

    def light_control_voltate(self) -> int:
        """
        Light control voltage (volts)
        """
        return self._read_register(0xE01F)

    def led_load_current_setting(self) -> float:
        """
        LED load current setting (milliamps)
        """
        return self._read_register(0xE020) * 10

    # Special power control
    def charging_mode_controlled_by(self) -> Union[ChargingModeController, None]:
        """
        Special power charging mode controlled by (voltage or state of charge)
        """
        register = self._read_register(0xE020)
        high_byte = register >> 8
        value = high_byte >> 2 & 0x01
        try:
            return ChargingModeController(value)
        except ValueError:
            logger.warning(f"unknown charging mode controller ({value})")
            return None

    def special_power_control_state(self) -> Union[OnOff, None]:
        """
        Special power control state (on/off)
        """
        register = self._read_register(0xE020)
        high_byte = register >> 8
        value = high_byte >> 1 & 0x01
        try:
            return OnOff(value)
        except ValueError:
            logger.warning(f"unknown special power control state ({value})")
            return None

    def each_night_on_function_state(self) -> Union[OnOff, None]:
        """
        Each night on function state (on/off)
        """
        register = self._read_register(0xE020)
        high_byte = register >> 8
        value = high_byte & 0x01
        try:
            return OnOff(value)
        except ValueError:
            logger.warning(f"unknown special power control state ({value})")
            return None

    def no_charging_below_freezing(self) -> Union[OnOff, None]:
        """
        Allow charging below 0C (on/off)
        """
        register = self._read_register(0xE021)
        low_byte = register & 0x00FF
        value = low_byte >> 2 & 0x01
        try:
            return OnOff(value)
        except ValueError:
            logger.warning(
                f"unknown value for no charging below freezing setting ({value})"
            )
            return None

    def charging_method(self) -> Union[ChargingMethod, None]:
        """
        Charging method
        """
        register = self._read_register(0xE021)
        low_byte = register & 0x00FF
        value = low_byte & 0x01
        try:
            return ChargingMethod(value)
        except ValueError:
            logger.warning(f"unknown charging method ({value})")
            return None

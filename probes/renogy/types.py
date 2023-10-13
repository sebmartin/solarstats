from enum import Enum


class BatteryType(Enum):
    OPEN = 0x01
    SEALED = 0x02
    GEL = 0x03
    LITHIUM = 0x04
    SELF_CUSTOMIZED = 0x05

    def __str__(self) -> str:
        match self:
            case BatteryType.OPEN:
                return "Open"
            case BatteryType.SEALED:
                return "Sealed"
            case BatteryType.GEL:
                return "Gel"
            case BatteryType.LITHIUM:
                return "Lithium"
            case BatteryType.SELF_CUSTOMIZED:
                return "Self-customized"
            case _:
                return "Unknown battery type"


class ProductType(Enum):
    CHARGE_CONTROLLER = 0x00
    INVERTER = 0x01

    def __str__(self) -> str:
        match self:
            case ProductType.CHARGE_CONTROLLER:
                return "Charge controller"
            case ProductType.INVERTER:
                return "Inverter"
            case _:
                return "Unknown product type"


class OnOff(Enum):
    OFF = 0x00
    ON = 0x01

    def __str__(self) -> str:
        match self:
            case OnOff.OFF:
                return "Off"
            case OnOff.ON:
                return "On"
            case _:
                return "Unknown on/off state"


class ChargingState(Enum):
    DEACTIVATED = 0x00
    ACTIVATED = 0x01
    MPPT = 0x02
    EQUALIZING = 0x03
    BOOST = 0x04
    FLOATING = 0x05
    CURRENT_LIMITING = 0x06

    def __str__(self) -> str:
        match self:
            case ChargingState.DEACTIVATED:
                return "Charging deactivated"
            case ChargingState.ACTIVATED:
                return "Charging activated"
            case ChargingState.MPPT:
                return "MPPT charging mode"
            case ChargingState.EQUALIZING:
                return "Equalizing charging mode"
            case ChargingState.BOOST:
                return "Boost charging mode"
            case ChargingState.FLOATING:
                return "Floating charging mode"
            case ChargingState.CURRENT_LIMITING:
                return "Current limiting (overpower)"
            case _:
                return "Unknown charging state"


class Fault(Enum):
    BATTERY_OVER_DISCHARGE = 1 << 16
    BATTERY_OVER_VOLTAGE = 1 << 17
    BATTERY_UNDER_VOLTAGE = 1 << 18
    LOAD_SHORT_CIRCUIT = 1 << 19
    LOAD_OVER_CURRENT = 1 << 20
    CONTROL_TEMPERATURE_TOO_HIGH = 1 << 21
    AMBIENT_TEMPERATURE_TOO_HIGH = 1 << 22
    PHOTOVOLTAIC_OVER_POWER = 1 << 23
    PHOTOVOLTAIC_INPUT_SHORT_CIRCUIT = 1 << 24
    PHOTOVOLTAIC_INPUT_OVER_VOLTAGE = 1 << 25
    SOLAR_COUNTER_CURRENT = 1 << 26
    SOLAR_WORKING_POINT_OVER_VOLTAGE = 1 << 27
    SOLAR_REVERSELY_CONNECTED = 1 << 28
    ANTI_REVERSE_MOS_SHORT_CIRCUIT = 1 << 29
    CIRCUIT_CHARGE_MOS_SHORT_CIRCUIT = 1 << 30

    def __str__(self) -> str:
        match self:
            case Fault.BATTERY_OVER_DISCHARGE:
                return "Battery over discharge"
            case Fault.BATTERY_OVER_VOLTAGE:
                return "Battery over voltage"
            case Fault.BATTERY_UNDER_VOLTAGE:
                return "Battery under voltage"
            case Fault.LOAD_SHORT_CIRCUIT:
                return "Load short circuit"
            case Fault.LOAD_OVER_CURRENT:
                return "Load over current"
            case Fault.CONTROL_TEMPERATURE_TOO_HIGH:
                return "Control temperature too high"
            case Fault.AMBIENT_TEMPERATURE_TOO_HIGH:
                return "Ambient temperature too high"
            case Fault.PHOTOVOLTAIC_OVER_POWER:
                return "Photovoltaic over power"
            case Fault.PHOTOVOLTAIC_INPUT_SHORT_CIRCUIT:
                return "Photovoltaic input short circuit"
            case Fault.PHOTOVOLTAIC_INPUT_OVER_VOLTAGE:
                return "Photovoltaic input over voltage"
            case Fault.SOLAR_COUNTER_CURRENT:
                return "Solar counter current"
            case Fault.SOLAR_WORKING_POINT_OVER_VOLTAGE:
                return "Solar working point over voltage"
            case Fault.SOLAR_REVERSELY_CONNECTED:
                return "Solar reversely connected"
            case Fault.ANTI_REVERSE_MOS_SHORT_CIRCUIT:
                return "Anti-reverse MOS short circuit"
            case Fault.CIRCUIT_CHARGE_MOS_SHORT_CIRCUIT:
                return "Circuit charge MOS short circuit"
            case _:
                return "Unknown fault"


class ChargingModeController(Enum):
    VOLTAGE = 0x01
    SOC = 0x00

    def __str__(self) -> str:
        match self:
            case ChargingModeController.VOLTAGE:
                return "Voltage"
            case ChargingModeController.SOC:
                return "State of charge"
            case _:
                return "Unknown charging mode controller"


class ChargingMethod(Enum):
    DIRECT = 0x00
    PWM = 0x01

    def __str__(self) -> str:
        match self:
            case ChargingMethod.DIRECT:
                return "Direct charging"
            case ChargingMethod.PWM:
                return "PWM"
            case _:
                return "Unknown charging method"


class LoadWorkingModes(Enum):
    SOLELY_LIGHT_CONTROL = 0x00
    OFF_AFTER_1H = 0x01
    OFF_AFTER_2H = 0x02
    OFF_AFTER_3H = 0x03
    OFF_AFTER_4H = 0x04
    OFF_AFTER_5H = 0x05
    OFF_AFTER_6H = 0x06
    OFF_AFTER_7H = 0x07
    OFF_AFTER_8H = 0x08
    OFF_AFTER_9H = 0x09
    OFF_AFTER_10H = 0x0A
    OFF_AFTER_11H = 0x0B
    OFF_AFTER_12H = 0x0C
    OFF_AFTER_13H = 0x0D
    OFF_AFTER_14H = 0x0E
    MANUAL = 0x0F
    DEBUG = 0x10
    NORMAL_ON = 0x11

    def __str__(self) -> str:
        match self:
            case LoadWorkingModes.SOLELY_LIGHT_CONTROL:
                return "Sole light control over " "on/off of load"
            case LoadWorkingModes.OFF_AFTER_1H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 1 hour"
                )
            case LoadWorkingModes.OFF_AFTER_2H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 2 hours"
                )
            case LoadWorkingModes.OFF_AFTER_3H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 3 hours"
                )
            case LoadWorkingModes.OFF_AFTER_4H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 4 hours"
                )
            case LoadWorkingModes.OFF_AFTER_5H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 5 hours"
                )
            case LoadWorkingModes.OFF_AFTER_6H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 6 hours"
                )
            case LoadWorkingModes.OFF_AFTER_7H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 7 hours"
                )
            case LoadWorkingModes.OFF_AFTER_8H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 8 hours"
                )
            case LoadWorkingModes.OFF_AFTER_9H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 9 hours"
                )
            case LoadWorkingModes.OFF_AFTER_10H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 10 hours"
                )
            case LoadWorkingModes.OFF_AFTER_11H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 11 hours"
                )
            case LoadWorkingModes.OFF_AFTER_12H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 12 hours"
                )
            case LoadWorkingModes.OFF_AFTER_13H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 13 hours"
                )
            case LoadWorkingModes.OFF_AFTER_14H:
                return (
                    "Load is turned on by light control, and goes off after a time "
                    "delay of 14 hours"
                )
            case LoadWorkingModes.MANUAL:
                return "Manual on/off of load"
            case LoadWorkingModes.DEBUG:
                return "Debug mode"
            case LoadWorkingModes.NORMAL_ON:
                return "Load is always on"
            case _:
                return "Unknown load working mode"

import aiohttps

from .constants import SYSTEM_STATE_NAME
from .util import parse


class Senec:
    """Senec Home Battery Sensor"""

    def __init__(self, host, websession):
        self.host = host
        self.websession: aiohttp.websession = websession
        self.url = f"https://{host}/lala.cgi"

    @property
    def system_state(self) -> str:
        """
        Textual descritpion of energy status

        """
        value = self._raw["ENERGY"]["STAT_STATE"]
        return SYSTEM_STATE_NAME[value]

    @property
    def raw_status(self) -> dict:
        """
        Raw dict with all information

        """
        return self._raw

    @property
    def house_power(self) -> float:
        """
        Current power consumption (W)

        """
        return self._raw["ENERGY"]["GUI_HOUSE_POW"]

    @property
    def house_total_consumption(self) -> float:
        """
        Total energy used by house (kWh)

        Does not include Wallbox.
        """
        return self._raw["STATISTIC"]["LIVE_HOUSE_CONS"]

    @property
    def solar_generated_power(self) -> float:
        """
        Current power generated by solar panels (W)

        """
        return abs(self._raw["ENERGY"]["GUI_INVERTER_POWER"])

    @property
    def solar_total_generated(self) -> float:
        """
        Total energy generated by solar panels (kWh)

        """
        return self._raw["STATISTIC"]["LIVE_PV_GEN"]

    @property
    def battery_charge_percent(self) -> float:
        """
        Current battery charge value (%)

        """
        return self._raw["ENERGY"]["GUI_BAT_DATA_FUEL_CHARGE"]

    @property
    def battery_charge_power(self) -> float:
        """
        Current battery charging power (W)

        """
        value = self._raw["ENERGY"]["GUI_BAT_DATA_POWER"]
        if value > 0:
            return value
        return 0

    @property
    def battery_discharge_power(self) -> float:
        """
        Current battery discharging power (W)

        """
        value = self._raw["ENERGY"]["GUI_BAT_DATA_POWER"]
        if value < 0:
            return abs(value)
        return 0
    
    @property
    def mpp_power_0(self) -> float:
        return self._raw["PV1"]["MPP_POWER"][0] 
    @property
    def mpp_power_1(self) -> float:
        return self._raw["PV1"]["MPP_POWER"][1] 
    @property
    def mpp_power_2(self) -> float:
        return self._raw["PV1"]["MPP_POWER"][2] 
    
    @property
    def ac_spannung_l1(self) -> float:
        return self._raw["PM1OBJ1"]["U_AC"][0]
    @property
    def ac_spannung_l2(self) -> float:
        return self._raw["PM1OBJ1"]["U_AC"][1]
    @property
    def ac_spannung_l3(self) -> float:
        return self._raw["PM1OBJ1"]["U_AC"][2]
    
    @property
    def ac_strom_l1(self) -> float:
        return self._raw["PM1OBJ1"]["I_AC"][0]
    @property
    def ac_strom_l2(self) -> float:
        return self._raw["PM1OBJ1"]["I_AC"][1]
    @property
    def ac_strom_l3(self) -> float:
        return self._raw["PM1OBJ1"]["I_AC"][2]
    
    @property
    def ac_leistung_l1(self) -> float:
        return self._raw["PM1OBJ1"]["P_AC"][0]
    @property
    def ac_leistung_l2(self) -> float:
        return self._raw["PM1OBJ1"]["P_AC"][1]
    @property
    def ac_leistung_l3(self) -> float:
        return self._raw["PM1OBJ1"]["P_AC"][2]

    @property
    def battery_state_power(self) -> float:
        """
        Battery charging power (W)

        Value is positive when battery is charging
        Value is negative when battery is discharging.
        """
        return self._raw["ENERGY"]["GUI_BAT_DATA_POWER"]

    @property
    def battery_total_charged(self) -> float:
        """
        Total energy charged to battery (kWh)

        """
        return self._raw["STATISTIC"]["LIVE_BAT_CHARGE"]

    @property
    def battery_total_discharged(self) -> float:
        """
        Total energy discharged from battery (kWh)

        """
        return self._raw["STATISTIC"]["LIVE_BAT_DISCHARGE"]

    @property
    def grid_imported_power(self) -> float:
        """
        Current power imported from grid (W)

        """
        value = self._raw["ENERGY"]["GUI_GRID_POW"]
        if value > 0:
            return value
        return 0

    @property
    def grid_exported_power(self) -> float:
        """
        Current power exported to grid (W)

        """
        value = self._raw["ENERGY"]["GUI_GRID_POW"]
        if value < 0:
            return abs(value)
        return 0

    @property
    def grid_state_power(self) -> float:
        """
        Grid exchange power (W)

        Value is positive when power is imported from grid.
        Value is negative when power is exported to grid.
        """
        return self._raw["ENERGY"]["GUI_GRID_POW"]

    @property
    def grid_total_export(self) -> float:
        """
        Total energy exported to grid export (kWh)

        """
        return self._raw["STATISTIC"]["LIVE_GRID_EXPORT"]

    @property
    def grid_total_import(self) -> float:
        """
        Total energy imported from grid (kWh)

        """
        return self._raw["STATISTIC"]["LIVE_GRID_IMPORT"]

    @property
    def wallbox_power(self) -> float:
        """
        Wallbox Total Charging Power (W)
        Derived from the 3 phase voltages multiplied with the phase currents from the wallbox

        """
        return self._raw["WALLBOX"]["APPARENT_CHARGING_POWER"][0]

    @property
    def wallbox_ev_connected(self) -> bool:
        """
        Wallbox EV Connected

        """
        return self._raw["WALLBOX"]["EV_CONNECTED"][0]

    @property
    def wallbox_energy(self) -> float:
        """
        Wallbox Total Energy

        """
        return self._raw["STATISTIC"]["LIVE_WB_ENERGY"][0] / 1000.0

    @property
    def battery_temp(self) -> float:
        """
        Current battery temperature
        """
        return self._raw["TEMPMEASURE"]["BATTERY_TEMP"]
    @property
    def case_temp(self) -> float:
        """
        Current case temperature
        """
        return self._raw["TEMPMEASURE"]["CASE_TEMP"]
    @property
    def mcu_temp(self) -> float:
        """
        Current controller temperature
        """
        return self._raw["TEMPMEASURE"]["MCU_TEMP"]
    
    @property
    def bms_cell_temp_A1(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_A"][0] 
    @property
    def bms_cell_temp_A2(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_A"][1] 
    @property
    def bms_cell_temp_A3(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_A"][2] 
    @property
    def bms_cell_temp_A4(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_A"][3] 
    @property
    def bms_cell_temp_A5(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_A"][4] 
    @property
    def bms_cell_temp_A6(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_A"][5] 

    @property
    def bms_cell_temp_B1(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_B"][0] 
    @property
    def bms_cell_temp_B2(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_B"][1] 
    @property
    def bms_cell_temp_B3(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_B"][2] 
    @property
    def bms_cell_temp_B4(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_B"][3] 
    @property
    def bms_cell_temp_B5(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_B"][4] 
    @property
    def bms_cell_temp_B6(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_B"][5] 

    @property
    def bms_cell_temp_C1(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_C"][0] 
    @property
    def bms_cell_temp_C2(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_C"][1] 
    @property
    def bms_cell_temp_C3(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_C"][2] 
    @property
    def bms_cell_temp_C4(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_C"][3] 
    @property
    def bms_cell_temp_C5(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_C"][4] 
    @property
    def bms_cell_temp_C6(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_C"][5] 

    @property
    def bms_cell_temp_D1(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_D"][0] 
    @property
    def bms_cell_temp_D2(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_D"][1] 
    @property
    def bms_cell_temp_D3(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_D"][2] 
    @property
    def bms_cell_temp_D4(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_D"][3] 
    @property
    def bms_cell_temp_D5(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_D"][4] 
    @property
    def bms_cell_temp_D6(self) -> float:
        return self._raw["BMS"]["CELL_TEMPERATURES_MODULE_D"][5] 


    @property
    def bms_cell_volt_A1(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][0] 
    @property
    def bms_cell_volt_A2(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][1]  
    @property
    def bms_cell_volt_A3(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][2]  
    @property
    def bms_cell_volt_A4(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][3]  
    @property
    def bms_cell_volt_A5(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][4]  
    @property
    def bms_cell_volt_A6(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][5]  
    @property
    def bms_cell_volt_A7(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][6]  
    @property
    def bms_cell_volt_A8(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][7]  
    @property
    def bms_cell_volt_A9(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][8]  
    @property
    def bms_cell_volt_A10(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][9]  
    @property
    def bms_cell_volt_A11(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][10] 
    @property
    def bms_cell_volt_A12(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][11] 
    @property
    def bms_cell_volt_A13(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][12] 
    @property
    def bms_cell_volt_A14(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_A"][13] 
    @property
    def bms_cell_volt_B1(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][0] 
    @property
    def bms_cell_volt_B2(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][1]  
    @property
    def bms_cell_volt_B3(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][2]  
    @property
    def bms_cell_volt_B4(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][3]  
    @property
    def bms_cell_volt_B5(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][4]  
    @property
    def bms_cell_volt_B6(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][5]  
    @property
    def bms_cell_volt_B7(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][6]  
    @property
    def bms_cell_volt_B8(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][7]  
    @property
    def bms_cell_volt_B9(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][8]  
    @property
    def bms_cell_volt_B10(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][9]  
    @property
    def bms_cell_volt_B11(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][10] 
    @property
    def bms_cell_volt_B12(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][11] 
    @property
    def bms_cell_volt_B13(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][12] 
    @property
    def bms_cell_volt_B14(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_B"][13] 
    @property
    def bms_cell_volt_C1(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][0] 
    @property
    def bms_cell_volt_C2(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][1]  
    @property
    def bms_cell_volt_C3(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][2]  
    @property
    def bms_cell_volt_C4(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][3]  
    @property
    def bms_cell_volt_C5(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][4]  
    @property
    def bms_cell_volt_C6(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][5]  
    @property
    def bms_cell_volt_C7(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][6]  
    @property
    def bms_cell_volt_C8(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][7]  
    @property
    def bms_cell_volt_C9(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][8]  
    @property
    def bms_cell_volt_C10(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][9]  
    @property
    def bms_cell_volt_C11(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][10] 
    @property
    def bms_cell_volt_C12(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][11] 
    @property
    def bms_cell_volt_C13(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][12] 
    @property
    def bms_cell_volt_C14(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_C"][13] 
    @property
    def bms_cell_volt_D1(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][0] 
    @property
    def bms_cell_volt_D2(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][1]  
    @property
    def bms_cell_volt_D3(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][2]  
    @property
    def bms_cell_volt_D4(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][3]  
    @property
    def bms_cell_volt_D5(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][4]  
    @property
    def bms_cell_volt_D6(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][5]  
    @property
    def bms_cell_volt_D7(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][6]  
    @property
    def bms_cell_volt_D8(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][7]  
    @property
    def bms_cell_volt_D9(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][8]  
    @property
    def bms_cell_volt_D10(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][9]  
    @property
    def bms_cell_volt_D11(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][10] 
    @property
    def bms_cell_volt_D12(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][11] 
    @property
    def bms_cell_volt_D13(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][12] 
    @property
    def bms_cell_volt_D14(self) -> float:
        return self._raw["BMS"]["CELL_VOLTAGES_MODULE_D"][13] 

    @property
    def bms_soc_A(self) -> float:
        return self._raw["BMS"]["SOC"][0] 
    @property
    def bms_soc_B(self) -> float:
        return self._raw["BMS"]["SOC"][1] 
    @property
    def bms_soc_C(self) -> float:
        return self._raw["BMS"]["SOC"][2] 
    @property
    def bms_soc_D(self) -> float:
        return self._raw["BMS"]["SOC"][3] 

    @property
    def bms_soh_A(self) -> float:
        return self._raw["BMS"]["SOH"][0] 
    @property
    def bms_soh_B(self) -> float:
        return self._raw["BMS"]["SOH"][1] 
    @property
    def bms_soh_C(self) -> float:
        return self._raw["BMS"]["SOH"][2] 
    @property
    def bms_soh_D(self) -> float:
        return self._raw["BMS"]["SOH"][3] 

    @property
    def bms_voltage_A(self) -> float:
        return self._raw["BMS"]["VOLTAGE"][0] 
    @property
    def bms_voltage_B(self) -> float:
        return self._raw["BMS"]["VOLTAGE"][1] 
    @property
    def bms_voltage_C(self) -> float:
        return self._raw["BMS"]["VOLTAGE"][2] 
    @property
    def bms_voltage_D(self) -> float:
        return self._raw["BMS"]["VOLTAGE"][3] 

    @property
    def bms_current_A(self) -> float:
        return self._raw["BMS"]["CURRENT"][0] 
    @property
    def bms_current_B(self) -> float:
        return self._raw["BMS"]["CURRENT"][1] 
    @property
    def bms_current_C(self) -> float:
        return self._raw["BMS"]["CURRENT"][2] 
    @property
    def bms_current_D(self) -> float:
        return self._raw["BMS"]["CURRENT"][3] 

    @property
    def bms_cycles_A(self) -> float:
        return self._raw["BMS"]["CYCLES"][0] 
    @property
    def bms_cycles_B(self) -> float:
        return self._raw["BMS"]["CYCLES"][1] 
    @property
    def bms_cycles_C(self) -> float:
        return self._raw["BMS"]["CYCLES"][2] 
    @property
    def bms_cycles_D(self) -> float:
        return self._raw["BMS"]["CYCLES"][3] 

    @property
    def bms_charge_limit_A(self) -> float:
        return self._raw["BMS"]["CHARGE_CURRENT_LIMIT"][0] 
    @property
    def bms_charge_limit_B(self) -> float:
        return self._raw["BMS"]["CHARGE_CURRENT_LIMIT"][1] 
    @property
    def bms_charge_limit_C(self) -> float:
        return self._raw["BMS"]["CHARGE_CURRENT_LIMIT"][2] 
    @property
    def bms_charge_limit_D(self) -> float:
        return self._raw["BMS"]["CHARGE_CURRENT_LIMIT"][3] 

    @property
    def bms_fw_A(self) -> float:
        return self._raw["BMS"]["FW"][0] 
    @property
    def bms_fw_B(self) -> float:
        return self._raw["BMS"]["FW"][1] 
    @property
    def bms_fw_C(self) -> float:
        return self._raw["BMS"]["FW"][2] 
    @property
    def bms_fw_D(self) -> float:
        return self._raw["BMS"]["FW"][3] 

    @property
    def socket_0_state(self) -> float:
        return self._raw["SOCKETS"]["POWER_ON"][0] 
    @property
    def socket_1_state(self) -> float:
        return self._raw["SOCKETS"]["POWER_ON"][1] 

    async def update(self):
        await self.read_senec_v21()

    async def read_senec_v21(self):
        """Read values used by webinterface from Senec Home v2.1

        Note: Not all values are "high priority" and reading everything causes problems with Senec device, i.e. no sync with Senec cloud possible.
        """
        form = {
            "ENERGY": {
                "STAT_STATE": "",
                "GUI_BAT_DATA_POWER": "",
                "GUI_INVERTER_POWER": "",
                "GUI_HOUSE_POW": "",
                "GUI_GRID_POW": "",
                "GUI_BAT_DATA_FUEL_CHARGE": "",
                "GUI_CHARGING_INFO": "",
                "GUI_BOOSTING_INFO": "",
                "GUI_BAT_DATA_POWER": "",
                "GUI_BAT_DATA_VOLTAGE": "",
                "GUI_BAT_DATA_CURRENT": "",
                "GUI_BAT_DATA_FUEL_CHARGE": "",
                "GUI_BAT_DATA_OA_CHARGING": "",
                "STAT_LIMITED_NET_SKEW": "",
            },
            "STATISTIC": {
                "LIVE_BAT_CHARGE": "",
                "LIVE_BAT_DISCHARGE": "",
                "LIVE_GRID_EXPORT": "",
                "LIVE_GRID_IMPORT": "",
                "LIVE_HOUSE_CONS": "",
                "LIVE_PV_GEN": "",
                "LIVE_WB_ENERGY": "",
            },
            "PV1": {"POWER_RATIO": "", "MPP_POWER": ""},
            "PWR_UNIT": {"POWER_L1": "", "POWER_L2": "", "POWER_L3": ""},
            "PM1OBJ1": {"FREQ": "", "U_AC": "", "I_AC": "", "P_AC": "", "P_TOTAL": ""},
            "PM1OBJ2": {"FREQ": "", "U_AC": "", "I_AC": "", "P_AC": "", "P_TOTAL": ""},
            "WALLBOX": {
                "APPARENT_CHARGING_POWER": "",
                "L1_CHARGING_CURRENT": "",
                "L2_CHARGING_CURRENT": "",
                "L3_CHARGING_CURRENT": "",
                "EV_CONNECTED": "",
            },
            "TEMPMEASURE": {
                "BATTERY_TEMP": "",
                "CASE_TEMP": "",
                "MCU_TEMP": "",
            },
            "BMS": {
                "CELL_TEMPERATURES_MODULE_A": "",
                "CELL_TEMPERATURES_MODULE_B": "",
                "CELL_TEMPERATURES_MODULE_C": "",
                "CELL_TEMPERATURES_MODULE_D": "",
                "CELL_VOLTAGES_MODULE_A": "",
                "CELL_VOLTAGES_MODULE_B": "",
                "CELL_VOLTAGES_MODULE_C": "",
                "CELL_VOLTAGES_MODULE_D": "",
                "CHARGE_CURRENT_LIMIT": "",
                "SOC": "",
                "SOH": "",
                "VOLTAGE": "",
                "CYCLES": "",
                "CURRENT": "",
                "FW": "",
            },
            "SOCKETS": {
                "POWER_ON": "",
            },
        }

        async with self.websession.post(self.url, json=form) as res:
            res.raise_for_status()
            self._raw = parse(await res.json())

    async def read_senec_v21_all(self):
        """Read ALL values from Senec Home v2.1

        Note: This causes high demand on the SENEC machine so it shouldn't run too often. Adverse effects: No sync with Senec possible if called too often.
        """
        form = {
            "STATISTIC": {},
            "ENERGY": {},
            "FEATURES": {},
            "LOG": {},
            "SYS_UPDATE": {},
            "WIZARD": {},
            "BMS": {},
            "BAT1": {},
            "BAT1OBJ1": {},
            "BAT1OBJ2": {},
            "BAT1OBJ2": {},
            "BAT1OBJ3": {},
            "BAT1OBJ4": {},
            "PWR_UNIT": {},
            "PV1": {},
        }

        async with self.websession.post(self.url, json=form) as res:
            res.raise_for_status()
            self._raw = parse(await res.json())

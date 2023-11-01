""" Enum with TypeName spaceheat.make.model, Version 001, Status Pending"""
from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class MakeModel(StrEnum):
    """
    Determines Make/Model of device associated to a Spaceheat Node supervised by SCADA
    [More Info](https://gridworks-protocol.readthedocs.io/en/latest/make-model.html).

    Name (EnumSymbol, Version): description
    
      * UNKNOWNMAKE__UNKNOWNMODEL (00000000, 000): 
      * EGAUGE__4030 (beb6d3fb, 000): A power meter in Egauge's 403x line. 
          [More Info](https://store.egauge.net/meters).
      * NCD__PR814SPST (fabfa505, 000): NCD's 4-channel high-power relay controller + 4 GPIO 
          with I2C interface.
          [More Info](https://store.ncd.io/product/4-channel-high-power-relay-controller-4-gpio-with-i2c-interface/?attribute_pa_choose-a-relay=20-amp-spdt).
      * ADAFRUIT__642 (acd93fb3, 000): Adafruit's high-temp, water-proof 1-wire temp sensor. 
          [More Info](https://www.adafruit.com/product/642).
      * GRIDWORKS__TSNAP1 (d0178dc3, 000): Actual GridWorks TSnap 1.0 SCADA Box
      * GRIDWORKS__WATERTEMPHIGHPRECISION (f8b497e8, 000): Simulated temp sensor
      * GRIDWORKS__SIMPM1 (076da322, 000): Simulated power meter
      * SCHNEIDERELECTRIC__IEM3455 (d300635e, 000): Schneider Electric IEM 344 utility meter
      * GRIDWORKS__SIMBOOL30AMPRELAY (e81d74a8, 000): Simulated relay
      * OPENENERGY__EMONPI (c75d269f, 000): Open Energy's open source multipurpose sensing device
          (including internal power meter). 
          [More Info](https://docs.openenergymonitor.org/emonpi/technical.html).
      * GRIDWORKS__SIMTSNAP1 (3042c432, 000): Simulated SCADA Box
      * ATLAS__EZFLO (d0b0e375, 000): Atlas Scientific EZO Embedded Flow Meter Totalizer, pulse to I2C. 
          [More Info](https://drive.google.com/drive/u/0/folders/142bBV1pQIbMpyIR_0iRUr5gnzWgknOJp).
      * HUBITAT__C7__LAN1 (4d649420, 001): This refers to a Hubitat C7 that has been configured
          in a specific way with respect to the APIs it presents on the Local Area Network. The
          Hubitat C7 is a home automation hub that supports building ZigBee and ZWave meshes, 
          plugs into Ethernet, has a reasonable user interface and has an active community of 
          open-source developers who create drivers and package managers for devices, and supports
          the creation of various types of APIs on the Local Area Network.
          [More Info](https://drive.google.com/drive/folders/1AqAU_lC2phzuI9XRYvogiIYA7GXNtlr6).
      * GRIDWORKS__TANK_MODULE_1 (bd759051, 001): This refers to a small module designed and 
          assembled by GridWorks that is meant to be mounted to the side of a hot water tank. It 
          requires 24V DC and has 4 temperature sensors coming out of it labeled 1, 2, 3 and 4. 
          It is meant to provide temperature readings (taken within a half a second of each other) 
          of all 4 of its sensors once a minute.
        [More Info](https://drive.google.com/drive/folders/1GSxDd8Naf1GKK_fSOgQU933M1UcJ4r8q).
      * FIBARO__ANALOG_TEMP_SENSOR (1f19839d, 001): This enum refers to a Fibaro home automation 
          device that has been configured in a specific way. This includes (1) being attached to two 
          10K NTC thermistors and a specific voltage divider circuit that specifies its temperature
          as a function of voltage and (2) one of its potential free outputs being in-line with 
          the power of a partner Fibaro, so that it can power cycle its partner (because there are 
          reports of Fibaros no longer reporting temp change after weeks or months until power cylced).
          The Fibaro itself is a tiny (29 X 18 X 13 mm) Z-Wave device powered on 9-30V DC that can read 
          up to 6 1-wire DS18B20 temp sensors, 2 0-10V analog inputs and also has 2 potential free outputs.
          [More Info](https://drive.google.com/drive/u/0/folders/1Muhsvw00goppHIfGSEmreX4hM6V78b-m).
      * AMPHENOL__NTC_10K_THERMISTOR_MA100GG103BN (46f21cd5, 001): A small gauge, low-cost, rapid response 
          NTC 10K Thermistor designed for medical applications.
         [More Info](https://drive.google.com/drive/u/0/folders/11HW4ov66UvxKAwqApW6IrtoXatZBLQkd).
    """
    UNKNOWNMAKE__UNKNOWNMODEL = auto()
    EGAUGE__4030 = auto()
    NCD__PR814SPST = auto()
    ADAFRUIT__642 = auto()
    GRIDWORKS__TSNAP1 = auto()
    GRIDWORKS__WATERTEMPHIGHPRECISION = auto()
    GRIDWORKS__SIMPM1 = auto()
    SCHNEIDERELECTRIC__IEM3455 = auto()
    GRIDWORKS__SIMBOOL30AMPRELAY = auto()
    OPENENERGY__EMONPI = auto()
    GRIDWORKS__SIMTSNAP1 = auto()
    ATLAS__EZFLO = auto()
    HUBITAT__C7__LAN1 = auto()
    GRIDWORKS__TANK_MODULE_1 = auto()
    FIBARO__ANALOG_TEMP_SENSOR = auto()
    AMPHENOL__NTC_10K_THERMISTOR_MA100GG103BN = auto()
    
    @classmethod
    def default(cls) -> "MakeModel":
        """
        Returns default value UNKNOWNMAKE__UNKNOWNMODEL
        """
        return cls.UNKNOWNMAKE__UNKNOWNMODEL

    @classmethod
    def values(cls) -> List[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]

from typing import Optional

import yarl

from gwproto.data_classes.component import Component
from gwproto.data_classes.components.hubitat_component import HubitatComponent
from gwproto.data_classes.resolver import ComponentResolver
from gwproto.data_classes.sh_node import ShNode
from gwproto.types.hubitat_component_gt import HubitatComponentGt
from gwproto.types.hubitat_component_gt import HubitatRESTResolutionSettings
from gwproto.types.hubitat_gt import HubitatGt
from gwproto.types.hubitat_tank_gt import FibaroTempSensorSettings
from gwproto.types.hubitat_tank_gt import FibaroTempSensorSettingsGt
from gwproto.types.hubitat_tank_gt import HubitatTankSettingsGt
from gwproto.types.telemetry_reporting_config import TelemetryReportingConfig


class HubitatTankComponent(Component, ComponentResolver):
    hubitat: HubitatComponentGt
    sensor_supply_voltage: float
    devices_gt: list[FibaroTempSensorSettingsGt]
    devices: list[FibaroTempSensorSettings] = []

    def __init__(
        self,
        component_id: str,
        component_attribute_class_id: str,
        tank_gt: HubitatTankSettingsGt,
        display_name: Optional[str] = None,
        hw_uid: Optional[str] = None,
    ):
        # Create self.hubitat as a proxy containing only the id
        # of the hubitat; the actual component data will be resolved
        # when resolve() is called; Here in the constructor we cannot
        # rely on the actual HubitatComponentGt existing yet.
        self.hubitat = HubitatComponentGt(
            ComponentId=tank_gt.hubitat_component_id,
            ComponentAttributeClassId="00000000-0000-0000-0000-000000000000",
            Hubitat=HubitatGt(
                Host="",
                MakerApiId=-1,
                AccessToken="",
                MacAddress="000000000000",
            ),
        )
        self.sensor_supply_voltage = tank_gt.sensor_supply_voltage
        self.devices_gt = list(tank_gt.devices)
        super().__init__(
            display_name=display_name,
            component_id=component_id,
            hw_uid=hw_uid,
            component_attribute_class_id=component_attribute_class_id,
        )

    def resolve(
        self,
        tank_node_name: str,
        nodes: dict[str, ShNode],
        components: dict[str, Component],
    ):
        hubitat_component = components.get(self.hubitat.ComponentId, None)
        if hubitat_component is None:
            raise ValueError(
                "ERROR. No component found for "
                f"HubitatTankComponent.hubitat.CompnentId {self.hubitat.ComponentId}"
            )
        if not isinstance(hubitat_component, HubitatComponent):
            raise ValueError(
                "ERROR. Referenced hubitat component has type "
                f"{type(hubitat_component)}; "
                "must be instance of HubitatComponent. "
                f"Hubitat component id: {self.hubitat.ComponentId}"
            )
        hubitat_component_gt = HubitatComponentGt.from_data_class(hubitat_component)
        hubitat_settings = HubitatRESTResolutionSettings(hubitat_component_gt)
        devices = [
            FibaroTempSensorSettings.create(
                tank_name=tank_node_name,
                settings_gt=device_gt,
                hubitat=hubitat_settings,
            )
            for device_gt in self.devices_gt
            if device_gt.enabled
        ]
        for device in devices:
            if device.node_name not in nodes:
                raise ValueError(
                    f"ERROR. Node not found for tank temp sensor <{device.node_name}>"
                )
        # replace proxy hubitat component, which only had component id.
        # with the actual hubitat component containing data.
        self.hubitat = hubitat_component_gt
        self.devices = devices

    def urls(self) -> dict[str, Optional[yarl.URL]]:
        urls = self.hubitat.urls()
        for device in self.devices:
            urls[device.node_name] = device.url
        return urls

    @property
    def config_list(self) -> list[TelemetryReportingConfig]:
        return [
            TelemetryReportingConfig(
                TelemetryName=device.telemetry_name,
                AboutNodeName=device.node_name,
                ReportOnChange=False,
                SamplePeriodS=int(device.rest.poll_period_seconds),
                Exponent=device.exponent,
                Unit=device.unit,
            )
            for device in self.devices
        ]

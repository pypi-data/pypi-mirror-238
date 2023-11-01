import copy
import re
from functools import cached_property
from typing import Optional

import yarl
from pydantic import BaseModel
from pydantic import Extra
from pydantic import conint
from pydantic import validator

from gwproto.enums import TelemetryName as EnumTelemetryName
from gwproto.enums import Unit as EnumUnit
from gwproto.types.hubitat_component_gt import HubitatRESTResolutionSettings
from gwproto.types.rest_poller_gt import RequestArgs
from gwproto.types.rest_poller_gt import RESTPollerSettings
from gwproto.types.rest_poller_gt import URLArgs
from gwproto.types.rest_poller_gt import URLConfig
from gwproto.types.simple_temp_sensor_cac_gt import TelemetryNameMap
from gwproto.types.simple_temp_sensor_cac_gt import UnitMap
from gwproto.utils import snake_to_camel


HUBITAT_ID_REGEX = re.compile(
    r".*/apps/api/(?P<api_id>-?\d+)/devices/(?P<device_id>-?\d+).*?"
)
HUBITAT_ACCESS_TOKEN_REGEX = re.compile(
    r".*\?.*access_token=(?P<access_token>[a-fA-F0-9\-]+).*"
)


class FibaroTempSensorSettingsGt(BaseModel):
    stack_depth: conint(ge=1)
    device_id: int
    fibaro_component_id: str
    analog_input_id: conint(ge=1, le=2)
    tank_label: str = ""
    exponent: int = 1
    telemetry_name_gt_enum_symbol: str = "c89d0ba1"
    temp_unit_gt_enum_symbol: str = "ec14bd47"
    enabled: bool = True
    rest: Optional[RESTPollerSettings] = None

    class Config:
        extra = Extra.allow
        alias_generator = snake_to_camel
        allow_population_by_field_name = True

    @validator("telemetry_name_gt_enum_symbol")
    def _check_telemetry_name_symbol(cls, v: str) -> str:
        if v not in TelemetryNameMap.type_to_versioned_enum_dict:
            v = TelemetryNameMap.local_to_type(EnumTelemetryName.default())
        return v

    @validator("temp_unit_gt_enum_symbol")
    def _checktemp_unit_gt_enum_symbol(cls, v: str) -> str:
        if v not in UnitMap.type_to_versioned_enum_dict:
            v = UnitMap.local_to_type(EnumUnit.default())
        return v


DEFAULT_SENSOR_NODE_NAME_FORMAT = "{tank_name}.temp.depth{stack_depth}"


class FibaroTempSensorSettings(FibaroTempSensorSettingsGt):
    node_name: str

    class Config:
        keep_untouched = (cached_property, EnumTelemetryName)

    @validator("rest")
    def _collapse_rest_url(cls, v: Optional[RESTPollerSettings]):
        if v is not None:
            # Collapse session.base_url and request.url into
            # request.url.
            collapsed_url = v.url
            v.session.base_url = URLConfig()
            v.request.url.url_args = URLArgs.from_url(collapsed_url)
        return v

    @property
    def telemetry_name(self) -> EnumTelemetryName:
        return TelemetryNameMap.type_to_local(
            self.telemetry_name_gt_enum_symbol,
        )

    @property
    def unit(self) -> EnumUnit:
        return UnitMap.type_to_local(
            self.temp_unit_gt_enum_symbol,
        )

    @cached_property
    def url(self) -> yarl.URL:
        return self.rest.url

    @cached_property
    def api_id(self) -> int:
        return int(HUBITAT_ID_REGEX.match(str(self.url)).group("api_id"))

    @property
    def host(self) -> str:
        return self.rest.url.host

    @cached_property
    def access_token(self) -> Optional[str]:
        match = HUBITAT_ACCESS_TOKEN_REGEX.match(str(self.url))
        if match:
            return match.group("access_token")
        return None

    def clear_property_cache(self):
        if self.rest is not None:
            self.rest.clear_property_cache()
        for prop in [
            "url",
            "api_id",
            "access_token",
        ]:
            self.__dict__.pop(prop, None)

    def resolve_rest(
        self,
        hubitat: HubitatRESTResolutionSettings,
    ) -> None:
        # Constuct url config on top of maker api url url config
        constructed_config = copy.deepcopy(hubitat.maker_api_url_config)
        constructed_config.url_path_format += "/devices/{device_id}/refresh"
        constructed_config.url_path_args["device_id"] = self.device_id

        if self.rest is None:
            # Since no "inline" rest configuration is present, use constructed url config
            self.rest = RESTPollerSettings(request=RequestArgs(url=constructed_config))
        else:
            # Again, no inline url config is found; use constructed url config
            if self.rest.request.url is None:
                self.rest.request.url = constructed_config
            else:
                # An inline config exists; take items *not* in inline config from
                # constructed config (inline config 'wins' on disagreement)
                existing_config = self.rest.request.url
                if not existing_config.url_args.host:
                    existing_config.url_args.host = constructed_config.url_args.host
                if existing_config.url_path_format is None:
                    existing_config.url_path_format = constructed_config.url_path_format
                if existing_config.url_path_args is None:
                    existing_config.url_path_args = constructed_config.url_path_args
                else:
                    existing_config.url_path_args = dict(
                        constructed_config.url_path_args,
                        **existing_config.url_path_args,
                    )
        self.rest.clear_property_cache()

        # Verify new URL produced by combining any inline REST configuration
        # with hubitat configuration is valid.
        url_str = str(self.rest.url)
        hubitat_gt = hubitat.component_gt.Hubitat
        # check host
        if hubitat_gt.Host != self.rest.url.host:
            raise ValueError(
                "ERROR host expected to be "
                f"{hubitat_gt.Host} but host in url is "
                f"{self.rest.url.host}, from url: <{url_str}>"
            )

        # check api_id
        if hubitat_gt.MakerApiId != self.api_id:
            raise ValueError(
                "ERROR api_id expected to be "
                f"{hubitat_gt.MakerApiId} but api_id in url is "
                f"{self.api_id}, from url: <{url_str}>"
            )

        # check device_id
        id_match = HUBITAT_ID_REGEX.match(url_str)
        if not id_match:
            raise ValueError(
                f"ERROR. ID regex <{HUBITAT_ID_REGEX.pattern}> failed to match "
                f" url <{url_str}>"
            )
        found_device_id = int(id_match.group("device_id"))
        if self.device_id != found_device_id:
            raise ValueError(
                "ERROR explicit device_id is "
                f"{self.device_id} but device in url is "
                f"{found_device_id}, from url: <{url_str}>"
            )

        # check token match
        if hubitat_gt.AccessToken != self.access_token:
            raise ValueError(
                "ERROR explicit access_token is "
                f"{hubitat_gt.AccessToken} but device in url is "
                f"{self.access_token}, from url: <{url_str}>"
            )

    @classmethod
    def create(
        cls,
        tank_name: str,
        settings_gt: FibaroTempSensorSettingsGt,
        hubitat: HubitatRESTResolutionSettings,
        node_name_format=DEFAULT_SENSOR_NODE_NAME_FORMAT,
    ) -> "FibaroTempSensorSettings":
        settings = FibaroTempSensorSettings(
            node_name=node_name_format.format(
                tank_name=tank_name,
                stack_depth=settings_gt.stack_depth,
            ),
            **settings_gt.dict(),
        )
        settings.resolve_rest(hubitat)
        return settings


DEFAULT_TANK_MODULE_VOLTAGE = 23.7


class HubitatTankSettingsGt(BaseModel):
    hubitat_component_id: str
    sensor_supply_voltage: float = DEFAULT_TANK_MODULE_VOLTAGE
    devices: list[FibaroTempSensorSettingsGt] = []

    class Config:
        extra = Extra.allow
        alias_generator = snake_to_camel
        allow_population_by_field_name = True

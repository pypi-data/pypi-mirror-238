from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instrument_resource_profile import InstrumentResourceProfile
    from ..models.resource_profile import ResourceProfile


T = TypeVar("T", bound="SegmentDefinition")


@_attrs_define
class SegmentDefinition:
    """
    Attributes:
        name (str):
        mnemonic (str):
        prime_segment (bool):
        description (Union[Unset, None, str]):
        resources (Union[Unset, None, List['ResourceProfile']]):
        instrument_resources (Union[Unset, None, List['InstrumentResourceProfile']]):
        group (Union[Unset, str]):
        riders (Union[Unset, List[str]]):
        pointing_request_file (Union[Unset, None, str]):
        slew_policy (Union[Unset, str]):
        pointing_target (Union[Unset, None, str]):
        platform_power_profile (Union[Unset, str]):
        scheduler_flag (Union[Unset, None, bool]):
        scheduling_priority (Union[Unset, None, int]):
        observation_definitions (Union[Unset, List[str]]):
    """

    name: str
    mnemonic: str
    prime_segment: bool
    description: Union[Unset, None, str] = UNSET
    resources: Union[Unset, None, List["ResourceProfile"]] = UNSET
    instrument_resources: Union[Unset, None, List["InstrumentResourceProfile"]] = UNSET
    group: Union[Unset, str] = UNSET
    riders: Union[Unset, List[str]] = UNSET
    pointing_request_file: Union[Unset, None, str] = UNSET
    slew_policy: Union[Unset, str] = UNSET
    pointing_target: Union[Unset, None, str] = UNSET
    platform_power_profile: Union[Unset, str] = UNSET
    scheduler_flag: Union[Unset, None, bool] = UNSET
    scheduling_priority: Union[Unset, None, int] = UNSET
    observation_definitions: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        mnemonic = self.mnemonic
        prime_segment = self.prime_segment
        description = self.description
        resources: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.resources, Unset):
            if self.resources is None:
                resources = None
            else:
                resources = []
                for resources_item_data in self.resources:
                    resources_item = resources_item_data.to_dict()

                    resources.append(resources_item)

        instrument_resources: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.instrument_resources, Unset):
            if self.instrument_resources is None:
                instrument_resources = None
            else:
                instrument_resources = []
                for instrument_resources_item_data in self.instrument_resources:
                    instrument_resources_item = instrument_resources_item_data.to_dict()

                    instrument_resources.append(instrument_resources_item)

        group = self.group
        riders: Union[Unset, List[str]] = UNSET
        if not isinstance(self.riders, Unset):
            riders = self.riders

        pointing_request_file = self.pointing_request_file
        slew_policy = self.slew_policy
        pointing_target = self.pointing_target
        platform_power_profile = self.platform_power_profile
        scheduler_flag = self.scheduler_flag
        scheduling_priority = self.scheduling_priority
        observation_definitions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.observation_definitions, Unset):
            observation_definitions = self.observation_definitions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mnemonic": mnemonic,
                "prime_segment": prime_segment,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if resources is not UNSET:
            field_dict["resources"] = resources
        if instrument_resources is not UNSET:
            field_dict["instrument_resources"] = instrument_resources
        if group is not UNSET:
            field_dict["group"] = group
        if riders is not UNSET:
            field_dict["riders"] = riders
        if pointing_request_file is not UNSET:
            field_dict["pointing_request_file"] = pointing_request_file
        if slew_policy is not UNSET:
            field_dict["slew_policy"] = slew_policy
        if pointing_target is not UNSET:
            field_dict["pointing_target"] = pointing_target
        if platform_power_profile is not UNSET:
            field_dict["platform_power_profile"] = platform_power_profile
        if scheduler_flag is not UNSET:
            field_dict["scheduler_flag"] = scheduler_flag
        if scheduling_priority is not UNSET:
            field_dict["scheduling_priority"] = scheduling_priority
        if observation_definitions is not UNSET:
            field_dict["observation_definitions"] = observation_definitions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.instrument_resource_profile import InstrumentResourceProfile
        from ..models.resource_profile import ResourceProfile

        d = src_dict.copy()
        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        prime_segment = d.pop("prime_segment")

        description = d.pop("description", UNSET)

        resources = []
        _resources = d.pop("resources", UNSET)
        for resources_item_data in _resources or []:
            resources_item = ResourceProfile.from_dict(resources_item_data)

            resources.append(resources_item)

        instrument_resources = []
        _instrument_resources = d.pop("instrument_resources", UNSET)
        for instrument_resources_item_data in _instrument_resources or []:
            instrument_resources_item = InstrumentResourceProfile.from_dict(instrument_resources_item_data)

            instrument_resources.append(instrument_resources_item)

        group = d.pop("group", UNSET)

        riders = cast(List[str], d.pop("riders", UNSET))

        pointing_request_file = d.pop("pointing_request_file", UNSET)

        slew_policy = d.pop("slew_policy", UNSET)

        pointing_target = d.pop("pointing_target", UNSET)

        platform_power_profile = d.pop("platform_power_profile", UNSET)

        scheduler_flag = d.pop("scheduler_flag", UNSET)

        scheduling_priority = d.pop("scheduling_priority", UNSET)

        observation_definitions = cast(List[str], d.pop("observation_definitions", UNSET))

        segment_definition = cls(
            name=name,
            mnemonic=mnemonic,
            prime_segment=prime_segment,
            description=description,
            resources=resources,
            instrument_resources=instrument_resources,
            group=group,
            riders=riders,
            pointing_request_file=pointing_request_file,
            slew_policy=slew_policy,
            pointing_target=pointing_target,
            platform_power_profile=platform_power_profile,
            scheduler_flag=scheduler_flag,
            scheduling_priority=scheduling_priority,
            observation_definitions=observation_definitions,
        )

        segment_definition.additional_properties = d
        return segment_definition

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

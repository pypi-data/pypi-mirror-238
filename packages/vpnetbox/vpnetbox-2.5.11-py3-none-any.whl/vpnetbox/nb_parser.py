"""NbParser, Extract a value from a Netbox object using a chain of keys.

Netbox object has None instead of a dictionary when a related object is absent,
which is why it is necessary to constantly check the data type.
NbParser returns the desired value with the expected data type, even if the data is missing.
"""
import re
from typing import Type

from vhelpers import vlist, vre

from vpnetbox import wrappers
from vpnetbox.exceptions import NbParserError
from vpnetbox.types_ import DAny, SStr, LStr, T2Str, SeqStr

RE_PREFIX = r"\d+\.\d+\.\d+\.\d+/\d+"


class NbParser:  # pylint: disable=R0904
    """NbParser, Extracts a value from a Netbox object using a chain of keys."""

    def __init__(self, data: DAny, strict: bool = False, **kwargs):
        """Init NbParser.

        :param data: Netbox object.
        :param strict: True - Raise ERROR if data is invalid,
                       False - Return empty data if data is invalid.
        :param version: Netbox version. Helpful for compatibility with different versions.
        :type version: str
        """
        self.data = data
        self.strict = strict
        self.version = str(kwargs.get("version") or "0")

    # ====================== universal get methods =======================

    def dict(self, *keys) -> dict:
        """Get dictionary value by keys.

        :param keys: Chaining dictionary keys to retrieve the desired value.
        :return: Dictionary value or an empty dictionary if the value is absent.
        :raise NbParserError: If strict=True and the value is not a dictionary or key is absent.
        """
        return self._get_keys(type_=dict, keys=keys, data=self.data)

    # noinspection DuplicatedCode
    def int(self, *keys) -> int:
        """Get integer value by keys.

        :param keys: Chaining dictionary keys to retrieve the desired value.
        :return: Integer value or 0 if the value is absent.
        :raise NbParserError: If strict=True and the value is not a digit or key is absent.
        """
        data = self.data
        try:
            for key in keys:
                data = data[key]
        except (KeyError, TypeError) as ex:
            if self.strict:
                type_ = type(ex).__name__
                raise NbParserError(f"{type_}: {ex}, {keys=} in {self._source()}") from ex
            return 0

        if isinstance(data, int):
            return data

        if isinstance(data, str) and data.isdigit():
            return int(data)

        if self.strict:
            raise NbParserError(f"{keys=} {int} expected in {self._source()}.")
        return 0

    def list(self, *keys) -> list:
        """Get list value by keys.
        
        :param keys: Chaining dictionary keys to retrieve the desired value.
        :return: List value or an empty list if the value is absent.
        :raise NbParserError: If strict=True and the value is not a list or key is absent.
        """
        return self._get_keys(type_=list, keys=keys, data=self.data)

    def str(self, *keys) -> str:
        """Get string value by keys.
        
        :param keys: Chaining dictionary keys to retrieve the desired value.
        :return: String value or an empty string if the value is absent.
        :raise NbParserError: If strict=True and the value is not a string or key is absent.
        """
        return self._get_keys(type_=str, keys=keys, data=self.data)

    @wrappers.strict_value
    def strict_dict(self, *keys) -> dict:
        """Get dictionary value by keys in strict manner, value is mandatory.

        :param keys: Chaining dictionary keys to retrieve the desired value.
        :return: Dictionary value.
        :raise NbParserError: If the value is not a dictionary or key is absent or value is empty.
        """
        return self.dict(*keys)

    @wrappers.strict_value
    def strict_int(self, *keys) -> int:
        """Get integer value by keys in strict manner, value is mandatory.

        :param keys: Chaining dictionary keys to retrieve the desired value.
        :return: Integer value.
        :raise NbParserError: If the value is not a int or key is absent or value is 0.
        """
        return self.int(*keys)

    @wrappers.strict_value
    def strict_list(self, *keys) -> list:
        """Get string value by keys in strict manner, value is mandatory.

        :param keys: Chaining dictionary keys to retrieve the desired value.
        :return: List value.
        :raise NbParserError: If the value is not a list or key is absent or value is empty.
        """
        return self.list(*keys)

    @wrappers.strict_value
    def strict_str(self, *keys) -> str:
        """Get string value by keys in strict manner, value is mandatory.

        :param keys: Chaining dictionary keys to retrieve the desired value.
        :return: String value.
        :raise NbParserError: If the value is not a string or key is absent or value is absent.
        """
        return self.str(*keys)

    def _get_keys(self, type_: Type, keys: SeqStr, data: dict):
        """Retrieve values from data using keys and check their data types.

        :param type_: Data type.
        :param keys: Chaining dictionary keys to retrieve the desired value.
        :param data: Dictionary.
        :return: Value with proper data type.
        :raise NbParserError: If strict=True and key absent or type not match.
        """
        try:
            for key in keys:
                data = data[key]
        except (KeyError, TypeError) as ex:
            if self.strict:
                ex_type = type(ex).__name__
                raise NbParserError(f"{ex_type}: {ex}, {keys=} in {self._source()}.") from ex
            return type_()

        if not isinstance(data, type_):
            if self.strict:
                ex_type = "TypeError"
                raise NbParserError(f"{ex_type}: {keys=} {type_} expected in {self._source()}.")
            return type_()

        return data

    def _source(self) -> str:
        """Return URL of source object or data."""
        if isinstance(self.data, dict):
            if url := self.data.get("url"):
                return str(url)
        return str(self.data)

    # ============================= methods ==============================

    def address(self) -> str:
        """ipam/ip-addresses/address.

        :return: IP address with prefix length A.B.C.D/LEN.
        :raise NbParserError: if strict=True and the address does not match the naming
            convention A.B.C.D/LEN.
        """
        address = self.str("address")
        if self.strict:
            if not self._is_prefix(subnet=address):
                raise NbParserError(f"address A.B.C.D/LEN expected in {self.data}.")
        return address

    def assigned_device(self) -> str:
        """ipam/ip-addresses/assigned_object/device/name.

        :return: Assigned device name.
        :raise NbParserError: if strict=True and device has no assigned_object/device/name.
        """
        device = self.str("assigned_object", "device", "name")
        if self.strict and not device:
            raise NbParserError(f"assigned_object/device/name expected in {self.data}.")
        return device

    def device_type_model(self) -> str:
        """dcim/devices/device_type/model.

        :return: Device type mode.
        :raise NbParserError: if strict=True and device has no device_type.
        """
        model = self.str("device_type", "model")
        if self.strict and not model:
            raise NbParserError(f"device_type/model expected in {self.data}.")
        return model

    def device_role_name(self) -> str:
        """dcim/devices/device_role/name.

        :return: Device role mode.
        :raise NbParserError: if strict=True and device has no device_role.
        """
        device_role = self.str("device_role", "name")
        if self.strict and not device_role:
            raise NbParserError(f"device_role/name expected in {self.data}.")
        return device_role

    def group_name(self) -> str:
        """imap/vlans/group/name.

        :return: Vlans group name.
        :raise NbParserError: if strict=True and Vlan has no group.
        """
        group_name = self.str("group", "name")
        if self.strict and not group_name:
            raise NbParserError(f"group/name expected in {self.data}.")
        return group_name

    def id_(self) -> int:
        """ipam/prefixes/id."""
        return self.int("id")

    def model(self) -> str:
        """dcim/devices/device-types/model.

        :return: Device-types model.
        :raise NbParserError: if strict=True and device-types has no model.
        """
        model = self.str("model")
        if self.strict and not model:
            raise NbParserError(f"model expected in {self.data}.")
        return model

    def name(self) -> str:
        """dcim/devices/name, dcim/vlans/name.

        :return: Name value.
        :raise NbParserError: if strict=True and device has no name.
        """
        name = self.str("name")
        if self.strict and not name:
            raise NbParserError(f"name expected in {self.data}.")
        return name

    def overlapped(self) -> str:
        """ipam/prefixes/overlapped."""
        return self.str("overlapped")

    def platform_slug(self) -> str:
        """dcim/devices/platform/slug.

        :return: Platform slug.
        :raise NbParserError: if strict=True and device has no platform.
        """
        platform = self.str("platform", "slug")
        if self.strict and not platform:
            raise NbParserError(f"platform/slug expected in {self.data}.")
        return platform

    def prefix(self) -> str:
        """ipam/prefixes/prefix, ipam/aggregates/prefix.

        :return: Prefix with length A.B.C.D/LEN.
        :raise NbParserError: if strict=True and the prefix does not match the naming
            convention A.B.C.D/LEN.
        """
        prefix = self.str("prefix")
        if self.strict:
            if not self._is_prefix(subnet=prefix):
                raise NbParserError(f"prefix expected in {self.data}.")
        return prefix

    def primary_ip4(self) -> str:
        """dcim/devices/primary_ip4/address.

        :return: primary_ip4 address.
        :raise NbParserError: if strict=True and device has no primary_ip4 address.
        """
        try:
            primary_ip4 = self.data["primary_ip4"]["address"]
        except (KeyError, TypeError):
            primary_ip4 = ""
        if not isinstance(primary_ip4, str):
            primary_ip4 = ""

        if self.strict:
            if not primary_ip4:
                raise NbParserError(f"primary_ip4/address expected in {self.data}.")
            if not re.match(r"^\d+\.\d+\.\d+\.\d+(/\d+)?$", primary_ip4):
                raise NbParserError(f"primary_ip4/address A.B.C.D expected in {self.data}.")
        return primary_ip4

    def role_slug(self) -> str:
        """ipam/prefixes/role/slug.

        :return: Role slug.
        :raise NbParserError: if strict=True and object has no role.
        """
        return self.str("role", "slug")

    def site_name(self, upper: bool = True) -> str:
        """ipam/prefixes/site/name, dcim/devices/sites/name.

        Convert site name to the same manner.
        Different objects have different upper or lower case:
        sites/name="SITE1",
        devices/site/name="SITE1",
        vlans/site/name="site1".

        :param upper: Whether to return the name in uppercase. Default is True.
        :return: Site name.
        :raise NbParserError: if strict=True and object has no site name.
        """
        site = self.str("site", "name")
        if self.strict and not site:
            raise NbParserError(f"site/name expected in {self.data}.")
        if upper:
            return site.upper()
        return site.lower()

    def status(self) -> str:
        """ipam/prefixes/status/value.

        :return: Status value.
        :raise NbParserError: if strict=True and object has no status.
        """
        return self.str("status", "value")

    def tenant(self) -> str:
        """ipam/prefixes/tenant/name.

        :return: Tenant name.
        :raise NbParserError: if strict=True and object has no tenant.
        """
        return self.str("tenant", "name")

    def vid(self) -> int:
        """ipam/vlans/vid.

        :return: Vlan id or 0 if no Vlan id
        :raise NbParserError: if strict=True and object has no vlans key.
        """
        return self.int("vid")

    def vlan(self) -> int:
        """ipam/prefixes/vlan/vid.

        :return: Vlan id or 0 if no Vlan
        :raise NbParserError: if strict=True and object has no vlan key.
        """
        return self.int("vlan", "vid")

    def tags(self) -> LStr:
        """ipam/prefixes/tags/id/slug.

        :return: List og tags.
        """
        tags_ = self.list("tags")
        if not tags_:
            return []

        tags: LStr = []
        for tag_d in tags_:
            if tag := self._get_keys(type_=str, keys=["slug"], data=tag_d):
                tags.append(tag)
        return tags

    def url(self) -> str:
        """ipam/prefixes/url.

        :return: API URL to object.
        :raise NbParserError: if strict=True and object has no URL.
        """
        url = self.str("url")
        if self.strict:
            if not url:
                raise NbParserError(f"url expected in {self.data}.")
        return url

    # ========================== custom_fields ===========================

    def cf_cloud_account(self) -> str:
        """ipam/aggregates/custom_fields/cloud_account/label."""
        return self.str("custom_fields", "cloud_account")

    def cf_end_of_support(self) -> str:
        """dcim/devices/custom_fields/end_of_support/value."""
        cf_value = self.str("custom_fields", "end_of_support").strip()
        return cf_value

    def cf_env(self) -> str:
        """ipam/prefixes/custom_fields/env/label."""
        return self.str("custom_fields", "env")

    def cf_super_aggr(self) -> T2Str:
        """ipam/aggregates/custom_fields/super_aggregate/value."""
        value = self.str("custom_fields", "super_aggregate")
        value = value.strip()
        prefix, descr = vre.find2(f"^({RE_PREFIX})(.*)", value)
        return prefix, descr.strip()

    def cf_sw_planned(self) -> str:
        """dcim/devices/device-types/custom_fields/sw_planned."""
        return self.str("custom_fields", "sw_planned")

    def cf_sw_version(self) -> str:
        """dcim/devices/custom_fields/sw_version."""
        return self.str("custom_fields", "sw_version")

    # ========================== custom values ===========================

    def firewalls__in_aggregate(self) -> SStr:
        """aggregates/custom_fields/ or description."""
        if hostnames := self._hosts_in_cf_firewalls():
            return hostnames
        if hostnames := self._hosts_in_aggr_descr():
            return hostnames
        return set()

    def _hosts_in_cf_firewalls(self) -> SStr:
        """Hostnames in aggregates/custom_fields/firewalls."""
        try:
            value = self.data["custom_fields"]["firewalls"]
        except (KeyError, TypeError):
            return set()
        if not value or not isinstance(value, str):
            return set()
        hostnames_ = "\n".join(vlist.split(value, ignore="_-"))
        hostnames = re.findall(r"^(\w+-\w+-\w+-\w+)", hostnames_, re.M)
        return set(hostnames)

    def _hosts_in_aggr_descr(self) -> SStr:
        """Hostnames in aggregates/description."""
        tags = self.tags()
        if "noc_aggregates_belonging" not in tags:
            return set()

        try:
            description = self.data["description"]
        except (KeyError, TypeError):
            if self.strict:
                raise
            return set()

        if not isinstance(description, str):
            if self.strict:
                raise TypeError(f"{description=}, {str} expected.")
            return set()

        descr_ = "\n".join(vlist.split(description, ignore="_-"))
        hostnames = set(re.findall(r"^(\w+-\w+-\w+-\w+)", descr_, re.M))
        return hostnames

    # ================================ is ================================

    def is_dcim(self, dcim: str) -> bool:
        """Return True if object is dcim/devices.

        :raise NbParserError: - if url is not /api/dcim/ and self.strict=True
        """
        try:
            url = self.data["url"]
            if re.search(f"/api/dcim/{dcim}/", url):
                return True
            return False
        except (KeyError, TypeError) as ex:
            if self.strict:
                raise NbParserError(f"invalid url in {self.data}.") from ex
            return False

    def is_ipam(self, ipam: str) -> bool:
        """Return True if object is ipam.

        If ipam url "/api/ipam/" contains "aggregate", "prefix", "address".
        :raise NbParserError: - if url is not /api/ipam/aggregate or prefix or address
            and self.strict=True
        """
        try:
            url = self.data["url"]
            if re.search(f"/api/ipam/{ipam}/", url):
                return True
            return False
        except (KeyError, TypeError) as ex:
            if self.strict:
                raise NbParserError(f"ipam url expected in {self.data}.") from ex
            return False

    def is_vrf(self) -> bool:
        """Return True if data has vrf."""
        if self.data.get("vrf"):
            return True
        return False

    @staticmethod
    def _is_prefix(subnet: str) -> bool:
        """Return True if subnet has A.B.C.D/LEN format."""
        if re.match(fr"^{RE_PREFIX}$", subnet):
            return True
        return False

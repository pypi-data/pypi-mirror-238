# SPDX-License-Identifier: LGPL-2.1-or-later

# Copyright (C) 2020-2022 igo95862

# This file is part of python-sdbus

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Tuple

from .dbus_common_funcs import _parse_properties_vardict, get_default_bus
from .dbus_proxy_async_interface_base import DbusInterfaceBaseAsync
from .dbus_proxy_async_method import dbus_method_async
from .dbus_proxy_async_signal import dbus_signal_async
from .sd_bus_internals import SdBus, SdBusSlot


class DbusPeerInterfaceAsync(
    DbusInterfaceBaseAsync,
    interface_name='org.freedesktop.DBus.Peer',
    serving_enabled=False,
):

    @dbus_method_async(method_name='Ping')
    async def dbus_ping(self) -> None:
        raise NotImplementedError

    @dbus_method_async(method_name='GetMachineId')
    async def dbus_machine_id(self) -> str:
        raise NotImplementedError


class DbusIntrospectableAsync(
    DbusInterfaceBaseAsync,
    interface_name='org.freedesktop.DBus.Introspectable',
    serving_enabled=False,
):

    @dbus_method_async(method_name='Introspect')
    async def dbus_introspect(self) -> str:
        raise NotImplementedError


DBUS_PROPERTIES_CHANGED_TYPING = Tuple[str,
                                       Dict[str, Tuple[str, Any]],
                                       List[str]]


class DbusPropertiesInterfaceAsync(
    DbusInterfaceBaseAsync,
    interface_name='org.freedesktop.DBus.Properties',
    serving_enabled=False,
):

    @dbus_signal_async('sa{sv}as')
    def properties_changed(self) -> DBUS_PROPERTIES_CHANGED_TYPING:
        raise NotImplementedError

    @dbus_method_async('s', 'a{sv}', method_name='GetAll')
    async def _properties_get_all(
            self, interface_name: str) -> Dict[str, Tuple[str, Any]]:
        raise NotImplementedError

    async def properties_get_all_dict(
            self,
            on_unknown_member: Literal['error', 'ignore', 'reuse'] = 'error',
    ) -> Dict[str, Any]:

        properties: Dict[str, Any] = {}

        for interface_name in self._dbus_served_interfaces_names:
            dbus_properties_data = await self._properties_get_all(
                interface_name)

            properties.update(
                _parse_properties_vardict(
                    self._dbus_to_python_name_map,
                    dbus_properties_data,
                    on_unknown_member,
                )
            )

        return properties


class DbusInterfaceCommonAsync(
        DbusPeerInterfaceAsync, DbusPropertiesInterfaceAsync,
        DbusIntrospectableAsync):
    ...


class DbusObjectManagerInterfaceAsync(
    DbusInterfaceCommonAsync,
    interface_name='org.freedesktop.DBus.ObjectManager',
    serving_enabled=False,
):
    def __init__(self) -> None:
        super().__init__()
        self._object_manager_slot: Optional[SdBusSlot] = None
        self._managed_object_to_path: Dict[DbusInterfaceBaseAsync, str] = {}

    @dbus_method_async(result_signature='a{oa{sa{sv}}}')
    async def get_managed_objects(
            self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        raise NotImplementedError

    @dbus_signal_async('oa{sa{sv}}')
    def interfaces_added(self) -> Tuple[str, Dict[str, Dict[str, Any]]]:
        raise NotImplementedError

    @dbus_signal_async('oao')
    def interfaces_removed(self) -> Tuple[str, List[str]]:
        raise NotImplementedError

    def export_to_dbus(
        self,
        object_path: str,
        bus: Optional[SdBus] = None,
    ) -> None:
        if bus is None:
            bus = get_default_bus()

        super().export_to_dbus(
            object_path,
            bus,
        )
        slot = bus.add_object_manager(object_path)
        self._object_manager_slot = slot

    def export_with_manager(
        self,
        object_path: str,
        object_to_export: DbusInterfaceBaseAsync,
        bus: Optional[SdBus] = None,
    ) -> None:
        if self._object_manager_slot is None:
            raise RuntimeError('ObjectManager not intitialized')

        if bus is None:
            bus = get_default_bus()

        object_to_export.export_to_dbus(
            object_path,
            bus,
        )
        bus.emit_object_added(object_path)
        self._managed_object_to_path[object_to_export] = object_path

    def remove_managed_object(
            self,
            managed_object: DbusInterfaceBaseAsync) -> None:
        if self._attached_bus is None:
            raise RuntimeError('Object manager not exported')

        removed_path = self._managed_object_to_path.pop(managed_object)
        self._attached_bus.emit_object_removed(removed_path)

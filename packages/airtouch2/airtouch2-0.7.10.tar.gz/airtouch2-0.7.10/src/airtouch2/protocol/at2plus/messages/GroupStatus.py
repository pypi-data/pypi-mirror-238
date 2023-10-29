from __future__ import annotations
from dataclasses import dataclass

from airtouch2.common.interfaces import Serializable
from airtouch2.protocol.at2plus.enums import GroupPower

@dataclass
class GroupStatus(Serializable):
    power: GroupPower
    damp: int
    supports_turbo: bool
    spill_active: bool

    @staticmethod
    def from_bytes() -> GroupStatus:
        pass

from __future__ import annotations

import sys

sys.path.append(".")

from src.red_sysinfo import PLATFORM
from src.red_sysinfo.domain.enums.platform import (
    EnumLinux,
    EnumMac,
    EnumPlatform,
    EnumPython,
    EnumSystemTypes,
    EnumUname,
    EnumUnix,
    EnumWin32,
)
from src.red_sysinfo.domain.platform import PlatformInfo

def test_platform_instance(platform_info):
    assert platform_info is not None

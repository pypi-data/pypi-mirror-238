from __future__ import annotations

import sys

sys.path.append(".")

from red_sysinfo.domain.platform import PlatformInfo
from red_sysinfo.utils.platform_utils import get_platform

## Initialize platform object
PLATFORM: PlatformInfo = get_platform()


if __name__ == "__main__":
    print(f"Platform:\n{PLATFORM}")

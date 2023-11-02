from __future__ import annotations

import sys

sys.path.append(".")

from red_sysinfo import PLATFORM, print_platform

if __name__ == "__main__":
    print_platform(p=PLATFORM)

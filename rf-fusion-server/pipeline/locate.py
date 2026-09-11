# PROJECT:     SNOOPY-RF-FUSION (web reference)
# CREATED:     2026-09-10 19:33 MDT | 21:33 EDT | 2026-09-11 01:33 Zulu
# DESCRIPTION: EXTENSION POINT for precise non-cooperative localization (RSSI-SLAM). The reference
#              already gives a COARSE position for each emitter, an RSSI-weighted centroid of the
#              devices that heard it (see fuse.py). That is honest but rough.
#
#              *** THERE IS NOTHING IN HERE ON PURPOSE. ***
#              Turning many RSSI readings, as devices move, into a tightened position estimate with an
#              uncertainty (the RSSI-SLAM engine) is the production capability and is not in this
#              repository. Remote ID contacts do not need this: a cooperative drone broadcasts its own
#              GPS, so its position is exact already. This slot is for the non-cooperative case.

from typing import Optional


def refine(emitter, history=None) -> Optional[dict]:
    """Upgrade an emitter's coarse RSSI-centroid position to a precise estimate + uncertainty.

    Returns {"x","y","sigma_m"} or None if no precision engine is wired in. The reference returns
    None and the coarse centroid from fuse.py stands. The production RSSI-SLAM engine attaches here."""
    return None


def available() -> bool:
    """True when a precise localization engine is wired in. False in the reference."""
    return False

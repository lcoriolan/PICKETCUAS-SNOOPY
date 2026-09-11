# PROJECT:     SNOOPY-RF-FUSION (web reference)
# CREATED:     2026-09-10 19:33 MDT | 21:33 EDT | 2026-09-11 01:33 Zulu
# DESCRIPTION: EXTENSION POINT for the cooperative-vs-non-cooperative correlation (the "delta").
#              A drone that broadcasts Remote ID is cooperative and self-locating; a drone that is
#              heard (acoustically, or seen as a drone-signature RF emitter) but is NOT broadcasting
#              Remote ID is non-cooperative and the real threat. Correlating those two streams to
#              call COOPERATIVE vs NON-COOPERATIVE is a core capability.
#
#              *** THERE IS NOTHING IN HERE ON PURPOSE. ***
#              The correlation/gating logic is the production capability and is not in this
#              repository. The reference reports Remote ID tracks and flagged emitters side by
#              side but does not fuse them into a cooperative/non-cooperative verdict.


def correlate(rid_tracks, flagged_emitters, acoustic=None):
    """Decide COOPERATIVE / NON-COOPERATIVE per track by correlating Remote ID against heard drones.

    *** NOT IMPLEMENTED. *** Returns an empty list in the reference. The production correlator attaches
    here and emits per-contact verdicts with confidence."""
    return []


def available() -> bool:
    """True when the correlation engine is wired in. False in the reference."""
    return False

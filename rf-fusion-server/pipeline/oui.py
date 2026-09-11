# PROJECT:     SNOOPY-RF-FUSION (web reference)
# CREATED:     2026-09-10 19:33 MDT | 21:33 EDT | 2026-09-11 01:33 Zulu
# DESCRIPTION: MAC vendor lookup. A MAC's first three octets (the OUI) are a globally-registered
#              manufacturer prefix, so the vendor is public information (the full IEEE registry is a
#              free download). This ships a tiny SAMPLE table to show the mechanism. What is NOT here
#              is the curated drone-maker signature list, the judgement of which OUIs and patterns mark
#              a drone radio, which is the production capability; is_drone_maker is the extension point.

# A few illustrative OUI -> vendor entries (lowercase "xx:xx:xx"). Swap in the full IEEE OUI list
# for real coverage; nothing here is secret.
SAMPLE_OUI = {
    "00:1a:11": "Google",
    "3c:5a:b4": "Google",
    "d0:03:4b": "Apple",
    "ac:bc:32": "Apple",
    "60:60:1f": "DJI",
    "34:d2:62": "Parrot",
}


def label(mac):
    """Return a vendor for a MAC, or a graceful fallback. Public lookup, no secrets.

    Locally-administered addresses (the 0x02 bit of the first octet) are randomized/private and carry
    no vendor, so they are reported as such rather than guessed."""
    if not mac or len(mac) < 8:
        return "unknown"
    mac = mac.lower()
    try:
        first = int(mac[0:2], 16)
    except ValueError:
        return "unknown"
    if first & 0x02:
        return "randomized MAC (private)"
    return SAMPLE_OUI.get(mac[0:8], "OUI " + mac[0:8])


def is_drone_maker(mac):
    """EXTENSION POINT: does this MAC's OUI belong to a known drone maker / match a drone signature?

    *** NOT IMPLEMENTED IN THE REFERENCE. *** The reference never flags on OUI alone; it relies on the
    device's own is_drone_sig field. The curated drone-maker OUI list and signature patterns are the
    production capability and are not in this repository. This is where that list plugs in."""
    return False

<!--
PROJECT: PICKET SNOOPY public distribution
CREATED: 2026-10-19 21:32 MDT | 2026-10-19 23:32 EDT | 2026-10-20 03:32 Zulu
DESCRIPTION: Public release history for the signed ATAK plugin downloads.
-->

# Release history

## 2.1.0

2026-10-19 21:32 MDT | 2026-10-19 23:32 EDT | 2026-10-20 03:32 Zulu

- Publish TAK Product Center-signed APKs for ATAK-CIV 5.5.1, 5.6.0, and 5.8.0.
- Add the ATAK 5.6.0 build requested in issue #2.
- Include receive-only RTL-SDR reception through `rtl_tcp` and HackRF One reception
  through USB-OTG, requested in issue #1.
- Update the README download table and include APK SHA-256 checksums in the release.
- Verify each APK's signature, package version, and declared ATAK plugin API.
  Physical RTL-SDR/HackRF hardware testing and on-device validation of these
  returned APKs remain pending.

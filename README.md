# QuietCool ESP32 RF Fan Controller

ESPHome configuration for the **LILYGO / TTGO LoRa32 V2.1** QuietCool controller using a custom **SX1278 433.920 MHz** radio component.

This repository holds the **ESP32 firmware configuration**, separately from the [QuietCool Setup Bridge Home Assistant app](https://github.com/kurtwilliamcarlton/quietcool-setup-bridge).

## Files

| File | Purpose |
| --- | --- |
| `firmware/QuietCool_v5.5_reference.yaml` | Reference firmware configuration, based on the supplied v5.5 source; secrets removed |
| `firmware/QuietCool_v5.6_candidate.yaml` | **Unverified candidate** with two Wi-Fi/API stability changes |
| `secrets.example.yaml` | Template for locally stored web-login and fallback access-point credentials |
| `tests/test_config.py` | Static YAML configuration and safety checks |
| `.github/workflows/check.yml` | GitHub Actions static checks |

## Important: missing custom component

Both firmware files reference a local custom radio component at:

```
/config/esphome/quietcool-source/components/quietcool/
```

The custom component **was not included in the firmware archive supplied for this project**, so this repository does **not yet contain all code needed to compile or flash a working controller**. The SX1278 radio protocol, RF behavior, and fan control have not been reconstructed or modified.

**Do not flash v5.6 until the original component is added and the entire firmware has been compiled and physically tested.**

## Prepare firmware locally

1. Install the ESPHome development environment.
2. Copy the desired YAML from `firmware/` into your ESPHome configuration directory, such as `/config/esphome/`.
3. Copy the entries in `secrets.example.yaml` into the **local** `/config/esphome/secrets.yaml` and replace placeholders with strong credentials. Do not overwrite other devices' secrets.
4. Place the original `quietcool-source/components/quietcool/` folder inside `/config/esphome/quietcool-source/components/quietcool/`.
5. Run `esphome config /config/esphome/QuietCool_v5.6_candidate.yaml` and `esphome compile /config/esphome/QuietCool_v5.6_candidate.yaml`.
6. Test hardware behavior, radio pairing, fallback recovery, and factory reset before any OTA update.

`secrets.yaml` is ignored by Git and must **never** be committed. Choose an appropriate fallback password and enter that same password in Setup Bridge; the bridge does not know or change the password stored in firmware.

## v5.6 candidate changes

Compared with v5.5, the candidate adds:

- `api.reboot_timeout: 0s` — prevents an API-connection watchdog restart simply because Home Assistant is unavailable. This also disables that reboot recovery mechanism.
- `wifi.power_save_mode: NONE` — favors steadier Wi-Fi connectivity over power savings.

All radio, GPIO, OLED, fan-control, and factory-reset settings otherwise remain as in the reference YAML. This is a **candidate, not an approved production release**.

## Onboarding and remote setup

After properly installing and powering the ESP32, the firmware can provide a temporary access point named **QuietCool Fallback**. The companion Setup Bridge allows a Home Assistant Yellow to join that network over its secondary `wlan0` interface while retaining the Yellow's primary Ethernet connection.

The bridge guides the user through identifying the ESP32, submitting home Wi-Fi credentials, automatically looking for it on the home LAN, and manually disabling temporary Yellow Wi-Fi when finished. Setup Bridge does **not** build, install, or flash ESP32 firmware.

If the ESP32 is already online, its fallback access point may not be broadcast. To reconfigure Wi-Fi, activate fallback mode using the controller's supported recovery procedure.

## Security

The public firmware YAML contains **no embedded web-login or fallback Wi-Fi password**. ESPHome captive-portal provisioning uses local unencrypted HTTP, so use it only in a trusted setting. Keep the ESPHome and Home Assistant systems updated, and use unique credentials.

## Tests

GitHub Actions runs **static Python/YAML checks only**. They verify certain configuration invariants but **do not compile the device firmware** or validate actual RF behavior.

## Hardware warning

Do not alter wiring, RF module configuration, or mains-powered fan connections based solely on these source files. For changes to electrical hardware or power circuits, follow the hardware-specific documentation and use a qualified installer when appropriate.

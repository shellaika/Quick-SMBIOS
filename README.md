# Quick SMBIOS

Quick SMBIOS is a simple SMBIOS generator for macOS virtualization and Hackintosh environments.  
It generates realistic Apple SMBIOS values suitable for use with OpenCore or OSX-KVM setups.

The application provides a minimal graphical interface built with PyQt6 and can generate values such as serial numbers, MLB, UUID, MAC address, and ROM.

## Features

- Generate Apple-style SMBIOS values
- Model-aware serial generation
- Base-34 serial encoding
- Deterministic UUID generation
- Realistic Apple MAC address prefixes
- Simple and minimal PyQt6 interface
- Copy individual fields or full plist snippet

## Generated Values

The tool generates the following SMBIOS fields:

- SystemProductName
- SystemSerialNumber
- MLB
- SystemUUID
- ROM
- Board-ID

These values can be inserted into the `PlatformInfo -> Generic` section of an OpenCore `config.plist`.

## Supported Models

The generator currently supports several Apple models including:

- MacBookPro16,1
- MacBookPro15,1
- Macmini8,1
- MacPro7,1
- iMac19,1
- iMac20,1
- iMacPro1,1
- MacBookAir9,1


## Disclaimer

This tool generates synthetic SMBIOS data that mimics Apple hardware formats.  
The generated values are not guaranteed to pass Apple server validation or work with Apple services such as iMessage or FaceTime.

## License

MIT License

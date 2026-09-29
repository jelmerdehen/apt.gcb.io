# apt.gcb.io

Official GCB APT repository for iOS rootless mobile telemetry, security tools, and runtime diagnostics.

## Features

- Rootless Architecture: `iphoneos-arm64` (`/var/jb` prefix)
- Compatible with Sileo, Zebra, and standard APT CLI
- Packages:
  - `io.gcb.substrate-logger`: Untethered streaming telemetry, oslog diagnostics, and hardware vitals

## Adding Repository

### Sileo / Zebra
Click the repository link or add:
```
https://apt.gcb.io/
```

### APT CLI (/var/jb/etc/apt/sources.list.d/gcb.sources)
```
Types: deb
URIs: https://apt.gcb.io/
Suites: ./
Components:
```
Or classic list syntax:
```
deb [trusted=yes] https://apt.gcb.io/ ./
```

## Maintenance

To regenerate repository indexes after dropping new `.deb` packages into `debs/`:
```bash
make generate
```

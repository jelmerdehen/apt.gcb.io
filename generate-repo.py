#!/usr/bin/env python3
import os
import sys
import io
import gzip
import tarfile
import hashlib
import subprocess

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
DEBS_DIR = os.path.join(REPO_DIR, "debs")

def hash_file(path):
    with open(path, "rb") as f:
        data = f.read()
    return len(data), hashlib.md5(data).hexdigest(), hashlib.sha1(data).hexdigest(), hashlib.sha256(data).hexdigest()

def extract_control(deb_path):
    ar_out = subprocess.check_output(["ar", "t", deb_path]).decode().splitlines()
    control_archive = None
    for name in ar_out:
        if name.startswith("control.tar"):
            control_archive = name
            break
    if not control_archive:
        raise ValueError(f"No control archive found in {deb_path}")

    archive_data = subprocess.check_output(["ar", "p", deb_path, control_archive])
    with tarfile.open(fileobj=io.BytesIO(archive_data)) as tf:
        for member in tf.getmembers():
            if os.path.basename(member.name) == "control":
                f = tf.extractfile(member)
                return f.read().decode("utf-8").strip()
    raise ValueError(f"No control file inside {control_archive} in {deb_path}")

def main():
    if not os.path.exists(DEBS_DIR):
        os.makedirs(DEBS_DIR, exist_ok=True)

    deb_files = [f for f in os.listdir(DEBS_DIR) if f.endswith(".deb")]
    deb_files.sort()

    packages_entries = []
    for deb in deb_files:
        deb_path = os.path.join(DEBS_DIR, deb)
        control_text = extract_control(deb_path)
        size, md5, sha1, sha256 = hash_file(deb_path)

        entry = control_text + "\n"
        entry += f"Filename: debs/{deb}\n"
        entry += f"Size: {size}\n"
        entry += f"MD5sum: {md5}\n"
        entry += f"SHA1: {sha1}\n"
        entry += f"SHA256: {sha256}\n"
        packages_entries.append(entry)

    packages_content = "\n".join(packages_entries) + "\n" if packages_entries else ""
    packages_path = os.path.join(REPO_DIR, "Packages")
    with open(packages_path, "w", encoding="utf-8") as f:
        f.write(packages_content)

    # Generate Packages.gz
    with open(packages_path, "rb") as f_in:
        with gzip.open(os.path.join(REPO_DIR, "Packages.gz"), "wb", compresslevel=9) as f_out:
            f_out.write(f_in.read())

    # Generate Packages.xz
    if subprocess.call(["which", "xz"], stdout=subprocess.DEVNULL) == 0:
        with open(os.path.join(REPO_DIR, "Packages.xz"), "wb") as f_out:
            subprocess.check_call(["xz", "-c9", packages_path], stdout=f_out)

    # Generate Packages.zst
    if subprocess.call(["which", "zstd"], stdout=subprocess.DEVNULL) == 0:
        with open(os.path.join(REPO_DIR, "Packages.zst"), "wb") as f_out:
            subprocess.check_call(["zstd", "-c19", packages_path], stdout=f_out)

    target_files = ["Packages", "Packages.gz"]
    if os.path.exists(os.path.join(REPO_DIR, "Packages.xz")):
        target_files.append("Packages.xz")
    if os.path.exists(os.path.join(REPO_DIR, "Packages.zst")):
        target_files.append("Packages.zst")

    md5_lines = []
    sha1_lines = []
    sha256_lines = []

    for filename in target_files:
        file_path = os.path.join(REPO_DIR, filename)
        size, md5, sha1, sha256 = hash_file(file_path)
        md5_lines.append(f" {md5} {size} {filename}")
        sha1_lines.append(f" {sha1} {size} {filename}")
        sha256_lines.append(f" {sha256} {size} {filename}")

    release_content = (
        "Origin: GCB Repository\n"
        "Label: GCB\n"
        "Suite: stable\n"
        "Version: 1.0\n"
        "Codename: ios\n"
        "Architectures: iphoneos-arm64\n"
        "Components: main\n"
        "Description: GCB Mobile Telemetry and Diagnostics Repository\n"
        "MD5Sum:\n" + "\n".join(md5_lines) + "\n"
        "SHA1:\n" + "\n".join(sha1_lines) + "\n"
        "SHA256:\n" + "\n".join(sha256_lines) + "\n"
    )

    release_path = os.path.join(REPO_DIR, "Release")
    with open(release_path, "w", encoding="utf-8") as f:
        f.write(release_content)

    print(f"Generated repository metadata for {len(deb_files)} package(s) in {REPO_DIR}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
netmiko_generic_script.py

* Reads `hosts.txt`  – one hostname / IP per line
* Reads `commands.txt` – one command per line
* Prompts the user once for username/password (password is hidden)
* Executes all commands on every host (the same user/pass for all)
* Saves the combined output in a host‑specific folder
  filename format: <host>_<DD>_<MM>_<YYYY>_<HH>_<MM>.txt
  (e.g. 192.0.2.1_07_10_2025_14_32.txt)

The script expects `hosts.txt` and `commands.txt` to be in the same
directory as the script.  All output files are created in
`<script_dir>/<host_name>/`.
"""

import sys
import os
import getpass
from pathlib import Path
from datetime import datetime

try:
    from netmiko import ConnectHandler
except ImportError:
    print("netmiko is not installed. Run:\n    pip install netmiko")
    sys.exit(1)

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def read_file_lines(path: Path) -> list[str]:
    """Return a list of non‑empty, non‑comment lines from the file."""
    if not path.is_file():
        print(f"ERROR: {path} does not exist.")
        sys.exit(1)

    lines = []
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines

def create_output_dir(base: Path, host: str) -> Path:
    """Create a directory for the host under <base>/host/."""
    dir_path = base / host
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def timestamp() -> str:
    """Return the current date & time formatted as DD_MM_YYYY_HH_MM."""
    return datetime.now().strftime("%d_%m_%Y_%H_%M")

# ----------------------------------------------------------------------
# Main routine
# ----------------------------------------------------------------------
def main():
    # 1. Locate the script directory
    script_dir = Path(__file__).resolve().parent

    # 2. Read hosts and commands
    hosts_file = script_dir / "hosts.txt"
    commands_file = script_dir / "commands.txt"

    hosts = read_file_lines(hosts_file)
    commands = read_file_lines(commands_file)

    if not hosts:
        print("No hosts found in hosts.txt. Exiting.")
        sys.exit(1)

    if not commands:
        print("No commands found in commands.txt. Exiting.")
        sys.exit(1)

    # 3. Prompt for credentials (once)
    username = input("Enter SSH username: ").strip()
    password = getpass.getpass("Enter SSH password: ")

    # 4. Process each host
    for host in hosts:
        print(f"\n=== Connecting to {host} ===")

        # Build Netmiko device dictionary
        device = {
            "device_type": "generic_ssh",   # generic SSH handler
            "host": host,
            "username": username,
            "password": password,
            "conn_timeout": 10,            # seconds
            "auth_timeout": 10,
            # Optional: set this if your device requires a different SSH port
            # "port": 22,
        }

        try:
            with ConnectHandler(**device) as ssh:
                # Collect all command outputs
                output_lines = []

                for cmd in commands:
                    print(f"  Running: {cmd}")
                    try:
                        out = ssh.send_command(cmd, strip_command=False, strip_prompt=False)
                        output_lines.append(f"\n--- {cmd} ---\n{out}\n")
                    except Exception as e:
                        output_lines.append(f"\n--- {cmd} (ERROR) ---\n{e}\n")

                # Prepare output directory and file
                out_dir = create_output_dir(script_dir, host)
                out_file = out_dir / f"{host}_{timestamp()}.txt"

                # Write output
                out_file.write_text("\n".join(output_lines), encoding="utf-8")
                print(f"  Output written to: {out_file}")

        except Exception as e:
            print(f"ERROR: Failed to connect to {host}: {e}")

    print("\nAll hosts processed. Exiting.")


if __name__ == "__main__":
    main()
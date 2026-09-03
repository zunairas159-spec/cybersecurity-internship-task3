"""
2FA-Protected Folder Access Demo
----------------------------------
Demonstrates how a Time-based One-Time Password (TOTP), the same
kind Google Authenticator generates, can be used as a second
authentication factor before granting access to something (here,
opening a folder).

IMPORTANT NOTE FOR YOUR REPORT:
This script demonstrates the 2FA VERIFICATION LOGIC only. It does
NOT encrypt the folder or change Windows file permissions - someone
could still open the folder directly through File Explorer without
running this script. In a real system, this same code-check logic
is what runs on a server before granting access to an account or
action. Mention this limitation in your report - it shows you
understand what 2FA actually protects (the login/action gate, not
the data itself - that's what AES-256 encryption is for, which is
your next task).
"""

import hmac
import hashlib
import struct
import time
import base64
import os
import sys

# ==========================================================
# STEP 1: Paste the SAME Base32 secret you scanned into
# Google Authenticator earlier (from the TOTP demo website).
# Example: "JBSWY3DPEHPK3PXP"
# ==========================================================
SECRET_BASE32 = "PASTE_YOUR_SECRET_HERE"

# ==========================================================
# STEP 2: Set the folder you want to "protect" (must exist
# on your PC). Use your own path.
# ==========================================================
FOLDER_PATH = r"C:\Users\YourName\Desktop\ProtectedFolder"


def generate_totp(secret_base32, time_step=30, digits=6):
    """Generates the current 6-digit TOTP code from a Base32 secret."""
    padding = "=" * ((8 - len(secret_base32) % 8) % 8)
    key = base64.b32decode(secret_base32.upper() + padding)

    counter = int(time.time() // time_step)
    counter_bytes = struct.pack(">Q", counter)

    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    truncated = hmac_hash[offset:offset + 4]
    code_int = struct.unpack(">I", truncated)[0] & 0x7FFFFFFF
    code = code_int % (10 ** digits)

    return str(code).zfill(digits)


def main():
    print("=" * 50)
    print(" 2FA VERIFICATION REQUIRED TO ACCESS FOLDER")
    print("=" * 50)

    if SECRET_BASE32 == "PASTE_YOUR_SECRET_HERE":
        print("\n[SETUP NEEDED] Open this file and paste your real")
        print("Base32 secret into SECRET_BASE32 before running.\n")
        sys.exit(1)

    user_code = input("Enter the 6-digit code from Google Authenticator: ").strip()
    valid_code = generate_totp(SECRET_BASE32)

    if user_code == valid_code:
        print("\n[SUCCESS] Code verified. Opening folder...\n")
        if os.path.exists(FOLDER_PATH):
            os.startfile(FOLDER_PATH)  # Windows only
        else:
            print(f"(Demo note: folder path '{FOLDER_PATH}' does not exist on this machine.")
            print("Update FOLDER_PATH at the top of the script to a real folder on your PC.)")
    else:
        print("\n[DENIED] Incorrect code. Access blocked.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

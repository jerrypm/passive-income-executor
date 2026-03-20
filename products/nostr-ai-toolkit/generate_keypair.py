#!/usr/bin/env python3
"""
Generate Nostr keypair (nsec/npub) using pure Python.
Nostr uses secp256k1 keys. Private key = 32 random bytes.
Public key = x-coordinate of privkey * G (secp256k1 generator point).
Output saved to .env file.
"""

import secrets
import hashlib
import os

# secp256k1 curve parameters
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def modinv(a, m=P):
    return pow(a, m - 2, m)


def point_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and y1 != y2:
        return None
    if x1 == x2:
        lam = (3 * x1 * x1) * modinv(2 * y1) % P
    else:
        lam = (y2 - y1) * modinv(x2 - x1) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return (x3, y3)


def scalar_mult(k, point):
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result


# bech32 encoding for npub/nsec
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def bech32_polymod(values):
    GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= GEN[i] if ((b >> i) & 1) else 0
    return chk


def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for value in data:
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    return ret


def bech32_encode(hrp, data_bytes):
    data5 = convertbits(list(data_bytes), 8, 5)
    checksum = bech32_create_checksum(hrp, data5)
    return hrp + "1" + "".join([CHARSET[d] for d in data5 + checksum])


def main():
    # Generate private key (32 random bytes)
    privkey_bytes = secrets.token_bytes(32)
    privkey_int = int.from_bytes(privkey_bytes, 'big')

    # Ensure private key is valid (1 < privkey < N)
    while privkey_int >= N or privkey_int == 0:
        privkey_bytes = secrets.token_bytes(32)
        privkey_int = int.from_bytes(privkey_bytes, 'big')

    # Compute public key (x-only, 32 bytes)
    pub_point = scalar_mult(privkey_int, (Gx, Gy))
    pubkey_bytes = pub_point[0].to_bytes(32, 'big')

    # Hex representations
    privkey_hex = privkey_bytes.hex()
    pubkey_hex = pubkey_bytes.hex()

    # Bech32 representations (NIP-19)
    nsec = bech32_encode("nsec", privkey_bytes)
    npub = bech32_encode("npub", pubkey_bytes)

    print("=" * 60)
    print("NOSTR KEYPAIR GENERATED")
    print("=" * 60)
    print(f"\nPrivate Key (hex): {privkey_hex}")
    print(f"Public Key  (hex): {pubkey_hex}")
    print(f"\nnsec: {nsec}")
    print(f"npub: {npub}")
    print("\nWARNING: SAVE YOUR PRIVATE KEY! It cannot be recovered!")
    print("=" * 60)

    # Save to .env
    env_path = os.path.join(os.path.dirname(__file__), '.env')

    env_lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            env_lines = f.readlines()

    # Remove old Nostr keys if present
    env_lines = [l for l in env_lines if not l.startswith('NOSTR_PRIVKEY') and not l.startswith('NOSTR_PUBKEY') and not l.startswith('NOSTR_NSEC') and not l.startswith('NOSTR_NPUB')]

    with open(env_path, 'w') as f:
        for line in env_lines:
            f.write(line)
        f.write(f"\n# Nostr Keys (generated)\n")
        f.write(f"NOSTR_PRIVKEY={privkey_hex}\n")
        f.write(f"NOSTR_PUBKEY={pubkey_hex}\n")
        f.write(f"NOSTR_NSEC={nsec}\n")
        f.write(f"NOSTR_NPUB={npub}\n")

    print(f"\nKeys saved to {env_path}")


if __name__ == "__main__":
    main()

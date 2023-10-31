"""Format addresses."""

import eth_utils.address

# GENERIC #####################################################################

def strip_hex_prefix(data: str) -> str:
    return data.replace('0x', '')

# ADDRESS #####################################################################

def format_with_checksum(address: str) -> str:
    return (
        eth_utils.address.to_checksum_address('0x{0:0>40x}'.format(int(address, 16))) if address
        else '')

"""Format transaction traces."""

import hexbytes

import forta_toolkit.parsing.address

# TRACES ######################################################################

def parse_trace_data(trace: dict) -> dict:
    """Flatten and format all the data in a transaction trace."""
    # common
    __block = getattr(trace, 'block_number', getattr(trace, 'blockNumber', 0))
    __hash = getattr(trace, 'transaction_hash', getattr(trace, 'transactionHash', '0x'))
    __type = getattr(trace, 'type', '')
    __action = getattr(trace, 'action', {})
    __result = getattr(trace, 'result', {})
    __value = getattr(__action, 'value', 0)
    __gas = getattr(__result, 'gas_used', getattr(__result, 'gasUsed', 0))
    # output
    __data = {
        'block': __block,
        'hash': __hash,
        'type': __type,
        'value': __value,
        'gas': __gas,
        'from': '',
        'to': '',
        'input': '',
        'output': ''}
    # call
    if __type == 'call':
        __data['type'] = getattr(__action, 'call_type', getattr(__action, 'callType', 'call')) # actually get the exact variant of the call
        __data['from'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'from_', getattr(__action, 'from', '')))
        __data['to'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'to', ''))
        __data['input'] = getattr(__action, 'input', '0x')
        __data['output'] = getattr(__result, 'output', '0x')
    # create
    if __type == 'create':
        __data['from'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'from_', getattr(__action, 'from', '')))
        __data['to'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__result, 'address', ''))
        __data['input'] = getattr(__action, 'init', '0x')
        __data['output'] = getattr(__result, 'code', '0x')
    # suicide
    if __type == 'suicide':
        __data['from'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'address', ''))
        __data['to'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'refund_address', getattr(__action, 'refundAddress', '')))
        __data['input'] = getattr(__action, 'balance', '0x0')
        __data['output'] = '0x'
    # sanitize and have all the data in HEX strings format
    for __k in __data:
        # convert bytes to hex string
        if isinstance(__data[__k], hexbytes.HexBytes):
            __data[__k] = (__data[__k]).hex()
        if isinstance(__data[__k], int):
            __data[__k] = hex(__data[__k])
        if not __data[__k]: # catches None values too
            __data[__k] = '0x'
    # output
    return __data

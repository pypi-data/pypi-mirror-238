"""Format blockchain logs."""

import forta_agent.transaction

import forta_toolkit.parsing.address

# TRANSACTION LOGS ############################################################

def parse_transaction_data(transaction: forta_agent.transaction.Transaction) -> dict:
    """Flatten and format all the data in a transaction log."""
    return {
        'hash': getattr(transaction, 'hash', '0x'),
        'from': forta_toolkit.parsing.address.format_with_checksum(getattr(transaction, 'from_', '')),
        'to': forta_toolkit.parsing.address.format_with_checksum(getattr(transaction, 'to', '')),
        'value': getattr(transaction, 'value', '0x'),
        'data': getattr(transaction, 'data', '0x'),}

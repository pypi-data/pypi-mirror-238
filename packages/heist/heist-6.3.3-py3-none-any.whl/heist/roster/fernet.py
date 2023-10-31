from typing import Any
from typing import Dict


async def read(hub, roster_file: str = "") -> Dict[str, Any]:
    """
    Read in the data from an encrypted roster
    """
    if roster_file:
        return hub.crypto.init.decrypt_file(
            roster_file, hub.OPT.acct.acct_key, crypto_plugin="fernet"
        )
    return {}

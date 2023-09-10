from typing import List

import pycardano
import solara
from minswap.models import (
    Address,
    Assets,
)
from cip30 import CIP30

# load_dotenv()


# context = pycardano.BlockFrostChainContext(
#     os.environ["PROJECT_ID"],
#     base_url=getattr(pycardano.blockfrost.ApiUrls, os.environ["NETWORK"]).value,
# )


class States:

    # Wallet info
    address = solara.reactive("")
    firstAddress = solara.reactive("")
    assets = solara.reactive("")
    activeWallet = solara.reactive("")
    collateral = solara.reactive(None)
    wallets = solara.reactive([])
    signTx = solara.reactive("")
    signedTx = solara.reactive("")
    witness = solara.reactive("")
    txId = solara.reactive("")

    def __init__(self):

        # Wallet info
        self.address = solara.reactive("")
        self.firstAddress = solara.reactive("")
        self.assets = solara.reactive("")
        self.activeWallet = solara.reactive("")
        self.collateral = solara.reactive(None)
        self.wallets = solara.reactive([])
        self.signTx = solara.reactive("")
        self.signedTx = solara.reactive("")
        self.witness = solara.reactive("")
        self.txId = solara.reactive("")

    def convert_address(self, addresses: List[str]):
        self.address.set(addresses)
        self.firstAddress.set(self.get_address().bech32)

    def set_wallets(self, wallets):
        print(wallets)
        self.wallets.set(wallets)

    def get_assets(self):
        if self.address.value == "":
            return None
        value: pycardano.Value = pycardano.Value.from_cbor(self.assets.value)
        assets = Assets(lovelace=value.coin)
        for policy, value in value.multi_asset.data.items():
            for name, quantity in value.items():
                assets += Assets(**{str(policy) + str(name): quantity})
        return assets

    def get_address(self) -> pycardano.Address:
        address_hash = bytes.fromhex(self.address.value[0])

        address = Address(
            bech32=pycardano.Address.from_primitive(address_hash).encode()
        )
        return address

    def get_collaterals(self) -> List[pycardano.UTxO]:
        utxos = [pycardano.UTxO.from_cbor(utxo) for utxo in self.collateral.value]
        return 

    def submit_tx(self, witness):
        """CODE TO SUBMIT A TX

        Use pycardano to build a transaction, then convert to cbor and set the 
        signedTx value to the cbor hex value to submit.
        """


states = States()


@solara.component
def Page():
    # states = States()


    with solara.AppBar():
        CIP30(
            wallets=states.wallets.value,
            on_wallets=states.set_wallets,
            activeWallet=states.activeWallet.value,
            on_activeWallet=states.activeWallet.set,
            assets=states.activeWallet.value,
            on_assets=states.assets.set,
            collateral=states.collateral.value,
            on_collateral=states.collateral.set,
            address=states.address.value,
            on_address=states.convert_address,
            signTx=states.signTx.value,
            on_signTx=states.signTx.set,
            signedTx=states.signedTx.value,
            on_signedTx=states.signedTx.set,
            witness=states.witness.value,
            on_witness=states.submit_tx,
            txId=states.witness.value,
            on_txId=states.witness.set,
            firstAddress=states.firstAddress.value,
            on_firstAddress=states.firstAddress.set,
        )

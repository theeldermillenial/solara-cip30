from typing import List

import solara
import solara.lab


@solara.component_vue("cip30.vue")
def CIP30(
    wallets: List[str] = [],
    activeWallet: str = "",
    assets: str = "",
    address: str = "",
    collateral: str = "",
    signTx: str = "",
    signedTx: str = "",
    witness: str = "",
    txId: str = "",
    firstAddress: str = ",",
):
    """Set the title of a page.

    ```python
    import solara

    @solara.component
    def Page():
        with solara.VBox() as main:
            MyAwesomeComponent()
            solara.Title("My page title")
        return main
    ```

    If multiple Title components are used, the 'deepest' child will take precedence.

    ## Arguments

     * title: the title of the page
    """

from web3 import Web3

from models.Account import Account


class Contract(object):
    """
    Contract Model.
    Defines high-level contract operations.
    """
    _address = None
    _abi = None

    def __init__(self, web3: Web3):
        self.__web3 = web3
        self.__contract = web3.eth.contract(address=self._address, abi=self._abi)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if getattr(cls, '_address') is None:
            raise TypeError("Subclass must define class attribute '_address'")
        if getattr(cls, '_abi') is None:
            raise TypeError("Subclass must define class attribute '_abi'")

    def _functions(self):
        return self.__contract.functions

    def _read(self, function_name: str, *params, block_identifier: int = -1):
        return getattr(self.__contract.functions, function_name)(*params).call(block_identifier=block_identifier)

    def _write(self, caller: Account, function_name: str, *params):
        tx = getattr(self.__contract.functions, function_name)(*params).buildTransaction(caller.get_tx_param())
        signed_tx = self.__web3.eth.account.sign_transaction(tx, caller.get_private_key())
        tx_hash = self.__web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.__web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_address(self) -> str:
        return self._address

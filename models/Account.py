from web3 import Web3


class Account(object):
    """
    Account Model.
    Defines account operations.
    """

    def __init__(self, web3: Web3, address: str, private_key: str):
        self.__web3 = web3
        self.__address = address
        self.__private_key = private_key
        self.__value = None

    def get_tx_param(self):
        """
        Get transaction params for this account
        :return: from, nonce, Optional<value>
        """
        if self.__value is None:
            return {
                'from': self.__address,
                'nonce': self.get_nonce(),
            }
        else:
            return {
                'value': self.__value,
                'from': self.__address,
                'nonce': self.get_nonce(),
            }

    def get_address(self) -> str:
        """
        Get account address.
        :return: account address.
        """
        return self.__address

    def get_private_key(self) -> str:
        return self.__private_key

    def get_nonce(self):
        """
        Get the latest transaction nonce.
        :return: the latest transaction nonce.
        """
        return self.__web3.eth.get_transaction_count(self.__address)

    def set_msg_value(self, value: int) -> None:
        """
        Set account message value (msg.value).
        :param value: message value.
        """
        self.__value = value

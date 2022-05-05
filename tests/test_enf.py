from brownie import Wei, accounts
from conftest import *

from scripts.helpful_scripts import get_account, get_contract, listen_for_event


def log(text, desc=""):
    print("\033[32m" + text + "\033[0m" + desc)


def test_can_get_latest_price(
    deploy_safeerc20,
    deploy_addressArray,
    deploy_tl,
    gett_token_tl,
    deploy_el,
    deploy_vault,
):

    account = accounts[0]

    balance_before = account.balance()
    log("balance of account eth before", str(balance_before))

    tx = deploy_vault.deposit(
        Wei("10 ether"),
        {
            "from": account,
            "gas_price": 100,
            "gas_limit": 3000000,
            "allow_revert": True,
            "value": Wei("100 ether"),
        },
    )

    balance_after = account.balance()
    log("balance of account eth end", str(balance_after))

    assert len(tx.events["CFFDeposit"]) == 1
    event_new = tx.events["CFFDeposit"][0]
    log("ef balance ", str(deploy_el.balanceOf(account)))
    volumne = deploy_vault.getVolume()
    log("volumne", str(volumne))
    assert event_new["eth_amount"] == Wei("100 ether")
    virtual_price = deploy_vault.getVirtualPrice()
    log("balance of el token", str(deploy_el.balanceOf(account)))
    assert virtual_price == event_new["virtual_price"]

    assert deploy_el.balanceOf(account) == event_new["ef_amount"]
    collateral = deploy_vault.getCollecteral()
    log("collateral", str(collateral))
    debt = deploy_vault.getDebt()
    log("Debt ", str(debt))

    log("---------withdraw-------------")

    balance_before = account.balance()
    log("balance of account eth before", str(balance_before))
    balance_Of_el = deploy_el.balanceOf(account)
    withdraw_amount = balance_Of_el / 3

    tx = deploy_vault.withdraw(
        withdraw_amount,
        {"from": account, "gas_price": 100, "gas_limit": 3000000, "allow_revert": True},
    )

    print(tx.info())

    balance_after = account.balance()
    log("balance of account eth end", str(balance_after))

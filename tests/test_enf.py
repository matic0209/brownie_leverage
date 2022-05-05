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

    tx = deploy_vault.deposit(
        Wei("10 ether"),
        {
            "from": account,
            "gas_price": 100,
            "gas_limit": 3000000,
            "allow_revert": True,
            "value": Wei("10 ether"),
        },
    )

    # log("balance of crv", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))
    # listen_for_event(deploy_vault, "CFFDeposit", 200, 2)
    print(tx.events["CFFDeposit"])
    assert len(tx.events["CFFDeposit"]) == 1
    event_new = tx.events["CFFDeposit"][0]

    log("ef balance ", str(deploy_el.balanceOf(account)))

    volumne = deploy_vault.getVolume()
    log("volumne", str(volumne))
    assert event_new["eth_amount"] == Wei("10 ether")
    collateral = deploy_vault.getCollecteral()
    log("collateral", str(collateral))
    debt = deploy_vault.getDebt()
    log("Debt ", str(debt))

    # log("1")
    # deploy_vault.deposit(deposit_amount, {"from": account_crv})

    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))

    # log("2")
    # deploy_vault.deposit(deposit_amount, {"from": account_crv})

    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))

    # log("3")
    # deploy_vault.deposit(deposit_amount, {"from": account_crv})

    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))

    # log(" deposit 1")
    # deploy_vault.deposit(deposit_amount, {"from": account_crv})

    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))

    # log("deposit 2")
    # deploy_vault.deposit(deposit_amount, {"from": account_crv})

    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))

    # log("deposit 3")
    # deploy_vault.deposit(deposit_amount, {"from": account_crv})

    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))

    # log("deposit 4")
    # deploy_vault.deposit(deposit_amount, {"from": account_crv})

    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))

    # withdraw_amount = balance/10
    # log("withdraw 1")
    # tx = deploy_vault.withdraw(withdraw_amount, False, {"from": account_crv})
    # tx.wait(1)
    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf after withdraw", str(balance))
    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv after withdraw", str(balance))

    # log("withdraw 2")
    # tx = deploy_vault.withdraw(withdraw_amount, False, {"from": account_crv})
    # tx.wait(1)
    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf after withdraw", str(balance))
    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv after withdraw", str(balance))

    # log("withdraw 3")
    # tx = deploy_vault.withdraw(withdraw_amount, False, {"from": account_crv})
    # tx.wait(1)
    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf after withdraw", str(balance))
    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv after withdraw", str(balance))

    # log("withdraw 4")
    # tx = deploy_vault.withdraw(withdraw_amount, False, {"from": account_crv})
    # tx.wait(1)
    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf after withdraw", str(balance))
    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv after withdraw", str(balance))

    # log("withdraw 5")
    # tx = deploy_vault.withdraw(withdraw_amount, False, {"from": account_crv})
    # tx.wait(1)
    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf after withdraw", str(balance))
    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv after withdraw", str(balance))

    # log("withdraw 6")
    # tx = deploy_vault.withdraw(withdraw_amount, False, {"from": account_crv})
    # tx.wait(1)
    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf after withdraw", str(balance))
    # balance = crv.balanceOf(account_crv, {"from": account})
    # log("balance of crv after withdraw", str(balance))

    # balance = usdc.balanceOf(account_crv, {"from": account})
    # log("balance of usdc before withdraw", str(balance))

    # deploy_vault.withdraw(withdraw_amount, True, {"from": account_crv})

    # balance = usdc.balanceOf(account_crv, {"from": account})
    # log("balance of usdc after  withdraw", str(balance))

    # balance = usdc.balanceOf(account_crv, {"from": account})
    # log("balance of usdc before depositstable", str(balance))
    # print(balance)

    # usdc.approve(deploy_vault.address,1000000000000000000000000000000000, {"from": account_crv})

    # tx = deploy_vault.depositStable(balance/2, {"from": account_crv})
    # tx.wait(1)
    # chain.sleep(1)

    # balance = usdc.balanceOf(account_crv, {"from": account})
    # log("balance of usdc after depositStable", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))

    # log("start earn rewards")

    # tx = deploy_vault.earnReward({"from": account})
    # tx.wait(1)
    # chain.sleep(1)

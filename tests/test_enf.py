import pytest
from brownie import *

from scripts.helpful_scripts import get_account, get_contract
from conftest import *
from brownie import (
    accounts,
    Contract,
    config,
    network,
    ERC20TokenFactory,
    AddressArray,
    ERC20Token,
    TrustListFactory,
    TrustList,
)


def log(text, desc=""):
    print("\033[32m" + text + "\033[0m" + desc)


def transfer_tokens(address):
    log("Start Transfer  ")

    account_tricrv = accounts[-3]
    account_cvx = accounts[-2]
    account_crv = accounts[-1]

    crv = get_contract("crv")
    cvx = get_contract("cvx")
    tricrv = get_contract("tricrv")

    tx = crv.transfer(address, 100000, {"from": account_crv})
    tx.wait(1)

    cvx.transfer(address, 100000, {"from": account_cvx})
    tx.wait(1)

    crv.transfer(address, 100000, {"from": account_tricrv})
    tx.wait(1)


def test_can_get_latest_price(
    deploy_safeerc20,
    deploy_addressArray,
    deploy_tl,
    gett_token_tl,
    deploy_ef,
    deploy_vault,
    addExtraToken,
    configFee,
):
    # Arrange

    # address = get_contract("eth_usd_price_feed").address
    # # Act
    # price_feed = PriceFeedConsumer.deploy(address, {"from": get_account()})
    # # Assert
    # value = price_feed.getLatestPrice({"from": get_account()})

    account_crv = accounts[-1]
    account = accounts[0]
    log("add _asset ")
    crv = get_contract("crv")
    usdc = get_contract("usdc")

    balance = crv.balanceOf(account_crv, {"from": account})
    deposit_amount = balance / 10

    crv.approve(
        deploy_vault.address, 1000000000000000000000000000000000, {"from": account_crv}
    )

    log("1")

    usdt = ERC20Token.at("0xdAC17F958D2ee523a2206206994597C13D831ec7")

    balance = usdt.balanceOf(deploy_vault, {"from": account})
    log("balance of usdt before deposit ", str(balance))

    deploy_vault.deposit(deposit_amount, {"from": account_crv})

    balance = crv.balanceOf(account_crv, {"from": account})
    log("balance of crv", str(balance))

    balance = deploy_ef.balanceOf(account_crv, {"from": account})
    log("balance of enf", str(balance))

    # log("withdraw 1")
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

    # usdc.approve(
    #     deploy_vault.address, 1000000000000000000000000000000000, {"from": account_crv}
    # )

    # tx = deploy_vault.depositStable(balance / 2, {"from": account_crv})
    # tx.wait(1)

    # balance = usdc.balanceOf(account_crv, {"from": account})
    # log("balance of usdc after depositStable", str(balance))

    # balance = deploy_ef.balanceOf(account_crv, {"from": account})
    # log("balance of enf", str(balance))

    log("start earn rewards")

    balance = deploy_vault.getLPTokenBalance({"from": account})
    log("lp balance  before earn ", str(balance))

    balance = deploy_ef.balanceOf(deploy_vault, {"from": account})
    log("ef balance of vault before earn ", str(balance))

    balance = deploy_ef.balanceOf(
        "0x39F4Ef6294512015AB54ed3ab32BAA1794E8dE70", {"from": account}
    )
    log("ef balance of fee pool  before earn ", str(balance))

    balance = crv.balanceOf(
        "0x39F4Ef6294512015AB54ed3ab32BAA1794E8dE70", {"from": account}
    )
    log("balance of crv of fee pool before earn", str(balance))

    tx = deploy_vault.earnReward(
        {
            "from": account,
            "allow_revert": True,
            "gas_price": 100,
            "gas_limit": 3000000,
        }
    )
    tx.wait(1)

    balance = deploy_ef.balanceOf(deploy_vault, {"from": account})
    log("ef balance of vault after earn ", str(balance))

    balance = deploy_ef.balanceOf(
        "0x39F4Ef6294512015AB54ed3ab32BAA1794E8dE70", {"from": account}
    )
    log("ef balance of fee pool  after earn ", str(balance))

    balance = deploy_vault.getLPTokenBalance({"from": account})
    log("lp balance  after earn ", str(balance))

    balance = crv.balanceOf(
        "0x39F4Ef6294512015AB54ed3ab32BAA1794E8dE70", {"from": account}
    )
    log("balance of crv of fee pool after earn ", str(balance))

    balance = crv.balanceOf(deploy_vault, {"from": account})
    log("crv balance of vault before transfer  ", str(balance))

    transfer_tokens(deploy_vault.address)

    balance = crv.balanceOf(deploy_vault, {"from": account})
    log("crv balance of vault after transfer  ", str(balance))

    log("start earn rewards after transfer")

    balance = deploy_vault.getLPTokenBalance({"from": account})
    log("lp balance  before earn ", str(balance))

    balance = deploy_ef.balanceOf(deploy_vault, {"from": account})
    log("ef balance of vault before earn ", str(balance))

    balance = deploy_ef.balanceOf(
        "0x39F4Ef6294512015AB54ed3ab32BAA1794E8dE70", {"from": account}
    )
    log("ef balance of fee pool  before earn ", str(balance))

    balance = crv.balanceOf(
        "0x39F4Ef6294512015AB54ed3ab32BAA1794E8dE70", {"from": account}
    )
    log("balance of crv of fee pool before earn", str(balance))

    tx = deploy_vault.earnReward(
        {
            "from": account,
            "allow_revert": True,
            "gas_price": 100,
            "gas_limit": 3000000,
        }
    )
    tx.wait(1)

    balance = deploy_ef.balanceOf(deploy_vault, {"from": account})
    log("ef balance of vault after earn ", str(balance))

    balance = deploy_ef.balanceOf(
        "0x39F4Ef6294512015AB54ed3ab32BAA1794E8dE70", {"from": account}
    )
    log("ef balance of fee pool  after earn ", str(balance))

    balance = deploy_vault.getLPTokenBalance({"from": account})
    log("lp balance  after earn ", str(balance))

    balance = crv.balanceOf(
        "0x39F4Ef6294512015AB54ed3ab32BAA1794E8dE70", {"from": account}
    )
    log("balance of crv of fee pool after earn ", str(balance))

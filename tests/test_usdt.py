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
    CurveInterface256,
)


def log(text, desc=""):
    print("\033[32m" + text + "\033[0m" + desc)


def test_can_get_latest_price(
    deploy_safeerc20,
    deploy_addressArray,
    deploy_tl,
    gett_token_tl,
    deploy_ef,
    deploy_vault,
    addExtraToken,
):
    # Arrange

    # address = get_contract("eth_usd_price_feed").address
    # # Act
    # price_feed = PriceFeedConsumer.deploy(address, {"from": get_account()})
    # # Assert
    # value = price_feed.getLatestPrice({"from": get_account()})

    account_usdt = accounts[-1]
    usdt = ERC20Token.at("0xdAC17F958D2ee523a2206206994597C13D831ec7")

    tx = usdt.approve(
        "0xD51a44d3FaE010294C616388b506AcdA1bfAAE46",
        usdt.balanceOf(account_usdt),
        {
            "from": account,
            "allow_revert": True,
            "gas_price": 100,
            "gas_limit": 3000000,
        },
    )
    tx.wait(1)

    tx = CurveInterface256("0xD51a44d3FaE010294C616388b506AcdA1bfAAE46").exchange(
        0,
        2,
        1931,
        0,
        {
            "from": account_usdt,
            "allow_revert": True,
            "gas_price": 100,
            "gas_limit": 3000000,
        },
    )
    tx.wait(1)

import pytest
from brownie import web3
from web3.auto import w3


from brownie import (
    Address,
    AddressArray,
    Contract,
    EFLeverVault,
    ERC20Token,
    ERC20TokenFactory,
    SafeMath,
    SafeERC20,
    TrustList,
    TrustListFactory,
    accounts,
    config,
    network,
)

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)


@pytest.fixture(scope="session")
def deploy_address():
    account = accounts[0]
    address_array = Address.deploy({"from": account})
    return address_array


@pytest.fixture(scope="session")
def deploy_safeerc20():
    account = accounts[0]
    address_array = SafeERC20.deploy({"from": account})
    return address_array


@pytest.fixture(scope="session")
def deploy_addressArray(deploy_address):
    account = accounts[0]
    address_array = AddressArray.deploy({"from": account})
    return address_array


@pytest.fixture(scope="session")
def deploy_tl():
    account = accounts[0]
    trustlist_factory = TrustListFactory.deploy({"from": account})
    trustlist_factory.tx.wait(1)
    return trustlist_factory


@pytest.fixture(scope="session")
def deploy_safemath():
    account = accounts[0]
    trustlist_factory = SafeMath.deploy({"from": account})
    trustlist_factory.tx.wait(1)
    return trustlist_factory


@pytest.fixture(scope="session")
def gett_token_tl(deploy_tl):
    account = accounts[0]
    tx = deploy_tl.createTrustList(
        ["0x0000000000000000000000000000000000000000"], {"from": account}
    )
    tx.wait(1)
    token_trustlist = TrustList.at(tx.return_value)
    token_trustlist.add_trusted(accounts[0], {"from": account})
    return token_trustlist


# @pytest.fixture(scope="session")
# def gett_oracle_tl(deploy_tl):
#     account = accounts[0]
#     tx =deploy_tl.createTrustList(['0x0000000000000000000000000000000000000000'],{"from": account});
#     tx.wait(1)
#     oracle_trustlist =  TrustList.at(tx.return_value);
#     return oracle_trustlist


@pytest.fixture(scope="session")
def deploy_el(deploy_addressArray, gett_token_tl):
    account = accounts[0]
    token_factory = ERC20TokenFactory.deploy({"from": account})
    token_factory.tx.wait(1)
    tx = token_factory.createCloneToken(
        "0x0000000000000000000000000000000000000000",
        0,
        "ef_lever_token",
        18,
        "EF_LEV",
        True,
        {"from": account},
    )
    tx.wait(1)
    ef_crv = ERC20Token.at(tx.return_value)
    ef_crv.changeTrustList(gett_token_tl.address, {"from": account})
    return ef_crv


@pytest.fixture(scope="session")
def deploy_vault(deploy_el, gett_token_tl, deploy_safemath):
    account = accounts[0]
    ef_vault = EFLeverVault.deploy(
        deploy_el.address, {"from": account, "gas_limit": 12000000000000}
    )
    ef_vault.tx.wait(1)
    tx = gett_token_tl.add_trusted(ef_vault.address, {"from": account})
    tx.wait(1)
    return ef_vault


# @pytest.fixture(scope="session")
# def addExtraToken(deploy_vault):
#     account = accounts[0]

#     crv = "0xD533a949740bb3306d119CC777fa900bA034cd52";
#     cvx = "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B";
#     eth_cvx = "0xb576491f1e6e5e62f1d8f26062ee822b40b0e0d4";
#     tricrv = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490";

#     tripoolswap = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7";

#     tx = deploy_vault.addExtraToken(crv, crv, 0, {"from": account})
#     tx.wait(1)
#     tx = deploy_vault.addExtraToken(cvx, eth_cvx, 1, {"from": account})
#     tx.wait(1)
#     tx = deploy_vault.addExtraToken(tricrv, tripoolswap, 2, {"from": account})
#     tx.wait(1)
#     print("end of addExtraToken")


# @pytest.fixture(scope="session")
# def deploy_cl(deploy_safemath):
#     account = accounts[0]
#     cl_factory = ChainlinkOracleTypeFactory.deploy({"from": account})
#     cl_factory.tx.wait(1)
#     tx = cl_factory.newChainlinkOracleType({"from": account})
#     tx.wait(1)
#     cloracletype = ChainlinkOracleType.at(tx.return_value)
#     return cloracletype


# @pytest.fixture(scope="session")
# def deploy_oracle(gett_oracle_tl):
#     account = accounts[0]
#     oracle_factory = OracleFactory.deploy({"from": account})
#     oracle_factory.tx.wait(1)
#     tx = oracle_factory.newOracle({"from": account})
#     tx.wait(1)
#     oracle = Oracle.at(tx.return_value)
#     oracle.changeTrustList(gett_oracle_tl.address,{"from": account});
#     return oracle


# @pytest.fixture(scope="session")
# def deploy_vt(deploy_chip,deploy_oracle,gett_oracle_tl,gett_token_tl):
#     account = accounts[0]
#     vt_factory = VirtualTradeFactory.deploy({"from": account})
#     vt_factory.tx.wait(1)
#     tx = vt_factory.newVirtualTrade(deploy_chip.address, deploy_oracle.address,{"from": account});
#     tx.wait(1)
#     vtrade = VirtualTrade.at(tx.return_value)
#     gett_oracle_tl.add_trusted(vtrade.address,{"from": account})
#     gett_token_tl.add_trusted(vtrade.address,{"from": account});

#     return vtrade


# @pytest.fixture(scope="session")
# def deploy_entry(deploy_address,deploy_chip, deploy_vt, gett_token_tl):
#     account = accounts[0]
#     pusd = get_contract("pusd_token")
#     entry_factory = EntryFactory.deploy({"from": account})
#     entry_factory.tx.wait(1)
#     tx = entry_factory.newEntry(pusd.address,
#                                 deploy_chip.address, deploy_vt.address,
#                                 {"from": account});
#     tx.wait(1)
#     entry = Entry.at(tx.return_value)

#     gett_token_tl.add_trusted(entry.address,{"from": account});
#     return entry


# @pytest.fixture(scope="session")
# def deploy_univ20(deploy_safemath):
#     account = accounts[0]
#     entry = UniV2OracleType.deploy({"from": account})
#     entry.tx.wait(1)
#     return entry


# @pytest.fixture
# def dev_account():
#     return accounts[0]


# @pytest.fixture(scope="session")
# def add_asset(deploy_vt,deploy_cl,deploy_oracle):
#     account = accounts[0]
#     contract_new =w3.eth.contract(address = deploy_cl.address,abi= deploy_cl.abi)

#     data = contract_new.encodeABI(fn_name="get_asset_price", args=["0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"])
#     deploy_vt.add_asset("pETH", deploy_cl.address, data,{"from": account});
#     data = contract_new.encodeABI(fn_name="get_asset_price",args=["0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c"])
#     deploy_vt.add_asset("pBTC", deploy_cl.address, data,{"from": account});


@pytest.fixture(scope="session")
def add_asset_stock(deploy_vt, deploy_oracle, deploy_univ20):
    account = accounts[0]
    contract_new = w3.eth.contract(address=deploy_univ20.address, abi=deploy_univ20.abi)

    data = contract_new.encodeABI(
        fn_name="get_asset_price",
        args=["0xB022e08aDc8bA2dE6bA4fECb59C6D502f66e953B", True],
    )
    deploy_vt.add_asset("pAAPL", deploy_univ20.address, data, {"from": account})
    data = contract_new.encodeABI(
        fn_name="get_asset_price",
        args=["0x5233349957586A8207c52693A959483F9aeAA50C", False],
    )
    deploy_vt.add_asset("pTSLA", deploy_univ20.address, data, {"from": account})


# @pytest.fixture
# def pusd_balanceof():
#     pusd = get_contract("pusd_token")
#     return pusd.balanceOf(accounts[-1])


@pytest.fixture
def node_account():
    return accounts[1]


@pytest.fixture
def chainlink_fee():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return 1000000000000000000
    if network.show_active() in config["networks"]:
        return config["networks"][network.show_active()]["fee"]
    else:
        pytest.skip("Invalid network/link token specified ")


@pytest.fixture
def expiry_time():
    return 300

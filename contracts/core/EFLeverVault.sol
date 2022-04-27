pragma solidity >=0.4.21 <0.6.0;

import "../utils/Ownable.sol";
import "../utils/SafeMath.sol";
import "../utils/Address.sol";
import "../utils/ReentrancyGuard.sol";
import "../erc20/SafeERC20.sol";
import "./Interfaces.sol";

contract TokenInterfaceERC20{
  function destroyTokens(address _owner, uint _amount) public returns(bool);
  function generateTokens(address _owner, uint _amount) public returns(bool);
}

contract EFCRVVault is Ownable, ReentrancyGuard{
  using SafeERC20 for IERC20;
  using SafeMath for uint256;
  using Address for address;

  uint256 public constant ratio_base = 10000;

  uint256 public mlr;
  address payable public fee_pool;
  address public ef_token;
  uint256 public last_earn_block;

  uint256 public block_rate;
  uint256 last_volume;
  uint256 last_st;
  uint256 last_e;
  uint256 temp;


  address public constant aave = address(0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9);
  address public constant balancer = address(0xBA12222222228d8Ba445958a75a0704d566BF2C8);
  address public constant balancer_fee = address(0xce88686553686DA562CE7Cea497CE749DA109f9F);
  address public constant lido = address(0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84);
  address public constant asteth = address(0x1982b2F5814301d4e9a8b0201555376e62F82428);
  address public constant curve_pool = address(0xDC24316b9AE028F1497c275EB9192a3Ea0f67022);
  address public constant weth = address(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);

  bool is_paused;

  //@param _crv, means ETH if it's 0x0
  constructor(address _ef_token) public {
    ef_token = _ef_token;
    mlr = 6750;
    last_earn_block = block.number;
  }
  /*
  function initAddresses(address[11] memory addr) public onlyOwner{
    crv = addr[0];
    usdc = addr[1];
    eth_usdc_router = addr[2];
    weth = addr[3];
    cvxcrv = addr[4];
    eth_crv_router = addr[5];
    crv_cvxcrv_router = addr[6];
    eth_usdt_router = addr[7];
    usdt = addr[8];
    oracle = addr[9];
    staker = addr[10];
  }*/

  function receiveFlashLoan(
        IERC20[] memory tokens,
        uint256[] memory amounts,
        uint256[] memory feeAmounts,
        bytes memory userData
    ) public payable {
        require(msg.sender == balancer, "only flashloan vault");

        uint256 loan_amount = amounts[0];
        uint256 fee_amount = feeAmounts[0];

        if (keccak256(userData) == keccak256("0x1")){
          _deposit(loan_amount, fee_amount);
        }
        if (keccak256(userData) == keccak256("0x2")){
          _withdraw(loan_amount, fee_amount);
        }
    }

  event EFDeposit(address from, uint256 eth_amount, uint256 ef_amount, uint256 virtual_price);

  function getFeePara() public view returns(uint256){
    return IBalancerFee(balancer_fee).getFlashLoanFeePercentage().safeDiv(1e14).safeAdd(ratio_base); //10000(1+fee/1e18) 
  }

  function getCollecteral() public view returns(uint256){ //decimal 18
    (uint256 c, , , , ,) = IAAVE(aave).getUserAccountData(address(this));
    return c;
  }
  function getDebt() public view returns(uint256){ //decimal 18
    ( , uint256 d, , , ,) = IAAVE(aave).getUserAccountData(address(this));
    return d;
  }
  function getVolume() public view returns(uint256){
    return getCollecteral().safeSub(getDebt());
  }
  function getVirtualPrice() public view returns(uint256){
    if (IERC20(ef_token).totalSupply() == 0) {return 0;}
    return getVolume().safeMul(1e18).safeDiv(IERC20(ef_token).totalSupply());
  }

  function deposit(uint256 _amount) public payable nonReentrant{
    require(!is_paused, "paused");
    require(_amount == msg.value, "inconsist amount");
    require(_amount != 0, "too small amount");
    uint256 volume_before = getVolume();
    if (volume_before == 0) {require(_amount >= 1e16, "Too small initial amount");}

    uint256 fee_para = getFeePara();
    uint256 loan_amount = mlr.safeMul(_amount).safeDiv(fee_para.safeSub(mlr));//mx/(a-m)

    address[] memory tokens;
    uint256[] memory amounts;
    bytes memory userData = "0x1";
    tokens[0] = weth;
    amounts[0] = loan_amount;
    IBalancer(balancer).flashLoan(address(this), tokens, amounts, userData);
    uint256 ef_amount;
    if ((volume_before == 0)){
      ef_amount = _amount;
    }
    else{
      ef_amount = _amount.safeMul(IERC20(ef_token).totalSupply()).safeDiv(volume_before);
    }
    TokenInterfaceERC20(ef_token).generateTokens(msg.sender, ef_amount);
    emit EFDeposit(msg.sender, _amount, ef_amount, getVirtualPrice());
  }

  function _deposit(uint256 amount, uint256 fee_amount) internal{
    IWETH(weth).withdraw(amount);
    ILido(lido).submit.value(address(this).balance)(address(this));

    uint256 lido_bal = IERC20(lido).balanceOf(address(this));

    if (IERC20(lido).allowance(address(this), aave) != 0) {IERC20(lido).safeApprove(aave, 0);}
    IERC20(lido).safeApprove(aave, lido_bal);
    IAAVE(aave).deposit(lido, lido_bal, address(this), 0);

    uint256 to_repay = amount.safeAdd(fee_amount);
    IAAVE(aave).borrow(weth, to_repay, 2, 0, address(this));
    IERC20(weth).safeTransfer(balancer, to_repay);
  }

  event CFFWithdraw(address from, uint256 eth_amount, uint256 ef_amount, uint256 virtual_price);
  function withdraw(uint256 _amount) public nonReentrant{
    require(IERC20(ef_token).balanceOf(msg.sender) >= _amount, "not enough balance");
    if (is_paused){
      uint256 to_send = address(this).balance.safeMul(_amount).safeDiv(IERC20(ef_token).totalSupply());
      (bool status, ) = msg.sender.call.value(to_send)("");
      require(status, "transfer eth failed");
      TokenInterfaceERC20(ef_token).destroyTokens(msg.sender, _amount);
      return;
    }
    //uint256 user_collecteral = getCollecteral().safeMul(_amount).safeDiv(IERC20(ef_token).totalSupply());
    uint256 loan_amount = getDebt().safeMul(_amount).safeDiv(IERC20(ef_token).totalSupply());
    
    address[] memory tokens;
    uint256[] memory amounts;
    bytes memory userData = "0x2";
    tokens[0] = weth;
    amounts[0] = loan_amount;
    //uint256 user_eth_before = msg.sender.balance;
    IBalancer(balancer).flashLoan(address(this), tokens, amounts, userData);

    uint256 to_send = address(this).balance;
    (bool status, ) = msg.sender.call.value(to_send)("");
    require(status, "transfer eth failed");

    TokenInterfaceERC20(ef_token).destroyTokens(msg.sender, _amount);
    emit CFFWithdraw(msg.sender, to_send, _amount, getVirtualPrice());
  }

  function _withdraw(uint256 amount, uint256 fee_amount) internal{
    uint256 steth_amount = amount.safeMul(IERC20(asteth).balanceOf(address(this))).safeDiv(getDebt());

    if (IERC20(weth).allowance(address(this), aave) != 0) {IERC20(weth).safeApprove(aave, 0);}
    IERC20(weth).safeApprove(aave, amount);

    IAAVE(aave).repay(weth, amount, 2, address(this));
    IAAVE(aave).withdraw(lido, steth_amount, address(this));
    ICurve(curve_pool).exchange(1, 0, steth_amount, 0);

    IWETH(weth).deposit(amount.safeAdd(fee_amount));
    IERC20(weth).safeTransfer(balancer, amount.safeAdd(fee_amount));
  }
  event Pause(uint256 eth_amount, uint256 virtual_price);
  function pause() public onlyOwner{
    require(!is_paused, "paused");
    //uint256 user_collecteral = getCollecteral().safeMul(_amount).safeDiv(IERC20(ef_token).totalSupply());
    uint256 loan_amount = getDebt();
    
    address[] memory tokens;
    uint256[] memory amounts;
    bytes memory userData = "0x2";
    tokens[0] = weth;
    amounts[0] = loan_amount;
    //uint256 user_eth_before = msg.sender.balance;
    IBalancer(balancer).flashLoan(address(this), tokens, amounts, userData);
    emit Pause(address(this).balance, getVirtualPrice());
  }

  /*function _pause(uint256 amount, uint256 fee_amount) internal{
    if (IERC20(weth).allowance(address(this), aave) != 0) {IERC20(weth).safeApprove(aave, 0);}
    IERC20(weth).safeApprove(aave, amount);
    IAAVE(aave).repay(weth, amount, 2, address(this));
    IAAVE(aave).withdraw(lido, IERC20(asteth).balanceOf(this), address(this));
    uint256 eth_amount = ICurve(curve_pool).exchange(1, 0, IERC20(lindo).balanceOf(address(this)), 0);

    IWETH(weth).deposit(amount.safeAdd(fee_amount));
    IERC20(weth).safeTransfer(balancer, amount.safeAdd(fee_amount));
  }*/

  event Restart(uint256 eth_amount, uint256 virtual_price);
  function restart() public onlyOwner{
    require(is_paused, "not pause");

    uint256 _amount = address(this).balance;
    uint256 fee_para = getFeePara();
    uint256 loan_amount = mlr.safeMul(_amount).safeDiv(fee_para.safeSub(mlr));//mx/(a-m)

    address[] memory tokens;
    uint256[] memory amounts;
    bytes memory userData = "0x1";
    tokens[0] = weth;
    amounts[0] = loan_amount;
    IBalancer(balancer).flashLoan(address(this), tokens, amounts, userData);
    emit Restart(_amount, getVirtualPrice());
  }


  event ActualLTVChanged(uint256 debt_before, uint256 collecteral_before, uint256 debt_after, uint256 collecteral_after);
  function reduceActualLTV() public onlyOwner{
    uint256 e = getDebt();
    uint256 st = getCollecteral();    
    require(e.safeMul(10000) > st.safeMul(mlr), "no need to reduce");
    uint256 x = (e.safeMul(10000).safeSub(st.safeMul(mlr))).safeDiv(uint256(10000).safeSub(mlr));//x = (E-mST)/(1-m)

    uint256 loan_amount = x.safeMul(getCollecteral()).safeDiv(getDebt());
    address[] memory tokens;
    uint256[] memory amounts;
    bytes memory userData = "0x3";
    tokens[0] = weth;
    amounts[0] = loan_amount;
    IBalancer(balancer).flashLoan(address(this), tokens, amounts, userData);

    IWETH(weth).deposit(address(this).balance);
    if (IERC20(weth).allowance(address(this), aave) != 0) {IERC20(weth).safeApprove(aave, 0);}
    IERC20(weth).safeApprove(aave, IERC20(weth).balanceOf(address(this)));
    IAAVE(aave).repay(weth, IERC20(weth).balanceOf(address(this)), 2, address(this));
    emit ActualLTVChanged(e, st, getDebt(), getCollecteral());
  }

  function RaiseActualLTV(uint256 lt) public onlyOwner{//take lt = 7500
    uint256 e = getDebt();
    uint256 st = getCollecteral();    
    require(e.safeMul(10000) < st.safeMul(mlr), "no need to raise");
    uint256 x = st.safeMul(mlr).safeSub(e.safeMul(10000)).safeDiv(uint256(10000).safeSub(mlr));//x = (mST-E)/(1-m)
    uint256 y = st.safeMul(lt).safeDiv(10000).safeSub(e).safeSub(1);
    if (x > y) {x = y;}
    IAAVE(aave).borrow(weth, x, 2, 0, address(this));
    IWETH(weth).withdraw(IERC20(weth).balanceOf(address(this)));
    ILido(lido).submit.value(address(this).balance)(address(this));

    IERC20(weth).balanceOf(address(this));

    if (IERC20(lido).allowance(address(this), aave) != 0) {IERC20(lido).safeApprove(aave, 0);}
    IERC20(lido).safeApprove(aave, IERC20(lido).balanceOf(address(this)));
    IAAVE(aave).deposit(lido, IERC20(lido).balanceOf(address(this)), address(this), 0);

    emit ActualLTVChanged(e, st, getDebt(), getCollecteral());
  }
  event EarnReward(uint256 eth_amount, uint256 ef_amount);
  function earnReward() public onlyOwner{
    if (fee_pool == address(0x0)) return;
    uint256 len = block.number.safeSub(last_earn_block);
    uint256 A = last_volume.safeMul(block_rate).safeMul(len).safeDiv(1e18);
    uint256 B = getVolume().safeMul(block_rate).safeMul(len).safeDiv(1e18);
    uint256 st_fee;
    if (A <= B){
      st_fee = A.safeAdd(B).safeDiv(2);
    }
    else{
      st_fee = B;
    }
    st_fee = st_fee.safeMul(IERC20(ef_token).balanceOf(fee_pool)).safeDiv(IERC20(ef_token).totalSupply());
    uint256 ef_amount = st_fee.safeMul(IERC20(ef_token).totalSupply()).safeDiv(getVolume().safeSub(st_fee));
    TokenInterfaceERC20(ef_token).generateTokens(fee_pool, ef_amount);
    last_volume = getVolume();
    last_earn_block = block.number;

    emit EarnReward(st_fee, ef_amount);
  }

  event ChangeMaxLoanRate(uint256 old, uint256 _new);
  function changeMaxLoanRate(uint256 _new) public onlyOwner{
    uint256 old = mlr;
    mlr = _new;
    emit ChangeMaxLoanRate(old, _new);
  }

  event ChangeBlockRate(uint256 old, uint256 _new);
  function changeBlockRate(uint256 _r) public onlyOwner{//18 decimal, 2102400 blocks in a year
    uint256 old = block_rate;
    block_rate = _r;
    emit ChangeBlockRate(old, _r);
  }

  event ChangeFeePool(address old, address _new);
  function changeFeePool(address payable _fp) public onlyOwner{
    address old = fee_pool;
    fee_pool = _fp;
    emit ChangeFeePool(old, fee_pool);
  }

  function() external payable{}
  }

contract EFCRVVaultFactory{
  event NewCFVault(address addr);

  function createCFVault(address _ef_token) public returns(address){
    EFCRVVault cf = new EFCRVVault(_ef_token);
    cf.transferOwnership(msg.sender);
    emit NewCFVault(address(cf));
    return address(cf);
  }

}

pragma solidity >=0.4.21 <0.6.0;

contract UniswapV3Interface{
    function swapExactTokensForTokens(uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to) external payable returns (uint256 amountOut);
}
contract CurveInterface256{
    function exchange(uint256 i, uint256 j, uint256 dx, uint256 min_dy) external payable returns(uint256);//change i to j
    //0 weth, 1 crv
}
contract CurveInterface128{
    function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) external returns(uint256);
    function get_dy(int128 i, int128 j, uint256 dx) external view returns(uint256);
    //0 crv, 1 cvxcrv
}
contract CurveInterface256NoReturn{
    function exchange(uint256 i, uint256 j, uint256 dx, uint256 min_dy) external payable;
}
contract TriPoolInterface{
    function remove_liquidity_one_coin(uint256 _token_amount, int128 i, uint256 min_amount) external;//DAI, USDC, USDT
}
contract ConvexInterface{
    function stake(uint256 amount) public returns(bool);
    function withdraw(uint256 amount, bool claim) public returns(bool);
    function getReward() external returns(bool);
    function withdrawAll(bool claim) public;
}
contract ChainlinkInterface{
  function latestAnswer() external view returns (int256);
}
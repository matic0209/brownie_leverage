pragma solidity >=0.4.21 <0.6.0;
interface CurveNew{
    function exchange(uint256 i, uint256 j, uint256 dx, uint256 min_dy) external payable returns(uint256);//change i to j
    //0 weth, 1 crv
}


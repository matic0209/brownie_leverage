pragma solidity >=0.4.21 <0.6.0;

interface IWETH {
    function withdraw(uint256) external;
}
interface IAAVE {
    function borrow(
        address asset,
        uint256 amount,
        uint256 interestRateMode,
        uint16 referralCode,
        address onBehalfOf
    ) external;

    function deposit(
        address asset,
        uint256 amount,
        address onBehalfOf,
        uint16 referralCode
    ) external;

    function withdraw(
        address asset,
        uint256 amount,
        address to
    ) external returns (uint256);

    function repay(
        address asset,
        uint256 amount,
        uint256 rateMode,
        address onBehalfOf
    ) external returns (uint256);

    function getUserAccountData(address)
        external
        view
        returns (
            uint256 totalCollateralETH,
            uint256 totalDebtETH,
            uint256 availableBorrowsETH,
            uint256 currentLiquidationThreshold,
            uint256 ltv,
            uint256 healthFactor
        );
}

interface ILido {
    function submit(address) external payable;
}

interface IBalancer {
    function flashLoan(
        address recipient,
        address[] calldata tokens,
        uint256[] calldata amounts,
        bytes calldata userData
    ) external;
}

interface IBalancerFee{
    function getFlashLoanFeePercentage() external view returns (uint256);//18 decimal
}

interface ICurve{
    function get_dy(int128 i, int128 j, uint256 dx) external view returns(uint256);
    function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) external payable returns(uint256);
}
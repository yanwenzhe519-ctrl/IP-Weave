pragma solidity ^0.8.20;

contract RevenueSplitter {
    address[] public beneficiaries;
    uint256[] public shares;
    uint256 public totalShares;
    address public owner;

    constructor(address[] memory _b, uint256[] memory _s) {
        require(_b.length == _s.length, "Length mismatch");
        owner = msg.sender;
        beneficiaries = _b;
        shares = _s;
        for (uint i = 0; i < _s.length; i++) {
            totalShares += _s[i];
        }
    }

    receive() external payable {}

    function distribute() public {
        uint256 balance = address(this).balance;
        require(balance > 0, "No balance");
        for (uint i = 0; i < beneficiaries.length; i++) {
            payable(beneficiaries[i]).transfer(balance * shares[i] / totalShares);
        }
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}

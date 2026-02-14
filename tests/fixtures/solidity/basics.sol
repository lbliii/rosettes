pragma solidity ^0.8.0;

contract Token {
    mapping(address => uint) public balances;
    event Transfer(address from, address to, uint amount);

    function transfer(address to, uint amount) public returns (bool) {
        emit Transfer(msg.sender, to, amount);
        return true;
    }
}
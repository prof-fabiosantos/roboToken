// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TokenMarketplace {   
    address public token1Address;
    address public token2Address;
    address public ownerToken1;
          
    constructor(address _token1Address, address _token2Address) {
        token1Address = _token1Address; //token para venda
        token2Address = _token2Address; //token para compra    
    }    
    
    function sellTokens(uint256 amount) external {               
        IERC20 token1 = IERC20(token1Address);
        require(amount > 0, "Amount must be greater than zero");
        require(token1.balanceOf(msg.sender) >= amount, "Insufficient balance");
        require(token1.transferFrom(msg.sender, address(this), amount), "Falha na transferencia do token.");
        ownerToken1 = msg.sender;
    }
 

    function buyTokens(uint256 amount) external {
        IERC20 token1 = IERC20(token1Address);
        IERC20 token2 = IERC20(token2Address);
        require(amount > 0, "Amount must be greater than zero");
        uint256 totalCost = amount * getPrice();
        require(totalCost > 0, "Total cost must be greater than zero");
        require(token2.balanceOf(msg.sender) >= totalCost, "Insufficient balance");
        require(token2.transferFrom(msg.sender, address(this), totalCost), "Falha na transferencia do token.");
        require(token1.transfer(msg.sender, totalCost), "Transfer of token2 failed");
    }     
        
    function getPrice() public pure returns (uint256) {
        // Implemente a lógica para obter o preço atual do token
        // Retorne o preço como um número uint256
        // Por exemplo, você pode usar uma API externa ou um oráculo para obter o preço
        // Neste exemplo, retornaremos um valor fixo de 1
        return 1;
    }

    function withdrawTokens(uint256 amount) external {
        require(msg.sender == ownerToken1, "Somente o proprietario do token 1 pode chamar esta funcao.");
        IERC20 token = IERC20(token2Address);
        require(token.transfer(msg.sender, amount), "Falha na transferencia do token.");
    }
   
}
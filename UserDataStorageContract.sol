pragma solidity ^0.4.2;

/* 
	The following is an contract to store Userdata in Solidity and Pay it
*/

// The contract definition. A constructor of the same name will be automatically called on contract creation. 
contract UserDataRequestContract {

    address creator;     // At first, an empty "address"-type variable of the name "creator". Will be set in the constructor.
    address public beneficiary;
    
    uint contractbalance; // TIP: uint is an alias for uint256. Ditto int and int256

    // The constructor. It accepts a string input and saves it to the contract's "greeting" variable.
    function UserDataRequestContract(uint8 setbalance) public {
        creator = msg.sender;
        if(creator.balance < setbalance)
          suicide(creator); // kills this contract and sends remaining funds back to creator
        this.transfer(setbalance);
        beneficiary = 0x01e755e87134DeAa63DC1709446F4d039529fFaB;
    }

    function() payable public {
        suicide(creator); // kills this contract and sends remaining funds back to creator
    }

    function ReleaseMount() public {
       if (msg.sender == creator) {
           beneficiary.transfer(this.balance);
           kill();
       } 
    }
    
     /**********
     Standard kill() function to recover funds 
     **********/
    
    function kill() public { 
        if (msg.sender == creator) {
            // only allow this action if the account sending the signal is the creator
            if (this.balance > 0) {
                creator.transfer(this.balance);
            }
            suicide(creator);       // kills this contract and sends remaining funds back to creator
        }
    }

}

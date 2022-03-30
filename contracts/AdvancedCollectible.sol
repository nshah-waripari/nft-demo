// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase{
    
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIDToSender;
    event requestedCollectible(bytes32 indexed requestId, address requestor);
    event breedAssigned(uint256 indexed tokenID, Breed breed);



    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyHash, uint256 _fee) public 
    VRFConsumerBase(_vrfCoordinator, _linkToken)
    ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIDToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);

    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address onwer = requestIDToSender[requestId];
        _safeMint(onwer, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not ownwer nor approved");
        _setTokenURI(tokenId, _tokenURI);

    }

}
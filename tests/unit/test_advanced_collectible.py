from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import network, config, AdvancedCollectible
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    # deploy and create a contract
    # create a NFT
    # get a random breed back

    # Unit Test Steps
    # 1. Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # 2. Act
    advanced_collectible, creation_tx = deploy_and_create()
    requestId = creation_tx.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )
    # 3. Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3

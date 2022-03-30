from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import network, config, AdvancedCollectible
import pytest
import time
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    # deploy and create a contract
    # create a NFT
    # get a random breed back

    # Unit Test Steps
    # 1. Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # 2. Act
    advanced_collectible, creation_tx = deploy_and_create()
    time.sleep(60)
    # 3. Assert
    assert advanced_collectible.tokenCounter() == 1

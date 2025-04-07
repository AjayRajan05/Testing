from Wallet import Wallet
import pytest

@pytest.fixture
def empty_wallet():
    return Wallet()

@pytest.fixture
def wallet():
    return Wallet(20)

def test_default_init_amt(empty_wallet):
    assert empty_wallet.balance == 0

def test_setting_init_amt(wallet):
    assert wallet.balance == 20

def test_wallet_deposit(wallet):
    wallet.deposit(90)
    assert wallet.balance == 110

def test_wallet_withdraw(wallet):
    wallet.withdraw(10)
    assert wallet.balance == 10

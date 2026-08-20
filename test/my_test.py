import pytest
from app.calculation import add , BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1,num2,expected",[
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300)
])
def test_add(num1, num2, expected):
   
    assert add(num1, num2) == expected

def test_bank_account():
    account=BankAccount(100)
    assert account.balance == 100
def test_bank_default_balance(zero_bank_account):
    
    assert zero_bank_account.balance == 0
def test_deposit():
    account=BankAccount(100)
    account.deposit(50)
    assert account.balance == 150   
def test_withdraw():
    account=BankAccount(100)
    account.withdraw(50)
    assert account.balance == 50
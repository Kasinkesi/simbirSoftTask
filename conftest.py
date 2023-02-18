import pytest
from selenium import webdriver
from datetime import datetime


@pytest.fixture(scope="session")
def browser():
    # driver = webdriver.Chrome()
    driver = webdriver.Remote(
        command_executor='http://172.17.0.1:4444',
        desired_capabilities={'browserName': 'chrome'})
    yield driver
    driver.quit()


# чисел в месяце не так много поэтому обойдемся рекурсией
def recursive_fib(n):
    if n == 1 or n == 2:
        return 1
    return recursive_fib(n - 1) + recursive_fib(n - 2)


@pytest.fixture(scope="session")
def fib_from_date():
    current_day = datetime.now().day
    fib_num = recursive_fib(current_day + 1)
    return fib_num

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from datetime import datetime
import csv
import allure
from page_objects.XYZ_bank_page import HomePage, CustomerLoginPage, AccountPage, TransactionsPage

BASE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"


def make_csv_from(table: list[list]) -> None:
    with open('transactions.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(table)


def reformated_table_for_csv(table: list[list]) -> list[list]:
    reformated_table = table[:]
    for row in reformated_table:
        dt_object = datetime.strptime(row[0], "%b %d, %Y %I:%M:%S %p")
        row[0] = dt_object.strftime("%d %B, %Y %H:%M:%S")
    return reformated_table


@allure.step
def attach_transactions_csv(transactions_table: list[list]) -> None:
    make_csv_from(reformated_table_for_csv(transactions_table))
    allure.attach.file('./transactions.csv', name='transactions.csv', attachment_type=allure.attachment_type.CSV)
    os.remove('./transactions.csv')


def test_smoke(browser, fib_from_date):
    # открывается главная страница
    home_page = HomePage(browser, BASE_URL)
    home_page.open()
    # переход на страницу авторизации
    home_page.go_to_customer_login_page()
    login_page = CustomerLoginPage(browser, browser.current_url)
    # автоизация как "Harry Potter"
    login_page.login_with_name("Harry Potter")
    account_page = AccountPage(browser, browser.current_url)
    # совершается дипозит
    deposit = account_page.make_deposit(fib_from_date)
    # совершается списание
    withdrawl = account_page.make_withdrawl(fib_from_date)
    # проверка баланса
    balance = account_page.balance()
    expected_balance = "0"
    account_page.check_balance(balance, expected_balance)
    # проверка наличия тразакций
    account_page.go_to_transactions_page()
    transactions_page = TransactionsPage(browser, browser.current_url)
    transactions_table = transactions_page.get_table()
    transactions_page.check_tranactions_in_table(deposit, withdrawl, transactions_table)
    # формируется CSV файл и прикрепляется к отчету
    attach_transactions_csv(transactions_table)

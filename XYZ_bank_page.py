import time
from datetime import datetime
from base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePageLocators:
    CUSTOMER_LOGIN_BUTTON = (By.XPATH, '//button[@ng-click = "customer()"]')


class CustomerPageLocators:
    NAME_LIST = (By.ID, 'userSelect')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')


class AccountPageLocators:
    TRANSACTIONS_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="transactions()"]')
    DEPOSIT_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="deposit()"]')
    WITHDRAWL_BUTTON = (By.CSS_SELECTOR, 'button[ng-click="withdrawl()"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    DEPOSIT_INPUT_FIELD = (By.XPATH, '//label[text()="Amount to be Deposited :"]/following-sibling::input')
    WITHDRAWL_INPUT_FIELD = (By.XPATH, '//label[text()="Amount to be Withdrawn :"]/following-sibling::input')
    BALANCE = (By.XPATH, '//div[@ng-hide="noAccount"]/strong[2]')
    # DEPOSITE_SUCCESSFUL = (By.XPATH, '//span[text()="Deposit Successful"]')
    # WITHDRAWL_SUCCESSFUL = (By.XPATH, '//span[text()="Transaction successful"]')


class TransactionsPageLocators:
    BACK_BUTTON = (By.CSS_SELECTOR, 'button[ng-click = "back()"]')
    RESET_BUTTON = (By.CSS_SELECTOR, 'button[ng-click = "reset()"]')
    TABLE_BODY_ROWS = (By.CSS_SELECTOR, 'tbody > tr')
    TABLE_COLUMN = (By.CSS_SELECTOR, 'td')


class HomePage(BasePage):
    def go_to_customer_login_page(self):
        customer_login_btn = self.find_elem(HomePageLocators.CUSTOMER_LOGIN_BUTTON)
        customer_login_btn.click()


class CustomerLoginPage(BasePage):
    def login_with_name(self, name):
        select_element = self.find_elem(CustomerPageLocators.NAME_LIST)
        select = Select(select_element)
        select.select_by_visible_text(name)
        login_btn = self.find_elem(CustomerPageLocators.LOGIN_BUTTON)
        login_btn.click()


class AccountPage(BasePage):
    def _datetime_format(self, datetime_obj):
        return datetime_obj.strftime("%b %d, %Y %-I:%M:%S %p")

    def make_deposit(self, value):
        deposite_btn = self.find_elem(AccountPageLocators.DEPOSIT_BUTTON)
        deposite_btn.click()
        input_field = self.find_elem(AccountPageLocators.DEPOSIT_INPUT_FIELD)
        input_field.send_keys(value)
        submit_button = self.find_elem(AccountPageLocators.SUBMIT_BUTTON)
        submit_button.click()
        now = self._datetime_format(datetime.now())
        # не смог понять закономерности в какой именно момент сохраняется результат
        time.sleep(1)
        return [now, str(value), 'Credit']

    def make_withdrawl(self, value):
        withdrawl_btn = self.find_elem(AccountPageLocators.WITHDRAWL_BUTTON)
        withdrawl_btn.click()
        input_field = self.find_elem(AccountPageLocators.WITHDRAWL_INPUT_FIELD)
        input_field.send_keys(value)
        submit_button = self.find_elem(AccountPageLocators.SUBMIT_BUTTON)
        submit_button.click()
        now = self._datetime_format(datetime.now())
        # не смог понять закономерности в какой именно момент сохраняется результат
        time.sleep(1)
        return [now, str(value), 'Debit']

    def balance(self):
        balance_elem = self.find_elem(AccountPageLocators.BALANCE)
        return balance_elem.text

    def go_to_transactions_page(self):
        transactrions_btn = self.find_elem(AccountPageLocators.TRANSACTIONS_BUTTON)
        transactrions_btn.click()


class TransactionsPage(BasePage):
    def back_to_account_page(self):
        back_btn = self.find_elem(TransactionsPageLocators.BACK_BUTTON)
        back_btn.click()

    def reset_transactions(self):
        reset_btn = self.find_elem(TransactionsPageLocators.RESET_BUTTON)
        reset_btn.click()

    def get_table(self):
        table = []
        table_rows = self.find_elems(TransactionsPageLocators.TABLE_BODY_ROWS)
        for row in table_rows:
            col = [d.text for d in row.find_elements(*TransactionsPageLocators.TABLE_COLUMN)]
            table.append(col)
        return table

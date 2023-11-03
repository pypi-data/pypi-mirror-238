import contextlib
import os
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

RUNNING_IN_PIPELINE = os.getenv('CI')

USERNAME = 'testuser'
PASSWORD = 'testpassword'


@contextlib.contextmanager
def firefox_webdriver() -> WebDriver:
    options = webdriver.FirefoxOptions()
    if RUNNING_IN_PIPELINE:
        options.add_argument("-headless")
    driver = webdriver.Firefox(options)
    try:
        yield driver
    finally:
        driver.quit()


def test_login():
    with firefox_webdriver() as driver:
        driver.get('http://localhost:8080')
        sleep(3)
        errors = [NoSuchElementException, ElementNotInteractableException]
        wait = WebDriverWait(driver, timeout=2, ignored_exceptions=errors)

        username_input: WebElement = driver.find_element(By.ID, 'username')
        wait.until(lambda d: username_input.is_displayed())
        password_input: WebElement = driver.find_element(By.ID, 'password')
        wait.until(lambda d: password_input.is_displayed())
        login_button: WebElement = driver.find_element(By.ID, 'kc-login')
        wait.until(lambda d: login_button.is_displayed())

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        login_button.click()

        sleep(3)

        gretting_label: WebElement = driver.find_element(By.ID, 'gretting_label')
        wait.until(lambda d: gretting_label.is_displayed())
        assert gretting_label.text == 'Hello NiceGUI!'

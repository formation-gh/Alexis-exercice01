import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


APPLICATION_URL = os.getenv(
    "APPLICATION_URL", "https://aouzgaga.github.io/formation-gh-api/"
)
APPLICATION_PASSWORD = os.getenv("APP_PASSWORD")


class BrowserTestCase(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        self.driver = webdriver.Chrome(options=options)
        self.addCleanup(self.driver.quit)
        self.driver.get(APPLICATION_URL)
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_elements(
                By.CSS_SELECTOR, "input[type='password']"
            )
        )

    def connect(self):
        if not APPLICATION_PASSWORD:
            self.skipTest(
                "Définissez APP_PASSWORD pour tester les parcours authentifiés."
            )

        self.driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(
            APPLICATION_PASSWORD
        )
        self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Se connecter']"
        ).click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_elements(By.CSS_SELECTOR, ".user-list")
        )

    def set_dates(self, start, end):
        date_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
        for element, value in zip(date_inputs, (start.isoformat(), end.isoformat())):
            self.driver.execute_script(
                """
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """,
                element,
                value,
            )

import unittest
from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from browser_test_case import APPLICATION_PASSWORD, BrowserTestCase


def next_weekday():
    selected = date.today() + timedelta(days=1)
    while selected.weekday() >= 5:
        selected += timedelta(days=1)
    return selected


@unittest.skipUnless(
    APPLICATION_PASSWORD,
    "Définissez le secret APP_PASSWORD pour tester les parcours authentifiés.",
)
class LeaveManagementTest(BrowserTestCase):
    def open_first_user(self):
        self.connect()
        self.driver.find_element(By.CSS_SELECTOR, ".user-card").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_elements(By.CSS_SELECTOR, ".balance-grid")
        )

    def test_user_details_show_balance_and_leave_form(self):
        self.open_first_user()

        self.assertTrue(
            self.driver.find_elements(
                By.XPATH, "//h2[normalize-space()='Poser un congé']"
            )
        )
        self.assertTrue(
            self.driver.find_elements(
                By.XPATH, "//h2[contains(normalize-space(), 'Congés posés')]"
            )
        )
        self.assertEqual(
            2, len(self.driver.find_elements(By.CSS_SELECTOR, "input[type='date']"))
        )
        self.assertTrue(
            self.driver.find_elements(
                By.XPATH, "//*[normalize-space()='Solde disponible']"
            )
        )

    def test_weekend_period_cannot_be_submitted(self):
        self.open_first_user()
        saturday = date.today() + timedelta(
            days=(5 - date.today().weekday()) % 7 or 7
        )
        self.set_dates(saturday, saturday)

        WebDriverWait(self.driver, 10).until(
            lambda driver: not driver.find_element(
                By.XPATH, "//button[normalize-space()='Poser le congé']"
            ).is_enabled()
        )
        submit_button = self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Poser le congé']"
        )
        self.assertFalse(submit_button.is_enabled())

    def test_weekday_leave_can_be_created_and_deleted(self):
        self.open_first_user()
        selected_day = next_weekday()
        self.set_dates(selected_day, selected_day)

        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                By.XPATH, "//button[normalize-space()='Poser le congé']"
            ).is_enabled()
        )
        submit_button = self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Poser le congé']"
        )
        submit_button.click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: len(driver.find_elements(By.CSS_SELECTOR, ".leave-row")) == 1
        )
        self.assertIn(
            selected_day.strftime("%d/%m/%Y"),
            self.driver.find_element(By.CSS_SELECTOR, ".leave-row").text,
        )

        self.driver.find_element(By.CSS_SELECTOR, ".delete-button").click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_elements(By.CSS_SELECTOR, ".empty-state")
        )
        self.assertFalse(self.driver.find_elements(By.CSS_SELECTOR, ".leave-row"))

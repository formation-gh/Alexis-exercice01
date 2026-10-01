from selenium.webdriver.common.by import By

from browser_test_case import BrowserTestCase


class ApplicationSmokeTest(BrowserTestCase):
    def test_application_loads_expected_login_screen_without_browser_errors(self):
        self.assertEqual(
            "Bienvenue", self.driver.find_element(By.TAG_NAME, "h1").text
        )
        self.assertIn(
            "ESPACE SÉCURISÉ", self.driver.find_element(By.TAG_NAME, "body").text
        )
        self.assertTrue(
            self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        )
        self.assertFalse(self.driver.find_elements(By.CSS_SELECTOR, ".user-list"))

        browser_errors = [
            entry
            for entry in self.driver.get_log("browser")
            if entry["level"] == "SEVERE" and entry["source"] == "javascript"
        ]
        self.assertFalse(browser_errors, f"Erreurs navigateur : {browser_errors}")

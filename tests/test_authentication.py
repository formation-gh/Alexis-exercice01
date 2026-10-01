import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from browser_test_case import APPLICATION_PASSWORD, BrowserTestCase


class AuthenticationTest(BrowserTestCase):
    def test_invalid_password_displays_error_and_clears_input(self):
        password_input = self.driver.find_element(
            By.CSS_SELECTOR, "input[type='password']"
        )
        password_input.send_keys("mot-de-passe-invalide-pour-le-test")
        self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Se connecter']"
        ).click()

        error = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, "[role='alert']")
        )
        self.assertEqual("Mot de passe incorrect.", error.text)
        self.assertEqual("", password_input.get_attribute("value"))
        self.assertFalse(self.driver.find_elements(By.CSS_SELECTOR, ".user-list"))

    @unittest.skipUnless(
        APPLICATION_PASSWORD,
        "Définissez le secret APP_PASSWORD pour tester la connexion réussie.",
    )
    def test_valid_password_opens_user_list(self):
        self.connect()

        self.assertEqual(
            "Les utilisateurs", self.driver.find_element(By.TAG_NAME, "h1").text
        )
        self.assertTrue(self.driver.find_elements(By.CSS_SELECTOR, ".user-card"))

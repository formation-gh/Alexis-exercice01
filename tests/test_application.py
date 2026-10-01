import unittest

from selenium import webdriver


class ApplicationSmokeTest(unittest.TestCase):
    def test_application_loads_without_browser_errors(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        driver = webdriver.Chrome(options=options)
        self.addCleanup(driver.quit)

        driver.get("https://aouzgaga.github.io/formation-gh-api/")

        self.assertEqual(
            "complete", driver.execute_script("return document.readyState")
        )
        browser_errors = [
            entry for entry in driver.get_log("browser") if entry["level"] == "SEVERE"
        ]
        self.assertFalse(browser_errors, f"Erreurs navigateur : {browser_errors}")


if __name__ == "__main__":
    unittest.main()

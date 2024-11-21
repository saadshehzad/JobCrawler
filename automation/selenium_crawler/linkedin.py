from time import sleep
from automation.selenium_crawler.base import BaseCrawler
from automation.selenium_crawler.human import Human
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedIn(BaseCrawler):

    def __init__(self, website):
        """LinkedIn-specific initialization."""
        super().__init__(website)

    def login(self):
        """Log into LinkedIn."""
        self.driver.get(self.website.url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "nav__button-secondary"))
            ).click()
        except Exception as e:
            print("Error: Could not click on the Sign In button.", e)
            return

        try:
            wait = WebDriverWait(self.driver, 10)

            username_field = wait.until(EC.presence_of_element_located((By.NAME, "session_key")))
            username_field.send_keys(self.website.username)

            password_field = wait.until(EC.presence_of_element_located((By.NAME, "session_password")))
            password_field.send_keys(self.website.password)

            login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn__primary--large")))
            login_button.click()

        except Exception as e:
            print("Error: Login process failed.", e)
            return

        try:
            security_check_h1 = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//h1[text()='Let's do a quick security check']"))
            )
            if security_check_h1:
                exc = Exception()
                print(exc)
                return
        except Exception as e:
            print(e)
            return
        except Exception:
            pass

        try:
            password_error_div = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "error-for-password"))
            )
            if password_error_div:
                error_message = password_error_div.text.strip()
                print(f"Login failed: {error_message}")
                return
        except Exception:
            pass

        return True

    def search_jobs(self):
        pass


    def apply(self):
        """Automate applying for a job on LinkedIn."""
        job_url = self.website.job_url
        self.driver.get(job_url)
        sleep(3)

        try:
            apply_button = self.driver.find_element_by_class_name(
                "jobs-s-apply__apply-button"
            )
            apply_button.click()
            sleep(2)

            self.driver.find_element_by_name("firstName").send_keys(
                self.website.first_name
            )
            self.driver.find_element_by_name("lastName").send_keys(
                self.website.last_name
            )

            submit_button = self.driver.find_element_by_xpath(
                '//button[text()="Submit"]'
            )
            submit_button.click()
            sleep(3)
            print("Job application completed successfully!")
        except Exception as e:
            print(f"Error applying for job: {e}")
from time import sleep
from automation.selenium_crawler.base import BaseCrawler
from automation.selenium_crawler.human import Human
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .utils import load_cookies, save_cookies
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select


class LinkedIn(BaseCrawler):

    def __init__(self, website):
        """LinkedIn-specific initialization."""
        super().__init__(website)

    def login(self):
        """Log into LinkedIn."""

        self.driver.get(self.website.url)
        load_cookies(self.driver)
        self.driver.refresh()

        if "feed" in self.driver.current_url:
            print("Logged in successfully using cookies.")
            return True

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

            sleep(10)

            login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn__primary--large")))
            login_button.click()

            save_cookies(self.driver)
            print("Manual login successful, cookies saved.")

        except Exception as e:
            print("Error: Login process failed.", e)
            return

        return True

    def search_jobs(self):
        self.driver.get("https://www.linkedin.com/jobs/")

        try:
            skill_name = "Django"
            country_name = "European Union"

            print("Waiting for skill search input field...")

            skill_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search by title, skill, or company']"))
            )
            skill_input.clear()
            skill_input.send_keys(skill_name)

            print(f"Successfully entered '{skill_name}' into the skill field.", flush=True)

            location_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='City, state, or zip code']"))
            )
            location_input.clear()
            location_input.send_keys(country_name)

            print(f"Successfully entered '{country_name}' into the country field.", flush=True)

            sleep(3) # Do not remove this

            location_input.click()
            location_input.send_keys(Keys.RETURN)

            print(f"Successfully searched for '{skill_name}' in '{country_name}' on LinkedIn Jobs.", flush=True)

            sleep(5)

            # easy_apply_button = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Easy Apply']]"))
            # )
            # easy_apply_button.click()
            # self.driver.implicitly_wait(5)

            # print("Successfully clicked on easy apply button")
            # sleep(5)

            retries = 3
            for attempt in range(retries):
                try:
                    # Wait for the company link to be present
                    company_link = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='job-details-jobs-unified-top-card__company-name']//a[@data-test-app-aware-link]"))
                    )

                    # Right-click on the company link
                    actions = ActionChains(self.driver)
                    actions.context_click(company_link).perform()
                    print("Right-clicked on the company link.")

                    # Open the company link in a new tab (using COMMAND for Mac, CONTROL for Windows)
                    actions.key_down(Keys.COMMAND).click(company_link).key_up(Keys.COMMAND).perform()  # Use CONTROL for Windows
                    print("Successfully selected 'Open in new tab' from the context menu.")
                    
                    sleep(5)  # Increased sleep time to ensure tab has time to load

                    # Close the context menu by pressing ESC
                    actions.send_keys(Keys.ESCAPE).perform()
                    print("Pressed Escape to close the context menu.")
                    sleep(2)  # Allow some time for the context menu to close
                    break  # Exit the loop if successful

                except StaleElementReferenceException:
                    print(f"StaleElementReferenceException encountered. Retrying... {attempt + 1}/{retries}")
                    sleep(2) 
                except Exception as e:
                    print(f"Error occurred: {e}")
                    break

            else:
                print("Failed to interact with the company link after multiple attempts.")

            try:
                window_handles = self.driver.window_handles

                if len(window_handles) > 1:
                    self.driver.switch_to.window(window_handles[1])
                    print("Switched to the second tab.")
                    
                    sleep(3)
                    
                else:
                    print("No second tab found. Please check if the link opened successfully.")
            except Exception as e:
                print(f"Error occurred while switching tabs: {e}")

            sleep(5)

            message_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Message']/parent::button"))
            )

            message_button.click()
            print("Clicked on the 'Message' button.")

            sleep(3)

            select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "msg-shared-modals-msg-page-modal-presenter-conversation-topic"))
            )
            select = Select(select_element)
            select.select_by_visible_text("Careers")
            print("Selected the 'Service request' topic.")
            sleep(3)

            message_box = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "org-message-page-modal-message"))
            )
            message_box.click()


            message = "Some message here"

        message_box.click()

        for line in message.split("\n"):
            message_box.send_keys(line.strip())
            message_box.send_keys(Keys.RETURN)

        print("Message has been pasted into the textarea.")
        sleep(5)

        message_box.send_keys(Keys.TAB)
        sleep(3)

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.RETURN).perform()
        print("Send message button has been clicked using TAB and simulated RETURN.")

        sleep(10)
        return True


    def apply(self):
        """Automate applying for a job on LinkedIn."""
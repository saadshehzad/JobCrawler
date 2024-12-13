from time import sleep

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from automation.models import MyMessage, SkillSet
from automation.selenium_crawler.base import BaseCrawler
from automation.selenium_crawler.human import Human

from .utils import load_cookies, save_cookies


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

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "session_key"))
            )
            username_field.send_keys(self.website.username)

            password_field = wait.until(
                EC.presence_of_element_located((By.NAME, "session_password"))
            )
            password_field.send_keys(self.website.password)
            sleep(10)

            login_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn__primary--large"))
            )
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
            skill_set, created = SkillSet.objects.get_or_create(
                skill_name="Django", country_name="European Union"
            )

            skill_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//input[@aria-label='Search by title, skill, or company']",
                    )
                )
            )
            skill_input.clear()
            skill_input.send_keys(skill_set.skill_name)
            print(
                f"Successfully entered '{skill_set.skill_name}' into the skill field.",
                flush=True,
            )

            location_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@aria-label='City, state, or zip code']")
                )
            )
            location_input.clear()
            location_input.send_keys(skill_set.country_name)
            print(
                f"Successfully entered '{skill_set.country_name}' into the country field.",
                flush=True,
            )

            sleep(3)  # Do not remove this

            location_input.click()
            location_input.send_keys(Keys.RETURN)
            print(
                f"Successfully searched for '{skill_set.skill_name}' in '{skill_set.country_name}' on LinkedIn Jobs.",
                flush=True,
            )
            sleep(5)

            retries = 3
            for attempt in range(retries):
                try:
                    company_link = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//div[@class='job-details-jobs-unified-top-card__company-name']//a[@data-test-app-aware-link]",
                            )
                        )
                    )

                    actions = ActionChains(self.driver)
                    actions.context_click(company_link).perform()
                    actions.move_by_offset(0, 50).click().perform()
                    print("Right-clicked on the company link.")

                    actions.key_down(Keys.COMMAND).click(company_link).key_up(
                        Keys.COMMAND
                    ).perform()
                    print(
                        "Successfully selected 'Open in new tab' from the context menu."
                    )
                    sleep(5)

                    actions.send_keys(Keys.ESCAPE).perform()
                    print("Pressed Escape to close the context menu.")
                    sleep(2)
                    break

                except StaleElementReferenceException:
                    print(
                        f"StaleElementReferenceException encountered. Retrying... {attempt + 1}/{retries}"
                    )
                    sleep(2)
                except Exception as e:
                    print(f"Error occurred: {e}")
                    break

            else:
                print(
                    "Failed to interact with the company link after multiple attempts."
                )

            try:
                window_handles = self.driver.window_handles

                if len(window_handles) > 1:
                    self.driver.switch_to.window(window_handles[1])
                    print("Switched to the second tab.")

                else:
                    print(
                        "No second tab found. Please check if the link opened successfully."
                    )
            except Exception as e:
                print(f"Error occurred while switching tabs: {e}")

            sleep(5)

            return True

        except Exception as e:
            import traceback

            print("Error: Job search process failed.")
            print(traceback.format_exc())
            return False

        return True

    def check_if_company_allow_message(self):
        try:
            message_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[text()='Message']/parent::button")
                )
            )
            message_button.click()
            print("Clicked on the 'Message' button.")
            sleep(3)
            return True

        except Exception as e:
            print(f"{e}")
            print("Company does not allow to send message.")
            return False

        return True

    def check_if_already_message_sent(self):
        try:
            select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        "msg-shared-modals-msg-page-modal-presenter-conversation-topic",
                    )
                )
            )
            return select_element
        except Exception as e:
            print(f"{e}")
            print("Message is already sent.")
            return False

    def paste_and_send_message(self):
        company_allow = self.check_if_company_allow_message()
        if company_allow:
            already_message = self.check_if_already_message_sent()
            if already_message:
                select = Select(already_message)
                select.select_by_visible_text("Careers")
                print("Selected the 'Service request' topic.")
                sleep(3)

                message_box = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.ID, "org-message-page-modal-message")
                    )
                )
                message_box.click()
                message = MyMessage.objects.get(name="Django - European Union").message
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
                print(
                    "Send message button has been clicked using TAB and simulated RETURN."
                )
                sleep(10)
                return True
        else:
            return False

    def switch_to_next_job(self):
        pass

    def apply(self):
        """Automate applying for a job on LinkedIn."""

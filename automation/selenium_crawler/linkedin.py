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
        
        print(self.website.url)
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
            
        except Exception as e:
            import traceback

            print("Error: Job search process failed.")
            print(traceback.format_exc())
            return False

        return True
    
    
    def jobs_list(self):
        url_list = []
        list_items = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'scaffold-layout__list')]//ul/li")
        print("list_items ===============> ", list_items)
        for item in list_items:
            links = item.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                # link_text = link.text
                # print(f"Link Text: {link_text}, URL: {href}")
                url_list.append(href)
                
        return url_list

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
                try:
                    select = Select(already_message)
                    select.select_by_visible_text("Careers")
                    print("Selected the 'Careers' topic.")
                    sleep(3)
                    message_box = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "org-message-page-modal-message"))
                    )
                    message_box.click()
                    message = MyMessage.objects.get(name="Abdul Haris").message
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
                
                except Exception as e:
                    print(f"Error occurred while sending the message: {e}")
            else:
                print("Message is already sent. Moving to the next job.")
        else:
            print("Company does not allow messaging. Moving to the next job.")
        self.switch_to_next_job()
        return False 
  
  
    def open_job_link(self, url_list):
        print(url_list)
        print("********************8")
        for url in url_list: 
            try:
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.get(url)
                # print(f"Opened job link in a new tab: {url}") 
                
                try:
                    company_link = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[@class='job-details-jobs-unified-top-card__company-name']//a[contains(@href, 'linkedin.com/company/')]")
                        )
                    )
                    company_link.click()
                    # print("Clicked on the company link successfully.")
                    
                except Exception as e:
                    print(f"Failed to locate or click the company link: {e}")   

                if not self.check_if_company_allow_message():
                    print("=====================================")
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    continue

                if self.check_if_already_message_sent():
                    print("-------------------------------------")
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    continue

                if self.paste_and_send_message():
                    print("Message successfully sent for the job link.")
                else:
                    print("Failed to send the message for the job link.")

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])

            except Exception as e:
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

        print("Finished processing all job links.")



    # def apply(self):
    #     """Automate applying for a job on LinkedIn."""
        

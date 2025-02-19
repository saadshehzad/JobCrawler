from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class BaseCrawler(ABC):

    def __init__(self, website):
        """Initializes the crawler with the website and sets up the headless browser."""
        self.website = website
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Setup Chrome WebDriver with headless option."""
        chromedriver_path = r"C:\Users\abdul haris\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
        chrome_options = Options()
        chrome_options.add_argument(
            "--start-maximized"
        )  # Open browser in maximized window
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")
        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    

    def is_two_step_verification(self):
        """Check if the website is asking for 2FA."""
        try:
            self.driver.find_element(By.ID, "two-step-verification-code")
            return True
        except Exception as e:
            return False

    @abstractmethod
    def login(self):
        """Method to perform login on the website."""
        pass

    @abstractmethod
    def search_jobs(self):
        """Method to perform login on the website."""
        pass

    # @abstractmethod
    def apply_jobs(self):
        """Method to perform login on the website."""
        pass

    # @abstractmethod
    def apply(self):
        """Method to apply for a job on the website."""
        pass

    def close_driver(self):
        """Properly close the driver after use."""
        if self.driver:
            self.driver.quit()
            print("Driver closed.")

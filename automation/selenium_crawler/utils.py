import os
import pickle
import fickling


def save_cookies(driver, path="cookies.pkl"):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, path="cookies.pkl"):
    if not os.path.exists(path):
        print("Cookie file not found. Proceeding with manual login.")
        return

    try:
        with open(path, "rb") as file:
            cookies = fickling.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

        print("Cookies loaded successfully.")
    except FileNotFoundError:
        print("Cookie file not found. Proceeding with manual login.")

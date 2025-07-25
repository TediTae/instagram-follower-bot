from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time

SIMILAR_ACCOUNT = "YOUR DESIRED ACCOUNT FOR FOLLOWERS"
INSTA_MAIL = "YOUR EMAIL"
INSTA_PASSWORD = "YOUR PASSWORD"


class InstaFollower:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)


    def login(self):
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        time.sleep(10)
        start_log_button = self.driver.find_element(By.XPATH, "//div[@role='button' and contains(text(), 'Log in')]")
        time.sleep(1)
        start_log_button.click()
        time.sleep(5)
        username = self.driver.find_element(By.XPATH, "//input[@name='username']")
        time.sleep(1)
        username.send_keys(INSTA_MAIL)
        time.sleep(2)
        password = self.driver.find_element(By.XPATH, "//input[@type='password' and @name='password']")
        time.sleep(1)
        password.send_keys(INSTA_PASSWORD)
        time.sleep(2)
        log_in_button = self.driver.find_element(By.XPATH, "//button[@type='submit' and .//div[contains(text(), 'Log in')]]")
        time.sleep(1)
        log_in_button.click()
        time.sleep(10)
        wait = WebDriverWait(self.driver, 10)
        not_now_but = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), 'Not now')]")))
        self.driver.execute_script("arguments[0].click();", not_now_but)

    def find_followers(self):
        wait = WebDriverWait(self.driver, 10)
        follower_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/chefsteps/followers/' and @role='link']")))
        self.driver.execute_script("arguments[0].click();", follower_tab)
        time.sleep(5)
        followers = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/"
                                                       "div/div/div[2]/div/div/div[3]")
        for i in range(5):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers)
            time.sleep(2)

    def follow(self):
        all_follow_buttons = self.driver.find_elements(By.XPATH, "//button[@type='button' and contains(., 'Follow')]")

        for button in all_follow_buttons:
             try:
                self.driver.execute_script("arguments[0].click();",button)
                time.sleep(1.1)
             #Clicking button for someone who is already being followed will trigger dialog to Unfollow/Cancel
             except ElementClickInterceptedException:
                 cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                 cancel_button.click()



bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()

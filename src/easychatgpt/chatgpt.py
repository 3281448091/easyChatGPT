import time
from typing import List

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class ChatClient:
    """Handler class to interact with ChatGPT"""

    #Paths for elements
    login_xq = '//button[text()="Log in"]'
    continue_xq = '//button[text()="Continue"]'
    next_xq = '//button[text()="Next"]'
    done_xq = '//button[text()="Done"]'

    chatbox_cq = 'text-sm'
    answer_cq = 'group'
    wait_cq = 'text-2xl'
    reset_xq = '//a[text()="New Chat"]'

    def __log(self, msg : str) -> None:
        if self.verbose:
            print(msg)

    def __init__(self, username: str, password: str,
                 headless: bool = False, verbose : bool = True) -> None:

        # initializing undetected-driver to prevent cloudflare bot detection
        if verbose:
            self.verbose = True
        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        if headless:
            options.add_argument("--headless")
        self.browser = uc.Chrome(options=options)
        self.browser.set_page_load_timeout(15)

        self.browser.get("https://chat.openai.com/chat")
        self.__log("Browser successfully launched, logging in to account...")
        self.__login(username, password)

    def __login(self, username: str, password: str) -> None:
        """To enter system"""
        # Find login button, click it

        # bypass announcement popup
        self.browser.execute_script("""
        window.localStorage.setItem('oai/apps/hasSeenOnboarding/chat', 'true');
        window.localStorage.setItem(
          'oai/apps/hasSeenReleaseAnnouncement/2022-12-15',
          'true'
        ); 
        window.localStorage.setItem(
          'oai/apps/hasSeenReleaseAnnouncement/2022-12-19',
          'true'
        ); """)

        login_button = self.__sleepy_find_element(By.XPATH, self.login_xq)
        login_button.click()
        time.sleep(1)

        # Find email textbox, enter e-mail
        email_box = self.__sleepy_find_element(By.ID, "username")
        email_box.send_keys(username)

        # solve recaptcha
        from pypasser import reCaptchaV2

        # Create an instance of webdriver and open the page has recaptcha v2
        # ...

        # pass the driver to reCaptchaV2
        is_checked = reCaptchaV2(self.browser, play=False)  # it returns bool
        self.__log("reCaptchaV2 is solved")
        # input("solved captcha?")

        # Click continue
        continue_button = self.__sleepy_find_element(By.XPATH, self.continue_xq)
        continue_button.click()
        time.sleep(1)

        # Find password textbox, enter password
        pass_box = self.__sleepy_find_element(By.ID, "password")
        pass_box.send_keys(password)
        # Click continue
        continue_button = self.__sleepy_find_element(By.XPATH, self.continue_xq)
        continue_button.click()
        time.sleep(1)

    def __sleepy_find_element(self, by, query, attempt_count: int = 20, sleep_duration: int = 1) -> List[WebElement]:
        """If the loading time is a concern, this function helps"""
        for _ in range(attempt_count):
            item = self.browser.find_elements(by, query)
            if len(item) > 0:
                item = item[0]
                break
            time.sleep(sleep_duration)
        return item

    def __wait_to_disappear(self, by, query, sleep_duration=1):
        """Wait until the item disappear, then return"""
        while True:
            thinking = self.browser.find_elements(by, query)
            if len(thinking) == 0:
                break
            time.sleep(sleep_duration)
        return

    def interact(self, question: str) -> str:
        """Function to get an answer for a question"""
        self.__log(f"Question received: {question}, awaiting chatgpt response... ")
        text_area = self.browser.find_element(By.TAG_NAME, 'textarea')
        for each_line in question.split("\n"):
            text_area.send_keys(each_line)
            text_area.send_keys(Keys.SHIFT + Keys.ENTER)
        text_area.send_keys(Keys.RETURN)
        self.__wait_to_disappear(By.CLASS_NAME, self.wait_cq)
        box = self.browser.find_elements(By.CLASS_NAME, self.chatbox_cq)[0]
        answer = box.find_elements(By.CLASS_NAME, self.answer_cq)[-1]
        self.__log("Got response... ")
        return answer.text

    def __reset_thread(self):
        """the conversation is refreshed"""
        self.browser.find_element(By.XPATH, self.reset_xq).click()

    def __switch_to_tab(self, idx: int = 0):
        "Switch to tab"
        windows = self.browser.window_handles
        if idx > len(windows):
            print(f"There is no tab with index {idx}")
            return
        self.browser.switch_to.window(windows[idx])

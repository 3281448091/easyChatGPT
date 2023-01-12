import asyncio
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import List

import undetected_chromedriver as uc

from threading import Thread

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


from easychatgpt.exceptions import NotEnoughInformationException, CouldNotSolveCaptcha

executor = ThreadPoolExecutor(10)


class ChatClient:
    """Handler class to interact with ChatGPT"""

    # Paths for elements
    login_xq = '//button[text()="Log in"]'
    continue_xq = '//button[text()="Continue"]'
    next_xq = '//button[text()="Next"]'
    done_xq = '//button[text()="Done"]'

    chatbox_cq = 'text-sm'
    answer_cq = 'group'
    wait_cq = 'text-2xl'
    reset_xq = '//a[text()="New Chat"]'
    thread_xq = '//*[@class="flex py-3 px-3 items-center gap-3 relative rounded-md hover:bg-[#2A2B32] cursor-pointer break-all hover:pr-4 group"]'
    thread_selected_xq = '//*[starts-with(@class, "flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer break-all pr-14 bg-gray-800 hover:bg-gray-800 group")]'
    thread_buttons_xq = '//button[@class="p-1 hover:text-white"]'
    text_xq = '//*[text()="{}"]' # append and format to search text field

    def __log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def update_session(self, interval: int = 10) -> None:
        """override the Local Storage getSession to fool OpenAI's script to not show a Login Expired message. Creds to Rowa"""
        while True:
            kv = '{"event":"session","data":{"trigger":"getSession"},"timestamp":' + str(round(time.time())) + '}'

            try:
                # window.localStorage.setItem('nextauth.message', '{"event":"session","data":{"trigger":"getSession"},"timestamp":'1672014120'}')
                self.browser.execute_script(f"window.localStorage.setItem('nextauth.message', '{kv}')")
            except:
                pass

            self.__log("Updated session")

            time.sleep(interval)

    def __init__(self, username: str, password: str,
                 headless: bool = False, verbose: bool = True, chrome_version: int = 0) -> None:

        # initializing undetected-driver to prevent cloudflare bot detection

        # TODO cloudlfare if you are a bot detection also auto update to pypi add exceptions too

        # class="big-button pow-button"

        if username is None or password is None:
            raise NotEnoughInformationException("You did not input username or password")

        if verbose:
            self.verbose = True

        options = uc.ChromeOptions()
        options.add_argument("--incognito")
        if headless:
            options.add_argument("--headless")
        
        # when version_main set to 0, works as though no version was supplied, uses defaut
        self.browser = uc.Chrome(options=options, version_main=chrome_version)
        self.browser.set_page_load_timeout(15)

        self.browser.get("https://chat.openai.com/chat")
        self.__log("Browser successfully launched, logging in to account...")

        t = Thread(target=self.update_session)
        t.setDaemon(True)
        t.start()

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

        # pass the driver to reCaptchaV2
        is_checked = reCaptchaV2(self.browser, play=False)  # it returns bool
        if not is_checked:
            raise CouldNotSolveCaptcha("Unexpected error occured while solving captcha")

        self.__log("reCaptchaV2 is solved")

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

    def __sleepy_find_element(self, by, query, attempt_count: int = 20, sleep_duration: int = 1):
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

    def switch_thread(self, name):
        """
        The thread is switched to the thread that goes by the name specified
        NOTE: When a new thread is created and then you switch to another thread immediately
                it interrupts the autonaming of the thread, which makes the name 'New Chat'
        """

        try:
            # this will give an error if thread currently selected
            # as currently selected thread is under a different xpath
            self.browser.find_element(By.XPATH, (self.thread_xq + self.text_xq.format(name))).click()
            self.__log("Thread {} selected".format(name))

        # in this case, the thread could be currently selected, so we check for that
        except NoSuchElementException:
            try:
                self.browser.find_element(By.XPATH, (self.thread_selected_xq + self.text_xq.format(name))).click()
                self.__log("Thread {} already selected".format(name))
            except Exception as e:
                self.__log("Thread could not be found")
                raise

        except Exception as e:
            raise

        else:
            # selected another thread, lets make sure its usable before we continue
            # NOTE: for some reason it takes a little too long to continue from this
            #       point. Not sure if it is because it really takes that long for
            #       the chatbox to become available.
            chat_box = self.__sleepy_find_element(By.XPATH, self.chatbox_cq)

    def delete_thread(self):
        """delete the current thread"""
        # make sure a thread is selected
        self.browser.find_element(By.XPATH, self.thread_selected_xq).click() 
        buttons = self.browser.find_elements(By.XPATH, self.thread_buttons_xq)
        delete_button = buttons[1]
        delete_button.click()

        confirm_buttons = self.browser.find_elements(By.XPATH, self.thread_buttons_xq)
        confirm_button = confirm_buttons[0]
        confirm_button.click()

    def edit_thread_name(self, name):
        """changes the name of the current thread"""
        self.browser.find_element(By.XPATH, self.thread_selected_xq).click() 
        buttons = self.browser.find_elements(By.XPATH, self.thread_buttons_xq)
        edit_button = buttons[0]
        edit_button.click()

        edit_field_xq = '//*[@class = "text-sm border-none bg-transparent p-0 m-0 w-full mr-0"]'
        edit_field = self.__sleepy_find_element(By.XPATH, edit_field_xq)
        edit_field.send_keys(Keys.CONTROL + "a", Keys.DELETE)
        edit_field.send_keys(name)

        confirm_buttons = self.browser.find_elements(By.XPATH, self.thread_buttons_xq)
        confirm_button = confirm_buttons[0]
        confirm_button.click()

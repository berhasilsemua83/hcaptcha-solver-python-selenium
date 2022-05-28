#! /home/masher2/.venvs/freebitbot/bin/python
import logging
import selenium
import time, os
from selenium import webdriver
import logging.config
import re
from time import sleep
from unittest import result
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotInteractableException, ElementClickInterceptedException,
    NoSuchElementException
)
from selenium.common.exceptions import TimeoutException as TE
from twocaptcha import TwoCaptcha
from colorama import init, Fore, Style
#from .utils.colors import GREEN, RED, RESET
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RESET = Style.RESET_ALL
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
            'datefmt': '%H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
})
logger = logging.getLogger(__name__)

PROXY = "45.142.28.83:8094"
class FreebitBot:

    def __init__(self):
        logger.info('Initializing FreebitBot.')
        options = webdriver.ChromeOptions()
        #options.add_argument('--proxy-server=%s' % PROXY)
        options.add_extension('C:/Users/mamas/Documents/2captcha-python-master/hcaptcha-solver-python-selenium-master/assets/Tampermonkey.crx')
        #self.driver = uc.Chrome(use_subprocess=True)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

        self.driver.get('https://freebitco.in/')
        time.sleep(2)
        self.window_handles(1) 
        self.driver.get('https://greasyfork.org/fr/scripts/445478-hcaptcha-solver')
        time.sleep(2)
        self.clickable('//*[@id="install-area"]/a[1]')
        time.sleep(3)
        self.window_handles(2)
        self.clickable('//*[@value="Install"]')
        time.sleep(2)
        self.window_handles(1)
        self.driver.close() 
        self.window_handles(0)

        

        self.deny_notifications()

        # Login
        logger.info('Navigating to the loging screen.')
        self.driver\
            .find_element(By.CLASS_NAME,'login_menu_button')\
            .click()
        self.driver\
            .find_element(By.ID, 'login_form_btc_address')\
            .send_keys('josenabdel@gmail.com') #('josenabdel@gmail.com') saliksewas@gmail.com
        self.driver\
            .find_element(By.ID,'login_form_password')\
            .send_keys('Bijaksana2020')
        self.driver\
            .find_element(By.ID,'login_button')\
            .click()       
        logger.info('Wating for the user to log in.')
        self.wait_for_login()

    def wait_for_login(self):
        try:
            self.driver.find_element(By.ID,'login_form_btc_address')
            sleep(5)
            self.wait_for_login()
        except NoSuchElementException:
            logger.info('Successfully logged')

    def deny_notifications(self):
        logger.info('Removing the notification popup')
        try:
            self.driver\
                .find_element(By.CSS_SELECTOR,'div.pushpad_deny_button')\
                .click()
            logger.info('Removed the pop up')
        except ElementNotInteractableException:
            logger.error('Could not remove the notification popup')
        except Exception as e:
            logger.error(f"Unexpected error, retrying.\nThe exception was: {e}")
    
    def tutup_popup(self):
        logger.info('Tutup popup setelah claim')
        try:
            WDW(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'myModal22')))
            self.driver\
                .find_element(By.CLASS_NAME, 'close-reveal-modal')\
                .click()
            logger.info('Tutup pop up')
        except ElementNotInteractableException:
            logger.error('ga bisa nutup popup')
            self.driver.refresh()
        except Exception as e:
            logger.error(f"Unexpected error, retrying.\nThe exception was: {e}")
    
    def claim_btc(self):
        try:
            logger.info('Trying to claim the btc.')
            self.driver.find_element(By.ID,'free_play_form_button').click()
            logger.info('BTC Claimed!')
        except Exception:
            sleep(5)
    

    def urus_hcaptcha(self):
        try:
            logger.info('mencoba solving captcha')
            WDW(self.driver, 600).until(lambda _: len(self.visible(
                '//div[@class="h-captcha"]/iframe').get_attribute(
                    'data-hcaptcha-response')) > 0)
            print(f'{GREEN}Solved.{RESET}')
        except TE:  # Something went wrong.
            print(f'{RED}Failed.{RESET}')

    def quit(self) :
        """Stop the webdriver."""
        try:  # Try to close the webdriver.
            self.driver.quit()
        except Exception:  # The webdriver is closed
            pass  # or no webdriver is started.

    def clickable(self, element: str):
        """Click on an element if it's clickable using Selenium."""
        try:
            WDW(self.driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, element))).click()
        except Exception:  # Some buttons need to be visible to be clickable,
            self.driver.execute_script(  # so JavaScript can bypass this.
                'arguments[0].click();', self.visible(element))

    def visible(self, element: str):
        """Check if an element is visible using Selenium."""
        return WDW(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, element)))

    def window_handles(self, window_number: int) :
        """Check for window handles and wait until a specific tab is opened."""
        WDW(self.driver, 10).until(lambda _: len(
            self.driver.window_handles) > window_number)
        self.driver.switch_to.window(  # Switch to the asked tab.
            self.driver.window_handles[window_number])




    def check(self):
        """ Checks if can claim the BTC
        Returns False if not ready to claim, True otherwise
        """
        try:
            # No internet
            if self.driver.title == 'Server Not Found':
                self.driver.refresh()
                return False

            # Stopped clock
            if re.search('^0m\:0s', self.driver.title):
                self.driver.refresh()
                return False

            # Waiting
            if re.search('^\d{1,2}m\:\d{1,2}s', self.driver.title):
                return False

            # Notification popup
            if self.driver.find_element(By.CSS_SELECTOR,'div.pushpad_deny_button').is_displayed():
                self.deny_notifications()
                return False

            # Are we ready?
            ready = self.driver.find_element(By.ID,'free_play_form_button').is_displayed()
            if ready:
                # Scrolling to bottom
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                print('scroll ke bawah')

                self.urus_hcaptcha()
                
                # time.sleep(1)
                # self.claim_btc()

            return ready

        except Exception:
            return False

    def main(self):
        while True:
            if self.check():
                self.claim_btc()
                time.sleep(3)
                self.tutup_popup()
            else:
                sleep(10)


if __name__ == '__main__':
    bot = FreebitBot()
    bot.main()

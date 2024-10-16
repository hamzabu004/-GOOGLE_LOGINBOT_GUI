
from PySide6 import QtCore
from selenium import webdriver
from multiprocessing import  Manager, Process
import time
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

import os

from utils import login_google, get_user_agent, construct_proxy


def launch_chrome(profile, profiles_path):
    """Function to launch Chrome browser using Selenium."""
    global driver
    print("Launching Chrome...")

    # Optional: You can set Chrome options if needed
    chrome_options = webdriver.ChromeOptions()
    # Initialize SeleniumAuthenticatedProxy
    # print(construct_proxy(profile))
    # proxy_helper = SeleniumAuthenticatedProxy(proxy_url=construct_proxy(profile))
    #
    # # Enrich Chrome options with proxy authentication
    # proxy_helper.enrich_chrome_options(chrome_options)
    user_agent = get_user_agent()
    chrome_options.add_argument(f"--user-data-dir={profiles_path}\\data\\profiles\\{profile['id']}")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-agent={user_agent}")

    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)


    # Create a new instance of the Chrome driver
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        driver.quit()
        print("proxy war gae")
        print(e)
        return
    # get current working directory from os
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")



    # pre processors
    try:
        if ((str(profile["module_name"])).lower() == "google"):
            login_google(driver, profile)

    except Exception as e:
        print(e)
        driver.quit()
        return

    flag = True
    while flag:
        # noinspection PyStatementEffect
        try:
            driver.title
        # exception will raise when browser is closed
        except Exception as e:
            print("Chrome driver has been closed.")
            flag = False
            driver.quit()

        time.sleep(2)  # Check every 2 seconds

# multi processing manager
class ProfilesManager:
    def __init__(self):
        self.manager = Manager()
        self.profiles = []
        self.drivers = []
        self.check_processes()


    def check_processes(self):
        for idx, process in enumerate(self.profiles):

            if not process.is_alive():
                print("Checking processes...")
                process.join()  # Ensure the process resources are cleaned up
                self.profiles.remove(process)  # Remove closed process from the list\
                print("Removed closed process from the list.")

        QtCore.QTimer.singleShot(2000, self.check_processes)




    def launch_profile(self, profiler, profiles_path = os.getcwd()):
        """Launch a profile in a separate process."""
        print(dict(profiler))

        chrome_process = Process(target=launch_chrome, args=(dict(profiler), profiles_path))
        chrome_process.start()
        self.profiles.append(chrome_process)

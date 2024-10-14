
from PySide6 import QtCore
from selenium import webdriver
from multiprocessing import  Manager, Process
import time
import undetected_chromedriver as uc
import os

from utils import login_google


def launch_chrome(profile, profiles_path):
    """Function to launch Chrome browser using Selenium."""
    print("Launching Chrome...")

    # Optional: You can set Chrome options if needed
    chrome_options = webdriver.ChromeOptions()
    # user_agent = profile["user_agent"]
    user_agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0 (Edition Yx 05)"
    chrome_options.add_argument(f"--user-data-dir={profiles_path}\\data\\profiles\\{profile['id']}")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-agent={user_agent}")

    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)


    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    # get current working directory from os
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")



    # pre processors
    if ((str(profile["module_name"])).lower() == "google"):
        login_google(driver, profile)

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


from PySide6 import QtCore
from selenium import webdriver
from multiprocessing import  Manager, Process
import time




def launch_chrome(profile, profiles_path):
    """Function to launch Chrome browser using Selenium."""
    print("Launching Chrome...")

    # Optional: You can set Chrome options if needed
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument(f"--user-data-dir={profiles_path}\\{profile['id']}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("detach", True)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # pre processors
    if ((str(profile["module"])).lower() == "google"):
        pass

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




    def launch_profile(self, profiler, profiles_path = "F:\\profiles"):
        """Launch a profile in a separate process."""
        print(dict(profiler))

        chrome_process = Process(target=launch_chrome, args=(dict(profiler), profiles_path))
        chrome_process.start()
        self.profiles.append(chrome_process)

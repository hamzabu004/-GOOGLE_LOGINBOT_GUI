from distutils.command.check import check

from PySide6 import QtCore
from selenium import webdriver
from multiprocessing import  Manager, Process, Queue
import time

def test_process():
    print("Test process started.")
    time.sleep(5)
    print("Test process finished.")


# multi processing manager
class ProfilesManager:
    def __init__(self):
        self.profiles = []
        self.drivers = []
        self.check_processes()


    def check_processes(self):
        """Check if processes are alive and clear the queue if closed."""
        for idx, process in enumerate(self.profiles):

            if not process.is_alive():
                print("Checking processes...")
                process.join()  # Ensure the process resources are cleaned up
                self.profiles.remove(process)  # Remove closed process from the list\
                # self.drivers[idx].quit()  # Quit the corresponding drivern to
                # del self.drivers[idx]  # Remove the corresponding driver from the list
                print("Removed closed process from the queue.")

        QtCore.QTimer.singleShot(2000, self.check_processes)

    def launch_chrome(self, profile):
        """Function to launch Chrome browser using Selenium."""
        print("Launching Chrome...")
        # print(profile)

        # Optional: You can set Chrome options if needed
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("user-data-dir=selenium")
        # chrome_options.add_argument("--profile-directory=F:\profiles\selenium-profile")
        chrome_options.add_argument("--user-data-dir=F:\profiles\selenium-profile\data")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("detach", True)

        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        # Open a webpage (e.g., Google)
        driver.get("https://www.google.com")
        self.drivers.append(driver)



    def launch_profile(self, profiler):
        print(dict(profiler))
        """Launch a profile in a separate process."""
        chrome_process = Process(target=self.launch_chrome, args=(dict(profiler),))
        chrome_process.start()
        self.profiles.append(chrome_process)

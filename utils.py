import os
import time
from traceback import print_tb

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from dotenv import load_dotenv


def login_google (driver: webdriver.Chrome, creds : dict):
    # check if already logged in
#     first open a new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://accounts.google.com")
    driver.implicitly_wait(1)
    if is_google_logged_in(driver):
        print("Already logged in")
        # driver.close()
        return


    email_field = driver.find_element(By.ID, "identifierId")
    email_field.send_keys(creds["email"])
    driver.find_element(By.ID, "identifierNext").click()
    time.sleep(5)
    # possibility of captcha
    captcha_handler(driver)

    driver.find_element(By.ID, "identifierNext").click()

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(creds["password"])

    driver.find_element(By.ID, "passwordNext").click()



def is_google_logged_in(driver: webdriver.Chrome) -> bool:
    return not is_element_exists(driver, By.ID, "identifierId")

def captcha_handler(driver: webdriver.Chrome):
    if not is_element_exists(driver, By.CSS_SELECTOR, "[data-site-key]"):
        print("No captcha found")
        return

    load_dotenv()
    api_key = os.getenv('2CPATCHA_API_KEY')
    solver = TwoCaptcha(api_key)
    site_key = driver.find_element(By.CSS_SELECTOR, "[data-site-key]")
    site_key = site_key.get_attribute("data-site-key")
    response = solver.solve_captcha(site_key=site_key, page_url=driver.current_url)


    driver.execute_script(f"const escapeHTMLPolicy = trustedTypes.createPolicy('forceInner', {{createHTML: (to_escape) => to_escape}});        document.getElementById('g-recaptcha-response').innerHTML = escapeHTMLPolicy.createHTML('{response}');")
    print("Captcha Solved")
    # check if captcha is present


def is_element_exists(driver: webdriver.Chrome, by: str, value: str) -> bool:
    wait = WebDriverWait(driver, 2)
    try:
        # Wait until the element is visible within the 10-second timeout
        element = wait.until(EC.visibility_of_element_located((by, value)))
        return True
    except:
        return False
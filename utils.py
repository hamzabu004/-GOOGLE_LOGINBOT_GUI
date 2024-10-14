import os
import time
from random import randint
from shutil import rmtree
from traceback import print_tb

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from dotenv import load_dotenv

import json

import globals
from db import DatabaseConnection


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

def get_user_agent() -> str:
    user_agents = json.load(open("data/user_agents.json", "r"))

    user_agent = user_agents[randint(0, len(user_agents) - 1)]

    return user_agent


def get_params_profile_read(profile: dict):
    return (profile["profile_name"], profile["email"], profile["password"], profile["recovery_email"],
            profile["module_index"], profile["module_name"],
            profile["proxy_ip"], profile["proxy_port"], profile["proxy_username"], profile["proxy_password"], profile["user_agent"])


def on_load_csv(path: str):
    csv_path = path
    profile_data = pd.read_csv(csv_path)
    db_conn = DatabaseConnection("data/profiles.db").connection

    for index, row in profile_data.iterrows():
        #             insert in sql

        sql_query = globals.sql_queries["insert_profile"]

        if (len(row["proxy"].split(":")) == 4):
            ip, port, username, password = row["proxy"].split(":")
        else:
            ip, port = row["proxy"].split(":")
            username = ""
            password = ""

        module_index = 0
        module_name = "Google"
        # random string for time being
        profile_name = "Profile " + str(index)

        db_conn.execute(sql_query, (profile_name, row["email"], row["password"], row["recovery_email"],
                                    module_index, module_name,
                                    ip, port, username, password, get_user_agent()))
        db_conn.commit()

def insert_to_db(query, params, callback=None):
    db_conn = DatabaseConnection("data/profiles.db").connection
    db_conn.execute(query, params)
    db_conn.commit()
    if callback:
        callback()

def delete_from_db(query, params, callback=None):
    db_conn = DatabaseConnection("data/profiles.db").connection
    db_conn.execute(query, params)
    db_conn.commit()
    if callback:
        callback()


def rm_dir(path: str):
    if (os.path.exists(path)):
        rmtree(path)

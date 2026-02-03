import os
import time
from selenium.webdriver.common.by import By
import re

# ===== Selenium Core =====
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ===== Selenium Helpers =====
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# ===== Waits =====
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# ===== Other =====
import time

# ===== GoLogin =====
from gologin import GoLogin
from tkinter import *

GOLOGIN_CONF = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzEzMTNiMzUxNGI3NzAxNzhjMDRiNDUiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2ODVhZWJjMzk2NzMyYTJjNjU2YTJhNTEifQ.xBSrKOOUX3djmsvr0T6zjqGbZ4Ic4gdHH20Xd2Krquk",
    "profile_id": "6834ec3749adaff086ca5eb9",
    "profile_path": r"C:/Users/Lenovo/Desktop/advance bot/Advance-Tiktok-bot/gologin profile"
}

CHROME_DRIVER_PATH = r"C:/Users/DELL/Desktop/another bot/chrome driver/chromedriver-win64/chromedriver.exe"
driver = None

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import time
gl = GoLogin(GOLOGIN_CONF)
debugger_address = gl.start()  # returns something like "127.0.0.1:XXXXX"
print("Started gologin")
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", debugger_address)
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://seller-us.tiktok.com/promotion/marketing-tools/regular-flash-sale/create?back=1&shop_region=US")

### Clicking on the button of select products:
wait = WebDriverWait(driver, 10)
try:
    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-tid="m4b_button"]'))
    )
    button.click()
except Exception:
    print("Could not open the product selection")

## Click on 50/pages
dropdown = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".theme-arco-select-view"))
)
dropdown.click()

wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//span[text()='1000/Page']")
    )
).click()

checkbox = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".theme-arco-checkbox-mask")
    )
)
checkbox.click()

## click on done
wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[normalize-space()='Done']]")
    )
).click()
time.sleep(130)
print("Done")
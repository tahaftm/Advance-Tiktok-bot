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
driver.switch_to.new_window('tab')
driver.get("https://seller-us.tiktok.com/promotion/marketing-tools/regular-flash-sale/create?back=1&shop_region=US")

### Clicking on the button of select products:
wait = WebDriverWait(driver, 10)
try:
    select_products_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[normalize-space()='Select products']]")
        )
    )

    select_products_btn.click()

except Exception:
    print("Could not open the product selection")

## Click on 50/pages
page_size_span = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='50/Page']")
    )
)
page_size_span.click()


wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//span[text()='1000/Page']")
    )
).click()
time.sleep(20)
checkbox = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//label[contains(@class,'theme-arco-checkbox')]")
    )
)

checkbox.click()

## click on done
wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[.//span[normalize-space()='Done']]")
    )
).click()
time.sleep(30)
print("Done")
# get all product rows
rows = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//div[contains(@class,'theme-arco-table-tr')]")
    )
)

print(f"Found {len(rows)} rows")

for index in range(len(rows)):
    # re-fetch rows every loop (prevents stale element issues)
    rows = driver.find_elements(
        By.XPATH, "//div[contains(@class,'theme-arco-table-tr')]"
    )
    row = rows[index]

    # 1️⃣ extract price text
    price_text = row.find_element(
        By.XPATH, ".//span[contains(@class,'theme-arco-table-cell-wrap-value')]//p"
    ).text
    # example: "$26.99"

    # 2️⃣ extract digits only
    price_value = float(re.sub(r"[^\d.]", "", price_text))

    # 3️⃣ add 10
    new_price = price_value - 10
    print(f"Row {index+1}: {price_value} → {new_price}")

    # 4️⃣ find input in same row
    price_input = row.find_element(
        By.XPATH, ".//input[@data-tid='m4b_input']"
    )

    # clear + send new value
    price_input.clear()
    price_input.send_keys(f"{new_price:.2f}")

    time.sleep(0.3)  # small delay to look human

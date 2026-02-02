from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
from filling_website import listing
from selenium.webdriver.common.by import By

def get_product_info(sku):
    url = f"https://www.amazon.com/dp/{sku}"

    folder_path = r"C:/Users/Lenovo/Downloads/Products_/"+product_title

    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    continue_button_bypass = driver.find_element(By.XPATH, "//button[text()='Continue shopping']")
    continue_button_bypass.click()
    time.sleep(3)  # wait for JS to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    title_tag = soup.find("span", id="productTitle")
    product_title = title_tag.text.strip() if title_tag else "Title not found"

    desc_elem = soup.select_one(".a-unordered-list.a-vertical.a-spacing-small")
    product_description = desc_elem.text.strip() if desc_elem else "Description not found"

    print("Title:", product_title)
    print("Description:", product_description)

    driver.quit()
    
    listing(product_title, product_description)

get_product_info("1847941842")
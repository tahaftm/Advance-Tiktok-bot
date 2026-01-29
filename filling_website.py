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

# ===== Other =====
import time

# ===== GoLogin =====
from gologin import GoLogin
from tkinter import *

GOLOGIN_CONF = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzEzMTNiMzUxNGI3NzAxNzhjMDRiNDUiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2ODVhZWJjMzk2NzMyYTJjNjU2YTJhNTEifQ.xBSrKOOUX3djmsvr0T6zjqGbZ4Ic4gdHH20Xd2Krquk",
    "profile_id": "6834ec3749adaff086ca5eb9",
    "profile_path": r"C:/GoLoginProfiles"
}

CHROME_DRIVER_PATH = r"C:/143_webdriver/chromedriver-win64/chromedriver-win64/chromedriver.exe"
driver = None
def get_driver():
    global driver

    if driver is not None:
        return driver  # ✅ reuse existing session

    print("🚀 Starting GoLogin for the first time")

    gl = GoLogin(GOLOGIN_CONF)
    debugger_address = gl.start()

    service = Service(CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", debugger_address)

    driver = webdriver.Chrome(service=service, options=options)
    time.sleep(10)

    return driver



def listing(product_title,product_description,sku, updated_price, weight, dimensions):
    driver = get_driver()
    driver.execute_script("window.open('');")  # open blank tab
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("https://seller-us.tiktok.com/product/create?channel=manage&shop_region=US")

    # Switch to the new tab
    time.sleep(20)
    # driver.get()

        ## -----------------------------------------------------------------------------------------------------------------------------------------
                                                            # Uploading the pictures
    try:
        # Remove invalid characters using regex
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', product_title)

        # Now build folder path
        folder_path = f"C://Users//DELL//Downloads//products//{safe_title}"
        # folder_path = f"C://Users//DELL//Downloads//products//{product_title}"
        files = os.listdir(folder_path)

        # Filter only image files
        image_files = [os.path.join(folder_path, f) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # 3️⃣ Locate the hidden file input
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")

        # 4️⃣ Upload all images (join paths with newline for multiple files)
        file_input.send_keys("\n".join(image_files))

        # 5️⃣ Wait a bit to see uploads
        time.sleep(5)
    except Exception:
        print("Could not add images")
    time.sleep(10)
        ## -----------------------------------------------------------------------------------------------------------------------------------------


        ## -----------------------------------------------------------------------------------------------------------------------------------------
                                                            # Product Title
    try:
        wait = WebDriverWait(driver, 20)
        input_box = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-id='product.publish.product_name']"))
        )

            # Type text
        input_box.clear()
        input_box.send_keys(product_title)
    except Exception: 
        print("Could not set the title")
    time.sleep(10)
    
        ## -----------------------------------------------------------------------------------------------------------------------------------------
                            ## Selecting Category
    try:
        ai_suggestion = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(text(),'AI suggestion')]")
        ))
        ai_suggestion.click()
        time.sleep(5)
        # 2️⃣ Click on the Apply button inside the popup
        apply_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Apply']]")
        ))
        apply_button.click()
    except Exception:
        print("Category already selected")
    time.sleep(10)
        ## -----------------------------------------------------------------------------------------------------------------------------------------
                                                            # Product Description
    try:
        wait = WebDriverWait(driver, 10)

        editor = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'ProseMirror')]")
            )
        )

            # Click to focus
        ActionChains(driver).move_to_element(editor).click().perform()

            # Type text
        editor.send_keys(product_description)
    except Exception:
        print("Could not set description")
    time.sleep(10)
    try:
        base_path = r"C:/Users/DELL/Downloads/products"
        folder_path = os.path.join(base_path, product_title)

        image_1 = os.path.join(folder_path, "image_1.jpg")
        image_2 = os.path.join(folder_path, "image_2.jpg")

        assert os.path.exists(image_1)
        assert os.path.exists(image_2)

        # Click image button to activate uploader
        image_button = driver.find_element(
            By.XPATH,
            "//button[contains(@class,'syl-toolbar-button')]"
        )
        driver.execute_script("arguments[0].click();", image_button)
        time.sleep(1)

        # Get latest file input
        file_input = driver.find_elements(By.XPATH, "//input[@type='file']")[-1]

        # Upload one by one
        file_input.send_keys(image_1)
        time.sleep(2)

        file_input.send_keys(image_2)
        time.sleep(2)

        print("✅ Description images uploaded successfully")
    except Exception as e:
        print("Could not set images for description: ",e)
    #     ## -----------------------------------------------------------------------------------------------------------------------------------------
    # # time.sleep(15)
    #     ## -----------------------------------------------------------------------------------------------------------------------------------------
    #                                                     ## Choosing a category
    # # category_div = driver.find_element(By.XPATH, "//div[contains(text(),'Floor Games')]")
    # # category_div.click()
    #     ## -----------------------------------------------------------------------------------------------------------------------------------------

    #     ## -----------------------------------------------------------------------------------------------------------------------------------------
    #                                                         # Retail price
    wait = WebDriverWait(driver, 30)

    # 1️⃣ Wait until at least ONE price input exists
    inputs = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//input[@data-tid='m4b_input_number']")
        )
    )

    # DEBUG: how many inputs Selenium sees
    print("Found inputs:", len(inputs))

    # 2️⃣ Retail price is the FIRST one
    retail_price_input = inputs[0]

    # 3️⃣ Scroll & focus
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", retail_price_input)
    driver.execute_script("arguments[0].focus();", retail_price_input)

    # 4️⃣ Clear safely
    retail_price_input.send_keys(Keys.CONTROL, "a")
    retail_price_input.send_keys(Keys.DELETE)

    # 5️⃣ Type value
    retail_price_input.send_keys(updated_price)

    # 6️⃣ Notify React
    driver.execute_script(
        "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
        retail_price_input
    )
    time.sleep(10)
    print("This has been done")
        ## -----------------------------------------------------------------------------------------------------------------------------------------
                                                                    # List Price
    # 7️⃣ List price is the SECOND input
    list_price_input = inputs[1]

    # Scroll & focus
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", list_price_input)
    driver.execute_script("arguments[0].focus();", list_price_input)

    # Clear safely
    list_price_input.send_keys(Keys.CONTROL, "a")
    list_price_input.send_keys(Keys.DELETE)

    # Type value
    list_price_input.send_keys("20")

    # Notify React
    driver.execute_script(
        "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
        list_price_input
    )
    time.sleep(10)
        ## -----------------------------------------------------------------------------------------------------------------------------------------
    # ## -----------------------------------------------------------------------------------------------------------------------------------------
    #                                                          # sku
    # Find SKU input separately (TEXT input, not number)
    try:
        sku_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@data-tid='m4b_input' and @maxlength='50']")
            )
        )

        # Scroll & focus
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            sku_input
        )
        driver.execute_script("arguments[0].focus();", sku_input)

        # Clear safely
        sku_input.send_keys(Keys.CONTROL, "a")
        sku_input.send_keys(Keys.DELETE)

        # Type SKU
        sku_input.send_keys(sku)

        # React notification
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            sku_input
        )
        wrapper = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//span[contains(@class,'core-input-inner-wrapper') and .//input[@data-tid='m4b_input_number']]"
            ))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
            wrapper
        )

        price_input = wait.until(
        EC.presence_of_element_located((
            By.XPATH, "//input[@data-tid='m4b_input_number']"
        ))
        )

        driver.execute_script("""
            arguments[0].focus();
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, price_input, "20")
        apply_button = wait.until(
        EC.presence_of_element_located((
            By.XPATH, "//button[@data-tid='m4b_button' and .//span[text()='Apply']]"
        ))
    )

        driver.execute_script("arguments[0].click();", apply_button)
    except Exception:
        print("Cant set sku")
    time.sleep(10)
        ## -----------------------------------------------------------------------------------------------------------------------------------------
    #                                                     # Radio Boxes
    wait = WebDriverWait(driver, 10)

    # 1️⃣ Scope to Product Compliance section
    compliance_section = wait.until(
        EC.presence_of_element_located(
            (By.ID, "product_publish_compliance")
        )
    )

    # 2️⃣ Find all "No" radio labels inside this section
    no_radios = compliance_section.find_elements(
        By.XPATH,
        ".//label[.//div[text()='No']]"
    )

    # 3️⃣ Click each "No" radio
    for radio in no_radios:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", radio)
        driver.execute_script("arguments[0].click();", radio)
    time.sleep(10)
        ## -----------------------------------------------------------------------------------------------------------------------------------------
                                    # Item weight configuration
    try:
        weight_value, weight_unit = weight  # e.g. (2.31, "pounds")

        weight_container = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-id='product.publish.package_weight']"))
        )

        # Now find the input inside this container
        weight_input = weight_container.find_element(By.CSS_SELECTOR, "input[data-tid='m4b_input_number']")

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", weight_input)
        time.sleep(0.5)

        # Clear existing value
        weight_input.click()
        weight_input.send_keys(Keys.CONTROL + "a")
        weight_input.send_keys(Keys.DELETE)

        # Send the new value
        weight_input.send_keys(weight_value)

        # Trigger input/change events for reactive framework
        driver.execute_script("""
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, weight_input)

        print("Weight set successfully in the correct box!")


    except Exception as e:
        print("Could not set the weight: ",e)
        ## -----------------------------------------------------------------------------------------------------------------------------------------
        
        ## -----------------------------------------------------------------------------------------------------------------------------------------
                                        # Listing Dimensions
                                        # FOR HEIGHT 
    try:
        height = dimensions[2]
        width = dimensions[1]
        length = dimensions[0]
        height_container = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[contains(@class,'core-input-number-suffix') and normalize-space(text())='inch']/ancestor::span[contains(@class,'core-input-inner-wrapper')]"
            ))
        )

        # 2️⃣ Find the input inside this container
        height_input = height_container.find_element(
            By.CSS_SELECTOR, "input[data-tid='m4b_input_number']"
        )

        # 3️⃣ Scroll into view
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", height_input
        )
        time.sleep(0.5)

        # 4️⃣ Clear existing value
        height_input.click()
        height_input.send_keys(Keys.CONTROL, "a")
        height_input.send_keys(Keys.DELETE)

        # 5️⃣ Send height value
        height_input.send_keys(height)

        # 6️⃣ Trigger React events
        driver.execute_script("""
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, height_input)

        print("Height set successfully in the correct box!")

    except Exception as e:
        print("Sorry could nt set height: ", e)

                                    ## FOR WIDTH
    try:
        width_container = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//input[@placeholder='Width']/ancestor::span[contains(@class,'core-input-inner-wrapper')]"
        ))
        )

        # 2️⃣ Find the input inside this container
        width_input = width_container.find_element(
            By.CSS_SELECTOR, "input[data-tid='m4b_input_number']"
        )

        # 3️⃣ Scroll into view
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", width_input
        )
        time.sleep(0.5)

        # 4️⃣ Clear existing value
        width_input.click()
        width_input.send_keys(Keys.CONTROL, "a")
        width_input.send_keys(Keys.DELETE)

        # 5️⃣ Send width value
        width_input.send_keys(width)

        # 6️⃣ Trigger React events
        driver.execute_script("""
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, width_input)

        print("Width set successfully in the correct box!")
    except Exception as e:
        print("Could not set width: ",e)

                                            ## FOR LENGTH
    try:
        length_container = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//input[@placeholder='Length']/ancestor::span[contains(@class,'core-input-inner-wrapper')]"
        ))
    )

        # 2️⃣ Find the input inside this container
        length_input = length_container.find_element(
            By.CSS_SELECTOR, "input[data-tid='m4b_input_number']"
        )

        # 3️⃣ Scroll into view
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", length_input
        )
        time.sleep(0.5)

        # 4️⃣ Clear existing value
        length_input.click()
        length_input.send_keys(Keys.CONTROL, "a")
        length_input.send_keys(Keys.DELETE)

        # 5️⃣ Send length value
        length_input.send_keys(length)

        # 6️⃣ Trigger React events
        driver.execute_script("""
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, length_input)

        print("Length set successfully in the correct box!")

    except Exception as e:
        print("Could not set length: ", e)

        ## -----------------------------------------------------------------------------------------------------------------------------------------
                                        # LIST PRICE
    try: 
        
        # Scroll
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", price_input
        )
        time.sleep(0.3)

        # Click & clear
        price_input.click()
        price_input.send_keys(Keys.CONTROL, "a")
        price_input.send_keys(Keys.DELETE)

        # 🔥 SET VALUE VIA JS (React-safe)
        driver.execute_script(
            "arguments[0].value = arguments[1];",
            price_input,
            updated_price
        )

        # 🔥 Fire ALL required events
        driver.execute_script("""
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """, price_input)

        # 🔥 Force focus-out (critical)
        driver.find_element(By.TAG_NAME, "body").click()

        print("List price committed successfully!")
        time.sleep(10)
    except Exception as e:
        print("List price not set")
    driver.switch_to.new_window('tab')
    # # driver.get("https://www.youtube.com")
# listing("12 Laws of Karma", "product-description","1234", "12.32", ["50", "pounds"],['7', '1', '9'])
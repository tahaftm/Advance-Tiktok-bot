import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import requests
from PIL import Image
from io import BytesIO
import imagehash
from selenium.common.exceptions import InvalidSessionIdException

# def start_listing(product_title, product_description, sku, updated_price, weight, dimensions):
#     threading.Thread(
#         target=listing,
#         args=(product_title, product_description, sku, updated_price, weight, dimensions)
#     ).start()

def extractAllinfo(sku):
    # ----------------- SETUP CHROME -----------------
    options = webdriver.ChromeOptions()

    # options.add_argument(r"user-data-dir=C:/selinium/chrome-taha")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")  
    options.add_argument("--start-maximized")  # This makes the Chrome window start maximized
    options.add_argument("--disable-popup-blocking")

    options.add_argument(
        r"--user-data-dir=C:/selinium/chrome-taha"
    )

    # EXACT profile folder name
    options.add_argument("--profile-directory=Default")  # change if needed

    driver = webdriver.Chrome(options=options)
    # ----------------- OPEN AMAZON PRODUCT -----------------
    url = f"https://www.amazon.com/dp/{sku}"
    driver.get(url)

    # Wait for JS to load content
    time.sleep(3)

    # ----------------- GET PRODUCT TITLE -----------------
    try:
        title_elem = driver.find_element(By.ID, "productTitle")
        product_title = title_elem.text.strip()
    except:
        product_title = "Title not found"

    print("Product Title:", product_title)

    # ----------------- GET PRODUCT DESCRIPTION / BULLETS -----------------
    try:
        bullets_elem = driver.find_element(By.ID, "detailBullets_feature_div")
        li_elements = bullets_elem.find_elements(By.TAG_NAME, "li")

        product_description = ""

        for li in li_elements:
            spans = li.find_elements(By.TAG_NAME, "span")
            if not spans:
                continue

            # Label is first bold span
            label = ""
            value = ""

            for span in spans:
                cls = span.get_attribute("class")
                if "a-text-bold" in cls:
                    label = span.text.strip()
                    break  # first bold span is label

            # Value is usually the last span text
            value = spans[-1].text.strip() if len(spans) > 1 else ""

            # Clean invisible unicode characters
            label = label.replace("\u200e", "").replace("\u200f", "")
            value = value.replace("\u200e", "").replace("\u200f", "")

            if label:
                product_description += f"{label} {value}\n"
            else:
                product_description += f"{value}\n"

    except:
        product_description = "Description not found"

    try:
        container = driver.find_element(By.ID, "bookDescription_feature_div")
        text = container.text.strip()

        product_description = product_description + "\n" + text

    except Exception:
        print("Could not extract complete text description")
    

    print("Product Description:\n", product_description)
    # # ----------------- GET ALL IMAGES -----------------
    
    def normalize_amazon_url(url):
        return re.sub(r'\._[^.]+_', '.', url)

    def perceptual_hash(img_bytes):
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
        return imagehash.phash(img)

    folder_name = re.sub(r'[<>:"/\\|?*]', '_', product_title)
    folder_path = os.path.join(r"C:/Users/DELL/Downloads/products", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }

    image_urls = set()
    saved_hashes = []
    image_index = 1

    try:
        # 1️⃣ Main image
        landing_img = driver.find_element(By.ID, "landingImage")
        img_data = landing_img.get_attribute("data-a-dynamic-image")

        if img_data:
            img_dict = json.loads(img_data)
            for url in img_dict.keys():
                image_urls.add(normalize_amazon_url(url))

        # 2️⃣ Thumbnails
        thumbs = driver.find_elements(By.CSS_SELECTOR, "#altImages img")
        for t in thumbs:
            src = t.get_attribute("data-old-hires") or t.get_attribute("src")
            if src and src.startswith("http"):
                image_urls.add(normalize_amazon_url(src))

        # 3️⃣ Download + PERCEPTUAL dedup
        for url in sorted(image_urls):
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code != 200:
                continue

            img_bytes = r.content
            phash = perceptual_hash(img_bytes)

            # Compare with existing hashes
            duplicate = False
            for existing in saved_hashes:
                if phash - existing <= 3:  # similarity threshold
                    duplicate = True
                    break

            if duplicate:
                print("Skipped visually duplicate image")
                continue

            saved_hashes.append(phash)

            file_path = os.path.join(folder_path, f"image_{image_index}.jpg")
            with open(file_path, "wb") as f:
                f.write(img_bytes)

            print("Saved:", file_path)
            image_index += 1

    except Exception as e:
        print("Image extraction error:", e)

    ## -----------------------------------------------------------------------------------------------
                                    ## Extracting price
    try:
        price_element = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole")

        # get the text and clean it
        price_text = price_element.text.strip()

        # convert to integer (or float if needed)
        price = int(price_text)

        updated_price = str(price + 10.99)
    except Exception:
        updated_price = 1.99
        print("Price extraction failed")

    ## -----------------------------------------------------------------------------------------------
                                    ## Item Weight extraction
    weight = None  # default if not found

    try:
        # Find the unordered list containing the details
        ul = driver.find_element(By.CSS_SELECTOR, "ul.detail-bullet-list")
        li_elements = ul.find_elements(By.TAG_NAME, "li")

        for li in li_elements:
            # Each li has a bold label span and a value span
            bold_span = li.find_element(By.CSS_SELECTOR, "span.a-text-bold")
            label_text = bold_span.text.strip()

            if "Item Weight" in label_text:
                # Value is usually the last span inside li
                spans = li.find_elements(By.TAG_NAME, "span")
                if len(spans) > 1:
                    weight = spans[-1].text.strip()
                break  # stop looping once found

        print("Item Weight:", weight)
        weight = weight.split()
    except Exception as e:
        print("Error extracting item weight")

        ## -----------------------------------------------------------------------------------------------------------------------------------------
        ## -----------------------------------------------------------------------------------------------------------------------------------------
                                            # Dimansions configuration
    dimensions = None
    try:
        ul = driver.find_element(By.CSS_SELECTOR, "ul.detail-bullet-list")
        li_elements = ul.find_elements(By.TAG_NAME, "li")

        for li in li_elements:
            try:
                label = li.find_element(By.CSS_SELECTOR, "span.a-text-bold").text
                label = label.replace("", "").replace("", "").strip()

                if "Dimensions" in label:
                    spans = li.find_elements(By.TAG_NAME, "span")
                    dimensions = spans[-1].text.strip()
                    break

            except:
                continue
        dimensions = dimensions.split()
        new_dimensions = []
        for i in dimensions:
            try:
                new_dimensions.append(str(round(float(i))))
            except Exception:
                pass
        print("Dimensions:", dimensions)
        print("New Dimensions:", new_dimensions)
    except Exception as e:
        new_dimensions = ['9','1','6']
        print("Could not extract weight: ", e)
        
        ## -----------------------------------------------------------------------------------------------------------------------------------------
    driver.quit()

    # def listing_info():
    #     print("Gologin about to start")
    #     from filling_website import listing
    #     threading.Thread(target=listing, args=(product_title,product_description,sku), daemon=True).start()
    # listing_info()
    print("extracted all info for one product!")
    # print(weight)
    from filling_website import listing
    try:
        listing(product_title, product_description, sku, updated_price, weight, new_dimensions)
    except InvalidSessionIdException:
        print("Session lost, retrying...")
        driver = None  # force restart
        listing(product_title, product_description, sku, updated_price, weight, new_dimensions)

# extractAllinfo("1368060730")

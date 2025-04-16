import time
import numpy as np
import tempfile
import shutil
from datetime import datetime
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pyperclip
import random
class Skin:    
    name = ""
    discount = 0
    LOWDISCOUNT = 27
    price = 0.0
    MAXPRICE = 20
    LOWPRICE = 2.50
    
    def buySkin(self,text):
        # Initialize undetected ChromeDriver Options
        options = uc.ChromeOptions()
        # Create a temporary directory for a unique profile
        temp_profile = tempfile.mkdtemp()
        ua = UserAgent() #Makes fake user
        options.add_argument(f"user-agent={ua.random}") #Makes fake agent
        options.add_argument(f"--user-data-dir={temp_profile}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        window_sizes = [(1366, 768), (1920, 1080), (1536, 864), (1440, 900)]
        width, height = random.choice(window_sizes)
        options.add_argument(f"--window-size={width},{height}") # Makes random window size
        options.add_argument("--disable-backgrounding-occluded-windows")  # Ensure foreground focus
        options.add_argument("--disable-blink-features=AutomationControlled")  # Removes Selenium flag
        options.add_argument("--disable-infobars")  # Removes “Chrome is being controlled” banner
        options.add_argument("--no-sandbox")  # Helps run Chrome smoother
        options.add_argument("--disable-dev-shm-usage")  # Helps in Docker environments
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("""
        Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
        Object.defineProperty(navigator, 'productSub', {get: () => '20100101'});
        Object.defineProperty(navigator, 'vendor', {get: () => 'Google Inc.'});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        """)

        # Opens specific skin url
        driver.get(text) # Opens specific skin
        self.randomDelay()
        driver.delete_all_cookies() # Clears Cookies
        try:
            # Wait for the button to be clickable
            wait = WebDriverWait(driver, 20)  # Wait up to 20 seconds
            time.sleep(1)
            recentButton = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[1]/ul/li[2]')))
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
            recentButton.click()
            print("Page is fully loaded.")
            time.sleep(1)
            if not self.checkSold(driver):
                print("Not Buyable")
                return False
            xPath = "/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/div/div"
            dates = []
            prices = [] 
            for i in range(2,12):
                recentSale = driver.find_element(By.XPATH, f"{xPath}[{i}]")
                saleText = recentSale.text
                dateTime = saleText.split("\n")[0]
                givenTime = datetime.strptime(dateTime, "%b %d, %Y %I:%M %p")
                currentTime = datetime.now()
                mins = (currentTime - givenTime).total_seconds()/60

                price = float(saleText.split("\n")[2].replace("$", ""))

                dates.append(mins)
                prices.append(price)
            mean = np.mean(prices)
            print("Mean:")
            print(mean)
            threashold = 0.84 * mean
            if self.price > threashold:
                print("Not actually Cheap enough")
                return False
            print("Going to buy NOW!!!")
            pyperclip.copy(text)
            return True #Bought Item
            
        except Exception as e:
            print(f"Error occurred: {e}")
            False  # Indicate failure
        finally:
            driver.quit()
            #Clears temporary profile
            shutil.rmtree(temp_profile)
    def randomDelay(self):
        time.sleep(random.uniform(1, 3))
    def checkSold(self,driver):
        try:
            cart = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[3]/a")
            print("Item has already been sold.")
            return False
        except NoSuchElementException:
            print("Element not found. Continuing...")
            return True  # Return True if the element is not found

    # Checks skin for bad items, prices and discounts
    def isProfitable(self,text):
        # Bad items
        words_to_check = ["Well-Worn", "Sticker", "Souvenir", "Charm", "Container", "Heat Treated", "Music Kit"]
        if self.contains_errase(text, words_to_check):
            return False
        # Sets price
        self.setPrice(text)
        # If price is bigger than max price or too low then it wont buy
        if self.price > self.MAXPRICE or self.price <= self.LOWPRICE:
            return False
        # Checks discount to find a good price
        if self.discount < self.LOWDISCOUNT:
            return False
        return True

    

    # Scans text from scrapped website to find the price and discount
    def setPrice(self, text):
        words = text.split()
        for word in words:
        # Check for price with a dollar sign
            if word.startswith("$"):
                try:
                    self.price = float(word[1:])  # Remove the '$' and convert to float
                except ValueError:
                    print(f"Error: Unable to parse price from '{word}'")
        
        # Check for discount with a percent sign
            if word.endswith("%"):
                try:
                    self.discount = int(word[:-1])  # Remove the '%' and convert to int
                    break
                except ValueError:
                    print(f"Error: Unable to parse discount from '{word}'")
    

    
    #Checks for bad items
    def contains_errase(self, text, words):
        return any(word in text for word in words)
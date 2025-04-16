import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import tempfile
import Skin
import customtkinter as ctk
import temp

def buy_items():
     # Initialize undetected ChromeDriver Options
    options = uc.ChromeOptions()
    # Create a temporary directory for a unique profile
    temp_profile = tempfile.mkdtemp()
    ua = UserAgent() #Makes fake user
    options.add_argument(f"user-agent={ua.random}") #Makes fake agent
    options.add_argument(f"--user-data-dir={temp_profile}")  # Use the temporary profile
        
    options.add_argument("--start-maximized")  # Start maximized
    options.add_argument("--disable-backgrounding-occluded-windows")  # Ensure foreground focus
    options.add_argument("--disable-blink-features=AutomationControlled")  # Removes Selenium flag
    options.add_argument("--disable-infobars")  # Removes “Chrome is being controlled” banner
    options.add_argument("--no-sandbox")  # Helps run Chrome smoother
    options.add_argument("--disable-dev-shm-usage")  # Helps in Docker environments
    driver = uc.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # Opens skinport
    driver.get("https://skinport.com/market?sort=date&order=desc")
    driver.delete_all_cookies() # Clears Cookies
    elements_set = set()
    try:
        # Wait for the button to be clickable
        wait = WebDriverWait(driver, 50)  # Wait up to 50 seconds
        live_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[2]/div[1]/div[1]/button')))

        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")

        # Click the live button
        live_button.click()
        print("Button clicked")
        # Runs until it finds new item listed on the market
        while True:
            # Gets current items on market
            current_elements = driver.find_elements(By.CLASS_NAME, "ItemPreview-link")
            # Goes through elements
            for element in current_elements:
                if element not in elements_set:
                    #Add elements to set so not duplicated
                    elements_set.add(element)
                    item_Filter = element.text
                    Current_Skin = Skin.Skin()
                    #Filters item
                    if Current_Skin.isProfitable(item_Filter) == True:
                        #Prints url to confirm it found a good item
                        url = element.get_attribute('href')
                        print(f"New item found: {element.text}, URL {url}")
                        try:
                            #time.sleep(random.uniform(2, 5))
                            wait.until(lambda _: Current_Skin.buySkin(url))
                        except Exception as e:
                            print(e)   
    except KeyboardInterrupt:
        print("Monitoring stopped.")

    finally:
        # Close the browser after the action is completed
        driver.quit()

class MyGUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        
        self.root.geometry("800x500")
        self.root.title("Skinport Bot")
        self.label = ctk.CTkLabel(self.root, text="Skinport BOT", font=("Segoe UI", 24))
        self.label.pack(pady=20)
        self.button = ctk.CTkButton(
            self.root,
            text="Start the Bot",
            corner_radius = 32,
            command=buy_items,
            fg_color="#FF7700",
            hover_color="#e66000",
            text_color="white",
            font=("Segoe UI", 16)
        )
        self.button.pack(pady= 10)
        self.root.mainloop()
# To actually run the GUI
if __name__ == "__main__":
    gui = MyGUI()
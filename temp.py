import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class temp:
    def __init__(self):
        self.driver = None
        self.profile_path = os.path.join(os.path.expanduser("~"), "stealth_browser_profile")
        
    def setup_driver(self):
        """Set up a Chrome driver with anti-detection measures"""
        options = Options()
        
        # Use a persistent profile
        if not os.path.exists(self.profile_path):
            os.makedirs(self.profile_path)
        options.add_argument(f"--user-data-dir={self.profile_path}")
        
        # Basic anti-detection settings
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Window size and user agent
        width = random.randint(1200, 1600)
        height = random.randint(800, 1000)
        options.add_argument(f"--window-size={width},{height}")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Standard options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Create and return the driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Apply JavaScript evasions
        self._apply_js_evasions()
        
        return self.driver
    
    def _apply_js_evasions(self):
        """Apply JavaScript-based evasions"""
        evasion_js = """
        // Hide automation
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """
        self.driver.execute_script(evasion_js)
    
    def click_button(self, url, button_selector):
        """Navigate to URL and click a button in a human-like way"""
        try:
            # Navigate to the page
            self.driver.get(url)
            print("Page loaded")
            
            # Wait for page to load
            time.sleep(random.uniform(2, 4))
            
            # Scroll a bit
            scroll_amount = random.randint(100, 300)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))
            
            # Find and wait for the button
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
            )
            print("Button found")
            
            # Move to element with a more human-like motion
            actions = ActionChains(self.driver)
            actions.move_to_element(button)
            actions.pause(random.uniform(0.1, 0.3))
            actions.click()
            actions.perform()
            
            print("Button clicked successfully")
            time.sleep(random.uniform(1, 3))
            
            return True
            
        except Exception as e:
            print(f"Error clicking button: {e}")
            return False
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
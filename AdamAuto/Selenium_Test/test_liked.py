import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLikedList:
    def setup_method(self, method):
        """Setup Chrome WebDriver"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        print("\n[INFO] Browser launched successfully.")

    def teardown_method(self, method):
        """Close the browser"""
        self.driver.quit()
        print("[INFO] Browser closed.")

    def test_liked_list(self):
        """Test the liked list feature"""
        print("[STEP] Opening website...")
        self.driver.get("http://127.0.0.1:8000/")

        # Assert title
        assert "Adam Automotive" in self.driver.title, f"Unexpected title: {self.driver.title}"

        # Click on Login
        print("[STEP] Clicking Login button...")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()

        # Enter login credentials
        print("[STEP] Entering login credentials...")
        email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_input.send_keys("alphin2002paul@gmail.com")

        password_input = self.driver.find_element(By.ID, "password-field")
        password_input.send_keys("Alphin@")

        # Click login button
        print("[STEP] Logging in...")
        self.driver.find_element(By.CSS_SELECTOR, "button").click()

        time.sleep(2)  # Allow login to process

        # Open car collection dropdown
        print("[STEP] Opening car collection...")
        self.wait.until(EC.element_to_be_clickable((By.ID, "carCollectionDropdown"))).click()

        # Select 'Adam Car Collection'
        print("[STEP] Selecting 'Adam Car Collection'...")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Adam Car Collection"))).click()

        # Click on 'Like' button for a car
        print("[STEP] Liking a car...")
        like_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-md-4:nth-child(2) .btn:nth-child(1)")))
        like_button.click()

        # Navigate to 'Liked List'
        print("[STEP] Opening Liked List...")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Liked List"))).click()

        # Verify the car is in the liked list
        liked_car = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".col-md-4:nth-child(1)")))
        assert liked_car is not None, "Car was not added to the liked list!"

        # ✅ Print the final success message
        print("\n✅ Successfully added to Liked List!\n")

if __name__ == "__main__":
    pytest.main()

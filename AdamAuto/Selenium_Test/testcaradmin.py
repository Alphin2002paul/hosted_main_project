from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time  # Add this import at the top of your file

def test_edit_sale_request():
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)

    try:
        driver.maximize_window()
        driver.get("http://localhost:8000/login")

        # Login process
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys("adamautomotive3@gmail.com")
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("adam")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Wait for the main page to load after successful login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "nav.navbar"))
        )
        print("Successfully signed in")

        # Directly navigate to the Edit Listing page after login
        driver.get("http://localhost:8000/edit-listing")  # Adjust the URL if necessary

        # Wait for the Edit Listing page to load
        WebDriverWait(driver, 10).until(
            EC.url_contains("edit-listing")
        )
        print("Successfully navigated to Edit Listing page")

        # Locate and click the "Delete Car" button for the first car
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-danger.delete-btn"))
        )
        print("Found Delete Car button")
        
        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", delete_button)
        
        # Wait a short time for any animations to complete
        time.sleep(1)
        
        # Get the number of cars before deletion
        cars_before = len(driver.find_elements(By.CSS_SELECTOR, ".car-wrap"))
        
        # Click the button
        delete_button.click()
        print("Clicked Delete Car button")

        # Wait for the page to update
        time.sleep(2)

        # Get the number of cars after deletion
        cars_after = len(driver.find_elements(By.CSS_SELECTOR, ".car-wrap"))

        if cars_after < cars_before:
            print("Successfully deleted the car")
        else:
            print("Car deletion may not have been successful")

        # Wait for 3 more seconds to observe the result
        time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    test_edit_sale_request()

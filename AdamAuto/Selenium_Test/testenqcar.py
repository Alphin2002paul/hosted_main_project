from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def test_enquire_car():
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)

    try:
        driver.maximize_window()
        driver.get("http://localhost:8000/login")
        # Login process
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys("alphin2002paul@gmail.com")
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("Alphin@")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Wait for the main page to load after successful login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "nav.navbar"))
        )
        print("Successfully signed in")

        # Navigate to Car Collection page
        car_collection_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Car Collection"))
        )
        car_collection_link.click()

        # Click on the first car to view details
        first_car = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".car-wrap:first-child"))
        )
        first_car.click()

        # Find and click the "Enquire" button
        enquire_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.enquire-btn"))
        )
        enquire_button.click()

        # Fill out the enquiry form (adjust selectors as needed)
        message_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "message"))
        )
        message_input.send_keys("I'm interested in this car. Can you provide more details?")

        # Submit the enquiry
        submit_enquiry_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_enquiry_button.click()

        # Wait for a success message
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".success-message"))
        )
        print("Successfully submitted car enquiry")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_enquire_car()
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def test_edit_profile():
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

        # Navigate to Account Details page
        account_details_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Account Details"))
        )
        account_details_link.click()

        # Click on the username to display the dropdown
        username_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".username-selector"))
        )
        username_element.click()

        # Click the "Request" button in the dropdown
        request_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Request"))
        )
        request_button.click()

        # Find the street address input field and update it
        street_address_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "street_address"))
        )
        street_address_input.clear()
        street_address_input.send_keys("123 New Test Street")

        # Click the update button
        update_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        update_button.click()

        # Wait for a success message or updated profile confirmation
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".success-message"))
        )
        print("Successfully updated profile")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_edit_profile()

from selenium import webdriver
from selenium.webdriver.common.by import By  # Import By class
from selenium.webdriver.common.keys import Keys
import os
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = os.getenv("LT_HUB_URL")
capabilities = {
    "build": os.getenv("LT_BUILD_NAME"),
    "name": "Quick Test",
    "platform": "Windows 10",
    "browserName": "Chrome",
    "version": "88.0",
    "resolution": "1920x1080",
    "tunnel": True
}

# Initialize the remote WebDriver
driver = webdriver.Remote(
    desired_capabilities=capabilities,
    command_executor=url
)

driver.get("http://localhost:8081/")

try:
    # Wait for the element to be clickable and click it
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "li3"))
    )
    element.click()
except NoSuchElementException:
    print("Element with NAME 'li3' not found.")
except Exception as e:
    print(f"An error occurred while clicking the element: {e}")

try:
    # Wait for the textbox element and send text
    textbox = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sampletodotext"))
    )
    textbox.send_keys("Testing")
except NoSuchElementException:
    print("Textbox with ID 'sampletodotext' not found.")
except Exception as e:
    print(f"An error occurred while interacting with the textbox: {e}")

try:
    # Wait for the add button and click it
    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "addbutton"))
    )
    add_button.click()
except NoSuchElementException:
    print("Add button with ID 'addbutton' not found.")
except Exception as e:
    print(f"An error occurred while clicking the add button: {e}")

# Check for the result
try:
    assert "No results found." not in driver.page_source
except AssertionError:
    print("Test failed: No results found message appeared on the page.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Report the test status to LambdaTest
try:
    driver.execute_script("lambda-status=passed")
except Exception as e:
    print(f"An error occurred while reporting the test status: {e}")

# Quit the driver after the test is complete
driver.quit()
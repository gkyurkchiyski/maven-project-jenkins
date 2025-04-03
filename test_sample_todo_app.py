from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Initialize the WebDriver (for Chrome in this case)
driver = webdriver.Chrome()  # Ensure you have the correct WebDriver installed

# Open the URL
driver.get("http://localhost:8081/")

try:
    # Wait for the element with name 'li3' to be clickable (or present)
    li3_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "li3"))
    )
    # Once the element is clickable, click it
    li3_element.click()

    # Continue with your other interactions
    textbox = driver.find_element(By.ID, "sampletodotext")
    textbox.send_keys("Testing")
    driver.find_element(By.ID, "addbutton").click()

    # Verify that the new item is added
    assert "No results found." not in driver.page_source

    # If no exception occurs, the test is passed
    print("Test Passed")

except TimeoutException:
    print("The element 'li3' was not found in time.")
    print("Test Failed")

except Exception as e:
    # Handle other exceptions
    print(f"An error occurred: {e}")
    print("Test Failed")

finally:
    # Close the browser
    driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json

url = os.getenv("LT_HUB_URL")
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Uncomment if you want the browser to run in headless mode

driver = webdriver.Remote(
    command_executor=url,
    options=options
)

driver.get("http://localhost:8081/")

# Use WebDriverWait to wait for the element to be visible before interacting with it
try:
    # Wait for the element with name "li3" to be clickable
    li3_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "li3"))
    )
    li3_element.click()
    
    textbox = driver.find_element(By.ID, "sampletodotext")
    textbox.send_keys("Testing")
    driver.find_element(By.ID, "addbutton").click()

    # Assert that the element doesn't contain the "No results found." text
    assert "No results found." not in driver.page_source

    driver.execute_script("lambda-status=passed")
finally:
    driver.quit()
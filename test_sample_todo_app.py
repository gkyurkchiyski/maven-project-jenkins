from selenium import webdriver
from selenium.webdriver.common.by import By  # Import By class
from selenium.webdriver.common.keys import Keys
import os
import json

url = os.getenv("LT_HUB_URL")
capabilities = {
    "build" : os.getenv("LT_BUILD_NAME"),
    "name" : "Quick Test",
    "platform" : "Windows 10",
    "browserName" : "Chrome",
    "version" : "88.0",
    "resolution" : "1920x1080",
    "tunnel" : True
}

driver = webdriver.Remote(
    desired_capabilities=capabilities,
    command_executor=url
)

driver.get("http://localhost:8081/")

# Use By.NAME to locate elements
driver.find_element(By.NAME, "li3").click()

# Use By.ID to locate elements
textbox = driver.find_element(By.ID, "sampletodotext")
textbox.send_keys("Testing")

driver.find_element(By.ID, "addbutton").click()

# Check for the result
assert "No results found." not in driver.page_source

# Report the test status to LambdaTest
driver.execute_script("lambda-status=passed")

driver.quit()
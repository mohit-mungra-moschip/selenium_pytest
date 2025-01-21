import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import tempfile
import os

@pytest.fixture
def driver():
    # Create a unique temporary directory for the user data
    user_data_dir = tempfile.mkdtemp()

    # Set Chrome options to specify the unique user data dir
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")  # Unique user data dir

    # Set up ChromeDriver with the specified options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()
    
    # Clean up the temporary directory (optional)
    try:
        os.rmdir(user_data_dir)
    except OSError:
        pass

def test_homepage_title(driver):
    driver.get("https://www.programiz.com/python-programming")
    assert driver.title == "Learn Python Programming"

def test_search_functionality(driver):
    driver.get("https://www.programiz.com/python-programming")
    search_icon = driver.find_element(By.XPATH, "/html/body/main/header/nav/div/div/form/div/div/input[1]")
    search_icon.click()
    search_icon.send_keys("functions")
    search_icon.send_keys(Keys.RETURN)
    time.sleep(2)
    results = driver.find_elements(By.CLASS_NAME, "search-result")
    assert len(results) > 0, "No search results found"

def test_learn_python_link(driver):
    driver.get("https://www.programiz.com/python-programming")
    learn_python_link = driver.find_element(By.LINK_TEXT, "Learn Python")
    learn_python_link.click()
    assert "https://www.programiz.com/learn-python" in driver.current_url, "Redirection failed"

def test_footer_about_us_link(driver):
    driver.get("https://www.programiz.com/python-programming")
    footer_about_us = driver.find_element(By.LINK_TEXT, "About")
    footer_about_us.click()
    time.sleep(2)
    assert "https://www.programiz.com/about" in driver.current_url, "'About Us' link is broken"


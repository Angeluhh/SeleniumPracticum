from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://gscsystem.site/login"

USERNAME = "angelamichelle.sy@lsu.edu.ph"
PASSWORD = "sy12345"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    driver.get(URL)

    username_field = wait.until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    password_field = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']")
        )
    )
    login_button.click()

    print("Login submitted.")
    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)

    driver.save_screenshot("TC01_User_Login.png")
    print("Screenshot saved: TC01_User_Login.png")

    input("Inspect the result, then press ENTER to close...")

except Exception as error:
    print("TEST ERROR:", type(error).__name__, error)

    driver.save_screenshot("TC01_User_Login_Error.png")
    print("Error screenshot saved: TC01_User_Login_Error.png")

    input("Inspect the browser, then press ENTER to close...")

finally:
    driver.quit()